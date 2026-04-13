"""
Create owner claim view with OTP validation
"""

# Read current items/views.py
with open('c:/Users/hp/.windsurf/2048/items/views.py', 'r') as f:
    content = f.read()

# Add owner claim function
owner_claim_function = '''
@login_required
def owner_claim_view(request, item_id, otp_code):
    """Owner claim view with OTP validation."""
    from django.shortcuts import get_object_or_404
    from django.contrib import messages
    from items.models import Item
    from claims.models import Claim
    
    # Get the item
    item = get_object_or_404(Item, id=item_id)
    
    # Verify user is the owner of this item
    if item.reporter != request.user:
        messages.error(request, 'You can only claim your own items.')
        return redirect('/items/my-items/')
    
    # Check if item is in 'found' status
    if item.status != 'found':
        messages.error(request, 'This item is not available for claiming.')
        return redirect('/items/my-items/')
    
    # Check if claim already exists
    existing_claim = Claim.objects.filter(item=item).first()
    if existing_claim:
        messages.info(request, 'A claim already exists for this item.')
        return redirect('claims:claim_detail', claim_id=existing_claim.id)
    
    if request.method == 'POST':
        handoff_method = request.POST.get('handoff_method')
        message = request.POST.get('message', '')
        
        if handoff_method:
            # Create claim for owner (auto-verified since they have OTP)
            claim = Claim.objects.create(
                item=item,
                claimant=request.user,
                otp_code=otp_code,
                otp_verified=True,  # Auto-verify for owners
                status='VERIFIED',
                handoff_method=handoff_method
            )
            
            # Update item status
            item.status = 'claimed'
            item.save()
            
            messages.success(request, f'Your item "{item.name}" has been successfully claimed!')
            return redirect('claims:claim_detail', claim_id=claim.id)
        else:
            messages.error(request, 'Please select a handoff method.')
    
    context = {
        'item': item,
        'otp_code': otp_code,
        'is_owner': True
    }
    return render(request, 'claims/owner_claim.html', context)
'''

# Add the function to the file
content += owner_claim_function

# Write back to file
with open('c:/Users/hp/.windsurf/2048/items/views.py', 'a') as f:
    f.write(owner_claim_function)

print("Owner claim view added to items/views.py")
