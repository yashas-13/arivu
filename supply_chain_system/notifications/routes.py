from fastapi import APIRouter

router = APIRouter()

@router.post("/email")
async def send_email(to: str, subject: str, body: str):
    # Stub for sending email
    return {"status": "sent", "to": to}

@router.post("/sms")
async def send_sms(to: str, message: str):
    # Stub for sending SMS
    return {"status": "sent", "to": to}
