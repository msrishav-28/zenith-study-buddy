Zenith Study Buddy - Voice-Powered Personalized Learning Platform

An innovative EdTech platform that leverages Omnidim.io's voice AI technology to create personalized, adaptive learning experiences through natural conversation.

## 🚀 Features

- **AI Voice Tutoring**: Natural conversation with subject-expert AI tutors
- **Language Learning**: Practice with native-speaking AI partners
- **Exam Preparation**: Voice-based quizzing and explanations
- **Adaptive Learning**: Real-time difficulty adjustment based on performance
- **Emotion Detection**: Adapts teaching style based on student emotions
- **Progress Analytics**: Detailed insights into learning patterns

## 🛠️ Tech Stack

- **Backend**: FastAPI (Python) with PostgreSQL
- **Frontend**: Next.js 14 with TypeScript
- **Voice AI**: Omnidim.io Platform
- **Real-time**: WebSocket streaming
- **Deployment**: Docker, Vercel, Railway

## 📋 Prerequisites

- Node.js 18+
- Python 3.11+
- Docker & Docker Compose
- Omnidim.io API Key

## 🔧 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/learnflow-ai.git
cd learnflow-ai

Set up environment variables:

bashcp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env

Start with Docker:

bashdocker-compose up -d

Or run locally:

Backend:
bashcd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
Frontend:
bashcd frontend
npm install
npm run dev
📱 Usage

Visit http://localhost:3000
Create an account
Choose your learning mode:

Voice Tutor
Language Practice
Exam Prep


Start speaking naturally!

🎯 Hackathon Demo
For Microsoft Hackathon judges:

Visit the live demo at [demo-url]
Use demo account: demo@learnflow.ai / password: Demo123!
Try the "Math Tutor" for best experience

📄 Documentation

API Documentation
Omnidim Integration
Deployment Guide
Architecture Overview

🤝 Contributing
We welcome contributions! Please see our Contributing Guide.
📝 License
This project is licensed under the MIT License - see the LICENSE file.
🙏 Acknowledgments

Omnidim.io for voice AI technology
Microsoft for hackathon opportunity
All contributors and testers