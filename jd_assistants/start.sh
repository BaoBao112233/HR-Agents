#!/bin/bash

echo "🚀 Starting HR-Agents System with ClickHouse..."

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Copying from .env.example..."
    cp .env.example .env
    echo "✅ .env created. Please edit it with your configuration."
fi

# Stop existing containers
echo "🛑 Stopping existing containers..."
docker-compose down

# Start ClickHouse and Redis first
echo "🚀 Starting ClickHouse and Redis..."
docker-compose up -d clickhouse redis

# Wait for ClickHouse to be ready
echo "⏳ Waiting for ClickHouse to be ready..."
sleep 10

# Check ClickHouse health
echo "🔍 Checking ClickHouse status..."
docker-compose exec -T clickhouse clickhouse-client --query "SELECT 1" > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ ClickHouse is ready"
else
    echo "❌ ClickHouse is not ready. Please check logs: docker-compose logs clickhouse"
    exit 1
fi

# Initialize database
echo "🗄️  Initializing ClickHouse database..."
python init_clickhouse.py

if [ $? -eq 0 ]; then
    echo "✅ Database initialized successfully"
else
    echo "❌ Database initialization failed"
    exit 1
fi

# Build and start application
echo "🏗️  Building and starting application..."
docker-compose build app
docker-compose up -d app

# Wait for app to be ready
echo "⏳ Waiting for application to start..."
sleep 5

# Check application health
echo "🔍 Checking application status..."
curl -s http://localhost:8000/health > /dev/null
if [ $? -eq 0 ]; then
    echo "✅ Application is running"
else
    echo "⚠️  Application might not be ready yet. Check logs: docker-compose logs app"
fi

# Show running containers
echo ""
echo "📦 Running containers:"
docker-compose ps

echo ""
echo "🎉 System started successfully!"
echo ""
echo "📝 Next steps:"
echo "  1. Access API: http://localhost:8000"
echo "  2. API Docs: http://localhost:8000/docs"
echo "  3. Login: admin@hr-system.com / admin123"
echo "  4. Add API keys in Settings"
echo ""
echo "📊 View logs:"
echo "  docker-compose logs -f app"
echo ""
echo "🛑 Stop system:"
echo "  docker-compose down"
