"""
Migration script to add 'model' column to api_keys table
Run this script once to update existing database schema
"""
from src.jd_assistants.clickhouse_db import get_clickhouse

def migrate_add_model_column():
    """Add model column to api_keys table if it doesn't exist"""
    db = get_clickhouse()
    
    try:
        # Check if column exists
        query = f"""
            SELECT name FROM system.columns 
            WHERE database = '{db.database}' 
            AND table = 'api_keys' 
            AND name = 'model'
        """
        result = db.query(query)
        
        if len(result.result_rows) == 0:
            # Column doesn't exist, add it
            print("Adding 'model' column to api_keys table...")
            alter_query = f"""
                ALTER TABLE {db.database}.api_keys 
                ADD COLUMN IF NOT EXISTS model String DEFAULT ''
            """
            db.execute(alter_query)
            print("✅ Successfully added 'model' column to api_keys table")
        else:
            print("✅ 'model' column already exists in api_keys table")
            
    except Exception as e:
        print(f"❌ Error during migration: {e}")
        raise

if __name__ == "__main__":
    print("Starting migration: Add model column to api_keys table")
    migrate_add_model_column()
    print("Migration completed!")
