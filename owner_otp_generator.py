"""
Add owner OTP generation functionality
"""

# Read current items/views.py
with open('c:/Users/hp/.windsurf/2048/items/views.py', 'r') as f:
    content = f.read()

# Add owner OTP generation view
owner_otp_function = '''
@login_required
def generate_owner_otp(request, item_id):
    """Generate OTP for owner to claim their found item."""
    from django.shortcuts import get_object_or_404
    from django.contrib import messages
    from django.http import JsonResponse
    from items.models import Item
    from claims.models import Claim
    from notifications.services import generate_and_send_owner_otp
    
    # Get item
    item = get_object_or_404(Item, id=item_id)
    
    # Verify user is owner of this item
    if item.reporter != request.user:
        return JsonResponse({'error': 'You can only generate OTP for your own items.'}, status=403)
    
    # Check if item is in 'found' status
    if item.status != 'found':
        return JsonResponse({'error': 'This item is not available for OTP claiming.'}, status=400)
    
    # Check if claim already exists
    existing_claim = Claim.objects.filter(item=item).first()
    if existing_claim:
        return JsonResponse({'error': 'A claim already exists for this item.'}, status=400)
    
    # Generate and send OTP
    otp_code = generate_and_send_owner_otp(request.user, item)
    
    if otp_code:
        return JsonResponse({
            'success': True,
            'message': f'OTP sent to {request.user.phone}',
            'otp_code': otp_code,
            'claim_url': f"/items/owner-claim/{item.id}/{otp_code}/"
        })
    else:
        return JsonResponse({'error': 'Failed to send OTP. Please try again.'}, status=500)
'''

# Add the function to the file
content += owner_otp_function

# Write back to file
with open('c:/Users/hp/.windsurf/2048/items/views.py', 'a') as f:
    f.write(owner_otp_function)

# Add URL routing
with open('c:/Users/hp/.windsurf/2048/items/urls.py', 'r') as f:
    url_content = f.read()

# Add the new URL
new_url = "    path('generate-owner-otp/<int:item_id>/', views.generate_owner_otp, name='generate_owner_otp'),"
url_content = url_content.replace(
    "    path('owner-claim/<int:item_id>/<str:otp_code>/', views.owner_claim_view, name='owner_claim'),",
    "    path('owner-claim/<int:item_id>/<str:otp_code>/', views.owner_claim_view, name='owner_claim'),\n    path('generate-owner-otp/<int:item_id>/', views.generate_owner_otp, name='generate_owner_otp'),"
)

with open('c:/Users/hp/.windsurf/2048/items/urls.py', 'w') as f:
    f.write(url_content)

print("Owner OTP generation functionality added successfully!")
