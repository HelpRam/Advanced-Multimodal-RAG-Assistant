from typing import List, Dict, Any
from PIL import Image
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import google.generativeai as genai
from config.settings import settings
from src.data_ingestion.data_loader import load_image

# Configure Gemini API
genai.configure(api_key=settings.GEMINI_API_KEY)

def analyze_image_with_gemini(image_path: str) -> str:
    """
    Uses Gemini Vision model to generate a descriptive caption for an image.
    """
    try:
        model = genai.GenerativeModel(settings.GEMINI_VISION_MODEL)
        image = Image.open(image_path).convert("RGB") # Ensure RGB for consistent processing

        # Safety settings (optional but recommended)
        safety_settings = {
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        }

        prompt = "Describe this image in detail, focusing on any text, charts, or relevant information present."
        response = model.generate_content(
            [prompt, image],
            safety_settings=safety_settings
        )
        return response.text
    except Exception as e:
        print(f"Error analyzing image {image_path} with Gemini: {e}")
        return ""

def process_multimodal_documents(documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Processes a list of documents, extracting text, and generating descriptions for images
    using Gemini Vision.
    """
    processed_documents = []
    for doc in documents:
        if doc["type"] == "text":
            processed_documents.append(doc) # Text documents are already loaded
        elif doc["type"] == "image":
            image_path = doc["content"]
            image_description = analyze_image_with_gemini(image_path)
            if image_description:
                # Add the image description as a new "text" document, linked to original image
                processed_documents.append({
                    "content": image_description,
                    "type": "image_description",
                    "metadata": {**doc["metadata"], "original_type": "image"}
                })
            else:
                print(f"Could not generate description for image: {image_path}")
        
    return processed_documents