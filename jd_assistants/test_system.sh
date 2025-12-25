#!/bin/bash

echo "========================================="
echo "Testing HR System with Agent Configuration"
echo "========================================="
echo ""

# Check containers
echo "1. Checking Docker containers..."
sudo docker ps --filter "name=hr_" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
echo ""

# Check ClickHouse
echo "2. Checking ClickHouse database..."
sudo docker exec hr_clickhouse clickhouse-client --query "SELECT count() as table_count FROM system.tables WHERE database = 'hr_system'" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✅ ClickHouse is running"
    sudo docker exec hr_clickhouse clickhouse-client --query "SHOW TABLES FROM hr_system"
else
    echo "❌ ClickHouse error"
fi
echo ""

# Check api_keys table schema
echo "3. Checking api_keys table (with model field)..."
sudo docker exec hr_clickhouse clickhouse-client --query "DESCRIBE TABLE hr_system.api_keys" 2>/dev/null | grep -E "id|provider|model"
echo ""

# Test API endpoints
echo "4. Testing API endpoints..."

echo "   Testing /api/v1/api-keys/providers/list..."
response=$(curl -s http://localhost:8000/api/v1/api-keys/providers/list)
if echo "$response" | grep -q "openai"; then
    echo "   ✅ Providers endpoint working"
    echo "$response" | python3 -c "import sys, json; data = json.load(sys.stdin); print(f\"   Found {len(data['providers'])} providers: {', '.join([p['id'] for p in data['providers']])}\")"
else
    echo "   ❌ Providers endpoint failed"
fi
echo ""

# Test frontend
echo "5. Testing frontend..."
frontend=$(curl -s http://localhost:8000/ | head -1)
if echo "$frontend" | grep -q "DOCTYPE"; then
    echo "   ✅ Frontend is accessible"
else
    echo "   ❌ Frontend not accessible"
fi
echo ""

# Check app logs
echo "6. Checking application logs (last 5 lines)..."
sudo docker logs hr_app --tail 5
echo ""

echo "========================================="
echo "✅ All tests completed!"
echo "========================================="
echo ""
echo "Access points:"
echo "- Frontend: http://localhost:8000"
echo "- API: http://localhost:8000/api/v1"
echo "- ClickHouse: http://52.65.20.57:8123"
echo ""
echo "To add an API key:"
echo "1. Open http://localhost:8000"
echo "2. Navigate to Settings page"
echo "3. Click 'Thêm API Key'"
echo "4. Select provider (OpenAI, Groq, etc.)"
echo "5. Select model"
echo "6. Enter API key"
echo "7. Click 'Thêm Key'"
