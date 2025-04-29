# Structured Relevance Assessment for Robust Retrieval-Augmented Language Models


## Quick Start

1. Install Ollama from [https://ollama.ai/](https://ollama.ai/) and create a virtual-environment (optional)
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the complete analysis with a single command:
   ```bash
   python run_all_models.py
   ```
4. View the results:
   - Open `results/report/source_attribution_report.md` in your preferred markdown viewer
   - The report includes:
     - Overall summary of model performance
     - Detailed results for each model
     - Visualizations of accuracy and confidence distributions
     - Question-by-question analysis

## Project Structure

```
.
├── core/                   # Core implementation files
│   ├── base_inference.py  # Base inference implementation
│   └── rag_inference.py   # RAG implementation
├── tests/                 # Test files
│   ├── base_tests.py     # Basic model tests
│   └── rag_tests.py      # RAG-specific tests
├── utils/                 # Utility scripts
│   └── inference_utils.py # Helper functions for inference
├── data/                  # Data storage
│   └── embeddings/       # Cached embeddings
├── results/              # Output directory
│   ├── report/          # Generated reports
│   │   ├── assets/     # Report visualizations
│   │   └── source_attribution_report.md  # Main report
│   └── source_testing_results.json  # Raw test results
├── requirements.txt      # Project dependencies
└── README.md            # Project documentation
```

## Supported Models (Small Language Models)

1. **DeepSeek Coder 1.3B** (776MB)
   - Optimized for code generation and understanding
   - Trained on two trillion code and natural language tokens

2. **Llama 3.2 1B** (1.3GB)
   - Meta's latest 1B parameter model
   - Optimized for edge devices
   - Balanced performance and resource usage

3. **Qwen2 Math 1.5B** (934MB)
   - Specialized math language model
   - Built upon Qwen2
   - Optimized for mathematical reasoning

## Prerequisites

1. Install Ollama from [https://ollama.ai/](https://ollama.ai/)
2. Python 3.8 or higher
3. pip/conda/uv/ or other python package manager

## Setup

1. Clone this repository
2. Install the required Python packages(change according to your package manager):
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
   python core/base_inference.py
   ```

3. Run the inference tests:
   ```bash
   python tests/base_tests.py
   ```

### RAG (Retrieval-Augmented Generation) Inference

1. Run the RAG inference example:
   ```bash
   python core/rag_inference.py
   ```

2. Run the RAG tests:
   ```bash
   python tests/rag_tests.py
   ```

### Using the API in Your Code

#### Basic Inference
```python
from core.base_inference import OllamaInference

client = OllamaInference()

# Pull a model
client.pull_model("deepseek-r1-1.5b")

# Generate text
response = client.generate(
    model_name="deepseek-r1-1.5b",
    prompt="Your prompt here",
    max_tokens=100,
    temperature=0.7
)
print(response["response"])
```

#### RAG Inference
```python
from core.rag_inference import RAGInference

# Initialize RAG with a specific model
rag = RAGInference("deepseek-r1-1.5b")

# Get an answer with context
result = rag.answer_question("Your question here")
print(result["answer"])
```

## Data Flow

1. **User Query** → RAGInference
2. **Context Retrieval** → Embedding Comparison
3. **Context Augmentation** → Model Generation
4. **Result Storage** → JSON Output

## API Reference

### OllamaInference Class

#### Methods
- `generate(model_name, prompt, max_tokens=None, temperature=0.7, top_p=0.9, stop=None, stream=False)`: Generate text
- `list_models()`: List available models
- `pull_model(model_name)`: Pull a model from Ollama

### RAGInference Class

#### Methods
- `get_embedding(text)`: Convert text to vector
- `compute_similarity(query_embedding, doc_embedding)`: Calculate similarity
- `retrieve_relevant_context(query, k=3)`: Get relevant contexts
- `answer_question(question)`: Generate RAG-based answer

## Notes

- Models are stored locally using Ollama
- Ensure sufficient disk space (approximately 3GB total)
- First-time model usage triggers automatic download
- Ollama service must be running for inference
- Test results are stored in the `results/` directory
- Embeddings are cached in the `data/embeddings/` directory
- Reports are generated in `results/report/` with visualizations in `results/report/assets/`

# Contribution
This repository is part of ongoing research work. While we are committed to building in the open and sharing our progress, the codebase represents extensive effort and many hours of development.If you use this code or any part of it in your own work, please cite both the code and the corresponding research publication(s). Proper attribution is the only acknowledgment we request in return for making this resource available. We plan to open the repository for external contributions soon. Until then, you are welcome to create issues for bug reports, feature suggestions, or general questions.

Thank you for your understanding and respect for our work.

## For Code use :
```
@article{raj2025structured,
  author = {Raj, Aryan and Garg, Astitva Veer and Anitha, D.},
  title = {Structured Relevance Assessment for Robust Retrieval-Augmented Language Models},
  year = {2025},
  email = {aryanraj2713@gmail.com, gargveerastitva@gmail.com, anithad@srmist.edu.in}
}
```
## Related research:
```
@misc{garg2025structured,
  author       = {Astitva Veer Garg and Aryan Raj and Anitha D},
  title        = {Structured Relevance Assessment for Robust Retrieval-Augmented Language Models},
  year         = {2025},
  institution  = {SRM Institute of Science and Technology},
  address      = {Kattankulathur, Chennai, Tamil Nadu, India},
  note         = {Preprint},
  howpublished = {\url{mailto:gargveerastitva@gmail.com}},
}
```
