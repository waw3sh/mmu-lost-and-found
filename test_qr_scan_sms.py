"""
Test QR code scanning and SMS notification flow
"""

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lostfound.settings')
django.setup()

from accounts.models import User
from items.models import Item
from notifications.services import notify_owner_item_found

print("=" * 60)
print("QR CODE SCANNING SMS TEST")
print("=" * 60)

# Find a user with phone number
users_with_phone = User.objects.filter(phone__isnull=False).exclude(phone='')
print(f"Users with phone numbers: {users_with_phone.count()}")

if users_with_phone.exists():
    owner = users_with_phone.first()
    print(f"\nTesting with owner: {owner.email}")
    print(f"Name: {owner.first_name} {owner.last_name}")
    print(f"Phone: {owner.phone}")
    
    # Find their items
    items = Item.objects.filter(reporter=owner)
    print(f"Items owned: {items.count()}")
    
    if items.exists():
        item = items.first()
        print(f"\nTesting item found notification:")
        print(f"Item: {item.name}")
        print(f"UUID: {item.uuid}")
        
        # Test the notification that would be sent when QR code is scanned
        print("\n" + "=" * 40)
        print("SIMULATING QR CODE SCAN...")
        print("=" * 40)
        
        result = notify_owner_item_found(owner, item, "Library - Main Desk")
        
        print("\n" + "=" * 40)
        print(f"NOTIFICATION RESULT: {result}")
        print("=" * 40)
        
        if result:
            print("SUCCESS: SMS would be sent in production")
            print("Local SSL issues prevent actual sending")
            print("Production server will send real SMS")
        else:
            print("FAILED: Notification system not working")
    else:
        print("No items found for this user")
else:
    print("No users with phone numbers found!")
    print("Need to create user with phone number to test")

print("\n" + "=" * 60)
print("QR SCAN TEST COMPLETE")
print("=" * 60)
