from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from typing import Dict, Any
import hmac
import hashlib
from ..config import load_config

webhook_router = APIRouter()

class WebhookPayload(BaseModel):
    event: str
    data: Dict[str, Any]

@webhook_router.post("/webhook")
async def handle_webhook(request: Request, payload: WebhookPayload):
    config = load_config()
    
    # Verify webhook signature
    signature = request.headers.get('X-Webhook-Signature')
    if not verify_signature(payload.dict(), signature, config.SECRET_KEY):
        raise HTTPException(status_code=401, detail="Invalid signature")
    
    # Process webhook
    try:
        await process_webhook_event(payload.event, payload.data)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def verify_signature(payload: Dict, signature: str, secret: str) -> bool:
    computed = hmac.new(
        secret.encode(),
        str(payload).encode(),
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(computed, signature)

async def process_webhook_event(event: str, data: Dict[str, Any]):
    # Implementation for processing different webhook events
    pass 