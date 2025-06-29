#!/bin/bash

# Zenith Study Buddy - Deployment Script

echo "🚀 Deploying Zenith Study Buddy..."

# Check environment
if [ "$1" != "staging" ] && [ "$1" != "production" ]; then
    echo "Usage: ./deploy.sh [staging|production]"
    exit 1
fi

ENVIRONMENT=$1
echo "📍 Deploying to: $ENVIRONMENT"

# Build Docker images
echo "🏗️ Building Docker images..."
docker-compose build

# Run tests
echo "🧪 Running tests..."
cd backend
pytest tests/
if [ $? -ne 0 ]; then
    echo "❌ Tests failed. Aborting deployment."
    exit 1
fi
cd ..

# Tag images
echo "🏷️ Tagging images..."
docker tag zenith-study-buddy-backend:latest your-registry/zenith-backend:$ENVIRONMENT
docker tag zenith-study-buddy-frontend:latest your-registry/zenith-frontend:$ENVIRONMENT

# Push images
echo "📤 Pushing images to registry..."
docker push your-registry/zenith-backend:$ENVIRONMENT
docker push your-registry/zenith-frontend:$ENVIRONMENT

# Deploy based on environment
if [ "$ENVIRONMENT" == "production" ]; then
    echo "🌐 Deploying to production..."
    # Add production deployment commands
    # kubectl apply -f k8s/production/
else
    echo "🔧 Deploying to staging..."
    # Add staging deployment commands
    # kubectl apply -f k8s/staging/
fi

echo "✅ Deployment complete!"