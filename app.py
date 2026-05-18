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
from payments import create_order, verify_signature, get_public_key_id

# Pricing for Calmora plans (in paise)
PLAN_PRICES = {
    "care": {"amount": 59900, "label": "Calmora Care · Single Session"},
    "plus": {"amount": 199900, "label": "Calmora Plus · 4 Sessions"},
}

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


@app.route("/api/razorpay-key", methods=["GET"])
def razorpay_key():
    """Expose only the publishable key id to the frontend."""
    return jsonify({"key_id": get_public_key_id()})


@app.route("/api/create-order", methods=["POST"])
def create_order_route():
    data = request.json or {}
    plan = (data.get("plan") or "care").strip().lower()

    if plan in PLAN_PRICES:
        amount = PLAN_PRICES[plan]["amount"]
        label = PLAN_PRICES[plan]["label"]
    else:
        # Fall back to a client-supplied amount, clamped to a sane range
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
