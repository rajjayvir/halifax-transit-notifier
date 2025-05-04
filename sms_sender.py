from dotenv import load_dotenv
import os
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from pprint import pprint

# Configure Brevo API key authorization
configuration = sib_api_v3_sdk.Configuration()
load_dotenv()
configuration.api_key['api-key'] = os.getenv("SENDINBLUE_API_KEY")
def send_sms(phone, carrier_gateway, message):
    # Prepare the recipient
    to_email = f"{phone}@{carrier_gateway}"
    print(f"📤 Preparing to send to: {to_email}")

    # Create instance of the API class
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=[{"email": to_email}],
        sender={"email": "rajjayvir0@gmail.com"}, 
        subject="Transit Update",
        text_content=message
    )

    try:
        # Send the email
        api_response = api_instance.send_transac_email(send_smtp_email)
        pprint(api_response)
        print("✅ Email sent successfully via Brevo API.")
    except ApiException as e:
        print("❌ Exception when sending email via Brevo API: %s\n" % e)

