from core.rag_inference import RAGInference
import json
import os
import time
from typing import Dict, List, Any
import matplotlib.pyplot as plt
import numpy as np
import argparse

def test_source_examples(models=None):
    """
    Test different types of questions to capture hallucinations and training data examples.
    
    Args:
        models (list, optional): List of models to test. If None, use default models.
    """
    # Questions designed to test different source types
    questions = {
        "RAG_DATASET": [
            "What is x/4 where x is 16?",
            "Predict the outcome of 2 + 3?",
            "What is the result of 12/3?",
            "What is 5 * 7?",
            "What is 100 / 10?"
        ],
        "TRAINING_DATA": [
            "What is the chemical formula for water?",
            "Who wrote 'Romeo and Juliet'?",
            "What is the capital of France?",
            "What is the speed of light?",
            "What is the largest planet in our solar system?",
            "Who was the first person to walk on the moon?",
            "What is the atomic number of carbon?"
        ],
        "HALLUCINATION": [
            "What will be the weather in Tokyo next week?",
            "What is the name of the first person who will walk on Mars?",
            "What will be the price of Bitcoin in 2025?",
            "What is the cure for cancer?",
            "What is the name of the next US President after 2024?",
            "What will be the population of Earth in 2100?",
            "What will be the next major technological breakthrough?"
        ]
    }
    
    if models is None:
        models = ["deepseek-r1-1.5b", "llama3.2-1b", "qwen2.5-1.5b"]
    
    results = {}
    
    for model_name in models:
        print(f"\nTesting {model_name}...")
        rag = RAGInference(model_name)
        
        model_results = {}
        for source_type, source_questions in questions.items():
            print(f"\nTesting {source_type} questions:")
            source_results = []
            
            for question in source_questions:
                print(f"\nQuestion: {question}")
                result = rag.answer_question(question)
                if result:
                    source_results.append({
                        "question": question,
                        "answer": result["answer"],
                        "source": result["source"],
                        "confidence": result["confidence"],
                        "expected_source": source_type
                    })
                    print(f"Answer: {result['answer'][:200]}...")
                    print(f"Source: {result['source']} (Expected: {source_type})")
                    print(f"Confidence: {result['confidence']}")
            
            model_results[source_type] = source_results
        
        results[model_name] = model_results
    
    # Save results
    results_dir = "results"
    os.makedirs(results_dir, exist_ok=True)
    results_file = os.path.join(results_dir, "source_testing_results.json")
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to {results_file}")
    
    # Print summary
    print("\nSource Attribution Summary:")
    for model_name, model_results in results.items():
        print(f"\n{model_name}:")
        for source_type, source_results in model_results.items():
            correct = sum(1 for r in source_results if r["source"] == source_type)
            total = len(source_results)
            print(f"  {source_type}: {correct}/{total} correct ({correct/total*100:.1f}%)")
    
    # Generate visualizations
    generate_visualizations(results)

def generate_visualizations(results):
    """
    Generate visualizations for the source attribution results.
    """
    results_dir = "results"
    os.makedirs(results_dir, exist_ok=True)
    
    # Prepare data for plotting
    models = list(results.keys())
    source_types = ["RAG_DATASET", "TRAINING_DATA", "HALLUCINATION"]
    
    # Accuracy by source type and model
    accuracy_data = np.zeros((len(models), len(source_types)))
    for i, model in enumerate(models):
        for j, source_type in enumerate(source_types):
            source_results = results[model][source_type]
            correct = sum(1 for r in source_results if r["source"] == source_type)
            total = len(source_results)
            accuracy_data[i, j] = correct / total if total > 0 else 0
    
    # Plot accuracy by source type and model
    plt.figure(figsize=(10, 6))
    bar_width = 0.25
    index = np.arange(len(models))
    
    for i, source_type in enumerate(source_types):
        plt.bar(index + i * bar_width, accuracy_data[:, i], bar_width, label=source_type)
    
    plt.xlabel('Model')
    plt.ylabel('Accuracy')
    plt.title('Source Attribution Accuracy by Model and Source Type')
    plt.xticks(index + bar_width, models)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(results_dir, 'source_attribution_accuracy.png'))
    
    # Confidence distribution by source type
    confidence_data = {source_type: {"HIGH": 0, "MEDIUM": 0, "LOW": 0} for source_type in source_types}
    
    for model in models:
        for source_type in source_types:
            for result in results[model][source_type]:
                confidence = result["confidence"]
                if confidence in ["HIGH", "MEDIUM", "LOW"]:
                    confidence_data[source_type][confidence] += 1
    
    # Plot confidence distribution
    plt.figure(figsize=(10, 6))
    confidence_types = ["HIGH", "MEDIUM", "LOW"]
    confidence_values = np.zeros((len(source_types), len(confidence_types)))
    
    for i, source_type in enumerate(source_types):
        for j, conf_type in enumerate(confidence_types):
            confidence_values[i, j] = confidence_data[source_type][conf_type]
    
    # Normalize to percentages
    row_sums = confidence_values.sum(axis=1)
    confidence_values = np.divide(confidence_values, row_sums[:, np.newaxis], where=row_sums[:, np.newaxis] != 0)
    
    # Plot confidence distribution
    bar_width = 0.25
    index = np.arange(len(confidence_types))
    
    for i, source_type in enumerate(source_types):
        plt.bar(index + i * bar_width, confidence_values[i], bar_width, label=source_type)
    
    plt.xlabel('Confidence Level')
    plt.ylabel('Percentage')
    plt.title('Confidence Distribution by Source Type')
    plt.xticks(index + bar_width, confidence_types)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(results_dir, 'confidence_distribution.png'))
    
    print(f"\nVisualizations saved to {results_dir}")

def main():
    parser = argparse.ArgumentParser(description='Test source attribution for different models')
    parser.add_argument('--models', type=str, help='Comma-separated list of models to test')
    args = parser.parse_args()
    
    models = None
    if args.models:
        models = [model.strip() for model in args.models.split(',')]
    
    test_source_examples(models)

if __name__ == "__main__":
    main() 