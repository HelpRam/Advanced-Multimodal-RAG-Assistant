from typing import List, Dict, Any
import google.generativeai as genai
from config.settings import settings
from google.generativeai.types import HarmCategory, HarmBlockThreshold

# Configure Gemini API
genai.configure(api_key=settings.GEMINI_API_KEY)

class Generator:
    def __init__(self):
        self.model = genai.GenerativeModel(settings.GEMINI_TEXT_MODEL)
        # Optional: Safety settings for generation
        self.safety_settings = {
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        }


    def generate_answer(self, query: str, retrieved_context: List[Dict[str, Any]]) -> str:
        if not retrieved_context:
            return "I couldn't find relevant information in my knowledge base."

    
        # Current implementation, suitable for using image descriptions as text:
        context_str = "\n\n".join([doc["content"] for doc in retrieved_context])

        prompt = f"""
        You are an intelligent research assistant. Use the following pieces of information to answer the user's question.
        If you cannot find the answer within the provided information, clearly state that you don't have enough information.
        Do not make up answers. Cite the sources of your information if possible.

        --- Retrieved Information ---
        {context_str}
        ---------------------------

        User Question: {query}

        Your Answer:
        """
        try:
            # For pure text input (which includes the image descriptions), just pass the prompt string
            response = self.model.generate_content(
                prompt,
                safety_settings=self.safety_settings
            )
            return response.text
        except Exception as e:
            print(f"Error generating content with Gemini: {e}")
            return "An error occurred while generating the answer."