from flask import Flask, render_template, request, jsonify
from chatbot_logic import get_response

# Initialize the Flask application
app = Flask(__name__)

@app.route("/")
def home():
    """Route to serve the main frontend HTML page."""
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    """API endpoint to receive user messages and return AI responses."""
    # Extract the user's message from the POST request
    user_message = request.json.get("message")
    
    # Handle empty submissions
    if not user_message:
        return jsonify({"response": "Please say something!"})

    # Pass the message to our NLP / rule-based AI logic
    bot_response = get_response(user_message)
    
    # Return the AI response back to the frontend JS as JSON
    return jsonify({"response": bot_response})

if __name__ == "__main__":
    # Run the local development server (temporarily locally stores variables, no permanent database)
    app.run(debug=True, port=5000)
