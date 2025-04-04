#!/usr/bin/env python3
"""
Run source attribution testing and analysis.
"""
import os
import sys
import subprocess
import time
import argparse

# Add the project root to the Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def run_command(command):
    """Run a command and print its output."""
    print(f"\n{'='*50}")
    print(f"Running: {command}")
    print(f"{'='*50}\n")
    
    process = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True
    )
    
    for line in process.stdout:
        print(line, end='')
    
    process.wait()
    return process.returncode

def main():
    parser = argparse.ArgumentParser(description='Run source attribution testing and analysis')
    parser.add_argument('--test-only', action='store_true', help='Only run the source testing')
    parser.add_argument('--analyze-only', action='store_true', help='Only run the source analysis')
    parser.add_argument('--models', type=str, help='Comma-separated list of models to test')
    args = parser.parse_args()
    
    # Create results directory if it doesn't exist
    os.makedirs("results", exist_ok=True)
    
    # Run source testing
    if not args.analyze_only:
        print("\nRunning source testing...")
        test_command = f"PYTHONPATH={project_root} python utils/source_testing.py"
        if args.models:
            test_command += f" --models {args.models}"
        
        start_time = time.time()
        run_command(test_command)
        print(f"\nSource testing completed in {time.time() - start_time:.2f} seconds")
    
    # Run source analysis
    if not args.test_only:
        print("\nRunning source analysis...")
        start_time = time.time()
        run_command(f"PYTHONPATH={project_root} python utils/source_analysis_new.py")
        print(f"\nSource analysis completed in {time.time() - start_time:.2f} seconds")
    
    print("\nAll tasks completed successfully!")

if __name__ == "__main__":
    main() 