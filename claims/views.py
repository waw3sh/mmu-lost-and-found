from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Claim
from items.models import Item

@login_required
def claims_list(request):
    """View all claims made by the current user"""
    claims = Claim.objects.filter(claimant=request.user).order_by('-created_at')
    return render(request, 'claims/claims_list.html', {'claims': claims})

@login_required
def create_claim(request, item_id):
    """Create a new claim for an item"""
    item = get_object_or_404(Item, id=item_id, status='found')
    
    # Check if user already has a claim for this item
    existing_claim = Claim.objects.filter(item=item, claimant=request.user).first()
    if existing_claim:
        messages.error(request, 'You have already submitted a claim for this item.')
        return redirect('claims:claim_detail', claim_id=existing_claim.id)
    
    if request.method == 'POST':
        otp = request.POST.get('otp')
        handoff_method = request.POST.get('handoff_method')
        message = request.POST.get('message', '')
        
        if otp and handoff_method:
            claim = Claim.objects.create(
                item=item,
                claimant=request.user,
                otp_code=otp,  # Fixed: use otp_code instead of otp
                handoff_method=handoff_method,
                message=message
            )
            messages.success(request, 'Your claim has been submitted successfully!')
            return redirect('claims:claim_detail', claim_id=claim.id)
        else:
            messages.error(request, 'Please fill in all required fields.')
    
    return render(request, 'claims/create_claim.html', {'item': item})

@login_required
def claim_detail(request, claim_id):
    """View details of a specific claim"""
    claim = get_object_or_404(Claim, id=claim_id, claimant=request.user)
    return render(request, 'claims/claim_detail.html', {'claim': claim})
