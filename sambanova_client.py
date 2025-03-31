import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class SambanovaClient:
    """Client for interacting with the SambaNova API."""
    
    def _init_(self, api_key=None, api_url=None):
        self.api_key = api_key or os.getenv("SAMBANOVA_API_KEY")
        self.api_url = api_url or os.getenv("SAMBANOVA_API_URL", "https://api.sambanova.ai/api/v1/completions")
        
        if not self.api_key:
            raise ValueError("SambaNova API key is required")
    
    def generate_answer(self, question, file_contents=None, max_tokens=1000, temperature=0.1, model="sambanova/falcon-7b"):
        """Generate an answer using the SambaNova LLM API."""
        
        # Prepare the prompt with file contents if available
        prompt = self._prepare_prompt(question, file_contents)
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        payload = {
            "prompt": prompt,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "model": model
        }
        
        try:
            response = requests.post(self.api_url, headers=headers, json=payload)
            response.raise_for_status()
            
            result = response.json()
            # Extract the answer from the response
            answer = result.get("choices", [{}])[0].get("text", "").strip()
            
            # Process the answer
            return self._extract_final_answer(answer)
        
        except requests.exceptions.RequestException as e:
            return f"Error calling SambaNova API: {str(e)}"

    def _prepare_prompt(self, question, file_contents=None):
        """Prepare a prompt for the LLM with proper formatting."""
        
        base_prompt = (
            "You are an assistant helping with IIT Madras' Online Degree in Data Science graded assignments. "
            "Answer the following question concisely with just the exact value or text to be submitted as the answer. "
            "Do not include explanations or extra text.\n\n"
            f"Question: {question}\n\n"
        )
        
        if file_contents is not None:
            if isinstance(file_contents, str):
                file_text = file_contents
            else:
                # Convert DataFrame to string representation
                file_text = str(file_contents)
            
            base_prompt += f"File contents:\n{file_text}\n\n"
        
        base_prompt += "Provide only the exact answer value without any additional text or explanation:"
        
        return base_prompt

    def _extract_final_answer(self, response_text):
        """Extract the final answer from the model's response text."""
        
        # Remove any common prefixes the model might add
        prefixes = [
            "answer:", "the answer is:", "final answer:", 
            "value:", "result:", "output:"
        ]
        
        cleaned_text = response_text.lower()
        
        for prefix in prefixes:
            if prefix in cleaned_text:
                # Get text after the prefix
                parts = cleaned_text.split(prefix, 1)
                if len(parts) > 1:
                    cleaned_text = parts[1].strip()
        
        # If the response has multiple lines, take the first non-empty line
        lines = [line.strip() for line in cleaned_text.split("\n") if line.strip()]
        if lines:
            return lines[0]
        
        # If all else fails, return the original response
        return response_text.strip()