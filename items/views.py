from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import qrcode
import io
import base64
from .models import Item
from claims.models import Claim

@login_required
def dashboard_view(request):
    """Main dashboard for authenticated users"""
    user = request.user
    user_items = Item.objects.filter(reporter=user)

    total_items = user_items.count()
    active_items = user_items.filter(status='active').count()
    recovered = user_items.filter(status='recovered').count()
    pending_claims = Claim.objects.filter(item__reporter=user, status='pending').count()

    recent_items = user_items.order_by('-updated_at')[:5]

    context = {
        'total_items': total_items,
        'active_items': active_items,
        'recovered': recovered,
        'pending_claims': pending_claims,
        'recent_items': recent_items,
        'is_admin': user.role == 'ADMIN',
    }
    return render(request, 'dashboard.html', context)

def landing_view(request):
    """Public landing page for non-authenticated users"""
    if request.user.is_authenticated:
        return redirect('/dashboard/')
    steps = [
        'Register your valuable item on the system',
        'Print the QR sticker and attach it to your item',
        'A finder scans the QR code with their phone',
        'You receive an SMS alert and arrange collection',
    ]
    return render(request, 'landing.html', {'steps': steps})

@login_required
def register_item_view(request):
    """Register a new item"""
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()
        category = request.POST.get('category', '').strip()
        photo = request.FILES.get('photo')

        # Validation
        errors = {}
        if len(name) < 2:
            errors['name'] = 'Item name must be at least 2 characters.'
        if len(description) < 10:
            errors['description'] = 'Description must be at least 10 characters.'
        if not category:
            errors['category'] = 'Please select a category.'

        if errors:
            return render(request, 'items/register.html', {
                'errors': errors,
                'values': request.POST,
                'categories': Item.CATEGORY_CHOICES,
            })

        item = Item.objects.create(
            name=name,
            description=description,
            category=category,
            reporter=request.user,
            photo=photo if photo else None,
            status='active',  # Personal registered items are 'active', not 'found'
        )
        
        # Send instant SMS notification to user
        if request.user.phone:
            try:
                from notifications.services import send_sms
                confirmation_message = f"Hi {request.user.first_name}! Your item '{name}' has been successfully registered on MMU Lost & Found. Keep it safe and attach the QR code for easy recovery."
                send_sms(request.user.phone, confirmation_message)
            except Exception as e:
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f"Item registration SMS failed: {str(e)}")
        
        messages.success(
            request,
            f'"{item.name}" registered successfully! Download your QR code below.'
        )
        return redirect(f'/items/{item.id}/')

    return render(request, 'items/register.html', {
        'categories': Item.CATEGORY_CHOICES,
    })

@login_required
def item_detail(request, item_id):
    """View details of a specific item with QR code generation"""
    item = get_object_or_404(Item, id=item_id, reporter=request.user)

    # Generate QR code pointing to the public finder URL
    from django.conf import settings
    # Use production URL for QR codes to make them scannable from anywhere
    app_url = getattr(settings, 'APP_URL', 'https://mmu-lost-and-found.onrender.com')
    finder_url = f"{app_url}/found/{item.uuid}/"

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(finder_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    # Convert QR to base64 string to embed directly in HTML
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    qr_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    context = {
        'item': item,
        'qr_code': qr_base64,
        'finder_url': finder_url,
    }
    return render(request, 'items/detail.html', context)

@login_required
def items_list_view(request):
    """View all items for the current user with filtering"""
    status_filter = request.GET.get('status', 'all')
    items = Item.objects.filter(reporter=request.user)  # Fixed: use reporter instead of owner

    if status_filter != 'all':
        items = items.filter(status=status_filter.upper())

    items = items.order_by('-created_at')

    filter_tabs = [
        ('all', 'All Items', 'gray'),
        ('active', 'Active', 'blue'),
        ('found', 'Found!', 'amber'),
        ('claimed', 'Claim Pending', 'orange'),
        ('recovered', 'Recovered', 'green'),
    ]

    context = {
        'items': items,
        'status_filter': status_filter,
        'total_count': Item.objects.filter(reporter=request.user).count(),  # Fixed: use reporter
        'filter_tabs': filter_tabs,
    }
    return render(request, 'items/list.html', context)

@login_required
def items_list(request):
    """View all found items (public)"""
    items = Item.objects.filter(status='found').order_by('-created_at')
    return render(request, 'items/items_list.html', {'items': items})

@login_required
def my_items(request):
    """View items reported by the current user"""
    items = Item.objects.filter(reporter=request.user).order_by('-created_at')
    return render(request, 'items/my_items.html', {'items': items})

@login_required
def create_item(request):
    """Report a new found item"""
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        category = request.POST.get('category')
        location_found = request.POST.get('location_found')
        
        if name and description and category:
            item = Item.objects.create(
                name=name,
                description=description,
                category=category,
                location_found=location_found,
                reporter=request.user,
                status='found'
            )
            messages.success(request, 'Item reported successfully!')
            return redirect('items:item_detail', item_id=item.id)
        else:
            messages.error(request, 'Please fill in all required fields.')
    
    return render(request, 'items/create_item.html')

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
        
        if handoff_method:
            try:
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
            except Exception as e:
                if 'UNIQUE constraint' in str(e):
                    messages.error(request, 'A claim already exists for this item.')
                else:
                    messages.error(request, f'Error creating claim: {str(e)}')
                return render(request, 'claims/owner_claim.html', {'item': item, 'otp_code': otp_code, 'is_owner': True})
        else:
            messages.error(request, 'Please select a handoff method.')
    
    context = {
        'item': item,
        'otp_code': otp_code,
        'is_owner': True
    }
    return render(request, 'claims/owner_claim.html', context)

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
