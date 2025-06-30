# 🎓 Zenith Study Buddy - AI-Powered Voice Learning Platform

<p align="center">
  <img src="https://img.shields.io/badge/Next.js-14.0-black?style=for-the-badge&logo=next.js" />
  <img src="https://img.shields.io/badge/FastAPI-0.104-009688?style=for-the-badge&logo=fastapi" />
  <img src="https://img.shields.io/badge/TypeScript-5.3-blue?style=for-the-badge&logo=typescript" />
  <img src="https://img.shields.io/badge/Python-3.11-yellow?style=for-the-badge&logo=python" />
</p>

<p align="center">
  <strong>Transform your learning experience with AI-powered voice conversations</strong>
</p>

## 🚀 Overview

Zenith Study Buddy is an innovative EdTech platform that leverages advanced voice AI technology to create personalized, adaptive learning experiences through natural conversation. Built for the Microsoft AI Classroom Hackathon, it demonstrates the future of education where AI tutors adapt to each student's unique learning style, pace, and emotional state.

### ✨ Key Features

- **🎙️ AI Voice Tutoring** - Natural conversations with subject-expert AI tutors
- **🌍 Language Practice** - Practice any language with native-speaking AI partners
- **📚 Exam Preparation** - Voice-based quizzing with adaptive difficulty
- **🎯 Emotion Detection** - AI adapts teaching style based on student emotions
- **📊 Progress Analytics** - Detailed insights into learning patterns
- **🔄 Real-time Feedback** - Instant pronunciation and comprehension scoring

## 🛠️ Technology Stack

### Frontend
- **Framework:** Next.js 14 with App Router
- **Language:** TypeScript
- **Styling:** Tailwind CSS
- **State Management:** Zustand
- **Real-time:** WebSocket
- **UI Components:** Custom components with Radix UI

### Backend
- **Framework:** FastAPI (Python)
- **Database:** PostgreSQL with SQLAlchemy ORM
- **Cache:** Redis
- **Authentication:** JWT
- **Voice AI:** Omnidim.io Platform
- **WebSocket:** Native FastAPI WebSocket

### Infrastructure
- **Container:** Docker & Docker Compose
- **Frontend Hosting:** Vercel (recommended)
- **Backend Hosting:** Railway/AWS/DigitalOcean
- **Database:** PostgreSQL 15+

## 📋 Prerequisites

- **Node.js** 18+ with npm
- **Python** 3.11+ with pip
- **Docker Desktop** (for easy setup)
- **PostgreSQL** 15+ (or use Docker)
- **Git**
- **Omnidim.io API Key** (for voice features)

## 🚀 Quick Start

### Windows Setup (Recommended)

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/zenith-study-buddy.git
   cd zenith-study-buddy
   ```

2. **Run the automated setup**
   ```bash
   scripts\setup.bat
   ```

3. **Configure environment variables**
   - Edit `backend\.env` - Add your Omnidim API key
   - Edit `frontend\.env.local` - Add your Omnidim API key

4. **Start the application**
   ```bash
   scripts\start.bat
   ```

5. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/api/docs

### Manual Setup

<details>
<summary>Click to expand manual setup instructions</summary>

#### Backend Setup

1. **Navigate to backend**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   copy .env.example .env
   # Edit .env with your settings
   ```

5. **Setup database**
   ```bash
   python scripts/create_db.py
   python scripts/init_db.py
   python scripts/seed_data.py
   ```

6. **Run the server**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

#### Frontend Setup

1. **Navigate to frontend**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Configure environment**
   ```bash
   copy .env.example .env.local
   # Edit .env.local with your settings
   ```

4. **Run development server**
   ```bash
   npm run dev
   ```

</details>

## 🧪 Demo Account

Use these credentials to explore the platform:
- **Username:** demo_student
- **Password:** Demo123!

## 📱 Usage Guide

### 1. Voice Tutoring
- Select a subject (Math, Science, Programming, etc.)
- Choose difficulty level
- Start speaking naturally - the AI tutor will respond
- Use voice commands like "explain again" or "give me an example"

### 2. Language Practice
- Choose target language and proficiency level
- Select conversation scenario (restaurant, travel, business)
- Practice with real-time pronunciation feedback
- Get grammar corrections and vocabulary suggestions

### 3. Exam Preparation
- Select exam type (SAT, GRE, TOEFL, etc.)
- Choose topics to focus on
- Answer questions verbally
- Receive instant feedback and explanations

## 🏗️ Project Structure

```
zenith-study-buddy/
├── frontend/          # Next.js frontend application
│   ├── app/          # App router pages and layouts
│   ├── components/   # Reusable React components
│   ├── hooks/        # Custom React hooks
│   ├── lib/          # Utilities and API clients
│   └── store/        # Zustand state management
│
├── backend/          # FastAPI backend application
│   ├── app/
│   │   ├── api/      # API endpoints
│   │   ├── models/   # Database models
│   │   ├── services/ # Business logic
│   │   └── schemas/  # Pydantic schemas
│   └── migrations/   # Database migrations
│
└── docs/            # Documentation
```

## 🔧 Configuration

### Environment Variables

#### Backend (.env)
```env
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
REDIS_URL=redis://localhost:6379
SECRET_KEY=your-secret-key-here
OMNIDIM_API_KEY=your-omnidim-api-key
```

#### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api
NEXT_PUBLIC_WS_URL=ws://localhost:8000
NEXT_PUBLIC_OMNIDIM_API_KEY=your-omnidim-api-key
```

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest tests/

# Frontend tests
cd frontend
npm run test

# E2E tests
npm run test:e2e
```

## 📊 API Documentation

Once the backend is running, access the interactive API documentation at:
- **Swagger UI:** http://localhost:8000/api/docs
- **ReDoc:** http://localhost:8000/api/redoc

## 🚀 Deployment

### Production Deployment

1. **Frontend (Vercel)**
   ```bash
   vercel --prod
   ```

2. **Backend (Railway/Heroku)**
   - Configure environment variables
   - Deploy using platform-specific CLI

3. **Database (PostgreSQL)**
   - Use managed database service
   - Run migrations: `alembic upgrade head`

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Omnidim.io** - For providing the voice AI platform
- **Microsoft** - For organizing the AI Classroom Hackathon
- **Open Source Community** - For the amazing tools and libraries

## 🐛 Known Issues & Troubleshooting

### Common Issues

1. **Microphone not working**
   - Check browser permissions
   - Ensure HTTPS in production

2. **WebSocket connection failed**
   - Check firewall settings
   - Verify WebSocket URL configuration

3. **Database connection error**
   - Ensure PostgreSQL is running
   - Check connection string in .env

### Getting Help

- 📧 Email: support@zenithstudybuddy.com
- 💬 Discord: [Join our community](https://discord.gg/studybuddy)
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/zenith-study-buddy/issues)

## 🌟 Future Roadmap

- [ ] Mobile app (React Native)
- [ ] Offline mode support
- [ ] Multi-language UI
- [ ] Advanced analytics dashboard
- [ ] Parent/Teacher portals
- [ ] Integration with LMS platforms

---

<p align="center">
  Made with ❤️ for the Microsoft AI Classroom Hackathon
</p>
```