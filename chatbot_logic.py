import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize the Groq client
# The client automatically looks for the GROQ_API_KEY environment variable.
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY")
)

# System prompt outlining the bot's persona and critical safety instructions
SYSTEM_PROMPT = """You are Calmora, an empathetic, professional, and supportive AI therapist.
Your purpose is to listen to the user, validate their feelings, and offer constructive, gentle guidance.
If the user indicates any thoughts of self-harm, suicide, or severe crisis, you MUST immediately provide emergency contact information (e.g., National Suicide Prevention Lifeline: 988 in the US/Canada, Crisis Text Line: Text HOME to 741741) and urge them to reach out to a human for immediate help.
Keep your responses warm, conversational, and relatively concise. Do not use overly complex or clinical jargon unless appropriate.
"""

def get_response(user_input):
    """
    Takes user input and streams it to the Groq API using the configured system prompt.
    """
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_input}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            max_tokens=300,
        )
        # Extract the AI's response text
        return chat_completion.choices[0].message.content
    except Exception as e:
        # Fallback response in case of API failure or missing keys
        return (
            "I'm sorry, I'm having trouble connecting to my thought process right now. "
            "Please make sure the Groq API key is added to the .env file. "
            f"(Error details: {str(e)})"
        )
