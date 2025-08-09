#!/usr/bin/env python3
"""
Script to run the Pilar2 backend server
"""

import os
import sys
import subprocess

def run_backend():
    """Run the backend server"""
    # Get the project root directory
    project_root = os.path.dirname(os.path.abspath(__file__))
    
    # Run the backend from project root with proper module path
    try:
        subprocess.run([
            sys.executable, '-m', 'uvicorn', 'backend.main:app', 
            '--reload', '--host', '0.0.0.0', '--port', '8000'
        ], cwd=project_root, check=True)
    except KeyboardInterrupt:
        print("\nBackend server stopped.")
    except Exception as e:
        print(f"Error running backend: {e}")

if __name__ == "__main__":
    run_backend()
