from core.rag_inference import RAGInference
import json
import os
import time
from typing import Dict, List, Any
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter

def analyze_source_distribution(results_file: str) -> Dict[str, Dict[str, int]]:
    """
    Analyze the distribution of sources across models.
    
    Args:
        results_file (str): Path to the results JSON file
        
    Returns:
        dict: Distribution of sources for each model
    """
    with open(results_file, 'r') as f:
        all_results = json.load(f)
    
    source_distribution = {}
    
    for model_name, model_results in all_results.items():
        source_counts = {
            "RAG_DATASET": 0,
            "TRAINING_DATA": 0,
            "HALLUCINATION": 0,
            "UNKNOWN": 0
        }
        
        for result in model_results.get("results", []):
            source = result.get("source", "UNKNOWN")
            source_counts[source] = source_counts.get(source, 0) + 1
        
        source_distribution[model_name] = source_counts
    
    return source_distribution

def plot_source_distribution(source_distribution: Dict[str, Dict[str, int]], output_file: str = None):
    """
    Plot the distribution of sources across models.
    
    Args:
        source_distribution (dict): Distribution of sources for each model
        output_file (str, optional): Path to save the plot
    """
    models = list(source_distribution.keys())
    sources = ["RAG_DATASET", "TRAINING_DATA", "HALLUCINATION", "UNKNOWN"]
    
    # Set up the figure
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Set up the bar positions
    bar_width = 0.2
    positions = np.arange(len(models))
    
    # Create bars for each source
    for i, source in enumerate(sources):
        values = [source_distribution[model].get(source, 0) for model in models]
        ax.bar(positions + i * bar_width, values, bar_width, label=source)
    
    # Add labels and title
    ax.set_xlabel('Models')
    ax.set_ylabel('Count')
    ax.set_title('Source Distribution Across Models')
    ax.set_xticks(positions + bar_width * 1.5)
    ax.set_xticklabels(models)
    ax.legend()
    
    # Save or show the plot
    if output_file:
        plt.savefig(output_file)
        print(f"Plot saved to {output_file}")
    else:
        plt.show()

def run_source_analysis(questions: List[str] = None) -> Dict[str, Any]:
    """
    Run a source analysis on a set of questions.
    
    Args:
        questions (list, optional): List of questions to analyze
        
    Returns:
        dict: Analysis results
    """
    if questions is None:
        questions = [
            "What is the capital of France?",
            "Who was the first President of the United States?",
            "What is the largest planet in our solar system?",
            "What is the chemical symbol for gold?",
            "Who painted the Mona Lisa?",
            "What is the square root of 144?",
            "What is the chemical formula for water?",
            "Who wrote 'Romeo and Juliet'?",
            "What is the speed of light?",
            "What is the capital of Japan?"
        ]
    
    models = ["deepseek-r1-1.5b", "llama3.2-1b", "qwen2.5-1.5b"]
    results = {}
    
    for model_name in models:
        print(f"\nAnalyzing {model_name}...")
        rag = RAGInference(model_name)
        
        model_results = []
        for question in questions:
            print(f"  Question: {question}")
            result = rag.answer_question(question)
            if result:
                model_results.append(result)
                print(f"    Answer: {result['answer'][:100]}...")
                print(f"    Source: {result['source']}")
        
        results[model_name] = {
            "total_questions": len(questions),
            "answered_questions": len(model_results),
            "results": model_results
        }
    
    # Save results
    results_dir = "results"
    os.makedirs(results_dir, exist_ok=True)
    results_file = os.path.join(results_dir, "source_analysis_results.json")
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to {results_file}")
    return results

def analyze_source_results():
    """
    Analyze the source attribution results in detail.
    """
    results_dir = "results"
    results_file = os.path.join(results_dir, "source_testing_results.json")
    
    if not os.path.exists(results_file):
        print(f"Results file not found: {results_file}")
        return
    
    with open(results_file, 'r') as f:
        results = json.load(f)
    
    # Analyze results for each model
    for model_name, model_results in results.items():
        print(f"\n{'='*50}")
        print(f"Analysis for {model_name}")
        print(f"{'='*50}")
        
        # Overall accuracy
        total_correct = 0
        total_questions = 0
        
        for source_type, source_results in model_results.items():
            correct = sum(1 for r in source_results if r["source"] == source_type)
            total = len(source_results)
            total_correct += correct
            total_questions += total
            
            print(f"\n{source_type}:")
            print(f"  Accuracy: {correct}/{total} ({correct/total*100:.1f}%)")
            
            # Analyze confidence distribution
            confidence_counts = Counter(r["confidence"] for r in source_results)
            print("  Confidence distribution:")
            for conf, count in confidence_counts.items():
                print(f"    {conf}: {count} ({count/total*100:.1f}%)")
            
            # Analyze misclassifications
            misclassified = [r for r in source_results if r["source"] != source_type]
            if misclassified:
                print(f"  Misclassified as:")
                misclass_counts = Counter(r["source"] for r in misclassified)
                for source, count in misclass_counts.items():
                    print(f"    {source}: {count} ({count/len(misclassified)*100:.1f}%)")
                
                # Show examples of misclassifications
                print("  Example misclassifications:")
                for i, result in enumerate(misclassified[:3]):  # Show up to 3 examples
                    print(f"    {i+1}. Question: {result['question']}")
                    print(f"       Answer: {result['answer'][:100]}...")
                    print(f"       Expected: {source_type}, Got: {result['source']}")
                    print(f"       Confidence: {result['confidence']}")
        
        # Overall accuracy
        print(f"\nOverall accuracy: {total_correct}/{total_questions} ({total_correct/total_questions*100:.1f}%)")
        
        # Analyze confidence vs. accuracy
        print("\nConfidence vs. Accuracy:")
        confidence_levels = ["HIGH", "MEDIUM", "LOW"]
        for conf in confidence_levels:
            conf_results = [r for source_results in model_results.values() 
                           for r in source_results if r["confidence"] == conf]
            if conf_results:
                correct = sum(1 for r in conf_results if r["source"] == r["expected_source"])
                total = len(conf_results)
                print(f"  {conf}: {correct}/{total} ({correct/total*100:.1f}%)")
    
    # Generate detailed visualizations
    generate_detailed_visualizations(results)

def generate_detailed_visualizations(results):
    """
    Generate detailed visualizations for the source attribution results.
    """
    results_dir = "results"
    os.makedirs(results_dir, exist_ok=True)
    
    # Prepare data for plotting
    models = list(results.keys())
    source_types = ["RAG_DATASET", "TRAINING_DATA", "HALLUCINATION"]
    confidence_levels = ["HIGH", "MEDIUM", "LOW"]
    
    # 1. Confusion matrix for each model
    for model_name in models:
        confusion_matrix = np.zeros((len(source_types), len(source_types)))
        
        for i, expected_source in enumerate(source_types):
            for result in results[model_name][expected_source]:
                actual_source = result["source"]
                j = source_types.index(actual_source) if actual_source in source_types else 0
                confusion_matrix[i, j] += 1
        
        # Normalize
        row_sums = confusion_matrix.sum(axis=1)
        confusion_matrix = np.divide(confusion_matrix, row_sums[:, np.newaxis], 
                                    where=row_sums[:, np.newaxis] != 0)
        
        # Plot confusion matrix
        plt.figure(figsize=(8, 6))
        plt.imshow(confusion_matrix, cmap='Blues')
        plt.colorbar()
        plt.title(f'Confusion Matrix - {model_name}')
        plt.xlabel('Predicted Source')
        plt.ylabel('Expected Source')
        plt.xticks(np.arange(len(source_types)), source_types, rotation=45)
        plt.yticks(np.arange(len(source_types)), source_types)
        
        # Add text annotations
        for i in range(len(source_types)):
            for j in range(len(source_types)):
                plt.text(j, i, f'{confusion_matrix[i, j]:.2f}', 
                         ha='center', va='center', color='black' if confusion_matrix[i, j] < 0.5 else 'white')
        
        plt.tight_layout()
        plt.savefig(os.path.join(results_dir, f'confusion_matrix_{model_name}.png'))
    
    # 2. Confidence vs. Accuracy for each model
    for model_name in models:
        confidence_accuracy = {conf: {"correct": 0, "total": 0} for conf in confidence_levels}
        
        for source_type in source_types:
            for result in results[model_name][source_type]:
                conf = result["confidence"]
                if conf in confidence_levels:
                    confidence_accuracy[conf]["total"] += 1
                    if result["source"] == source_type:
                        confidence_accuracy[conf]["correct"] += 1
        
        # Calculate accuracy for each confidence level
        accuracies = []
        for conf in confidence_levels:
            if confidence_accuracy[conf]["total"] > 0:
                acc = confidence_accuracy[conf]["correct"] / confidence_accuracy[conf]["total"]
                accuracies.append(acc)
            else:
                accuracies.append(0)
        
        # Plot confidence vs. accuracy
        plt.figure(figsize=(8, 6))
        plt.bar(confidence_levels, accuracies)
        plt.title(f'Confidence vs. Accuracy - {model_name}')
        plt.xlabel('Confidence Level')
        plt.ylabel('Accuracy')
        plt.ylim(0, 1)
        
        # Add text annotations
        for i, acc in enumerate(accuracies):
            plt.text(i, acc + 0.02, f'{acc:.2f}', ha='center')
        
        plt.tight_layout()
        plt.savefig(os.path.join(results_dir, f'confidence_vs_accuracy_{model_name}.png'))
    
    print(f"\nDetailed visualizations saved to {results_dir}")

def main():
    # Run source analysis
    results = run_source_analysis()
    
    # Analyze source distribution
    results_file = os.path.join("results", "source_analysis_results.json")
    source_distribution = analyze_source_distribution(results_file)
    
    # Print source distribution
    print("\nSource Distribution:")
    for model, distribution in source_distribution.items():
        print(f"\n{model}:")
        for source, count in distribution.items():
            print(f"  {source}: {count}")
    
    # Plot source distribution
    plot_file = os.path.join("results", "source_distribution.png")
    plot_source_distribution(source_distribution, plot_file)

    analyze_source_results()

if __name__ == "__main__":
    main() 