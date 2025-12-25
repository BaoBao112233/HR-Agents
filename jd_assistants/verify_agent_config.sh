#!/bin/bash

# Test Agent Configuration Feature
# Run this script to verify all changes are working

echo "=================================="
echo "Testing Agent Configuration Setup"
echo "=================================="

# Check if migration script exists
echo ""
echo "✓ Checking migration script..."
if [ -f "migrate_add_model_column.py" ]; then
    echo "  ✅ migrate_add_model_column.py exists"
else
    echo "  ❌ migrate_add_model_column.py NOT found"
fi

# Check backend files
echo ""
echo "✓ Checking backend files..."
if grep -q "model String DEFAULT" src/jd_assistants/clickhouse_db.py; then
    echo "  ✅ clickhouse_db.py has 'model' column definition"
else
    echo "  ❌ clickhouse_db.py missing 'model' column"
fi

if grep -q "model: Optional\[str\]" src/jd_assistants/backend/api/v1/api_keys.py; then
    echo "  ✅ api_keys.py has 'model' field in APIKeyCreate"
else
    echo "  ❌ api_keys.py missing 'model' field"
fi

# Check frontend files
echo ""
echo "✓ Checking frontend files..."
if grep -q "name=\"model\"" frontend/src/pages/Settings.jsx; then
    echo "  ✅ Settings.jsx has model selection form"
else
    echo "  ❌ Settings.jsx missing model selection"
fi

if grep -q "title: 'Model'" frontend/src/pages/Settings.jsx; then
    echo "  ✅ Settings.jsx has Model column in table"
else
    echo "  ❌ Settings.jsx missing Model column"
fi

# Check documentation
echo ""
echo "✓ Checking documentation..."
if [ -f "AGENT_CONFIG_GUIDE.md" ]; then
    echo "  ✅ AGENT_CONFIG_GUIDE.md exists"
else
    echo "  ❌ AGENT_CONFIG_GUIDE.md NOT found"
fi

if [ -f "AGENT_CONFIG_SUMMARY.md" ]; then
    echo "  ✅ AGENT_CONFIG_SUMMARY.md exists"
else
    echo "  ❌ AGENT_CONFIG_SUMMARY.md NOT found"
fi

echo ""
echo "=================================="
echo "Verification Complete!"
echo "=================================="
echo ""
echo "Next steps:"
echo "1. Run migration: python migrate_add_model_column.py"
echo "2. Start backend: cd src/jd_assistants && python api_main.py"
echo "3. Start frontend: cd frontend && npm run dev"
echo "4. Open browser and test Settings page"
echo ""
