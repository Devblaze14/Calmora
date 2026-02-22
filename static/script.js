/* ══════════════════════════════════════════════
   CALMORA — main.js
   Scroll reveals · Navbar · Mood check-in · Chat
══════════════════════════════════════════════ */

document.addEventListener("DOMContentLoaded", () => {

    /* ─── NAVBAR ─────────────────────────────── */
    const navbar   = document.getElementById("navbar");
    const hamburger= document.getElementById("hamburger");
    const navLinks = document.getElementById("nav-links");

    window.addEventListener("scroll", () => {
        navbar.classList.toggle("scrolled", window.scrollY > 40);
    }, { passive: true });

    hamburger.addEventListener("click", () => {
        hamburger.classList.toggle("active");
        navLinks.classList.toggle("open");
    });

    // Close mobile menu when a link is clicked
    navLinks.querySelectorAll("a").forEach(link => {
        link.addEventListener("click", () => {
            hamburger.classList.remove("active");
            navLinks.classList.remove("open");
        });
    });


    /* ─── SCROLL REVEAL ──────────────────────── */
    const revealObserver = new IntersectionObserver(
        (entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add("visible");
                    revealObserver.unobserve(entry.target);
                }
            });
        },
        { threshold: 0.12, rootMargin: "0px 0px -40px 0px" }
    );

    document.querySelectorAll(".reveal").forEach(el => revealObserver.observe(el));

    // Kick hero elements visible immediately
    document.querySelectorAll(".hero .reveal").forEach(el => {
        el.style.transitionDelay = el.style.transitionDelay || "0s";
        el.classList.add("visible");
    });


    /* ─── MOOD CHECK-IN ──────────────────────── */
    const moodBtns   = document.querySelectorAll(".mood-btn");
    const moodTipBox = document.getElementById("mood-tip-box");
    const moodTipText= document.getElementById("mood-tip-text");

    moodBtns.forEach(btn => {
        btn.addEventListener("click", () => {
            // Deselect all
            moodBtns.forEach(b => b.classList.remove("selected"));
            btn.classList.add("selected");

            const tip = btn.dataset.tip;
            moodTipText.textContent = tip;
            moodTipBox.classList.add("visible");

            // Smooth scroll to tip
            setTimeout(() => {
                moodTipBox.scrollIntoView({ behavior: "smooth", block: "nearest" });
            }, 150);
        });
    });


    /* ─── CHAT ───────────────────────────────── */
    const chatBox       = document.getElementById("chat-box");
    const userInput     = document.getElementById("user-input");
    const sendBtn       = document.getElementById("send-btn");
    const suggestions   = document.getElementById("chat-suggestions");

    /** Append a message bubble */
    function appendMessage(sender, htmlText) {
        const wrapper = document.createElement("div");
        wrapper.classList.add("message", sender === "user" ? "user-message" : "bot-message");

        const avatar = document.createElement("div");
        avatar.classList.add("msg-avatar");
        avatar.textContent = sender === "user" ? "🙂" : "🌱";

        const content = document.createElement("div");
        content.classList.add("msg-content");
        content.innerHTML = htmlText;

        wrapper.appendChild(avatar);
        wrapper.appendChild(content);
        chatBox.appendChild(wrapper);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    /** Show animated typing indicator */
    function showTyping() {
        const wrapper = document.createElement("div");
        wrapper.classList.add("typing-indicator");
        wrapper.id = "typing-indicator";

        const avatar = document.createElement("div");
        avatar.classList.add("msg-avatar");
        avatar.textContent = "🌱";

        const bubbles = document.createElement("div");
        bubbles.classList.add("typing-bubbles");
        bubbles.innerHTML = "<span></span><span></span><span></span>";

        wrapper.appendChild(avatar);
        wrapper.appendChild(bubbles);
        chatBox.appendChild(wrapper);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    /** Remove typing indicator */
    function removeTyping() {
        const el = document.getElementById("typing-indicator");
        if (el) el.remove();
    }

    /** Hide suggestion chips after first use */
    function hideSuggestions() {
        if (suggestions) {
            suggestions.style.opacity = "0";
            suggestions.style.transition = "opacity 0.3s";
            setTimeout(() => suggestions.remove(), 300);
        }
    }

    /** Main send function */
    async function sendMessage(text) {
        text = text || userInput.value.trim();
        if (!text) return;

        hideSuggestions();
        appendMessage("user", text);
        userInput.value = "";
        sendBtn.disabled = true;

        showTyping();

        try {
            const response = await fetch("/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: text })
            });

            const data = await response.json();

            setTimeout(() => {
                removeTyping();
                appendMessage("bot", data.response);
                sendBtn.disabled = false;
            }, 700);

        } catch (err) {
            removeTyping();
            appendMessage("bot",
                "⚡ Oops — I can't reach my brain right now! Make sure the Flask server is running and try again."
            );
            sendBtn.disabled = false;
        }
    }

    sendBtn.addEventListener("click", () => sendMessage());

    userInput.addEventListener("keydown", (e) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
});

/** Called by suggestion chips (onclick in HTML) */
function fillSuggestion(btn) {
    const input = document.getElementById("user-input");
    // Extract plain text from chip label (strip emoji)
    const text = btn.textContent.trim();
    input.value = text;
    input.focus();

    // Trigger send after brief moment so user sees the fill
    setTimeout(() => {
        const event = new KeyboardEvent("keydown", {
            key: "Enter", bubbles: true, cancelable: true
        });
        input.dispatchEvent(event);
    }, 200);
}
