import hashlib
import hmac
import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

MERCHANT_ACCOUNT = os.getenv("MERCHANT_ACCOUNT")
MERCHANT_DOMAIN = os.getenv("MERCHANT_DOMAIN")
MERCHANT_SECRET = os.getenv("MERCHANT_SECRET")


@app.get("/create-payment")
def create_payment(user_id: str):
    order_ref = f"order_{user_id}_{int(datetime.utcnow().timestamp())}"
    amount = 29.00
    currency = "UAH"
    desc = "Оплата PRO версії РецептБота"

    sign_string = ";".join([
        MERCHANT_ACCOUNT,
        MERCHANT_DOMAIN,
        order_ref,
        str(amount),
        currency,
        desc
    ])
    signature = hashlib.sha1((sign_string + MERCHANT_SECRET).encode()).hexdigest()

    return JSONResponse({
        "merchantAccount": MERCHANT_ACCOUNT,
        "merchantDomainName": MERCHANT_DOMAIN,
        "orderReference": order_ref,
        "amount": amount,
        "currency": currency,
        "productName": ["PRO доступ"],
        "productPrice": [amount],
        "productCount": [1],
        "clientFirstName": "Telegram",
        "clientEmail": "telegram@bot.ua",
        "language": "UA",
        "orderDate": int(datetime.utcnow().timestamp()),
        "merchantSignature": signature
    })


# ✅ Endpoint для перевірки оплати
@app.post("/payment-check")
async def payment_check(request: Request):
    data = await request.json()

    # Отримуємо підпис з запиту
    signature_from_request = data.get("merchantSignature")
    if not signature_from_request:
        return JSONResponse({"status": "error", "message": "No signature"}, status_code=400)

    fields_to_sign = [
        data.get("merchantAccount", ""),
        data.get("orderReference", ""),
        str(data.get("amount", "")),
        data.get("currency", ""),
        data.get("authCode", ""),
        data.get("cardPan",
