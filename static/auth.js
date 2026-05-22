/* ══════════════════════════════════════════════
   CALMORA — Supabase auth (modal + session)
══════════════════════════════════════════════ */

(function () {
    let supabase = null;
    let currentSession = null;
    const listeners = [];

    window.CalmoraAuth = {
        onChange(cb) { listeners.push(cb); cb(currentSession); },
        getSession() { return currentSession; },
        getToken() { return currentSession?.access_token || null; },
        getUser() { return currentSession?.user || null; },
        open: openModal,
        signOut: async () => {
            if (!supabase) return;
            await supabase.auth.signOut();
        },
    };

    function notify() { listeners.forEach(cb => { try { cb(currentSession); } catch {} }); }

    async function init() {
        try {
            const r = await fetch("/api/config");
            const cfg = await r.json();
            if (!cfg.supabase_url || !cfg.supabase_anon_key) {
                console.warn("[Calmora] Supabase not configured");
                return;
            }
            if (typeof window.supabase?.createClient !== "function") {
                console.warn("[Calmora] Supabase JS SDK not loaded");
                return;
            }
            supabase = window.supabase.createClient(cfg.supabase_url, cfg.supabase_anon_key, {
                auth: { persistSession: true, autoRefreshToken: true },
            });
            const { data } = await supabase.auth.getSession();
            currentSession = data.session || null;
            notify();
            supabase.auth.onAuthStateChange((_event, session) => {
                currentSession = session;
                notify();
            });
        } catch (e) {
            console.warn("[Calmora] auth init failed", e);
        }
    }

    /* ─── Navbar wiring ─── */
    function wireNavbar() {
        const trigger = document.getElementById("auth-trigger");
        if (!trigger) return;
        window.CalmoraAuth.onChange((session) => {
            if (session?.user) {
                trigger.textContent = "Sign Out";
                trigger.dataset.mode = "out";
            } else {
                trigger.textContent = "Sign In";
                trigger.dataset.mode = "in";
            }
        });
        trigger.addEventListener("click", async (e) => {
            e.preventDefault();
            if (trigger.dataset.mode === "out") {
                await window.CalmoraAuth.signOut();
            } else {
                openModal();
            }
        });
    }

    /* ─── Modal ─── */
    function openModal() {
        if (!supabase) {
            alert("Sign-in isn't configured yet. Please try again in a moment.");
            return;
        }
        const root = document.getElementById("auth-modal-root");
        if (!root) return;
        root.innerHTML = `
          <div class="auth-modal-backdrop" data-auth-close>
            <div class="auth-modal" role="dialog" aria-modal="true">
              <button class="auth-close" aria-label="Close" data-auth-close>×</button>
              <div class="auth-header">
                <span class="logo-mark">
                  <svg width="22" height="22" viewBox="0 0 24 24" fill="none"><path d="M12 2C8 6 6 10 6 14a6 6 0 0 0 12 0c0-4-2-8-6-12z" fill="currentColor"/></svg>
                </span>
                <h3>Welcome to Calmora</h3>
                <p>Sign in to save your conversations, journal entries, and bookings.</p>
              </div>
              <div class="auth-tabs">
                <button class="auth-tab active" data-tab="login">Log In</button>
                <button class="auth-tab" data-tab="signup">Sign Up</button>
              </div>
              <form class="auth-form" data-form="login">
                <input type="email" name="email" placeholder="Email" required autocomplete="email">
                <input type="password" name="password" placeholder="Password" required autocomplete="current-password">
                <button type="submit" class="btn btn-primary btn-block">Log In</button>
                <div class="auth-error" data-error></div>
              </form>
              <form class="auth-form" data-form="signup" style="display:none">
                <input type="text" name="full_name" placeholder="Your name" required>
                <input type="email" name="email" placeholder="Email" required autocomplete="email">
                <input type="password" name="password" placeholder="Password (min 6 chars)" required minlength="6" autocomplete="new-password">
                <button type="submit" class="btn btn-primary btn-block">Create account</button>
                <div class="auth-error" data-error></div>
              </form>
            </div>
          </div>`;
        root.querySelectorAll("[data-auth-close]").forEach(el =>
            el.addEventListener("click", (e) => { if (e.target === el) root.innerHTML = ""; })
        );
        root.querySelectorAll(".auth-tab").forEach(tab => {
            tab.addEventListener("click", () => {
                root.querySelectorAll(".auth-tab").forEach(t => t.classList.remove("active"));
                tab.classList.add("active");
                const which = tab.dataset.tab;
                root.querySelector('[data-form="login"]').style.display  = which === "login"  ? "" : "none";
                root.querySelector('[data-form="signup"]').style.display = which === "signup" ? "" : "none";
            });
        });

        const showErr = (form, msg) => {
            const e = form.querySelector("[data-error]");
            if (e) e.textContent = msg || "";
        };

        root.querySelector('[data-form="login"]').addEventListener("submit", async (e) => {
            e.preventDefault();
            const form = e.currentTarget;
            showErr(form, "");
            const fd = new FormData(form);
            const { error } = await supabase.auth.signInWithPassword({
                email: fd.get("email"),
                password: fd.get("password"),
            });
            if (error) { showErr(form, error.message); return; }
            root.innerHTML = "";
        });

        root.querySelector('[data-form="signup"]').addEventListener("submit", async (e) => {
            e.preventDefault();
            const form = e.currentTarget;
            showErr(form, "");
            const fd = new FormData(form);
            const { error } = await supabase.auth.signUp({
                email: fd.get("email"),
                password: fd.get("password"),
                options: { data: { full_name: fd.get("full_name") } },
            });
            if (error) { showErr(form, error.message); return; }
            showErr(form, "Account created. Check your inbox if email confirmation is on, then log in.");
        });
    }

    document.addEventListener("DOMContentLoaded", async () => {
        await init();
        wireNavbar();
    });
})();
