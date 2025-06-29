#!/bin/bash

# Zenith Study Buddy - Setup Script

echo "🚀 Setting up Zenith Study Buddy..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create .env files if they don't exist
if [ ! -f backend/.env ]; then
    echo "📝 Creating backend .env file..."
    cp backend/.env.example backend/.env
    echo "⚠️  Please update backend/.env with your actual values"
fi

if [ ! -f frontend/.env.local ]; then
    echo "📝 Creating frontend .env.local file..."
    echo "NEXT_PUBLIC_API_URL=http://localhost:8000/api" > frontend/.env.local
    echo "NEXT_PUBLIC_WS_URL=ws://localhost:8000" >> frontend/.env.local
    echo "NEXT_PUBLIC_OMNIDIM_API_KEY=your-omnidim-api-key" >> frontend/.env.local
    echo "⚠️  Please update frontend/.env.local with your Omnidim API key"
fi

# Start services
echo "🐳 Starting Docker services..."
docker-compose up -d postgres redis

# Wait for PostgreSQL to be ready
echo "⏳ Waiting for PostgreSQL to be ready..."
sleep 5

# Run database migrations
echo "🗄️ Running database migrations..."
cd backend
python scripts/init_db.py
python scripts/seed_data.py
cd ..

# Install frontend dependencies
echo "📦 Installing frontend dependencies..."
cd frontend
npm install
cd ..

# Start all services
echo "🚀 Starting all services..."
docker-compose up -d

echo "✅ Setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Update backend/.env with your Omnidim API key and other settings"
echo "2. Update frontend/.env.local with your Omnidim API key"
echo "3. Access the application at http://localhost:3000"
echo "4. API documentation available at http://localhost:8000/api/docs"
echo ""
echo "📧 Demo credentials:"
echo "Username: demo_student"
echo "Password: Demo123!"