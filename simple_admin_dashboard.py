"""
Create a simple admin dashboard as fallback
"""

# Read current accounts/views.py
with open('c:/Users/hp/.windsurf/2048/accounts/views.py', 'r') as f:
    content = f.read()

# Add simple admin dashboard function
new_function = '''
@login_required
def simple_admin_dashboard_view(request):
    """Simple admin dashboard - fallback version."""
    if request.user.role != 'ADMIN':
        return JsonResponse({'error': 'Admin only'}, status=403)
    
    try:
        from accounts.models import User
        from items.models import Item
        
        # Get basic statistics
        total_users = User.objects.count()
        total_items = Item.objects.count()
        
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
                'uuid': str(item.uuid)
            })
        
        # Get users with items count
        users_with_items = []
        for user in User.objects.all():
            items_count = Item.objects.filter(reporter=user).count()
            users_with_items.append({
                'email': user.email,
                'name': f"{user.first_name} {user.last_name}",
                'role': user.role,
                'phone': user.phone or 'Not provided',
                'is_active': user.is_active,
                'date_joined': user.date_joined.strftime('%Y-%m-%d %H:%M'),
                'items_count': items_count
            })
        
        context = {
            'total_users': total_users,
            'total_items': total_items,
            'total_claims': 0,  # Simplified version
            'recent_users': recent_users,
            'all_items': all_items,
            'all_claims': [],  # Simplified version
            'items_data': items_data,
            'claims_data': [],  # Simplified version
            'users_with_items': users_with_items,
            'active_users': User.objects.filter(is_active=True).count(),
            'student_users': User.objects.filter(role='STUDENT').count(),
            'staff_users': User.objects.filter(role='STAFF').count(),
            'admin_users': User.objects.filter(role='ADMIN').count(),
            'active_items': Item.objects.filter(status='active').count(),
            'found_items': Item.objects.filter(status='found').count(),
            'claimed_items': Item.objects.filter(status='claimed').count(),
            'recovered_items': Item.objects.filter(status='recovered').count(),
            'pending_claims': 0,  # Simplified version
            'approved_claims': 0,  # Simplified version
            'rejected_claims': 0,  # Simplified version
        }
        
        return render(request, 'accounts/admin_dashboard.html', context)
    
    except Exception as e:
        return JsonResponse({
            'error': f'Simple admin dashboard error: {str(e)}',
            'details': 'Using simplified version without claims data'
        }, status=500)
'''

# Add the new function at the end
lines = content.split('\n')
lines.append(new_function)

# Write back to file
with open('c:/Users/hp/.windsurf/2048/accounts/views.py', 'w') as f:
    f.write('\n'.join(lines))

print("Simple admin dashboard function added!")
