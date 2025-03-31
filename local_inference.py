import requests
from typing import Optional, Dict, Any

class OllamaInference:
    def __init__(self, base_url: str = "http://localhost:11434"):
        """Initialize the Ollama inference client.
        
        Args:
            base_url (str): The base URL for the Ollama API
        """
        self.base_url = base_url
        self.available_models = {
            "deepseek-r1-1.5b": "deepseek-coder:1.3b",
            "llama3.2-1b": "llama3.2:1b",
            "qwen2.5-1.5b": "qwen2-math:1.5b"
        }

    def _make_request(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Make a request to the Ollama API.
        
        Args:
            endpoint (str): The API endpoint
            data (dict): The request data
            
        Returns:
            dict: The API response
        """
        if endpoint == "api/tags":
            response = requests.get(f"{self.base_url}/{endpoint}")
        else:
            response = requests.post(f"{self.base_url}/{endpoint}", json=data)
        
        response.raise_for_status()
        return response.json()

    def generate(
        self,
        model_name: str,
        prompt: str,
        max_tokens: Optional[int] = None,
        temperature: float = 0.7,
        top_p: float = 0.9,
        stop: Optional[list] = None,
        stream: bool = False
    ) -> Dict[str, Any]:
        """Generate text using the specified model.
        
        Args:
            model_name (str): Name of the model to use
            prompt (str): The input prompt
            max_tokens (int, optional): Maximum number of tokens to generate
            temperature (float): Sampling temperature
            top_p (float): Top-p sampling parameter
            stop (list, optional): List of stop sequences
            stream (bool): Whether to stream the response
            
        Returns:
            dict: The generation response
        """
        if model_name not in self.available_models:
            raise ValueError(f"Model {model_name} not available. Available models: {list(self.available_models.keys())}")

        data = {
            "model": self.available_models[model_name],
            "prompt": prompt,
            "stream": stream,
            "options": {
                "temperature": temperature,
                "top_p": top_p
            }
        }

        if max_tokens is not None:
            data["options"]["num_predict"] = max_tokens
        if stop is not None:
            data["options"]["stop"] = stop

        return self._make_request("api/generate", data)

    def list_models(self) -> Dict[str, Any]:
        """List all available models.
        
        Returns:
            dict: List of available models
        """
        return self._make_request("api/tags", {})

    def pull_model(self, model_name: str) -> Dict[str, Any]:
        """Pull a model from Ollama.
        
        Args:
            model_name (str): Name of the model to pull
            
        Returns:
            dict: Pull response
        """
        if model_name not in self.available_models:
            raise ValueError(f"Model {model_name} not available. Available models: {list(self.available_models.keys())}")
        
        return self._make_request("api/pull", {"name": self.available_models[model_name]})

def main():
    # Example usage
    client = OllamaInference()
    
    # First, list available models
    try:
        available_models = client.list_models()
        print("\nAvailable models:")
        for model in available_models.get("models", []):
            print(f"- {model['name']}")
    except Exception as e:
        print(f"Error listing models: {e}")
        return
    
    # Test generation with DeepSeek
    try:
        print("\nTesting generation with DeepSeek...")
        response = client.generate(
            model_name="deepseek-r1-1.5b",
            prompt="Write a Python function to calculate fibonacci numbers.",
            max_tokens=100,
            temperature=0.7
        )
        print("Response:", response["response"])
    except Exception as e:
        print(f"Error during generation: {e}")

if __name__ == "__main__":
    main() 