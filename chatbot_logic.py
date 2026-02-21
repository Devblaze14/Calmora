import random
import re

# Crisis keywords that trigger immediate priority safety protocols
CRISIS_KEYWORDS = ['suicide', 'kill myself', 'end my life', 'die', 'harm myself', 'cut myself', 'give up on life']

# Predefined intents and randomized empathetic responses
INTENTS = {
    'greeting': {
        'keywords': ['hello', 'hi', 'hey', 'start', 'morning', 'evening'],
        'responses': [
            "Hello! I'm here to listen. How are you feeling today?",
            "Hi there. Take a deep breath. What's on your mind?",
            "Hey! I'm Calmora, your student support chatbot. How can I help you right now?"
        ]
    },
    'stress': {
        'keywords': ['stress', 'overwhelmed', 'pressure', 'too much', 'exhausted', 'burnout', 'tired'],
        'responses': [
            "It sounds like you're carrying a lot right now. Remember to take things one step at a time. Have you taken a break recently?",
            "Feeling overwhelmed is completely normal, especially for students. Try to do a quick 4-7-8 breathing exercise: breathe in for 4 seconds, hold for 7, exhale for 8.",
            "I hear you. Academic pressure can be heavy. Make sure you are drinking water and stepping away from your screen sometimes."
        ]
    },
    'anxiety': {
        'keywords': ['anxious', 'anxiety', 'panic', 'worry', 'scared', 'nervous', 'exams', 'test'],
        'responses': [
            "Exams and deadlines can cause a lot of anxiety. It helps to break your studying into small, manageable 20-minute chunks.",
            "When you feel anxious, try grounding yourself. Name 5 things you can see, 4 things you can touch, 3 things you can hear...",
            "It's okay to feel nervous. Your grades do not define your worth. Just do your best!"
        ]
    },
    'lonely': {
        'keywords': ['lonely', 'alone', 'isolated', 'no friends', 'sad', 'depressed'],
        'responses': [
            "College can feel incredibly lonely sometimes. You aren't the only one feeling this way. Is there a club or study group you might be interested in checking out?",
            "I'm sorry you're feeling isolated. Remember that reaching out to family or just studying in a public space like a cafe can sometimes help feel connected.",
            "Your feelings are valid. I'm just a bot, but I'm here to chat. Consider reaching out to your campus counseling center—they are there for this exact reason."
        ]
    }
}

def get_response(user_input):
    """
    Takes user input, checks for crisis keywords first, 
    and then matches intents based on simple NLP word counting.
    """
    user_input_lower = user_input.lower()

    # 1. CRISIS DETECTION (Highest Priority)
    for word in CRISIS_KEYWORDS:
        if word in user_input_lower:
            # Stop normal flow and immediately return safety contact information
            return (
                "🚨 **Safety Alert** 🚨<br><br>"
                "It sounds like you are going through a very difficult time, and I want to make sure you get the support you need. "
                "I am only an AI, and I cannot verify your safety. Please, reach out to someone who can help right now:<br><br>"
                "📞 **National Suicide Prevention Lifeline**: Call or text 988 (US/Canada)<br>"
                "💬 **Crisis Text Line**: Text HOME to 741741<br>"
                "🏫 **Campus Emergency**: Please contact your university's emergency line or go to the nearest hospital.<br><br>"
                "You matter, and help is available. Please reach out to them."
            )

    # 2. INTENT MATCHING (Simple NLP Keyword matching)
    # Remove basic punctuation to help match words better
    clean_input = re.sub(r'[^\w\s]', '', user_input_lower)
    
    matched_intent = None
    max_matches = 0

    # Find the intent with the most keyword matches in the user's sentence
    for intent, data in INTENTS.items():
        matches = sum(1 for keyword in data['keywords'] if keyword in clean_input)
        if matches > max_matches:
            max_matches = matches
            matched_intent = intent

    # 3. RESPONSE SELECTION
    if matched_intent:
        # Choose a random supportive response from the matched intent
        return random.choice(INTENTS[matched_intent]['responses'])
    else:
        # Fallback response if no keywords matched
        return (
            "I hear you. While I might not fully understand, I am here to listen. "
            "Can you tell me a little more about how that makes you feel? "
            "*(Remember: I'm a learning AI, not a therapist!)*"
        )
