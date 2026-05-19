# 🌱 Calmora

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![Groq](https://img.shields.io/badge/LLM-Groq%20Llama%203.3%2070B-orange.svg)](https://groq.com/)
[![Razorpay](https://img.shields.io/badge/payments-Razorpay-blue.svg)](https://razorpay.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A lightweight, empathetic, safety-first mental wellness companion built for Indian college and school students. Calmora pairs an LLM-powered chat experience with practical self-care tools (mood check-ins, weekly planners, journaling reflections, study breakdowns, affirmations) and an affordable path to a real 1-on-1 counselling session — all in one Flask app.

---

## 🌟 Features

### Conversational support
- **Calmora chat** — empathetic LLM persona fluent in the Indian student context (boards, JEE, NEET, CUET, GATE, CAT, placements, hostel life, family pressure, Hinglish).
- **Crisis guardrails** — built-in detection that surfaces Indian helplines (KIRAN 1800-599-0019, AASRA, Vandrevala, iCALL, NIMHANS, emergency 112) the moment self-harm or severe distress signals appear.

### Self-care toolkit (`/api/*` endpoints)
- **Mood micro-practices** (`/api/mood`) — pick a mood, get a 60–90 word grounding practice.
- **Weekly planner** (`/api/plan`) — generates a doable 7-day study + rest plan from your goal, energy, and daily hours.
- **Journal reflection** (`/api/journal`) — "what I'm hearing → gentle reframe → one small next step".
- **Study breakdown** (`/api/study`) — turns a task + deadline into 4–6 Pomodoro-sized steps.
- **Daily affirmation** (`/api/affirmation`) — fresh, non-cheesy, optionally Hinglish.

### Counsellor booking + payments
- **Razorpay integration** — `/api/create-order` and `/api/verify-payment` for HMAC-SHA256 signed payments.
- **Two plans** — Calmora Care (single session, ₹599) and Calmora Plus (4 sessions, ₹1999).
- **Warm AI confirmations** — `/api/book` generates a personalised booking confirmation message.

### Other
- Mobile-responsive vanilla HTML/CSS/JS frontend.
- No database — conversations live in the browser session only.

---

## 🛠️ Tech Stack

- **Backend**: Python 3.8+, Flask 3.0
- **LLM**: Groq API, `llama-3.3-70b-versatile`
- **Payments**: Razorpay (`razorpay==2.0.1`)
- **Frontend**: HTML5, CSS3, Vanilla JavaScript (ES6+)
- **Config**: `python-dotenv`

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- `pip`
- A [Groq API key](https://console.groq.com/)
- A [Razorpay key pair](https://dashboard.razorpay.com/) (test mode is fine for development)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/calmora.git
   cd calmora
   ```

2. **Create a `.env`** in the project root:
   ```env
   GROQ_API_KEY=your_groq_api_key
   RAZORPAY_KEY_ID=rzp_test_xxxxxxxxxxxx
   RAZORPAY_KEY_SECRET=your_razorpay_secret
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the app**
   ```bash
   python app.py
   ```

5. **Open** `http://127.0.0.1:5000/`.

> If Razorpay env vars are missing, payment endpoints return 401 but the rest of the app (chat, mood, plan, journal, study, affirmation) keeps working.

---

## 🔌 API Reference

| Method | Endpoint | Purpose |
| --- | --- | --- |
| `POST` | `/chat` | Main conversational endpoint |
| `POST` | `/api/mood` | Mood-based micro-practice |
| `POST` | `/api/plan` | 7-day study + rest plan |
| `POST` | `/api/journal` | Journal reflection |
| `POST` | `/api/study` | Pomodoro-style task breakdown |
| `GET`  | `/api/affirmation` | One fresh affirmation |
| `GET`  | `/api/razorpay-key` | Returns publishable `key_id` only |
| `POST` | `/api/create-order` | Creates a Razorpay order for the chosen plan |
| `POST` | `/api/verify-payment` | Verifies HMAC-SHA256 signature post-checkout |
| `POST` | `/api/book` | Confirms a counsellor booking |

---

## 🧠 System Design

1. **Frontend** — `templates/index.html` + `static/script.js` send AJAX requests to the Flask backend.
2. **`chatbot_logic.py`** — wraps the Groq client, holds the Calmora system prompt, per-feature prompts (mood, plan, journal, study, affirmation, booking), and offline fallbacks for when the LLM is unreachable.
3. **`payments.py`** — Razorpay order creation + defensive signature verification (constant-time HMAC compare + SDK cross-check).
4. **`app.py`** — Flask routes that glue the two together and enforce minimum payment amount, required fields, and basic validation.
5. **Safety-first prompt design** — the system prompt forces crisis escalation to Indian helplines before any other priority.

---

## 💳 Pricing (configured in `app.py`)

| Plan | Sessions | Amount |
| --- | --- | --- |
| Calmora Care | 1 | ₹599 |
| Calmora Plus | 4 | ₹1999 |

Amounts are stored in paise (`PLAN_PRICES`) and enforced server-side — never trust client-supplied prices.

---

## ⚠️ Disclaimer

> [!WARNING]
> Calmora is a wellness companion, **not a substitute** for professional medical advice, diagnosis, or treatment. In an emergency call **112**, or reach out to KIRAN (**1800-599-0019**), AASRA (**+91 9820-466-726**), or Vandrevala (**1860-2662-345**).

---

## 🛡️ Ethics & Safety

- **Crisis-first**: the LLM is instructed to surface Indian helplines before anything else when distress signals appear.
- **No persistent storage**: chat history lives only in the browser session.
- **Secrets stay server-side**: only the Razorpay publishable `key_id` is exposed to the frontend; the secret is used solely for HMAC verification.
- **Server-side price enforcement**: client cannot dictate the amount charged.

---

## 📈 Roadmap

- [x] Upgrade chat to an LLM (Groq Llama 3.3 70B).
- [x] Add mood, planner, journal, study, and affirmation tools.
- [x] Integrate Razorpay for paid counsellor sessions.
- [ ] Persist bookings + trigger WhatsApp confirmation to counsellors.
- [ ] Dark mode toggle.
- [ ] Expanded directory of campus wellness cells across India.

---

## 📄 License

MIT — see `LICENSE`.

---

## 🤝 Contributing

1. Fork the project
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit (`git commit -m 'Add some AmazingFeature'`)
4. Push (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
