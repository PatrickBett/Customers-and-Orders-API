import os
from africastalking.SMS import SMSService
from dotenv import load_dotenv

load_dotenv()
username = os.getenv("AFRICASTALKING_USERNAME")
api_key = os.getenv("AFRICASTALKING_API_KEY")

sms = SMSService(username, api_key)
def send_sms(phone_number,message):
    print(username)
    print(api_key)
    try:
        response = sms.send(message,[phone_number])
        print("✅ SMS sent successfully:", response)
        return response
    except Exception as e:
        print("❌ SMS sending failed:", str(e))
        return None