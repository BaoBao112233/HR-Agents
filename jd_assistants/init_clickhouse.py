#!/usr/bin/env python3
"""
Initialize ClickHouse database for HR System
"""
import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from jd_assistants.clickhouse_db import init_clickhouse, create_user, get_password_hash

def main():
    """Initialize ClickHouse database and create default admin user"""
    print("🚀 Initializing ClickHouse database...")
    
    try:
        # Initialize database schema
        init_clickhouse()
        print("✅ Database schema created successfully")
        
        # Create default admin user if not exists
        from jd_assistants.clickhouse_db import get_user_by_email
        admin_email = "admin@hr-system.com"
        
        if not get_user_by_email(admin_email):
            from passlib.context import CryptContext
            pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
            
            admin_user = {
                "email": admin_email,
                "password_hash": pwd_context.hash("admin123"),
                "role": "admin"
            }
            create_user(admin_user)
            print(f"✅ Default admin user created: {admin_email} / admin123")
            print("⚠️  Please change the default password after first login!")
        else:
            print(f"ℹ️  Admin user already exists: {admin_email}")
        
        print("\n🎉 Database initialization completed successfully!")
        print("\nNext steps:")
        print("1. Start the application: docker-compose up -d")
        print("2. Access the API: http://localhost:8000")
        print("3. Login with: admin@hr-system.com / admin123")
        print("4. Add your LLM API keys in settings")
        
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
