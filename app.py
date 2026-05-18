from flask import Flask, render_template, request, jsonify
from chatbot_logic import (
    get_response,
    get_mood_practice,
    get_weekly_plan,
    get_journal_reflection,
    get_study_breakdown,
    get_affirmation,
    get_booking_message,
)

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    user_message = (request.json or {}).get("message", "").strip()
    if not user_message:
        return jsonify({"response": "Please share what's on your mind."})
    return jsonify({"response": get_response(user_message)})


@app.route("/api/mood", methods=["POST"])
def mood():
    data = request.json or {}
    mood_val = data.get("mood", "").strip()
    context = data.get("context", "").strip()
    if not mood_val:
        return jsonify({"response": "Pick a mood first."}), 400
    return jsonify({"response": get_mood_practice(mood_val, context)})


@app.route("/api/plan", methods=["POST"])
def plan():
    data = request.json or {}
    goal = data.get("goal", "").strip()
    energy = data.get("energy", "").strip()
    hours = data.get("hours", "").strip()
    if not goal:
        return jsonify({"response": "Tell me what you'd like this week to feel like."}), 400
    return jsonify({"response": get_weekly_plan(goal, energy or "Steady", hours or "3–4 hours")})


@app.route("/api/journal", methods=["POST"])
def journal():
    data = request.json or {}
    entry = data.get("entry", "").strip()
    if not entry or len(entry) < 4:
        return jsonify({"response": "Take a breath and share a few words about how you're feeling."}), 400
    return jsonify({"response": get_journal_reflection(entry)})


@app.route("/api/study", methods=["POST"])
def study():
    data = request.json or {}
    task = data.get("task", "").strip()
    time_window = data.get("time", "").strip()
    if not task:
        return jsonify({"response": "Drop in the task and we'll break it down together."}), 400
    return jsonify({"response": get_study_breakdown(task, time_window or "a few days")})


@app.route("/api/affirmation", methods=["GET"])
def affirmation():
    return jsonify({"response": get_affirmation()})


@app.route("/api/book", methods=["POST"])
def book():
    data = request.json or {}
    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip()
    phone = (data.get("phone") or "").strip()
    concern = (data.get("concern") or "").strip()
    language = (data.get("language") or "").strip()
    slot = (data.get("slot") or "").strip()

    if not (name and email and phone and concern):
        return jsonify({"ok": False, "message": "Please fill in name, email, phone, and your main concern."}), 400

    # In a real product this would persist to a DB, trigger payment + WhatsApp notification.
    # For now, generate a warm, personalised confirmation message.
    first_name = name.split()[0]
    message = get_booking_message(first_name, concern, language, slot)
    return jsonify({
        "ok": True,
        "plan": "Calmora Care",
        "amount_inr": 599,
        "message": message,
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)
