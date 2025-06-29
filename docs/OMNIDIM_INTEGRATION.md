# Omnidim Integration Guide

## Overview

LearnFlow AI leverages Omnidim.io's voice AI platform for all voice-related features.

## Key Features Used

1. **Voice Sessions API**
   - Real-time voice streaming
   - Multi-language support
   - Emotion detection

2. **Speech Analysis API**
   - Pronunciation scoring
   - Fluency analysis
   - Accent coaching

3. **Voice Models**
   - Subject-specific tutors
   - Native language speakers
   - Emotion-aware responses

## Implementation

### Creating a Voice Session

```python
from app.services.omnidim.client import OmnidimClient

client = OmnidimClient()
session = await client.create_voice_session({
    "mode": "tutor",
    "user_id": "123",
    "context": {
        "subject": "mathematics",
        "difficulty": "intermediate"
    }
})
WebSocket Streaming
typescriptconst ws = new WebSocket(omnidimWsUrl)
ws.onmessage = (event) => {
  if (event.data instanceof ArrayBuffer) {
    // Handle audio data
    playAudio(event.data)
  } else {
    // Handle JSON messages
    const data = JSON.parse(event.data)
    handleMessage(data)
  }
}
Best Practices

Always validate audio format before sending
Handle connection drops gracefully
Implement proper error handling
Monitor API usage and limits
