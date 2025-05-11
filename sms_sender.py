from twilio.rest import Client
import os

# Send SMS via Twilio
def send_sms(to_number, message):
    account_sid = os.environ.get("TWILIO_SID")
    auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
    twilio_number = os.environ.get("TWILIO_PHONE")

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=message,
        from_=twilio_number,
        to=to_number
    )

    print(f"✅ SMS sent: {message.sid}")
