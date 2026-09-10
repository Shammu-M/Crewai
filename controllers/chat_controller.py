"""Controller coordinating Streamlit input with the banking service."""

from services.banking_service import answer_banking_request


def handle_chat_prompt(prompt: str) -> str:
    """Translate a view event into an application-service call."""
    try:
        return answer_banking_request(prompt)
    except Exception as error:
        message = str(error).lower()
        if "groq_api_key is missing" in message or "api key" in message:
            return "Groq is not configured. Add GROQ_API_KEY to the project .env file and restart Streamlit."
        if "429" in message or "rate limit" in message or "too many requests" in message:
            return "The Groq provider is rate-limiting requests right now. Please try again shortly."
        return "I could not complete that request. Please try again or ask about another demo banking topic."
