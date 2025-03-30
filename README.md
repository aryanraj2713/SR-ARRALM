# Local LLM Inference with Ollama

This project provides a Python interface for local inference using Ollama with three different models:
- DeepSeek Coder 1.3B (replacing DeepSeek-R1-1.5B)
- Llama 3.2 1B
- Qwen2 Math 1.5B

## Prerequisites

1. Install Ollama from [https://ollama.ai/](https://ollama.ai/)
2. Python 3.8 or higher
3. pip (Python package manager)

## Setup

1. Clone this repository
2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

## Model Storage

The model weights are stored locally using Ollama in the following directory:
- macOS/Linux: `~/.ollama/models/`
- Windows: `C:\Users\<username>\.ollama\models\`

When you run `client.pull_model()`, the model weights are downloaded from Ollama's servers and stored in this directory. The total size of all three models is approximately 3GB.

## Usage

### Basic Inference

1. Start the Ollama service:
   ```bash
   ollama serve
   ```

2. Run the basic inference example:
   ```bash
   python local_inference.py
   ```

3. Run the inference tests:
   ```bash
   python test_inference.py
   ```

### RAG (Retrieval-Augmented Generation) Inference

1. Run the RAG inference example:
   ```bash
   python rag_inference.py
   ```

2. Run the RAG tests:
   ```bash
   python rag_test.py
   ```

### Using the API in Your Code

You can use the `OllamaInference` class in your code:

```python
from local_inference import OllamaInference

client = OllamaInference()

# Pull a model
client.pull_model("deepseek-r1-1.5b")  # This will pull deepseek-coder:1.3b

# Generate text
response = client.generate(
    model_name="deepseek-r1-1.5b",
    prompt="Your prompt here",
    max_tokens=100,
    temperature=0.7
)
print(response["response"])
```

## Available Models

- `deepseek-r1-1.5b`: Maps to DeepSeek Coder 1.3B (776MB)
  - A capable coding model trained on two trillion code and natural language tokens
  - Optimized for code generation and understanding
  - Size: 776MB

- `llama3.2-1b`: Maps to Llama 3.2 1B (1.3GB)
  - Meta's latest 1B parameter model optimized for edge devices
  - Balanced performance and resource usage
  - Size: 1.3GB

- `qwen2.5-1.5b`: Maps to Qwen2 Math 1.5B (934MB)
  - Specialized math language model built upon Qwen2
  - Optimized for mathematical reasoning and problem-solving
  - Size: 934MB

## API Reference

### OllamaInference Class

#### Methods

- `generate(model_name, prompt, max_tokens=None, temperature=0.7, top_p=0.9, stop=None, stream=False)`: Generate text using the specified model
- `list_models()`: List all available models
- `pull_model(model_name)`: Pull a model from Ollama

## Notes

- The models are stored locally using Ollama
- Make sure you have sufficient disk space for the models (approximately 3GB total)
- The first time you use a model, it will be downloaded automatically
- The Ollama service must be running for the inference to work
- If you see "address already in use" error when starting Ollama, it means the service is already running
- Test results are stored in the `results/` directory 