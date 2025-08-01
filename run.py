#!/usr/bin/env python3
import os
import subprocess
import sys
import time
import webbrowser
from dotenv import load_dotenv

def main():
    load_dotenv()
    
    print("Starting Hybrid Search System...")
    
    try:
        import streamlit
        print("Streamlit is available")
    except ImportError:
        print("Streamlit not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "streamlit"])
    
    print("Launching application...")
    
    cmd = [sys.executable, "-m", "streamlit", "run", "hybrid_search_app.py", "--server.headless", "true"]
    
    process = subprocess.Popen(cmd)
    
    time.sleep(3)
    
    webbrowser.open("http://localhost:8501")
    
    print("Application started at http://localhost:8501")
    print("Press Ctrl+C to stop the application")
    
    try:
        process.wait()
    except KeyboardInterrupt:
        process.terminate()
        print("\nApplication stopped.")

if __name__ == "__main__":
    main() 