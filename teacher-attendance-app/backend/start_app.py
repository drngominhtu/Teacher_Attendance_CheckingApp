"""
Script khởi động app với xử lý ngoại lệ tốt hơn
"""
import sys
import os

def main():
    """Khởi động app với xử lý lỗi tốt hơn"""
    try:
        # Thêm thư mục hiện tại vào Python path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        if current_dir not in sys.path:
            sys.path.append(current_dir)
        
        # Import và chạy app
        print("🚀 Starting Flask application...")
        from app import app
        
        # Chạy app
        app.run(debug=True)
        
    except Exception as e:
        print(f"❌ Error starting app: {e}")
        import traceback
        traceback.print_exc()
        
        # Chờ input để người dùng có thể đọc lỗi
        input("Press Enter to exit...")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
