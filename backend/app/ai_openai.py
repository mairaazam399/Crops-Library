import os
import json
import base64
import asyncio
from typing import Dict, Any

import httpx

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini-vision")
OPENAI_API_URL = os.getenv("OPENAI_API_URL", "https://api.openai.com/v1/chat/completions")

SYSTEM_PROMPT = """
You are an expert plant identification and disease diagnosis assistant for farmers and researchers.
Given a single image (provided as a base64 data URL), return a concise JSON object with the following schema:
{
  "predictions": [
    {"name": "Common or scientific name of species or disease", "type": "species|disease", "confidence": float (0-1) }
  ],
  "explanation": "short explanation of how you reached the conclusion",
  "suggested_actions": "practical next steps for the farmer/researcher"
}
Only output valid JSON. If you are uncertain, produce low confidence values and state uncertainty in the explanation.
Use no additional prose outside the JSON block. Keep responses compact.
"""


async def identify_image_bytes(image_bytes: bytes) -> Dict[str, Any]:
    """Send the image to OpenAI Chat Completion API (as a base64 data URL in the user message)

    Returns a parsed JSON object according to the SYSTEM_PROMPT schema. Raises RuntimeError on failure.
    """
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY not set")

    b64 = base64.b64encode(image_bytes).decode('ascii')
    # prefixing with data URL so the model sees it's an image
    data_url = f"data:image/jpeg;base64,{b64}"

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Analyze this image and respond in strict JSON only: {data_url}"},
    ]

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": OPENAI_MODEL,
        "messages": messages,
        "max_tokens": 600,
        "temperature": 0.2,
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        resp = await client.post(OPENAI_API_URL, headers=headers, json=payload)

    if resp.status_code != 200:
        raise RuntimeError(f"OpenAI API error: {resp.status_code} - {resp.text}")

    data = resp.json()

    # Chat response text can be nested; try to extract it robustly
    try:
        # OpenAI chat completions: data['choices'][0]['message']['content']
        content = data.get('choices', [])[0].get('message', {}).get('content', '')
    except Exception:
        # Fallbacks: responses or text
        content = data.get('choices', [])[0].get('text', '') if data.get('choices') else ''

    if not content:
        raise RuntimeError('OpenAI returned empty content')

    # The model should return pure JSON. Attempt to parse the first JSON object in the content.
    content = content.strip()
    try:
        parsed = json.loads(content)
        return parsed
    except Exception:
        # Try to find a JSON substring
        start = content.find('{')
        end = content.rfind('}')
        if start != -1 and end != -1 and end > start:
            substring = content[start:end+1]
            try:
                parsed = json.loads(substring)
                return parsed
            except Exception as e:
                raise RuntimeError('Failed to parse JSON from OpenAI response: ' + str(e) + '\n' + content)
        else:
            raise RuntimeError('OpenAI response did not contain JSON')
