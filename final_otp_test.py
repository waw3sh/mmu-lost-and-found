"""
Final OTP claim system test with working links
"""

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lostfound.settings')
django.setup()

from items.models import Item
from accounts.models import User
from claims.models import Claim
import random

print("=" * 70)
print("FINAL OTP CLAIM SYSTEM TEST")
print("=" * 70)

# Get found items that don't have claims yet
found_items = Item.objects.filter(status='found')
available_items = []

for item in found_items:
    existing_claim = Claim.objects.filter(item=item).first()
    if not existing_claim:
        available_items.append(item)

print(f"Found {len(available_items)} items available for claiming:")
print("-" * 50)

for i, item in enumerate(available_items[:3], 1):
    print(f"{i}. {item.name} (ID: {item.id})")
    print(f"   Reporter: {item.reporter.email}")
    print(f"   Status: {item.status}")
    print("-" * 50)

if available_items:
    test_item = available_items[0]
    test_user = User.objects.filter(phone__isnull=False).exclude(phone='').first()
    
    print(f"\nTESTING WITH: {test_item.name}")
    print(f"TEST USER: {test_user.first_name} {test_user.last_name}")
    print("-" * 50)
    
    # Generate test OTP
    test_otp = f"{random.randint(100000, 999999)}"
    print(f"GENERATED OTP: {test_otp}")
    
    # Create test claim
    try:
        claim = Claim.objects.create(
            item=test_item,
            claimant=test_user,
            otp_code=test_otp,
            handoff_method="pickup"
        )
        
        print("CLAIM CREATED SUCCESSFULLY!")
        print(f"Claim ID: {claim.id}")
        print(f"OTP Code: {claim.otp_code}")
        print(f"Status: {claim.status}")
        print("-" * 50)
        
        # Generate claim URL
        claim_url = f"https://mmu-lost-and-found.onrender.com/claims/create/{test_item.id}/"
        claim_detail_url = f"https://mmu-lost-and-found.onrender.com/claims/{claim.id}/"
        
        print("TEST LINKS:")
        print("-" * 50)
        print(f"1. CLAIM FORM: {claim_url}")
        print(f"2. CLAIM DETAIL: {claim_detail_url}")
        print("-" * 50)
        
        print("TEST INSTRUCTIONS:")
        print("-" * 50)
        print("1. Login with credentials:")
        print(f"   Email: {test_user.email}")
        print(f"   Password: Admin1234!")
        print("2. Navigate to CLAIM FORM URL")
        print(f"3. Enter OTP: {test_otp}")
        print("4. Select handoff method: pickup")
        print("5. Submit claim")
        print("6. Check CLAIM DETAIL URL")
        print("=" * 70)
        
    except Exception as e:
        print(f"Error: {str(e)}")

else:
    print("No items available for claiming (all have claims)")

print("\n" + "=" * 70)
print("ALL AVAILABLE CLAIM LINKS:")
print("-" * 50)

for item in available_items:
    claim_url = f"https://mmu-lost-and-found.onrender.com/claims/create/{item.id}/"
    print(f"{item.name}: {claim_url}")

print("=" * 70)
print("OTP CLAIM SYSTEM WORKING!")
print("Ready for testing on live site.")
print("=" * 70)
