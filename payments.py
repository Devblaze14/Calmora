"""Razorpay payment helpers — order creation + signature verification."""

import hmac
import hashlib
import os
import uuid

import razorpay
from razorpay.errors import BadRequestError, SignatureVerificationError


def _credentials():
    key_id = os.environ.get("RAZORPAY_KEY_ID")
    key_secret = os.environ.get("RAZORPAY_KEY_SECRET")
    return key_id, key_secret


def get_public_key_id():
    """Return the publishable key id for the frontend (never the secret)."""
    return os.environ.get("RAZORPAY_KEY_ID", "")


def _client():
    key_id, key_secret = _credentials()
    if not (key_id and key_secret):
        return None
    return razorpay.Client(auth=(key_id, key_secret))


def create_order(amount_paise: int, currency: str = "INR", receipt: str | None = None, notes: dict | None = None):
    """Create a Razorpay order. Returns (status_code, payload_dict)."""
    if amount_paise is None or amount_paise < 100:
        return 400, {"error": "Amount must be at least 100 paise (₹1)."}

    client = _client()
    if client is None:
        return 401, {"error": "Razorpay is not configured on the server."}

    payload = {
        "amount": int(amount_paise),
        "currency": currency,
        "receipt": receipt or f"calmora_{uuid.uuid4().hex[:12]}",
        "payment_capture": 1,
    }
    if notes:
        payload["notes"] = {k: str(v)[:200] for k, v in notes.items() if v is not None}

    try:
        order = client.order.create(payload)
    except BadRequestError as e:
        return 400, {"error": f"Razorpay rejected the order: {e}"}
    except Exception as e:  # noqa: BLE001
        return 500, {"error": f"Could not reach Razorpay: {e}"}

    return 200, {
        "order_id": order["id"],
        "amount": order["amount"],
        "currency": order["currency"],
        "receipt": order["receipt"],
    }


def verify_signature(order_id: str, payment_id: str, signature: str) -> bool:
    """Verify HMAC-SHA256 signature returned by Razorpay checkout."""
    if not (order_id and payment_id and signature):
        return False

    _, key_secret = _credentials()
    if not key_secret:
        return False

    expected = hmac.new(
        key_secret.encode("utf-8"),
        f"{order_id}|{payment_id}".encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()

    # Constant-time comparison
    if not hmac.compare_digest(expected, signature):
        return False

    # Belt-and-braces: also let the SDK validate (raises on mismatch)
    client = _client()
    if client is not None:
        try:
            client.utility.verify_payment_signature({
                "razorpay_order_id": order_id,
                "razorpay_payment_id": payment_id,
                "razorpay_signature": signature,
            })
        except SignatureVerificationError:
            return False
        except Exception:
            # SDK unreachable but HMAC already matched — trust local verification
            pass
    return True
