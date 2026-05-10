"""
OpenRouter API service for OCR (image text extraction) and AI Q&A.
Uses free models available on OpenRouter.
"""

import httpx
import base64
import os
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

# Free models on OpenRouter
OCR_MODEL = "baidu/qianfan-ocr-fast:free"      # Free OCR model
CHAT_MODEL = "poolside/laguna-xs.2:free"       # Free model for Q&A


def _make_request(payload: dict) -> str:
    """Make a request to OpenRouter API."""
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8000",
        "X-Title": "Medical AI Application"
    }

    with httpx.Client(timeout=120.0) as client:
        response = client.post(
            OPENROUTER_BASE_URL,
            headers=headers,
            json=payload
        )
        response.raise_for_status()
        data = response.json()

    return data["choices"][0]["message"]["content"]


def extract_text_from_image(image_bytes: bytes, mime_type: str = "image/png") -> str:
    """
    Use a free vision model on OpenRouter to extract text from an image.
    
    Args:
        image_bytes: Raw image bytes
        mime_type: MIME type of the image (e.g., image/png, image/jpeg)
    
    Returns:
        Extracted text from the image
    """
    b64_image = base64.b64encode(image_bytes).decode("utf-8")

    payload = {
        "model": OCR_MODEL,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Extract all text from this medical document image."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{mime_type};base64,{b64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 4096
    }

    return _make_request(payload)


def ask_ai_question(question: str, context: str) -> str:
    """
    Ask an AI question with context from retrieved documents.
    
    Args:
        question: The user's question
        context: Relevant document text retrieved from ChromaDB
    
    Returns:
        AI-generated answer
    """
    payload = {
        "model": CHAT_MODEL,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a helpful medical AI assistant. You answer questions about "
                    "patient medical records based on the provided context. "
                    "Be accurate, clear, and concise. If the information is not available "
                    "in the context, say so honestly. Never make up medical information. "
                    "Always recommend consulting a healthcare professional for medical advice."
                )
            },
            {
                "role": "user",
                "content": (
                    f"Based on the following medical documents:\n\n"
                    f"---\n{context}\n---\n\n"
                    f"Question: {question}"
                )
            }
        ],
        "max_tokens": 2048
    }

    return _make_request(payload)
