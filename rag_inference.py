from datasets import load_dataset
from local_inference import OllamaInference
import numpy as np
from typing import List, Dict, Any
import time
from tqdm import tqdm
import json
import os

class RAGInference:
    def __init__(self, model_name: str):
        """Initialize RAG inference with a specific model.

        Args:
            model_name (str): Name of the model to use
        """
        self.model_name = model_name
        self.client = OllamaInference()
        self.dataset = None
        self.embeddings = None
        self.results_dir = "results"
        self.embeddings_file = os.path.join(self.results_dir, f"embeddings_{model_name}.json")
        self.main_results_file = os.path.join(self.results_dir, "rag_results.json")
        self.load_dataset()
        
    def load_dataset(self):
        """Load the General Knowledge dataset."""
        print(f"Loading dataset for {self.model_name}...")
        self.dataset = load_dataset("MuskumPillerum/General-Knowledge")
        print(f"Dataset loaded with {len(self.dataset['train'])} examples")
        
    def get_embedding(self, text: str) -> List[float]:
        """Get embedding for a text using the model."""
        try:
            return [ord(c) for c in text.lower()]
        except Exception as e:
            print(f"Error getting embedding: {e}")
            return None
            
    def compute_similarity(self, query_embedding: List[float], doc_embedding: List[float]) -> float:
        """Compute cosine similarity between two embeddings."""
        if not query_embedding or not doc_embedding:
            return 0.0
            
        # Pad or truncate embeddings to same length
        max_len = max(len(query_embedding), len(doc_embedding))
        query_padded = query_embedding + [0] * (max_len - len(query_embedding))
        doc_padded = doc_embedding + [0] * (max_len - len(doc_embedding))
        
        return np.dot(query_padded, doc_padded) / (
            np.linalg.norm(query_padded) * np.linalg.norm(doc_padded)
        )
        
    def retrieve_relevant_context(self, query: str, k: int = 3) -> List[str]:
        """Retrieve k most relevant contexts for a query."""
        if not self.embeddings:
            self.load_or_compute_embeddings()
            
        query_embedding = self.get_embedding(query)
        if not query_embedding:
            return []
            
        similarities = []
        for doc_embedding in self.embeddings:
            similarity = self.compute_similarity(query_embedding, doc_embedding)
            similarities.append(similarity)
            
        # Get top k indices
        top_k_indices = np.argsort(similarities)[-k:][::-1]
        
        # Return relevant contexts
        contexts = []
        for idx in top_k_indices:
            # Convert numpy.int64 to regular Python int
            idx_int = int(idx)
            item = self.dataset['train'][idx_int]
            # Format context as Q&A pair
            context = f"Q: {item['Question']}\nA: {item['Answer']}"
            contexts.append(context)
        return contexts
        
    def load_or_compute_embeddings(self):
        """Load embeddings from cache or compute new ones."""
        if os.path.exists(self.embeddings_file):
            print(f"Loading embeddings from {self.embeddings_file}...")
            with open(self.embeddings_file, 'r') as f:
                self.embeddings = json.load(f)
        else:
            print("Computing embeddings...")
            self.embeddings = []
            for item in tqdm(self.dataset['train']):
                # Use both question and answer for embedding
                text = f"{item['Question']} {item['Answer']}"
                embedding = self.get_embedding(text)
                if embedding:
                    self.embeddings.append(embedding)
                    
            # Save embeddings to cache
            os.makedirs(self.results_dir, exist_ok=True)
            with open(self.embeddings_file, 'w') as f:
                json.dump(self.embeddings, f)
                
    def answer_question(self, question: str) -> Dict[str, Any]:
        """Answer a question using RAG."""
        # Retrieve relevant context
        contexts = self.retrieve_relevant_context(question)
        
        # Construct prompt with context
        context_text = "\n\n".join(contexts)
        prompt = f"""Based on the following Q&A pairs from a knowledge base, please answer the question. If the answer cannot be found in the context, say so.

                    Knowledge Base:
                    {context_text}

                    Question: {question}

                    Answer:"""
        
        # Generate answer
        try:
            start_time = time.time()
            response = self.client.generate(
                model_name=self.model_name,
                prompt=prompt,
                max_tokens=200,
                temperature=0.7
            )
            duration = time.time() - start_time
            
            result = {
                "model": self.model_name,
                "question": question,
                "answer": response["response"],
                "contexts": contexts,
                "duration": duration
            }
            
            # Load existing results or create new ones
            if os.path.exists(self.main_results_file):
                with open(self.main_results_file, 'r') as f:
                    all_results = json.load(f)
            else:
                all_results = {}
            
            # Update results for this model
            if self.model_name not in all_results:
                all_results[self.model_name] = []
            all_results[self.model_name].append(result)
            
            # Save updated results
            with open(self.main_results_file, 'w') as f:
                json.dump(all_results, f, indent=2)
                
            return result
        except Exception as e:
            print(f"Error generating answer: {e}")
            return None

def main():
    # Initialize RAG for each model
    models = ["deepseek-r1-1.5b", "llama3.2-1b", "qwen2.5-1.5b"]
    rag_systems = {model: RAGInference(model) for model in models}
    
    # Test question
    test_question = "What is the capital of France?"
    
    # Get answers from all models
    for model_name, rag in rag_systems.items():
        print(f"\nGetting answer from {model_name}...")
        result = rag.answer_question(test_question)
        if result:
            print(f"Question: {result['question']}")
            print(f"Answer: {result['answer']}")
            print(f"Duration: {result['duration']:.2f} seconds")
            print("=" * 80)

if __name__ == "__main__":
    main() 