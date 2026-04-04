import requests
import logging
from decouple import config

logger = logging.getLogger(__name__)

AT_API_KEY = config('AT_API_KEY', default='')
AT_USERNAME = config('AT_USERNAME', default='sandbox')

# Use sandbox URL if username is sandbox, otherwise use live URL
if AT_USERNAME == 'sandbox':
    AT_SMS_URL = 'https://api.sandbox.africastalking.com/version1/messaging'
else:
    AT_SMS_URL = 'https://api.africastalking.com/version1/messaging'


def send_sms(phone_number, message):
    """
    Send SMS via Africa's Talking REST API directly.
    Uses requests library instead of AT SDK to avoid SSL issues.
    """
    if not phone_number:
        logger.warning("SMS skipped: no phone number provided")
        print("SMS skipped: no phone number")
        return False

    if not AT_API_KEY or AT_API_KEY == 'your-africastalking-api-key':
        logger.warning("SMS skipped: no valid API key configured")
        print("SMS skipped: API key not configured")
        return False

    # Ensure phone number is in international format
    if not phone_number.startswith('+'):
        phone_number = '+' + phone_number

    headers = {
        'apiKey': AT_API_KEY,
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
    }

    payload = {
        'username': AT_USERNAME,
        'to': phone_number,
        'message': message,
    }

    try:
        response = requests.post(
            AT_SMS_URL,
            headers=headers,
            data=payload,
            timeout=30,
        )

        response_data = response.json()
        logger.info(f"AT API response: {response_data}")
        print(f"AT API response: {response_data}")

        # Check if SMS was accepted
        if response.status_code == 201:
            recipients = response_data.get('SMSMessageData', {}).get(
                'Recipients', [])
            if recipients:
                status = recipients[0].get('status', '')
                if status == 'Success':
                    print(f"SMS sent successfully to {phone_number}")
                    return True
                else:
                    print(f"SMS failed with status: {status}")
                    logger.error(f"SMS status: {status}")
                    return False
        else:
            print(f"AT API error: {response.status_code} - {response.text}")
            logger.error(f"AT API error: {response.status_code}")
            return False

    except requests.exceptions.Timeout:
        print("SMS failed: request timed out")
        logger.error("SMS timeout")
        return False
    except requests.exceptions.ConnectionError as e:
        print(f"SMS failed: connection error - {e}")
        logger.error(f"SMS connection error: {e}")
        return False
    except Exception as e:
        print(f"SMS failed: {e}")
        logger.error(f"SMS error: {e}")
        return False


def notify_owner_item_found(owner, item, location_found):
    """
    Notify item owner when their item is reported found.
    Never expose owner details to finder.
    """
    if not owner.phone:
        print(f"SMS skipped: no phone for {owner.get_full_name()}")
        return False

    app_url = config('APP_URL', default='http://localhost:8000')
    claim_url = f"{app_url}/claims/"

    message = (
        f"Hello {owner.first_name}! "
        f"Your item \"{item.name}\" was found near \"{location_found}\". "
        f"Log in to claim it: {claim_url} "
        f"- MMU Lost & Found"
    )
    return send_sms(owner.phone, message)


def send_otp_sms(owner, otp_code):
    """
    Send OTP verification code to item owner.
    """
    if not owner.phone:
        print(f"OTP SMS skipped: no phone for {owner.get_full_name()}")
        return False

    message = (
        f"Your MMU Lost & Found verification code is: {otp_code}. "
        f"Valid for 15 minutes. Do not share this code."
    )
    return send_sms(owner.phone, message)


def notify_item_recovered(owner, item):
    """
    Notify owner when their item is successfully recovered.
    """
    if not owner.phone:
        return False

    message = (
        f"Great news {owner.first_name}! "
        f"Your item \"{item.name}\" has been marked as recovered. "
        f"Thank you for using MMU Lost & Found!"
    )
    return send_sms(owner.phone, message)
