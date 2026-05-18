# 🌱 Calmora

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A lightweight, empathetic, and safety-first mental health companion designed specifically for Indian college students. Built with **Python (Flask)** and **Vanilla Web Technologies (HTML/CSS/JS)**, this project focuses on learning, accessibility, and immediate crisis support.

---

## 🌟 Key Features

- **Friendly Interface**: A calming, responsive chat UI designed with student-friendly aesthetics.
- **AI Therapist Persona**: Powered by an advanced LLM configured to act as an empathetic and professional AI therapist.
- **Capabilities**: Specialized explicitly in offering actionable advice for timetable & study planning, exam stress coping mechanisms, and campus resource recommendations.
- **Crisis Guardrails**: Built-in instructions detect self-harm thoughts and immediately redirect users to professional Indian helplines (KIRAN 1800-599-0019, AASRA 9820-466-726, etc.).
- **Privacy Focused**: No permanent storage or database; conversations exist only in session memory.
- **Mobile Responsive**: Works seamlessly on desktop and mobile devices.

---

## 🛠️ Tech Stack

- **Frontend**: HTML5, CSS3 (Vanilla), JavaScript (ES6+)
- **Backend**: Python (Flask)
- **Logic**: Advanced LLM-based empathetic conversational engine

---

## 🚀 Getting Started

### Prerequisites

- [Python 3.8+](https://www.python.org/downloads/)
- `pip` (Python package manager)

### Installation

1. **Clone the repository** (if applicable) or download the files.
   ```bash
   git clone https://github.com/yourusername/calmora.git
   cd calmora
   ```

2. **Set up Environment Variables**:
   Create a `.env` file in the root directory and configure the underlying API key for the AI engine:
   ```env
   GROQ_API_KEY=your_api_key_here
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   python app.py
   ```

5. **Open in your browser**:
   Navigate to `http://127.0.0.1:5000/`.

---

## 🧠 System Design & Logic

The chatbot follows a "Safety First" architecture:

1. **Input**: User message is sent via AJAX to the Flask `/chat` endpoint.
2. **System Guardrails**: The AI engine is initialized with strict instructions to identify crisis situations, prioritizing safety by providing immediate emergency contacts when needed.
3. **AI Processing**: The bot streams the user context to the LLM backend, heavily guided by an empathetic therapist persona.
4. **Dynamic Response**: The AI generates a custom, context-aware, and supportive response tailored to the user's concerns.

---

## ⚠️ Important Disclaimer

> [!WARNING]
> This chatbot is an **educational project** and is NOT a substitute for professional medical advice, diagnosis, or treatment. It is intended to provide general support and stress-relief tips for students. If you are in immediate danger or experiencing a medical emergency, please contact professional emergency services (like 112) or your local campus security.

---

## 🛡️ Ethics & Safety

- **Transparency**: The bot clearly identifies as an AI at all times.
- **Data Policy**: No user data is saved to a disk. Once the browser session ends or the server restarts, data is cleared.
- **Escalation**: The bot is programmed to prioritize safety over "sounding smart" when sensitive topics arise.

---

## 📈 Future Roadmap

- [ ] Support for **Dark Mode** toggle.
- [ ] Integration with a professional NLP library like `NLTK` or `spaCy`.
- [x] Upgraded logic engine to an advanced LLM for dynamic, context-aware responses.
- [ ] Expanded database of campus-specific resources and links.

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

## 🤝 Contributing

Contributions are welcome!
1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git origin push feature/AmazingFeature`)
5. Open a Pull Request
