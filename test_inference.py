from local_inference import OllamaInference
import time
import json

def format_response(model_name: str, prompt: str, response: dict, duration: float) -> str:
    """Format the response for better readability."""
    return f"""
Model: {model_name}
Prompt: {prompt}
Response: {response['response']}
Duration: {duration:.2f} seconds
{'='*80}
"""

def test_model(client: OllamaInference, model_name: str, prompts: list) -> None:
    """Test a model with multiple prompts."""
    print(f"\nTesting {model_name}...")
    
    for prompt in prompts:
        try:
            start_time = time.time()
            response = client.generate(
                model_name=model_name,
                prompt=prompt,
                max_tokens=200,
                temperature=0.7
            )
            duration = time.time() - start_time
            
            print(format_response(model_name, prompt, response, duration))
            
        except Exception as e:
            print(f"Error with {model_name}: {e}")

def main():

    client = OllamaInference()
    
    # Test prompts for each model
    prompts = {
        "deepseek-r1-1.5b": [
            "Write a Python function to implement a binary search algorithm.",
            "Explain the concept of object-oriented programming in Python.",
            "Write a SQL query to find the second highest salary from an employees table."
        ],
        "llama3.2-1b": [
            "What are the key benefits of using renewable energy?",
            "Explain the concept of machine learning in simple terms.",
            "Write a short story about a robot learning to paint."
        ],
        "qwen2.5-1.5b": [
            "Solve this math problem: If a triangle has angles of 45°, 45°, and 90°, what is the ratio of its sides?",
            "Calculate the area of a circle with radius 5 units.",
            "Explain the concept of prime numbers and provide examples."
        ]
    }
    

    for model_name, model_prompts in prompts.items():
        test_model(client, model_name, model_prompts)
        time.sleep(2)  # Add a small delay between models

if __name__ == "__main__":
    main() 