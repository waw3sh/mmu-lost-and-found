import africastalking
from decouple import config
import logging

logger = logging.getLogger(__name__)

AT_API_KEY = config('AT_API_KEY', default='')
AT_USERNAME = config('AT_USERNAME', default='sandbox')

# Only initialize if API key is configured
if AT_API_KEY and AT_API_KEY != 'your-africastalking-api-key':
    africastalking.initialize(username=AT_USERNAME, api_key=AT_API_KEY)
    sms = africastalking.SMS
    AT_ENABLED = True
else:
    sms = None
    AT_ENABLED = False
    print("[SMS] Africa's Talking not configured. SMS will be logged only.")


def send_sms(phone_number, message):
    """
    Send SMS. Falls back to console log if AT not configured.
    Phone number must be in international format e.g. +254700000000
    """
    if not AT_ENABLED:
        print(f"[SMS LOG] To: {phone_number} | Message: {message}")
        return True
    try:
        if not phone_number:
            return False
        if not phone_number.startswith('+'):
            phone_number = '+' + phone_number
        response = sms.send(message, [phone_number])
        print(f"[SMS SENT] To: {phone_number}")
        logger.info(f"SMS sent: {response}")
        return True
    except Exception as e:
        print(f"[SMS ERROR] {str(e)}")
        logger.error(f"SMS failed: {str(e)}")
        return False


def notify_owner_item_found(owner, item, location_found, request):
    """Notify owner when their item is reported found."""
    print(f"[NOTIFICATION] Attempting to notify owner: {owner.email}")
    print(f"[NOTIFICATION] Item: {item.name}")
    print(f"[NOTIFICATION] Location: {location_found}")
    print(f"[NOTIFICATION] Owner phone: {owner.phone}")
    
    if not owner.phone:
        print(f"[SMS SKIP] {owner.email} has no phone number on file.")
        return False
    
    # Fix APP_URL if it has the typo
    app_url = config('APP_URL', default='http://localhost:8000')
    if 'https://' in app_url:
        app_url = app_url.replace('https://', 'https://')
    
    message = (
        f'Hello {owner.first_name}! Your item "{item.name}" was found '
        f'near "{location_found}". Log in to claim it: {app_url}/claims/'
    )
    
    print(f"[SMS MESSAGE] To: {owner.phone} | Message: {message}")
    result = send_sms(owner.phone, message)
    print(f"[SMS RESULT] Success: {result}")
    return result


def send_otp_sms(owner, otp_code):
    """Send OTP code for claim verification."""
    if not owner.phone:
        print(f"[OTP SKIP] {owner.email} has no phone.")
        return False
    message = (
        f'Your MMU Lost & Found verification code is: {otp_code}. '
        f'Valid for 15 minutes. Do not share this code.'
    )
    return send_sms(owner.phone, message)


def notify_item_recovered(owner, item):
    """Notify owner when their item is confirmed recovered."""
    if not owner.phone:
        return False
    message = (
        f'Your item "{item.name}" has been marked as recovered. '
        f'Thank you for using MMU Lost & Found.'
    )
    return send_sms(owner.phone, message)
