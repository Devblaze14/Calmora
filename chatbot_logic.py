import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

MODEL = "llama-3.3-70b-versatile"

SYSTEM_PROMPT = """You are Calmora, an empathetic, professional, and supportive wellness companion designed for college/university students.
Your purpose is to actively listen, validate feelings, and provide actionable, gentle guidance.

You help students with:
1. Exam Stress & Coping Mechanisms — grounding exercises, Pomodoro advice, mindfulness strategies.
2. Timetable & Study Planning — break down large tasks, organize the week, prevent burnout.
3. Campus Resource Recommendations — tutoring centers, counseling, advisors, health clinics.
4. Emotional Support — anxiety, loneliness, pressure, stress with compassion.

CRITICAL SAFETY PROTOCOL:
If the user indicates any thoughts of self-harm, suicide, or severe crisis, you MUST immediately provide emergency contact information (National Suicide Prevention Lifeline: 988 in the US/Canada, Crisis Text Line: Text HOME to 741741) and urge them to reach out to a human for immediate help.

Keep responses warm, conversational, and concise. Avoid clinical jargon. Never mention being an AI, language model, or any underlying technology — you are simply "Calmora".
"""

PROMPTS = {
    "mood": (
        "You are Calmora, a warm wellness companion. The user just shared their current mood and (optionally) a sentence of context. "
        "Reply with a short (60-90 word) personalised micro-practice: validate the feeling, then give ONE concrete, doable thing they can try in the next 5 minutes. "
        "Be specific, kind, and grounded. No lists, no headings — just one warm paragraph. End with a single encouraging sentence."
    ),
    "plan": (
        "You are Calmora, a warm wellness companion. The user describes a weekly goal, their current energy level, and daily study window. "
        "Draft a kind, doable 7-day plan. Use this exact format with each day on its own line:\n\n"
        "Mon — <one realistic activity>\nTue — <activity>\nWed — <activity>\n... through Sun.\n\n"
        "Include at least 2 rest/recovery items spread across the week. Then add one short closing sentence (max 20 words) of encouragement. Keep activities concrete (e.g. \"45-min revision: chapter 3\") not vague."
    ),
    "journal": (
        "You are Calmora, a warm wellness companion. The user shared a journal entry. "
        "Respond in this exact structure:\n\n"
        "What I'm hearing: <1-2 sentences gently naming the feelings/themes>\n\n"
        "A gentle reframe: <1-2 sentences offering a kinder perspective, never dismissive>\n\n"
        "One small next step: <a single, specific, doable action for the next hour or day>\n\n"
        "Keep total length under 110 words. Warm, validating, never preachy."
    ),
    "study": (
        "You are Calmora, a warm wellness companion. The user shared a study task and a deadline. "
        "Break the task into 4-6 Pomodoro-sized (25 min) numbered steps that fit the deadline. Format:\n\n"
        "1. <step> — ~25 min\n2. <step> — ~25 min\n...\n\n"
        "Then add a single closing line starting with 'Remember:' offering one piece of kind, study-life-balance advice. Total under 130 words."
    ),
    "affirmation": (
        "You are Calmora. Generate ONE fresh, original affirmation for a stressed student. "
        "It must be:\n- Between 10 and 20 words\n- Warm, grounded, never cheesy\n- Not start with 'You are' (vary the opening)\n- Feel handwritten, not corporate\n\n"
        "Reply with ONLY the affirmation text, no quotation marks, no preamble."
    ),
}


def _client():
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        return None
    return Groq(api_key=api_key)


def _complete(system, user, max_tokens=320, temperature=0.75):
    client = _client()
    if client is None:
        return None
    try:
        resp = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            model=MODEL,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        print(f"[Calmora] completion error: {e}")
        return None


def get_response(user_input):
    client = _client()
    if client is None:
        return (
            "I'm having trouble reaching my thoughts right now. "
            "Make sure GROQ_API_KEY is configured."
        )
    try:
        resp = client.chat.completions.create(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_input},
            ],
            model=MODEL,
            temperature=0.7,
            max_tokens=320,
        )
        return resp.choices[0].message.content
    except Exception as e:
        return (
            "I'm sorry, I'm having trouble responding right now. "
            f"Please try again in a moment. (details: {e})"
        )


def get_mood_practice(mood, context=""):
    user_msg = f"Mood: {mood}.\nContext: {context or '(none provided)'}"
    out = _complete(PROMPTS["mood"], user_msg, max_tokens=220)
    return out or _fallback_mood(mood)


def get_weekly_plan(goal, energy, hours):
    user_msg = f"Goal: {goal}\nEnergy level: {energy}\nDaily study window: {hours}"
    out = _complete(PROMPTS["plan"], user_msg, max_tokens=420)
    return out or "I couldn't draft your plan right now — try again in a moment."


def get_journal_reflection(entry):
    out = _complete(PROMPTS["journal"], entry, max_tokens=280)
    return out or "I couldn't reflect right now — try again in a moment."


def get_study_breakdown(task, time_window):
    user_msg = f"Task: {task}\nTime until due: {time_window}"
    out = _complete(PROMPTS["study"], user_msg, max_tokens=380)
    return out or "I couldn't break that down right now — try again in a moment."


def get_affirmation():
    out = _complete(PROMPTS["affirmation"], "Give me one fresh affirmation.", max_tokens=60, temperature=0.95)
    if not out:
        return "Rest is part of the work. You're allowed to be gentle with yourself today."
    # Strip surrounding quotes if model adds them anyway
    return out.strip().strip('"').strip("'")


# ─── Fallbacks ───
_MOOD_FALLBACK = {
    "great": "That's wonderful to hear. Try journaling one thing that contributed to today's lightness — it becomes an anchor for harder days.",
    "okay": "Okay is enough. Try the 5-4-3-2-1 grounding practice: 5 things you see, 4 you can touch, 3 you hear, 2 you smell, 1 you taste.",
    "meh": "Meh is real. A 10-minute walk in natural light can genuinely lift the fog — try it before judging the rest of your day.",
    "stressed": "Let's slow it down. Inhale for 4, hold for 7, exhale for 8. Three rounds. Your shoulders will thank you.",
    "sad": "Sadness deserves space too. Make a small comfort gesture for yourself — warm drink, soft music, a text to someone safe.",
    "anxious": "Plant your feet on the floor. Notice their weight. You are here, in this moment, and this moment is survivable.",
}
def _fallback_mood(mood):
    return _MOOD_FALLBACK.get(mood, _MOOD_FALLBACK["okay"])
