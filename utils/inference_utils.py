from core.base_inference import OllamaInference
import time

def get_inference(model_name: str, prompt: str, max_tokens: int = 200, temperature: float = 0.7) -> None:
    """
    Get inference from a specific model with a custom prompt.
    
    Args:
        model_name (str): Name of the model to use
        prompt (str): The prompt to send to the model
        max_tokens (int): Maximum number of tokens to generate
        temperature (float): Sampling temperature (0.0 to 1.0)
    """
    try:
        client = OllamaInference()
        print(f"\nUsing model: {model_name}")
        print(f"Prompt: {prompt}")
        print("-" * 80)
        
        start_time = time.time()
        response = client.generate(
            model_name=model_name,
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=temperature
        )
        duration = time.time() - start_time
        
        print(f"Response: {response['response']}")
        print(f"Duration: {duration:.2f} seconds")
        print("=" * 80)
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    MODEL = "deepseek-r1-1.5b"  # Options: "deepseek-r1-1.5b", "llama3.2-1b", "qwen2.5-1.5b"
    PROMPT = "Write a Python function to calculate fibonacci numbers."
    
    get_inference(MODEL, PROMPT) 