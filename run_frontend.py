#!/usr/bin/env python3
"""
Script to run the Pilar2 frontend application
"""

import os
import sys
import subprocess

def run_frontend():
    """Run the frontend application"""
    # Change to frontend directory
    frontend_dir = os.path.join(os.path.dirname(__file__), 'frontend')
    os.chdir(frontend_dir)
    
    # Run the frontend
    try:
        subprocess.run([
            sys.executable, '-m', 'streamlit', 'run', 'app.py', 
            '--server.port', '8501'
        ], check=True)
    except KeyboardInterrupt:
        print("\nFrontend application stopped.")
    except Exception as e:
        print(f"Error running frontend: {e}")

if __name__ == "__main__":
    run_frontend()
