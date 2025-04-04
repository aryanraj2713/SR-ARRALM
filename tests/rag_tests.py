from core.rag_inference import RAGInference
import time
import json
from typing import Dict, Any
import os

def test_rag(model_name: str, questions: list) -> Dict[str, Any]:
    """
    Test RAG system with a specific model and list of questions.
    
    Args:
        model_name (str): Name of the model to use
        questions (list): List of questions to test
        
    Returns:
        dict: Results of the test
    """
    print(f"\nInitializing RAG with {model_name}...")
    rag = RAGInference(model_name)
    
    results = []
    total_duration = 0
    
    for question in questions:
        print(f"\nTesting question: {question}")
        start_time = time.time()
        
        result = rag.answer_question(question)
        if result:
            duration = result["duration"]
            total_duration += duration
            
            print(f"Answer: {result['answer']}")
            print(f"Source: {result['source']}")
            print(f"Duration: {duration:.2f} seconds")
            print("Retrieved Contexts:")
            for i, context in enumerate(result["contexts"], 1):
                print(f"\nContext {i}:")
                print(context)
            print("=" * 80)
            
            results.append({
                "question": question,
                "answer": result["answer"],
                "source": result["source"],
                "duration": duration,
                "contexts": result["contexts"]
            })
    
    return {
        "model": model_name,
        "total_duration": total_duration,
        "average_duration": total_duration / len(questions),
        "results": results
    }

def main():
    # Test questions
    questions = [
        "What is the capital of France?",
        "Who was the first President of the United States?",
        "What is the largest planet in our solar system?",
        "What is the chemical symbol for gold?",
        "Who painted the Mona Lisa?"
    ]
    
    # Models to test
    models = ["deepseek-r1-1.5b", "llama3.2-1b", "qwen2.5-1.5b"]
    
    # Test each model
    all_results = {}
    for model in models:
        print(f"\n{'='*80}")
        print(f"Testing {model}")
        print(f"{'='*80}")
        
        results = test_rag(model, questions)
        all_results[model] = results
        
        # Print summary
        print(f"\nSummary for {model}:")
        print(f"Total duration: {results['total_duration']:.2f} seconds")
        print(f"Average duration per question: {results['average_duration']:.2f} seconds")
    
    # Save all results to the results directory
    results_dir = "results"
    os.makedirs(results_dir, exist_ok=True)
    results_file = os.path.join(results_dir, "rag_test_results.json")
    with open(results_file, 'w') as f:
        json.dump(all_results, f, indent=2)
    print(f"\nResults saved to {results_file}")

if __name__ == "__main__":
    main() 