"""Thin Supabase data-access helpers. Uses the service-role key for server-side writes."""

import os
from functools import lru_cache

from supabase import Client, create_client


@lru_cache(maxsize=1)
def service_client() -> Client | None:
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
    if not (url and key):
        return None
    return create_client(url, key)


def _safe_insert(table: str, row: dict) -> None:
    client = service_client()
    if client is None:
        return
    try:
        client.table(table).insert(row).execute()
    except Exception as e:
        print(f"[Calmora] insert into {table} failed: {e}")


def save_chat_message(user_id: str, role: str, content: str) -> None:
    if not user_id:
        return
    _safe_insert("chat_messages", {"user_id": user_id, "role": role, "content": content})


def save_mood(user_id: str, mood: str, context: str, response: str) -> None:
    if not user_id:
        return
    _safe_insert("mood_logs", {
        "user_id": user_id, "mood": mood, "context": context, "response": response,
    })


def save_journal(user_id: str, entry: str, reflection: str) -> None:
    if not user_id:
        return
    _safe_insert("journal_entries", {
        "user_id": user_id, "entry": entry, "reflection": reflection,
    })


def save_plan(user_id: str, goal: str, energy: str, hours: str, plan: str) -> None:
    if not user_id:
        return
    _safe_insert("weekly_plans", {
        "user_id": user_id, "goal": goal, "energy": energy, "hours": hours, "plan": plan,
    })


def save_study(user_id: str, task: str, time_window: str, breakdown: str) -> None:
    if not user_id:
        return
    _safe_insert("study_breakdowns", {
        "user_id": user_id, "task": task, "time_window": time_window, "breakdown": breakdown,
    })


def create_booking_row(user_id: str | None, plan: str, plan_label: str,
                       amount_paise: int, order_id: str, notes: dict) -> None:
    client = service_client()
    if client is None:
        return
    row = {
        "user_id": user_id,
        "plan": plan,
        "plan_label": plan_label,
        "amount_paise": amount_paise,
        "razorpay_order_id": order_id,
        "status": "pending",
        "name": notes.get("name") or "",
        "email": notes.get("email") or "",
        "phone": notes.get("phone") or "",
    }
    try:
        client.table("bookings").insert(row).execute()
    except Exception as e:
        print(f"[Calmora] create booking failed: {e}")


def mark_booking_paid(order_id: str, payment_id: str) -> None:
    client = service_client()
    if client is None or not order_id:
        return
    try:
        client.table("bookings").update({
            "razorpay_payment_id": payment_id,
            "status": "paid",
            "paid_at": "now()",
        }).eq("razorpay_order_id", order_id).execute()
    except Exception as e:
        print(f"[Calmora] mark booking paid failed: {e}")


def update_booking_details(order_id: str, fields: dict) -> None:
    client = service_client()
    if client is None or not order_id:
        return
    try:
        client.table("bookings").update(fields).eq("razorpay_order_id", order_id).execute()
    except Exception as e:
        print(f"[Calmora] update booking failed: {e}")


_HISTORY_TABLES = {
    "chat": "chat_messages",
    "mood": "mood_logs",
    "journal": "journal_entries",
    "plan": "weekly_plans",
    "study": "study_breakdowns",
    "booking": "bookings",
}


def list_history(user_id: str, kind: str, limit: int = 20) -> list[dict]:
    table = _HISTORY_TABLES.get(kind)
    client = service_client()
    if client is None or not user_id or not table:
        return []
    try:
        resp = (
            client.table(table)
            .select("*")
            .eq("user_id", user_id)
            .order("created_at", desc=True)
            .limit(limit)
            .execute()
        )
        return resp.data or []
    except Exception as e:
        print(f"[Calmora] list_history {kind} failed: {e}")
        return []


def get_profile(user_id: str) -> dict | None:
    client = service_client()
    if client is None or not user_id:
        return None
    try:
        resp = client.table("profiles").select("*").eq("user_id", user_id).limit(1).execute()
        rows = resp.data or []
        return rows[0] if rows else None
    except Exception as e:
        print(f"[Calmora] get_profile failed: {e}")
        return None
