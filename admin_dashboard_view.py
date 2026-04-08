"""
Create a comprehensive admin dashboard
"""

# Read current accounts/views.py
with open('c:/Users/hp/.windsurf/2048/accounts/views.py', 'r') as f:
    content = f.read()

# Add admin dashboard function
new_function = '''
@login_required
def admin_dashboard_view(request):
    """Comprehensive admin dashboard."""
    if request.user.role != 'ADMIN':
        return JsonResponse({'error': 'Admin only'}, status=403)
    
    from accounts.models import User
    from items.models import Item
    from claims.models import Claim
    
    # Get statistics
    total_users = User.objects.count()
    total_items = Item.objects.count()
    total_claims = Claim.objects.count()
    
    # Get recent users
    recent_users = User.objects.all().order_by('-date_joined')[:10]
    
    # Get all items with details
    all_items = Item.objects.all().order_by('-created_at')
    items_data = []
    for item in all_items:
        items_data.append({
            'id': item.id,
            'name': item.name,
            'category': item.category,
            'status': item.status,
            'reporter': item.reporter.email if item.reporter else 'Unknown',
            'reporter_name': f"{item.reporter.first_name} {item.reporter.last_name}" if item.reporter else 'Unknown',
            'location_found': item.location_found or 'Not specified',
            'created_at': item.created_at.strftime('%Y-%m-%d %H:%M'),
            'uuid': str(item.uuid),
            'claims_count': Claim.objects.filter(item=item).count()
        })
    
    # Get all claims with details
    all_claims = Claim.objects.all().order_by('-created_at')
    claims_data = []
    for claim in all_claims:
        claims_data.append({
            'id': claim.id,
            'item': claim.item.name,
            'item_uuid': str(claim.item.uuid),
            'claimant': claim.claimant.email if claim.claimant else 'Unknown',
            'claimant_name': f"{claim.claimant.first_name} {claim.claimant.last_name}" if claim.claimant else 'Unknown',
            'status': claim.status,
            'created_at': claim.created_at.strftime('%Y-%m-%d %H:%M'),
            'description': claim.description[:100] + '...' if len(claim.description) > 100 else claim.description
        })
    
    # Get users with items count
    users_with_items = []
    for user in User.objects.all():
        items_count = Item.objects.filter(reporter=user).count()
        claims_count = Claim.objects.filter(claimant=user).count()
        users_with_items.append({
            'email': user.email,
            'name': f"{user.first_name} {user.last_name}",
            'role': user.role,
            'phone': user.phone or 'Not provided',
            'is_active': user.is_active,
            'date_joined': user.date_joined.strftime('%Y-%m-%d %H:%M'),
            'items_count': items_count,
            'claims_count': claims_count
        })
    
    context = {
        'total_users': total_users,
        'total_items': total_items,
        'total_claims': total_claims,
        'recent_users': recent_users,
        'all_items': all_items,
        'all_claims': all_claims,
        'items_data': items_data,
        'claims_data': claims_data,
        'users_with_items': users_with_items,
        'active_users': User.objects.filter(is_active=True).count(),
        'student_users': User.objects.filter(role='STUDENT').count(),
        'staff_users': User.objects.filter(role='STAFF').count(),
        'admin_users': User.objects.filter(role='ADMIN').count(),
        'active_items': Item.objects.filter(status='active').count(),
        'found_items': Item.objects.filter(status='found').count(),
        'claimed_items': Item.objects.filter(status='claimed').count(),
        'recovered_items': Item.objects.filter(status='recovered').count(),
        'pending_claims': Claim.objects.filter(status='pending').count(),
        'approved_claims': Claim.objects.filter(status='approved').count(),
        'rejected_claims': Claim.objects.filter(status='rejected').count()
    }
    
    return render(request, 'accounts/admin_dashboard.html', context)
'''

# Add new function at the end
lines = content.split('\n')
lines.append(new_function)

# Write back to file
with open('c:/Users/hp/.windsurf/2048/accounts/views.py', 'w') as f:
    f.write('\n'.join(lines))

print("Admin dashboard function added!")
