import os
import subprocess
import sys
import time

def run_command(command, shell=True):
    """Run a command and display its output in real-time"""
    print(f"\n> Executing: {command}")
    try:
        process = subprocess.Popen(
            command,
            shell=shell,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )
        
        # Print output in real-time
        for line in process.stdout:
            print(line, end='')
        
        process.wait()
        
        if process.returncode != 0:
            print(f"Command failed with exit code {process.returncode}")
            return False
        return True
    except Exception as e:
        print(f"Error executing command: {e}")
        return False

def main():
    print("Starting VelozAcademy setup process...")
    
    # Step 2: Create a virtual environment
    print("\n--- Step 2: Creating virtual environment ---")
    if not os.path.exists("venv"):
        if not run_command("python -m venv venv"):
            return
    else:
        print("Virtual environment already exists, skipping creation.")
    
    # Activate virtual environment (by modifying PATH)
    if os.name == 'nt':  # Windows
        venv_path = os.path.abspath(os.path.join(os.curdir, "venv", "Scripts"))
    else:  # Non-Windows (e.g., Linux, macOS)
        venv_path = os.path.abspath(os.path.join(os.curdir, "venv", "bin"))
    os.environ["PATH"] = venv_path + os.pathsep + os.environ["PATH"]
    
    # Step 3: Install dependencies
    print("\n--- Step 3: Installing dependencies ---")
    if not run_command("pip install -r requirements.txt"):
        return
    
    # Step 4: Execute database migrations
    print("\n--- Step 4: Running database migrations ---")
    if not run_command("python manage.py migrate"):
        return
    
    # Step 6: Populate the database with initial data
    print("\n--- Step 6: Populating database with initial data ---")
    if not run_command("python populate_db.py"):
        return
    
    if not run_command("python populate_trilhas.py"):
        return
    
    # Step 8: Start the development server
    print("\n--- Step 8: Starting development server ---")
    print("Server will start at http://127.0.0.1:8000/")
    print("Press Ctrl+C to stop the server")
    time.sleep(2)  # Give user time to read the message
    run_command("python manage.py runserver")

if __name__ == "__main__":
    main() 