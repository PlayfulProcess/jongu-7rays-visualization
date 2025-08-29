#!/usr/bin/env python3
"""
Quick setup script to run the full pipeline
"""

import subprocess
import sys
from pathlib import Path

def run_command(cmd, description):
    """Run a command and handle errors"""
    print(f"\n[Running] {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"[Success] {description} completed successfully")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"[Error] {description} failed")
        if e.stdout:
            print("STDOUT:", e.stdout)
        if e.stderr:
            print("STDERR:", e.stderr)
        return False

def main():
    """Run the complete pipeline"""
    
    # Check if data directory exists
    if not Path('data').exists():
        Path('data').mkdir()
    
    # Step 1: Create knowledge graph triples
    if not run_command("python create_triples.py", "Creating knowledge graph triples"):
        return False
    
    # Step 2: Train knowledge graph embeddings  
    if not run_command("python train.py", "Training knowledge graph embeddings"):
        return False
    
    # Step 3: Launch the Gradio app
    print("\n[Ready] Ready to launch the Gradio app!")
    print("Run: python app.py")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
    
    print("\n[Complete] Setup complete! The Seven Rays Vector Space is ready to explore.")