document.addEventListener("DOMContentLoaded", () => {
    const chatBox = document.getElementById("chat-box");
    const userInput = document.getElementById("user-input");
    const sendBtn = document.getElementById("send-btn");

    // Logic to create and append message bubbles to the UI
    function appendMessage(sender, text) {
        const msgDiv = document.createElement("div");
        msgDiv.classList.add("message");
        msgDiv.classList.add(sender === "user" ? "user-message" : "bot-message");

        // Allows HTML elements like <br> from the crisis response
        msgDiv.innerHTML = text;

        chatBox.appendChild(msgDiv);

        // Auto-scroll to the bottom when a new message appears
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    // Connect User Input to Backend
    async function sendMessage() {
        const text = userInput.value.trim();
        if (!text) return; // Ignore empty clicks

        // 1. Immediately display the user's message
        appendMessage("user", text);
        userInput.value = ""; // Clear input field

        // 2. Transmit message to Flask API
        try {
            const response = await fetch("/chat", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ message: text }) // Serialize message details 
            });

            const data = await response.json();

            // 3. Display the response, with a slight delay so it feels natural
            setTimeout(() => {
                appendMessage("bot", data.response);
            }, 600);

        } catch (error) {
            console.error("Error connecting to server:", error);
            appendMessage("bot", "Oops! I can't reach the server right now. Make sure the app is running.");
        }
    }

    // Trigger logic on Send Button click
    sendBtn.addEventListener("click", sendMessage);

    // Trigger logic when Enter key is pressed
    userInput.addEventListener("keypress", (e) => {
        if (e.key === "Enter") {
            sendMessage();
        }
    });
});
