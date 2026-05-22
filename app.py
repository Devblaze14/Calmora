import os

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request

load_dotenv()

from chatbot_logic import (
    get_affirmation,
    get_booking_message,
    get_journal_reflection,
    get_mood_practice,
    get_response,
    get_study_breakdown,
    get_weekly_plan,
)
from payments import create_order, get_public_key_id, verify_signature
from auth import current_user
import db

# Pricing for Calmora plans (in paise)
PLAN_PRICES = {
    "care": {"amount": 59900, "label": "Calmora Care · Single Session"},
    "plus": {"amount": 199900, "label": "Calmora Plus · 4 Sessions"},
}

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/config", methods=["GET"])
def config():
    """Expose only the public Supabase keys to the frontend."""
    return jsonify({
        "supabase_url": os.environ.get("SUPABASE_URL", ""),
        "supabase_anon_key": os.environ.get("SUPABASE_ANON_KEY", ""),
    })


@app.route("/api/profile", methods=["GET"])
def profile():
    user = current_user(request)
    if not user:
        return jsonify({"error": "unauthorized"}), 401
    p = db.get_profile(user["id"]) or {}
    return jsonify({
        "id": user["id"],
        "email": user["email"],
        "full_name": p.get("full_name") or "",
        "phone": p.get("phone") or "",
        "preferred_language": p.get("preferred_language") or "",
    })


@app.route("/chat", methods=["POST"])
def chat():
    user_message = (request.json or {}).get("message", "").strip()
    if not user_message:
        return jsonify({"response": "Please share what's on your mind."})
    response = get_response(user_message)
    user = current_user(request)
    if user:
        db.save_chat_message(user["id"], "user", user_message)
        db.save_chat_message(user["id"], "assistant", response)
    return jsonify({"response": response})


@app.route("/api/mood", methods=["POST"])
def mood():
    data = request.json or {}
    mood_val = data.get("mood", "").strip()
    context = data.get("context", "").strip()
    if not mood_val:
        return jsonify({"response": "Pick a mood first."}), 400
    response = get_mood_practice(mood_val, context)
    user = current_user(request)
    if user:
        db.save_mood(user["id"], mood_val, context, response)
    return jsonify({"response": response})


@app.route("/api/plan", methods=["POST"])
def plan():
    data = request.json or {}
    goal = data.get("goal", "").strip()
    energy = data.get("energy", "").strip()
    hours = data.get("hours", "").strip()
    if not goal:
        return jsonify({"response": "Tell me what you'd like this week to feel like."}), 400
    response = get_weekly_plan(goal, energy or "Steady", hours or "3–4 hours")
    user = current_user(request)
    if user:
        db.save_plan(user["id"], goal, energy, hours, response)
    return jsonify({"response": response})


@app.route("/api/journal", methods=["POST"])
def journal():
    data = request.json or {}
    entry = data.get("entry", "").strip()
    if not entry or len(entry) < 4:
        return jsonify({"response": "Take a breath and share a few words about how you're feeling."}), 400
    response = get_journal_reflection(entry)
    user = current_user(request)
    if user:
        db.save_journal(user["id"], entry, response)
    return jsonify({"response": response})


@app.route("/api/study", methods=["POST"])
def study():
    data = request.json or {}
    task = data.get("task", "").strip()
    time_window = data.get("time", "").strip()
    if not task:
        return jsonify({"response": "Drop in the task and we'll break it down together."}), 400
    response = get_study_breakdown(task, time_window or "a few days")
    user = current_user(request)
    if user:
        db.save_study(user["id"], task, time_window, response)
    return jsonify({"response": response})


@app.route("/api/affirmation", methods=["GET"])
def affirmation():
    return jsonify({"response": get_affirmation()})


@app.route("/api/razorpay-key", methods=["GET"])
def razorpay_key():
    return jsonify({"key_id": get_public_key_id()})


@app.route("/api/create-order", methods=["POST"])
def create_order_route():
    data = request.json or {}
    plan = (data.get("plan") or "care").strip().lower()

    if plan in PLAN_PRICES:
        amount = PLAN_PRICES[plan]["amount"]
        label = PLAN_PRICES[plan]["label"]
    else:
        amount = int(data.get("amount") or 0)
        label = "Calmora session"

    if amount < 100:
        return jsonify({"error": "Amount must be at least 100 paise (₹1)."}), 400

    notes = {
        "plan": plan,
        "plan_label": label,
        "name": data.get("name") or "",
        "email": data.get("email") or "",
        "phone": data.get("phone") or "",
    }
    status, payload = create_order(amount_paise=amount, currency="INR", notes=notes)
    if status != 200:
        return jsonify(payload), status

    user = current_user(request)
    db.create_booking_row(
        user_id=user["id"] if user else None,
        plan=plan,
        plan_label=label,
        amount_paise=amount,
        order_id=payload["order_id"],
        notes=notes,
    )

    payload["plan"] = plan
    payload["plan_label"] = label
    payload["key_id"] = get_public_key_id()
    return jsonify(payload), 200


@app.route("/api/verify-payment", methods=["POST"])
def verify_payment_route():
    data = request.json or {}
    order_id = (data.get("razorpay_order_id") or "").strip()
    payment_id = (data.get("razorpay_payment_id") or "").strip()
    signature = (data.get("razorpay_signature") or "").strip()

    if not (order_id and payment_id and signature):
        return jsonify({"ok": False, "error": "Missing payment fields."}), 400

    if not verify_signature(order_id, payment_id, signature):
        return jsonify({"ok": False, "error": "Signature mismatch — payment not verified."}), 400

    db.mark_booking_paid(order_id, payment_id)

    return jsonify({
        "ok": True,
        "message": "Payment verified. Please pick a slot on the next screen.",
        "payment_id": payment_id,
        "order_id": order_id,
    }), 200


@app.route("/api/book", methods=["POST"])
def book():
    data = request.json or {}
    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip()
    phone = (data.get("phone") or "").strip()
    concern = (data.get("concern") or "").strip()
    language = (data.get("language") or "").strip()
    slot = (data.get("slot") or "").strip()
    order_id = (data.get("razorpay_order_id") or "").strip()

    if not (name and email and phone and concern):
        return jsonify({"ok": False, "message": "Please fill in name, email, phone, and your main concern."}), 400

    if order_id:
        db.update_booking_details(order_id, {
            "name": name, "email": email, "phone": phone,
            "concern": concern, "language": language, "slot": slot,
        })

    first_name = name.split()[0]
    message = get_booking_message(first_name, concern, language, slot)
    return jsonify({
        "ok": True,
        "plan": "Calmora Care",
        "amount_inr": 599,
        "message": message,
    })


@app.route("/api/history/<kind>", methods=["GET"])
def history(kind):
    user = current_user(request)
    if not user:
        return jsonify({"error": "unauthorized"}), 401
    rows = db.list_history(user["id"], kind, limit=20)
    return jsonify({"items": rows})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
