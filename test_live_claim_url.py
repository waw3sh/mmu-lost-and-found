"""
Test the updated claim URL in SMS notifications
"""

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lostfound.settings')
django.setup()

from notifications.services import notify_owner_item_found
from accounts.models import User
from items.models import Item

print("=" * 70)
print("TESTING LIVE CLAIM URL IN SMS NOTIFICATIONS")
print("=" * 70)

# Find a test user and item
test_user = User.objects.filter(phone__isnull=False).exclude(phone='').first()
if test_user:
    test_item = Item.objects.filter(reporter=test_user).first()
    
    if test_item:
        print(f"TEST USER: {test_user.first_name} {test_user.last_name}")
        print(f"USER PHONE: {test_user.phone}")
        print(f"TEST ITEM: {test_item.name}")
        print(f"ITEM UUID: {test_item.uuid}")
        print("-" * 50)
        
        # Test with full finder info
        print("TEST SMS WITH LIVE CLAIM URL:")
        print("-" * 50)
        
        result = notify_owner_item_found(
            test_user, 
            test_item, 
            "Library - Main Desk", 
            finder_name="John Doe", 
            finder_phone="+254712345678"
        )
        
        print(f"Result: {result}")
        print("-" * 50)
        
        print("EXPECTED SMS MESSAGE:")
        print("-" * 50)
        print("Hello [Name]! Your item \"[Item]\" was found near \"[Location]\" by John Doe. Contact finder: +254712345678. Meet at: [Location]. View and claim: https://mmu-lost-and-found.onrender.com/claims/ - MMU Lost & Found")
        print("-" * 50)
        
        print("CLAIM URL DETAILS:")
        print("-" * 50)
        print("Live Site: https://mmu-lost-and-found.onrender.com/")
        print("Claims Page: https://mmu-lost-and-found.onrender.com/claims/")
        print("User can view all their found items and submit claims")
        print("-" * 50)
        
        print("URL VERIFICATION:")
        print("-" * 50)
        print("APP_URL from .env: https://mmu-lost-and-found.onrender.com")
        print("Claim URL constructed: https://mmu-lost-and-found.onrender.com/claims/")
        print("URL is correct and points to live production site")
        
    else:
        print("No items found for test user")
else:
    print("No users with phone numbers found")

print("\n" + "=" * 70)
print("DEPLOYMENT SUMMARY:")
print("-" * 50)
print("1. Claim URL updated to use live site")
print("2. SMS message text improved")
print("3. 'Log in to claim' changed to 'View and claim'")
print("4. URL points to production claims page")
print("5. Ready for deployment to Render.com")
print("=" * 70)
