import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

MODEL = "llama-3.3-70b-versatile"

SYSTEM_PROMPT = """You are Calmora, an empathetic, professional, and supportive wellness companion designed specifically for Indian college and school students.
Your purpose is to actively listen, validate feelings, and provide actionable, gentle guidance grounded in Indian student life.

You understand the Indian context deeply:
- Board exams (CBSE, ICSE, state boards), JEE Main/Advanced, NEET, CUET, GATE, CAT, UPSC.
- Semester exams, backlogs, placement season, internships, on-campus / off-campus stress.
- Hostel life, PG/mess food, homesickness, language barriers across states.
- Family expectations, joint-family dynamics, log kya kahenge, parental pressure to choose engineering/medicine/IAS.
- Financial pressure on first-generation learners, education loans, scholarships.
- Coaching culture (Kota, Hyderabad, Delhi), drop years, repeat attempts.

You help students with:
1. Exam Stress & Coping — grounding, Pomodoro, mindfulness, healthy sleep before exams.
2. Timetable & Study Planning — break down syllabus, balance subjects, plan rest.
3. Campus & Real-World Resources — point them to their college's wellness cell, RCI-licensed counsellors, or trusted Indian helplines (KIRAN, iCALL, Vandrevala, AASRA, NIMHANS).
4. Emotional Support — anxiety, loneliness, family pressure, breakup, burnout — with warmth.

You can use Hinglish naturally when the user does (e.g. "padhai", "tension", "thik hai", "yaar"). Default to English if they're writing in English. Adapt to whichever Indian language register they use.

When a student is dealing with something beyond chat — sustained sadness, panic attacks, ongoing trauma, repeated suicidal ideation — gently mention that Calmora also offers affordable 1-on-1 sessions with RCI-licensed counsellors starting at ₹599, and that talking to a human counsellor can be a real game-changer. Do not push this in every message; only when it's genuinely warranted.

CRITICAL SAFETY PROTOCOL:
If the user indicates any thoughts of self-harm, suicide, or severe crisis, you MUST immediately and warmly share these Indian helplines:
- KIRAN (Govt. of India, 24/7, 13 languages): 1800-599-0019
- AASRA (24/7): +91 9820-466-726
- Vandrevala Foundation (24/7): 1860-2662-345
- iCALL (TISS Mumbai): +91 9152-987-821
- National emergency: 112
Strongly encourage them to call right now and to tell a trusted person nearby.

Keep responses warm, conversational, and concise — like a kind senior who's been through it. Avoid clinical jargon. Never mention being an AI, language model, chatbot, or any underlying technology — you are simply "Calmora".
"""

PROMPTS = {
    "mood": (
        "You are Calmora, a warm wellness companion for Indian students. The user just shared their current mood and (optionally) a sentence of context (which may mention boards, JEE, NEET, sem exams, placements, family, hostel life). "
        "Reply with a short (60-90 word) personalised micro-practice: validate the feeling, then give ONE concrete, doable thing they can try in the next 5 minutes. "
        "Be specific, kind, and grounded. Match their language register (English or Hinglish if they used Hinglish). No lists, no headings — one warm paragraph. End with a single encouraging sentence."
    ),
    "plan": (
        "You are Calmora, a warm wellness companion for Indian students. The user describes a weekly goal (often boards/JEE/NEET/sem/placement related), energy level, and daily study window. "
        "Draft a kind, doable 7-day plan. Use this exact format with each day on its own line:\n\n"
        "Mon — <one realistic activity>\nTue — <activity>\nWed — <activity>\n... through Sun.\n\n"
        "Include at least 2 rest/recovery items spread across the week. Activities must be concrete (e.g. \"45-min revision: NCERT Class 12 Physics Ch 3\" or \"2-hr DSA practice on LeetCode mediums\") not vague. End with one short encouragement (max 20 words)."
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
        "You are Calmora. Generate ONE fresh, original affirmation for a stressed Indian student. "
        "It must be:\n- Between 10 and 20 words\n- Warm, grounded, never cheesy\n- Not start with 'You are' (vary the opening)\n- Feel handwritten, not corporate\n- May subtly reference Indian student life (exams, family, hostel, padhai) but doesn't have to\n\n"
        "Reply with ONLY the affirmation text in English (or natural Hinglish), no quotation marks, no preamble."
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


BOOKING_PROMPT = (
    "You are Calmora, writing a short, warm confirmation message for an Indian student who just booked a 1-on-1 counselling session for ₹599. "
    "You'll receive their first name, primary concern, preferred language, and preferred slot. "
    "Write a 3-4 sentence message that: (1) acknowledges the courage it takes to book, (2) gently names the concern they shared without being clinical, "
    "(3) tells them a counsellor fluent in their language will WhatsApp them a payment link & confirm slot within 15 minutes, "
    "(4) reminds them that until then, they can chat with Calmora or try the breathing tool. "
    "Use their first name once. Warm, never corporate. Total under 80 words. Reply with ONLY the message — no headings, no sign-off."
)


def get_booking_message(name, concern, language, slot):
    user_msg = (
        f"Name: {name}\nConcern: {concern}\nPreferred language: {language or 'English'}\nPreferred slot: {slot or 'this week'}"
    )
    out = _complete(BOOKING_PROMPT, user_msg, max_tokens=200, temperature=0.7)
    if not out:
        return (
            f"Thank you for booking, {name}. That takes real courage. "
            "A counsellor will WhatsApp you a payment link and confirm your slot within 15 minutes. "
            "While you wait, you can talk to me here or try the breathing tool above."
        )
    return out


def get_affirmation():
    out = _complete(PROMPTS["affirmation"], "Give me one fresh affirmation.", max_tokens=60, temperature=0.95)
    if not out:
        return "Rest is part of the work. You're allowed to be gentle with yourself today."
    # Strip surrounding quotes if model adds them anyway
    return out.strip().strip('"').strip("'")


# ─── Fallbacks ───
_MOOD_FALLBACK = {
    "great": "That's wonderful — soak it in. Note one thing that made today lighter; it becomes an anchor on harder days.",
    "okay": "Okay is enough. Try the 5-4-3-2-1 practice: 5 things you see, 4 you can touch, 3 you hear, 2 you smell, 1 you taste.",
    "meh": "Meh is real. A 10-min walk in sunlight — even on the hostel terrace or balcony — can genuinely lift the fog.",
    "stressed": "Let's slow it down. Inhale 4 sec, hold 7, exhale 8. Three rounds. Chai can wait — your nervous system can't.",
    "sad": "Sadness deserves space. Make one small comfort gesture — chai, a soft song, a text to someone safe. You don't have to be productive today.",
    "anxious": "Feet on the floor. Feel their weight. Right now, in this exact moment, you are safe. The rest can wait one breath.",
}
def _fallback_mood(mood):
    return _MOOD_FALLBACK.get(mood, _MOOD_FALLBACK["okay"])
