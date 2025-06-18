"""
Debug script to start app with better error handling
"""
import sys
import os

# Add current directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

def main():
    try:
        print("=" * 50)
        print("🔧 DEBUGGING FLASK APP START")
        print("=" * 50)
        
        # Check database file
        instance_dir = os.path.join(current_dir, 'instance')
        db_path = os.path.join(instance_dir, 'teacher_attendance.db')
        print(f"📁 Instance dir: {instance_dir}")
        print(f"🗃️  Database path: {db_path}")
        print(f"📊 Database exists: {os.path.exists(db_path)}")
        
        # Try to run migration first
        print("\n🔄 Running migration...")
        try:
            from migrate_database_v3 import migrate_database
            result = migrate_database()
            print(f"✓ Migration result: {result}")
        except Exception as migrate_error:
            print(f"⚠️  Migration error: {migrate_error}")
        
        # Try to import models
        print("\n📦 Testing model imports...")
        try:
            from models.degree import Degree
            print("✓ Degree model imported")
        except Exception as e:
            print(f"✗ Degree model error: {e}")
            
        try:
            from models.Department import Department
            print("✓ Department model imported")
        except Exception as e:
            print(f"✗ Department model error: {e}")
        
        # Try to start app
        print("\n🚀 Starting Flask app...")
        from app import app
        
        print("✓ App imported successfully")
        print("🌐 Starting server on http://127.0.0.1:5000")
        print("🔄 Press Ctrl+C to stop")
        print("-" * 50)
        
        app.run(debug=True, host='127.0.0.1', port=5000, use_reloader=False)
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        print("\n📋 Full traceback:")
        traceback.print_exc()
        print("\n" + "=" * 50)
        input("⏸️  Press Enter to exit...")

if __name__ == "__main__":
    main()
