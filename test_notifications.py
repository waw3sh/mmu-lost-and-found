"""
Test notification system
Run this to verify SMS notifications are working
"""

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lostfound.settings')
django.setup()

from accounts.models import User
from items.models import Item
from notifications.services import notify_owner_item_found

print("=" * 60)
print("NOTIFICATION SYSTEM TEST")
print("=" * 60)

# Find a user with phone number
users_with_phone = User.objects.filter(phone__isnull=False).exclude(phone='')
print(f"Users with phone numbers: {users_with_phone.count()}")

if users_with_phone.exists():
    owner = users_with_phone.first()
    print(f"\nTesting with user: {owner.email}")
    print(f"Name: {owner.first_name} {owner.last_name}")
    print(f"Phone: {owner.phone}")
    
    # Find their items
    items = Item.objects.filter(reporter=owner)
    print(f"Items owned: {items.count()}")
    
    if items.exists():
        item = items.first()
        print(f"\nTesting notification for item: {item.name}")
        
        # Test the notification
        print("\n" + "=" * 40)
        print("SENDING TEST NOTIFICATION...")
        print("=" * 40)
        
        result = notify_owner_item_found(owner, item, "Test Location - Library", None)
        
        print("\n" + "=" * 40)
        print(f"NOTIFICATION RESULT: {result}")
        print("=" * 40)
    else:
        print("No items found for this user")
else:
    print("No users with phone numbers found!")
    print("\nTo test, create a user with phone number and register an item.")

print("\n" + "=" * 60)
print("TEST COMPLETE")
print("=" * 60)
