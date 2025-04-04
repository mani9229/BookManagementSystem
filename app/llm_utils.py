import os
from dotenv import load_dotenv
from langchain.llms import Ollama
from langchain.chains.summarize import load_summarize_chain
from langchain.prompts import PromptTemplate
from typing import List, Optional

load_dotenv()

# --- Configuration ---
LLM_PROVIDER = "OLLAMA"  
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "Llama-2-7b-chat-GGUF")  # model

# --- Ollama Setup ---
def get_ollama_model():
    """Initializes and returns the Ollama model."""
    return Ollama(model=OLLAMA_MODEL)  # model

# --- LLM Utility Functions ---

def generate_book_summary(book_content: str) -> str:
    """Generates a summary for a book using Ollama."""

    try:
        if LLM_PROVIDER == "OLLAMA":
            llm = get_ollama_model()
            prompt_template = """Write a concise summary of the following text:
            "{text}"
            CONCISE SUMMARY:"""
            prompt = PromptTemplate(template=prompt_template, input_variables=["text"])
            chain = load_summarize_chain(llm, chain_type="stuff", prompt=prompt)
            summary = chain.run(book_content)
            return summary.strip()

        else:
            return "Error: LLM_PROVIDER not configured correctly (OLLAMA expected)."

    except Exception as e:
        print(f"Error generating book summary: {e}")
        return "Failed to generate book summary."


def generate_review_summary(reviews: List[str]) -> Optional[str]:
    """Generates a summary of book reviews using Ollama."""

    try:
        if LLM_PROVIDER == "OLLAMA":
            if not reviews:
                return None

            llm = get_ollama_model()
            prompt_template = """Summarize the following book reviews:
            "{text}"
            SUMMARY:"""
            prompt = PromptTemplate(template=prompt_template, input_variables=["text"])
            chain = load_summarize_chain(llm, chain_type="stuff", prompt=prompt)
            summary = chain.run("\n".join(reviews))
            return summary.strip()
        else:
            return "Error: LLM_PROVIDER not configured correctly (OLLAMA expected)."

    except Exception as e:
        print(f"Error generating review summary: {e}")
        return None


def generate_recommendations(user_preferences: str, books_data: List[dict]) -> str:
    """Generates book recommendations based on user preferences."""

    try:
        if LLM_PROVIDER == "OLLAMA":
            llm = get_ollama_model()
            prompt_template = """Given these user preferences: {preferences}, recommend some of these books: {books}
            RECOMMENDATIONS:"""
            prompt = PromptTemplate(template=prompt_template, input_variables=["preferences", "books"])
            chain = load_summarize_chain(llm, chain_type="stuff", prompt=prompt)
            recommendations = chain.run(preferences=user_preferences, books=str(books_data))
            return recommendations.strip()
        else:
            return "Error: LLM_PROVIDER not configured correctly (OLLAMA expected)."

    except Exception as e:
        print(f"Error generating recommendations: {e}")
        return "Failed to generate recommendations."
