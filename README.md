# 🎓 Zenith Study Buddy - AI-Powered Voice Learning Platform

\<p align="center"\>
\<strong\>Transform your learning experience with AI-powered voice conversations\</strong\>
\</p\>

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
  - **Database:** SQLite with SQLAlchemy ORM
  - **Cache:** Redis
  - **Authentication:** JWT
  - **Voice AI:** Omnidim.io Platform
  - **WebSocket:** Native FastAPI WebSocket

### Infrastructure

  - **Container:** Docker & Docker Compose
  - **Frontend Hosting:** Vercel (recommended)
  - **Backend Hosting:** Railway/AWS/DigitalOcean
  - **Database:** SQLite (file-based)

## 📋 Prerequisites

  - **Node.js** 18+ with npm
  - **Python** 3.11+ with pip
  - **Git**
  - **Omnidim.io API Key** (for voice features)

## 🚀 Quick Start

### Windows Setup (Recommended)

1.  **Clone the repository**

    ```bash
    git clone https://github.com/yourusername/zenith-study-buddy.git
    cd zenith-study-buddy
    ```

2.  **Run the automated setup**
    This script will set up the frontend and backend dependencies and initialize the SQLite database.

    ```bash
    scripts\setup.bat
    ```

3.  **Configure environment variables**

      - Edit `backend\.env` - Add your Omnidim API key.
      - Edit `frontend\.env.local` - Add your Omnidim API key.

4.  **Start the application**

    ```bash
    scripts\start.bat
    ```

5.  **Access the application**

      - Frontend: `http://localhost:3000`
      - Backend API: `http://localhost:8000`
      - API Documentation: `http://localhost:8000/api/docs`

### Manual Setup

\<details\>
\<summary\>Click to expand manual setup instructions\</summary\>

#### Backend Setup

1.  **Navigate to backend**

    ```bash
    cd backend
    ```

2.  **Create virtual environment**

    ```bash
    python -m venv venv
    venv\Scripts\activate  # Windows
    source venv/bin/activate  # Linux/Mac
    ```

3.  **Install dependencies**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure environment**
    Create a `.env` file from the example and add your settings. The `DATABASE_URL` is already set for SQLite.

    ```bash
    # In Windows command prompt
    copy .env.example .env

    # In Linux/Mac/Git Bash
    cp .env.example .env
    ```

    Now, edit the `.env` file with your `OMNIDIM_API_KEY` and a `SECRET_KEY`.

5.  **Setup and seed the SQLite database**
    Run the initialization script to create the database file (`zenith_study_buddy.db`) and seed it with default users.

    ```bash
    python scripts/init_sqlite.py
    ```

6.  **Run the server**

    ```bash
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
    ```

#### Frontend Setup

1.  **Navigate to frontend**

    ```bash
    cd frontend
    ```

2.  **Install dependencies**

    ```bash
    npm install
    ```

3.  **Configure environment**
    Create a `.env.local` file from the example and add your API keys.

    ```bash
    # In Windows command prompt
    copy .env.example .env.local

    # In Linux/Mac/Git Bash
    cp .env.example .env.local
    ```

    Ensure `NEXT_PUBLIC_API_URL` points to your backend and add your `NEXT_PUBLIC_OMNIDIM_API_KEY`.

4.  **Run development server**

    ```bash
    npm run dev
    ```

\</details\>

## 🧪 Demo Account

Use these credentials to explore the platform:

  - **Username:** `demo_student`
  - **Password:** `Demo123!`

## 📱 Usage Guide

### 1\. Voice Tutoring

  - Select a subject (Math, Science, Programming, etc.)
  - Choose difficulty level
  - Start speaking naturally - the AI tutor will respond
  - Use voice commands like "explain again" or "give me an example"

### 2\. Language Practice

  - Choose target language and proficiency level
  - Select conversation scenario (restaurant, travel, business)
  - Practice with real-time pronunciation feedback
  - Get grammar corrections and vocabulary suggestions

### 3\. Exam Preparation

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
DATABASE_URL=sqlite:///./zenith_study_buddy.db
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
```

## 📊 API Documentation

Once the backend is running, access the interactive API documentation at:

  - **Swagger UI:** `http://localhost:8000/api/docs`
  - **ReDoc:** `http://localhost:8000/api/redoc`

## 🚀 Deployment

### Production Deployment

1.  **Frontend (Vercel)**

    ```bash
    vercel --prod
    ```

2.  **Backend (Railway/Heroku)**

      - Configure environment variables on your platform of choice.
      - The SQLite database will be a file within your deployed backend service. Be aware of ephemeral filesystems on some platforms.

## 🤝 Contributing

We welcome contributions\! Please follow these steps:

1.  Fork the repository
2.  Create a feature branch (`git checkout -b feature/amazing-feature`)
3.  Commit your changes (`git commit -m 'Add amazing feature'`)
4.  Push to the branch (`git push origin feature/amazing-feature`)
5.  Open a Pull Request

## 📝 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

  - **Omnidim.io** - For providing the voice AI platform
  - **Microsoft** - For organizing the AI Classroom Hackathon
  - **Open Source Community** - For the amazing tools and libraries

## 🐛 Known Issues & Troubleshooting

### Common Issues

1.  **Microphone not working**

      - Check browser permissions.
      - Ensure HTTPS is used in production.

2.  **WebSocket connection failed**

      - Check firewall settings.
      - Verify WebSocket URL configuration in `frontend/.env.local`.

### Getting Help

  - Open an issue on the project's GitHub page.

## 🌟 Future Roadmap

  - [ ] Mobile app (React Native)
  - [ ] Offline mode support
  - [ ] Multi-language UI
  - [ ] Advanced analytics dashboard
  - [ ] Parent/Teacher portals
  - [ ] Integration with LMS platforms

-----

\<p align="center"\>
Made with ❤️ for the Microsoft AI Classroom Hackathon
\</p\>