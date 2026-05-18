from flask import Flask, render_template, request, jsonify
from chatbot_logic import (
    get_response,
    get_mood_practice,
    get_weekly_plan,
    get_journal_reflection,
    get_study_breakdown,
    get_affirmation,
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


if __name__ == "__main__":
    app.run(debug=True, port=5000)
