from twilio.rest import Client
import os

def send_sms(to_number, _, message):
    account_sid = os.environ.get("TWILIO_SID")
    auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
    twilio_number = os.environ.get("TWILIO_PHONE")

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=message,
        from_=twilio_number,
        to=to_number  # e.g. "+17828822311"
    )

    print(f"✅ SMS sent: {message.sid}")
