import os
import requests
from typing import List, Dict

HF_MODEL = os.getenv('HF_MODEL', 'google/vit-base-patch16-224')
HF_API_TOKEN = os.getenv('HF_API_TOKEN')

HF_API_URL = f'https://api-inference.huggingface.co/models/{HF_MODEL}'


def identify_image_bytes(image_bytes: bytes) -> List[Dict]:
    """Call Hugging Face Inference API for image classification.

    Returns a list of dicts with keys: label, score
    Raises RuntimeError on failure.
    """
    if not HF_API_TOKEN:
        raise RuntimeError('HF_API_TOKEN not set')

    headers = {
        'Authorization': f'Bearer {HF_API_TOKEN}',
        'Accept': 'application/json',
    }

    response = requests.post(HF_API_URL, headers=headers, data=image_bytes)
    if response.status_code != 200:
        raise RuntimeError(f'HuggingFace API error: {response.status_code} - {response.text}')

    data = response.json()
    # Expecting a list of {label, score} entries for classification models
    if isinstance(data, dict) and data.get('error'):
        raise RuntimeError(f"HF model error: {data.get('error')}")

    return data
