#!/usr/bin/env python3
import os
import sys
import json
import time
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

def ensure_ollama_running():
    """Check if Ollama is running and start it if needed."""
    import subprocess
    try:
        # Try to connect to Ollama
        subprocess.run(["ollama", "list"], check=True, capture_output=True)
    except subprocess.CalledProcessError:
        print("Starting Ollama server...")
        subprocess.Popen(["ollama", "serve"])
        time.sleep(5)  # Wait for server to start

def run_model_test(model_name):
    """Run source testing for a specific model."""
    print(f"\nTesting {model_name}...")
    cmd = f"PYTHONPATH={os.getcwd()} python utils/source_testing.py --models '{model_name}'"
    os.system(cmd)
    
    # Load results from the main results file
    results_file = "results/source_testing_results.json"
    if os.path.exists(results_file):
        with open(results_file, 'r') as f:
            all_results = json.load(f)
            # Extract results for this model
            if model_name in all_results:
                return all_results[model_name]
    return None

def generate_visualizations(results, model_name):
    """Generate visualizations for model results."""
    # Create results directory if it doesn't exist
    Path("results").mkdir(exist_ok=True)
    
    # Prepare data
    categories = ['RAG_DATASET', 'TRAINING_DATA', 'HALLUCINATION']
    accuracies = []
    confidences = {cat: [] for cat in categories}
    
    for cat in categories:
        if cat in results:
            correct = sum(1 for q in results[cat] if q['source'] == q['expected_source'])
            total = len(results[cat])
            accuracies.append(correct/total if total > 0 else 0)
            
            # Collect confidence scores
            for q in results[cat]:
                if q['confidence'] == 'HIGH':
                    confidences[cat].append(1.0)
                elif q['confidence'] == 'MEDIUM':
                    confidences[cat].append(0.5)
                else:
                    confidences[cat].append(0.0)
    
    # Plot accuracy distribution
    plt.figure(figsize=(10, 6))
    sns.histplot(accuracies, bins=20)
    plt.title(f'Accuracy Distribution - {model_name}')
    plt.xlabel('Accuracy')
    plt.ylabel('Count')
    plt.savefig(f'results/accuracy_dist_{model_name}.png')
    plt.close()
    
    # Plot confidence distribution by source
    plt.figure(figsize=(12, 6))
    for cat in categories:
        if confidences[cat]:
            sns.kdeplot(data=confidences[cat], label=cat)
    plt.title(f'Confidence Distribution by Source - {model_name}')
    plt.xlabel('Confidence')
    plt.ylabel('Density')
    plt.legend()
    plt.savefig(f'results/confidence_dist_{model_name}.png')
    plt.close()

def generate_markdown_report(models_results):
    """Generate a markdown report with results and visualizations."""
    report = "# Source Attribution Analysis Report\n\n"
    report += f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    
    # Add overall summary
    report += "## Overall Summary\n\n"
    report += "| Model | RAG_DATASET | TRAINING_DATA | HALLUCINATION |\n"
    report += "|-------|-------------|---------------|---------------|\n"
    
    for model_name, results in models_results.items():
        row = f"| {model_name} |"
        for cat in ['RAG_DATASET', 'TRAINING_DATA', 'HALLUCINATION']:
            if cat in results:
                correct = sum(1 for q in results[cat] if q['source'] == q['expected_source'])
                total = len(results[cat])
                accuracy = (correct/total)*100 if total > 0 else 0
                row += f" {accuracy:.1f}% ({correct}/{total}) |"
            else:
                row += " N/A |"
        report += row + "\n"
    
    report += "\n## Detailed Results\n\n"
    
    for model_name, results in models_results.items():
        report += f"### {model_name}\n\n"
        
        # Summary statistics
        categories = ['RAG_DATASET', 'TRAINING_DATA', 'HALLUCINATION']
        for cat in categories:
            if cat in results:
                correct = sum(1 for q in results[cat] if q['source'] == q['expected_source'])
                total = len(results[cat])
                accuracy = (correct/total)*100 if total > 0 else 0
                report += f"#### {cat}\n"
                report += f"- Accuracy: {accuracy:.1f}% ({correct}/{total})\n\n"
        
        # Visualizations
        report += "#### Visualizations\n\n"
        report += f"![Accuracy Distribution](results/accuracy_dist_{model_name}.png)\n\n"
        report += f"![Confidence Distribution](results/confidence_dist_{model_name}.png)\n\n"
        
        # Detailed results
        report += "#### Question Details\n\n"
        for cat in categories:
            if cat in results:
                report += f"##### {cat} Questions\n\n"
                for q in results[cat]:
                    report += f"- Question: {q['question']}\n"
                    report += f"  - Answer: {q['answer']}\n"
                    report += f"  - Source: {q['source']} (Expected: {q['expected_source']})\n"
                    report += f"  - Confidence: {q['confidence']}\n\n"
    
    # Save report
    with open("results/source_attribution_report.md", 'w') as f:
        f.write(report)
    
    # Convert to PDF if pandoc is available
    try:
        os.system("pandoc results/source_attribution_report.md -o results/source_attribution_report.pdf")
    except:
        print("Pandoc not available. PDF generation skipped.")

def main():
    # Ensure Ollama is running
    ensure_ollama_running()
    
    # Models to test
    models = [
        "deepseek-r1-1.5b",
        "llama3.2-1b",
        "qwen2.5-1.5b"
    ]
    
    # Run tests and collect results
    models_results = {}
    for model in models:
        results = run_model_test(model)
        if results:
            models_results[model] = results
            generate_visualizations(results, model)
    
    # Generate report
    generate_markdown_report(models_results)
    
    print("\nAnalysis complete! Check results/source_attribution_report.md for the full report.")
    print("A PDF version has also been generated if pandoc was available.")

if __name__ == "__main__":
    main() 