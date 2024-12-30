from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import sys
import os
from dotenv import load_dotenv

def test_database_connection():
    try:
        # Load environment variables
        load_dotenv()
        
        # Get database URL from environment
        DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://localhost/resumerocket')
        
        # Create engine
        engine = create_engine(DATABASE_URL)
        
        # Try to connect and execute a simple query
        with engine.connect() as connection:
            result = connection.execute(text('SELECT 1'))
            print("✅ Database connection successful!")
            
            # Test table creation
            connection.execute(text('''
                CREATE TABLE IF NOT EXISTS test_table (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100)
                )
            '''))
            print("✅ Test table creation successful!")
            
            # Insert test data
            connection.execute(text('''
                INSERT INTO test_table (name) VALUES ('test_name')
            '''))
            connection.commit()
            print("✅ Test data insertion successful!")
            
            # Query test data
            result = connection.execute(text('SELECT * FROM test_table')).fetchall()
            print(f"✅ Retrieved {len(result)} rows from test table")
            
            # Cleanup
            connection.execute(text('DROP TABLE test_table'))
            connection.commit()
            print("✅ Cleanup successful!")
            
    except SQLAlchemyError as e:
        print("❌ Database error:", str(e))
        sys.exit(1)
    except Exception as e:
        print("❌ Error:", str(e))
        sys.exit(1)

if __name__ == "__main__":
    print("🔍 Testing database connection...")
    test_database_connection()