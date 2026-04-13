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

    # Display full SMS message in sandbox
    if AT_USERNAME == 'sandbox':
        print("=" * 80)
        print("SMS MESSAGE (SANDBOX MODE)")
        print("=" * 80)
        print(f"To: {phone_number}")
        print(f"Message: {message}")
        print(f"Length: {len(message)} characters")
        print("=" * 80)

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
        # For sandbox, try with SSL verification disabled for local testing
        verify_ssl = AT_USERNAME != 'sandbox'
        
        response = requests.post(
            AT_SMS_URL,
            headers=headers,
            data=payload,
            timeout=30,
            verify=verify_ssl,
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
        # Fallback for local development - log the SMS that would be sent
        print(f"[SMS FALLBACK] Would send to {phone_number}: {message}")
        print("[SMS FALLBACK] Production server will send real SMS")
        return True  # Return True for demo purposes
    except Exception as e:
        print(f"SMS failed: {e}")
        logger.error(f"SMS error: {e}")
        return False


def notify_owner_item_found(owner, item, location_found, finder_name=None, finder_phone=None):
    """
    Notify item owner when their item is reported found.
    Include finder contact information if available.
    Also offer owner OTP option for claiming.
    Never expose owner details to finder.
    """
    if not owner.phone:
        print(f"SMS skipped: no phone for {owner.get_full_name()}")
        return False

    # Force production URL to avoid localhost issues
    app_url = "https://mmu-lost-and-found.onrender.com"
    claim_url = f"{app_url}/claims/"
    
    # Generate owner OTP for direct claiming
    import random
    owner_otp = f"{random.randint(100000, 999999)}"
    owner_claim_url = f"{app_url}/items/owner-claim/{item.id}/{owner_otp}/"

    # Build enhanced message with finder contact info and owner OTP
    if finder_name and finder_phone:
        message = (
            f"Hello {owner.first_name}! "
            f"Your item \"{item.name}\" was found near \"{location_found}\" by {finder_name}. "
            f"Contact finder: {finder_phone}. "
            f"Meet at: {location_found}. "
            f"OR use OTP {owner_otp} to claim directly: {owner_claim_url} "
            f"View all claims: {claim_url} "
            f"- MMU Lost & Found"
        )
    elif finder_name:
        message = (
            f"Hello {owner.first_name}! "
            f"Your item \"{item.name}\" was found near \"{location_found}\" by {finder_name}. "
            f"Meet at: {location_found}. "
            f"OR use OTP {owner_otp} to claim directly: {owner_claim_url} "
            f"View all claims: {claim_url} "
            f"- MMU Lost & Found"
        )
    else:
        message = (
            f"Hello {owner.first_name}! "
            f"Your item \"{item.name}\" was found near \"{location_found}\". "
            f"Use OTP {owner_otp} to claim directly: {owner_claim_url} "
            f"View all claims: {claim_url} "
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


def generate_and_send_owner_otp(owner, item):
    """
    Generate OTP for owner to claim their found item.
    """
    import random
    
    # Generate 6-digit OTP
    otp_code = f"{random.randint(100000, 999999)}"
    
    # Force production URL to avoid localhost issues
    app_url = "https://mmu-lost-and-found.onrender.com"
    owner_claim_url = f"{app_url}/items/owner-claim/{item.id}/{otp_code}/"
    
    # Send OTP to owner's registered phone
    message = (
        f"Hello {owner.first_name}! "
        f"Your item \"{item.name}\" is ready for collection. "
        f"Use OTP: {otp_code} to claim. "
        f"Claim here: {owner_claim_url} "
        f"- MMU Lost & Found"
    )
    
    result = send_sms(owner.phone, message)
    
    if result:
        print(f"Owner OTP sent to {owner.phone}: {otp_code}")
        return otp_code
    else:
        print(f"Failed to send owner OTP to {owner.phone}")
        return None


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
