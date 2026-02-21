# 🌱 Calmora

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A lightweight, empathetic, and safety-first mental health companion designed specifically for college students. Built with **Python (Flask)** and **Vanilla Web Technologies (HTML/CSS/JS)**, this project focuses on learning, accessibility, and immediate crisis support.

---

## 🌟 Key Features

- **Friendly Interface**: A calming, responsive chat UI designed with student-friendly aesthetics.
- **Intent-Based Responses**: Uses simple NLP keyword matching to provide empathetic support for stress, anxiety, and loneliness.
- **Crisis Detection**: Immediate override logic detects self-harm keywords and redirects users to professional helplines.
- **Privacy Focused**: No permanent storage or database; conversations exist only in session memory.
- **Mobile Responsive**: Works seamlessly on desktop and mobile devices.

---

## 🛠️ Tech Stack

- **Frontend**: HTML5, CSS3 (Vanilla), JavaScript (ES6+)
- **Backend**: Python (Flask)
- **Logic**: Rule-based Intent Processing (Regex + Weighted Keyword Matching)

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

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```

4. **Open in your browser**:
   Navigate to `http://127.0.0.1:5000/`.

---

## 🧠 System Design & Logic

The chatbot follows a "Safety First" architecture:

1. **Input**: User message is sent via AJAX to the Flask `/chat` endpoint.
2. **Safety Guard**: The backend first checks for `CRISIS_KEYWORDS`. If any match, a `Safety Alert` is returned immediately, bypassing the conversational AI.
3. **NLP Processing**: If safe, the bot calculates the best-fit "Intent" (Greeting, Stress, Anxiety, Loneliness) based on keyword density.
4. **Varied Response**: It selects a randomized response from the best-fit category to maintain a natural feel.

---

## ⚠️ Important Disclaimer

> [!WARNING]
> This chatbot is an **educational project** and is NOT a substitute for professional medical advice, diagnosis, or treatment. It is intended to provide general support and stress-relief tips for students. If you are in immediate danger or experiencing a medical emergency, please contact professional emergency services or your local campus security.

---

## 🛡️ Ethics & Safety

- **Transparency**: The bot clearly identifies as an AI at all times.
- **Data Policy**: No user data is saved to a disk. Once the browser session ends or the server restarts, data is cleared.
- **Escalation**: The bot is programmed to prioritize safety over "sounding smart" when sensitive topics arise.

---

## 📈 Future Roadmap

- [ ] Support for **Dark Mode** toggle.
- [ ] Integration with a professional NLP library like `NLTK` or `spaCy`.
- [ ] Integration with Large Language Models (LLM) via API (e.g., OpenAI, Gemini) with strict system prompting.
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
