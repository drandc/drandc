"""
SQL Practice Generator - Setup Script
Run this script to initialize the application
"""
import os
import sys
import subprocess

def main():
    print("=" * 60)
    print("SQL Practice Generator - Setup")
    print("=" * 60)

    # Get the directory of this script
    base_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(base_dir)

    # Check Python version
    print(f"\nPython version: {sys.version}")
    if sys.version_info < (3, 8):
        print("Warning: Python 3.8 or higher is recommended")

    # Install dependencies
    print("\nInstalling dependencies...")
    requirements_file = os.path.join(base_dir, 'requirements.txt')
    if os.path.exists(requirements_file):
        try:
            subprocess.check_call([
                sys.executable, '-m', 'pip', 'install', '-r', requirements_file
            ])
            print("Dependencies installed successfully!")
        except subprocess.CalledProcessError as e:
            print(f"Error installing dependencies: {e}")
            print("You can install them manually with: pip install -r requirements.txt")
    else:
        print("requirements.txt not found, skipping dependency installation")

    # Create data directory
    data_dir = os.path.join(base_dir, 'data')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print(f"\nCreated data directory: {data_dir}")

    # Initialize exercise database
    print("\nInitializing exercise database...")
    try:
        from database.data_generator import initialize_exercise_database
        initialize_exercise_database()
        print("Exercise database initialized successfully!")
    except Exception as e:
        print(f"Error initializing database: {e}")
        print("The database will be initialized on first run")

    # Initialize user database
    print("\nInitializing user database...")
    try:
        from database.db_manager import DatabaseManager
        from config import DATABASE_PATH
        db = DatabaseManager(DATABASE_PATH)
        db.init_user_database()
        print("User database initialized successfully!")
    except Exception as e:
        print(f"Error initializing user database: {e}")

    print("\n" + "=" * 60)
    print("Setup complete!")
    print("=" * 60)
    print("\nTo start the application, run:")
    print(f"  python {os.path.join(base_dir, 'app.py')}")
    print("\nOr on Windows:")
    print(f"  python app.py")
    print("\nThen open http://127.0.0.1:5000 in your browser")
    print("=" * 60)

if __name__ == '__main__':
    main()
