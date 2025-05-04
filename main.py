import hashlib
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from datetime import datetime

app = FastAPI()

MERCHANT_ACCOUNT = "t_me_d82ef"
MERCHANT_DOMAIN = "t.me"
MERCHANT_SECRET = "ТУТ_ТВІЙ_SECRET_KEY"

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
