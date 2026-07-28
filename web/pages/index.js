import React, { useState } from 'react'

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000'

export default function Home() {
  const [file, setFile] = useState(null)
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)

  const onFileChange = (e) => {
    setFile(e.target.files[0])
    setResult(null)
  }

  const upload = async () => {
    if (!file) return
    setLoading(true)
    try {
      const formData = new FormData()
      formData.append('file', file)

      const res = await fetch(`${BACKEND_URL}/identify`, {
        method: 'POST',
        body: formData,
      })
      const data = await res.json()
      setResult(data)
    } catch (err) {
      alert('Upload failed: ' + String(err))
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{ maxWidth: 720, margin: '40px auto', fontFamily: 'Arial, sans-serif' }}>
      <h1>Crops Library — Web Demo</h1>
      <p>Upload an image of a leaf/plant and get an AI-powered identification (stub or model-backed).</p>

      <input type="file" accept="image/*" onChange={onFileChange} />
      <div style={{ marginTop: 12 }}>
        <button onClick={upload} disabled={!file || loading}>{loading ? 'Uploading...' : 'Upload & Identify'}</button>
      </div>

      {result && (
        <div style={{ marginTop: 20 }}>
          <h3>Results</h3>
          {result.success ? (
            <ul>
              {result.predictions.map((p, i) => (
                <li key={i}>{`${p.name} — ${(p.confidence * 100).toFixed(1)}%`}</li>
              ))}
            </ul>
          ) : (
            <div>Error: {result.error}</div>
          )}
        </div>
      )}
    </div>
  )
}
