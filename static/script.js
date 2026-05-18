/* ══════════════════════════════════════════════
   CALMORA — Premium UI interactions
══════════════════════════════════════════════ */

document.addEventListener("DOMContentLoaded", () => {

    /* ─── NAVBAR ─── */
    const navbar = document.getElementById("navbar");
    const hamburger = document.getElementById("hamburger");
    const navLinks = document.getElementById("nav-links");

    window.addEventListener("scroll", () => {
        navbar.classList.toggle("scrolled", window.scrollY > 30);
    }, { passive: true });

    hamburger?.addEventListener("click", () => {
        hamburger.classList.toggle("active");
        navLinks.classList.toggle("open");
    });
    navLinks?.querySelectorAll("a").forEach(link =>
        link.addEventListener("click", () => {
            hamburger.classList.remove("active");
            navLinks.classList.remove("open");
        })
    );

    /* ─── SCROLL REVEAL ─── */
    const revealObserver = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add("visible");
                revealObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.12, rootMargin: "0px 0px -40px 0px" });
    document.querySelectorAll(".reveal").forEach(el => revealObserver.observe(el));

    /* ─── HELPERS ─── */
    const setOutput = (el, html) => {
        el.innerHTML = html;
        el.classList.add("visible");
    };
    const loadingDots = `<div class="loading-dots"><span></span><span></span><span></span></div>`;
    const formatText = (text) => {
        // Convert plain text to gentle HTML: newlines → <br>, bold **x** → <strong>
        return text
            .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
            .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
            .replace(/\n/g, "<br>");
    };

    async function postJSON(url, payload) {
        const r = await fetch(url, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload || {}),
        });
        return r.json();
    }

    /* ─── MOOD TOOL ─── */
    const moodBtns = document.querySelectorAll(".mood-btn");
    const moodCtx = document.getElementById("mood-context");
    const moodOut = document.getElementById("mood-output");
    const moodSubmit = document.getElementById("mood-submit");
    let selectedMood = null;

    moodBtns.forEach(btn => {
        btn.addEventListener("click", () => {
            moodBtns.forEach(b => b.classList.remove("selected"));
            btn.classList.add("selected");
            selectedMood = btn.dataset.mood;
        });
    });

    moodSubmit?.addEventListener("click", async () => {
        if (!selectedMood) {
            setOutput(moodOut, "Pick a mood above first — even an approximation helps.");
            return;
        }
        setOutput(moodOut, loadingDots);
        try {
            const data = await postJSON("/api/mood", { mood: selectedMood, context: moodCtx.value });
            setOutput(moodOut, formatText(data.response));
        } catch {
            setOutput(moodOut, "I couldn't reach my thoughts — try again in a moment.");
        }
    });

    /* ─── PLAN TOOL ─── */
    const planForm = document.getElementById("plan-form");
    const planOut = document.getElementById("plan-output");
    planForm?.addEventListener("submit", async (e) => {
        e.preventDefault();
        const goal = document.getElementById("plan-goal").value.trim();
        const energy = document.getElementById("plan-energy").value;
        const hours = document.getElementById("plan-hours").value;
        if (!goal) {
            setOutput(planOut, "Share a goal for the week first — even a small one.");
            return;
        }
        setOutput(planOut, loadingDots);
        try {
            const data = await postJSON("/api/plan", { goal, energy, hours });
            setOutput(planOut, formatText(data.response));
        } catch {
            setOutput(planOut, "I couldn't draft your week — try again in a moment.");
        }
    });

    /* ─── JOURNAL TOOL ─── */
    const journalSubmit = document.getElementById("journal-submit");
    const journalOut = document.getElementById("journal-output");
    journalSubmit?.addEventListener("click", async () => {
        const entry = document.getElementById("journal-entry").value.trim();
        if (entry.length < 4) {
            setOutput(journalOut, "Take a breath and write a sentence or two — I'm here when you're ready.");
            return;
        }
        setOutput(journalOut, loadingDots);
        try {
            const data = await postJSON("/api/journal", { entry });
            setOutput(journalOut, formatText(data.response));
        } catch {
            setOutput(journalOut, "I couldn't reflect right now — try again in a moment.");
        }
    });

    /* ─── STUDY TOOL ─── */
    const studyForm = document.getElementById("study-form");
    const studyOut = document.getElementById("study-output");
    studyForm?.addEventListener("submit", async (e) => {
        e.preventDefault();
        const task = document.getElementById("study-task").value.trim();
        const time = document.getElementById("study-time").value.trim();
        if (!task) {
            setOutput(studyOut, "What are you tackling? Drop it in above.");
            return;
        }
        setOutput(studyOut, loadingDots);
        try {
            const data = await postJSON("/api/study", { task, time });
            setOutput(studyOut, formatText(data.response));
        } catch {
            setOutput(studyOut, "I couldn't break it down — try again in a moment.");
        }
    });

    /* ─── BREATHING TOOL ─── */
    const breathOrb = document.getElementById("breath-orb");
    const breathLabel = document.getElementById("breath-label");
    const breathStart = document.getElementById("breath-start");
    const breathStop = document.getElementById("breath-stop");
    let breathTimer = null;
    let breathStep = 0;
    const breathSteps = [
        { label: "Breathe in",  cls: "inhale", duration: 4000 },
        { label: "Hold",        cls: "inhale", duration: 4000 },
        { label: "Breathe out", cls: "exhale", duration: 4000 },
        { label: "Hold",        cls: "exhale", duration: 4000 },
    ];
    function runBreathStep() {
        const s = breathSteps[breathStep % breathSteps.length];
        breathLabel.textContent = s.label;
        breathOrb.classList.remove("inhale", "exhale");
        breathOrb.classList.add(s.cls);
        breathStep++;
        breathTimer = setTimeout(runBreathStep, s.duration);
    }
    breathStart?.addEventListener("click", () => {
        if (breathTimer) return;
        breathStep = 0;
        runBreathStep();
    });
    breathStop?.addEventListener("click", () => {
        if (breathTimer) { clearTimeout(breathTimer); breathTimer = null; }
        breathOrb.classList.remove("inhale", "exhale");
        breathLabel.textContent = "Paused";
    });

    /* ─── AFFIRMATION TOOL ─── */
    const affirmCard = document.getElementById("affirm-card");
    const affirmRefresh = document.getElementById("affirm-refresh");
    const heroAffirm = document.getElementById("hero-affirmation");

    async function fetchAffirmation(target) {
        target.innerHTML = `<span class="affirm-quote">${loadingDots}</span>`;
        try {
            const r = await fetch("/api/affirmation");
            const data = await r.json();
            target.innerHTML = `<span class="affirm-quote">"${formatText(data.response)}"</span>`;
            return data.response;
        } catch {
            target.innerHTML = `<span class="affirm-quote">"Rest is part of the work. You are allowed gentleness today."</span>`;
        }
    }
    affirmRefresh?.addEventListener("click", () => fetchAffirmation(affirmCard));

    // Load a fresh affirmation in the hero & tool on load
    if (heroAffirm) {
        fetch("/api/affirmation")
            .then(r => r.json())
            .then(d => { if (d.response) heroAffirm.textContent = d.response; })
            .catch(() => {});
    }

    /* ─── CHAT ─── */
    const chatBox = document.getElementById("chat-box");
    const userInput = document.getElementById("user-input");
    const sendBtn = document.getElementById("send-btn");
    const suggestions = document.getElementById("chat-suggestions");

    function appendMessage(sender, text) {
        const wrap = document.createElement("div");
        wrap.classList.add("message", sender === "user" ? "user-message" : "bot-message");
        const avatar = document.createElement("div");
        avatar.classList.add("msg-avatar");
        avatar.textContent = sender === "user" ? "🙂" : "🌿";
        const content = document.createElement("div");
        content.classList.add("msg-content");
        content.innerHTML = formatText(text);
        wrap.appendChild(avatar);
        wrap.appendChild(content);
        chatBox.appendChild(wrap);
        chatBox.scrollTop = chatBox.scrollHeight;
    }
    function showTyping() {
        const wrap = document.createElement("div");
        wrap.classList.add("typing-indicator");
        wrap.id = "typing-indicator";
        wrap.innerHTML = `<div class="msg-avatar">🌿</div><div class="typing-bubbles"><span></span><span></span><span></span></div>`;
        chatBox.appendChild(wrap);
        chatBox.scrollTop = chatBox.scrollHeight;
    }
    const removeTyping = () => document.getElementById("typing-indicator")?.remove();
    const hideSuggestions = () => { if (suggestions) suggestions.style.display = "none"; };

    async function sendMessage(text) {
        text = (text ?? userInput.value).trim();
        if (!text) return;
        hideSuggestions();
        appendMessage("user", text);
        userInput.value = "";
        sendBtn.disabled = true;
        showTyping();
        try {
            const data = await postJSON("/chat", { message: text });
            setTimeout(() => {
                removeTyping();
                appendMessage("bot", data.response);
                sendBtn.disabled = false;
            }, 500);
        } catch {
            removeTyping();
            appendMessage("bot", "I'm having trouble reaching my thoughts — try again in a moment.");
            sendBtn.disabled = false;
        }
    }
    sendBtn?.addEventListener("click", () => sendMessage());
    userInput?.addEventListener("keydown", (e) => {
        if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); sendMessage(); }
    });
});

/* Suggestion chips (global) */
function fillSuggestion(btn) {
    const input = document.getElementById("user-input");
    input.value = btn.textContent.trim();
    input.focus();
    setTimeout(() => {
        input.dispatchEvent(new KeyboardEvent("keydown", { key: "Enter", bubbles: true }));
    }, 150);
}
