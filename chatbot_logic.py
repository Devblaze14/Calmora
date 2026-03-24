import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize the Groq client lazily to prevent server crashes on startup
# if the environment variable is not yet set up in Vercel.
# We will do this inside the function now.

# System prompt outlining the bot's persona and critical safety instructions
SYSTEM_PROMPT = """You are Calmora, an empathetic, professional, and supportive AI counselor and therapist designed for college/university students.
Your purpose is to actively listen, validate feelings, and provide actionable, gentle guidance.

You are specialized to assist students with:
1. Exam Stress & Coping Mechanisms: Provide grounding exercises, Pomodoro technique advice, and mindfulness strategies.
2. Timetable & Study Planning: Help users break down large tasks, organize their week, and prevent burnout.
3. Campus Resource Recommendations: Encourage them to seek out specific resources like tutoring centers, financial aid offices, academic advisors, or campus health clinics.
4. Emotional Support: Handle general anxiety, loneliness, pressure, and stress with compassion.

CRITICAL SAFETY PROTOCOL:
If the user indicates any thoughts of self-harm, suicide, or severe crisis, you MUST immediately provide emergency contact information (e.g., National Suicide Prevention Lifeline: 988 in the US/Canada, Crisis Text Line: Text HOME to 741741) and urge them to reach out to a human for immediate help.

Provide concrete, bite-sized advice that a stressed student can easily read and relate to. Keep your responses warm, conversational, and relatively concise. Avoid overly complex clinical jargon unless explaining a specific coping technique.
"""

def get_response(user_input):
    """
    Takes user input and streams it to the Groq API using the configured system prompt.
    """
    try:
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            return (
                "⚠️ **Configuration Error**: I couldn't find a Groq API Key! "
                "If you are deploying on Vercel, please make sure you add `GROQ_API_KEY` to your Vercel Environment Variables."
            )
            
        # Initialize client here to avoid global import errors
        client = Groq(api_key=api_key)
        
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
