#!/usr/bin/env python3
"""
Start script with automatic database migration
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    """Main function"""
    print("=" * 60)
    print("🎓 TEACHER ATTENDANCE APP - STARTING...")
    print("=" * 60)
    
    # Change to backend directory
    backend_dir = Path(__file__).parent / "backend"
    if not backend_dir.exists():
        print("❌ Error: backend directory not found")
        return
    
    os.chdir(backend_dir)
    
    # Check if database exists
    db_path = backend_dir / "instance" / "teacher_attendance.db"
    
    if not db_path.exists():
        print("📊 Database not found. Creating new database...")
        choice = input("Do you want to (1) Create with sample data or (2) Create empty? [1/2]: ").strip()
        
        if choice == "1":
            try:
                subprocess.run([sys.executable, "reset_database.py"], input="y\n", text=True, check=True)
            except subprocess.CalledProcessError as e:
                print(f"❌ Error creating database: {e}")
                return
        else:
            print("Creating empty database...")
    else:
        print("📊 Database found. Running migration...")
        try:
            subprocess.run([sys.executable, "migrate_database.py"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Migration error: {e}")
            choice = input("Do you want to reset the database? (y/N): ").strip().lower()
            if choice == 'y':
                try:
                    subprocess.run([sys.executable, "reset_database.py"], input="y\n", text=True, check=True)
                except subprocess.CalledProcessError as e:
                    print(f"❌ Error resetting database: {e}")
                    return
    
    try:
        print("\n🚀 Starting Flask application...")
        print("📍 App will be available at: http://127.0.0.1:5000")
        print("🔄 Press Ctrl+C to stop the server")
        print("-" * 50)
        
        # Run the app
        subprocess.call([sys.executable, "app.py"])
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()