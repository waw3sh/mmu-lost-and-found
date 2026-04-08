"""
Create a public debug view to check users without login requirement
"""

# Read current accounts/views.py
with open('c:/Users/hp/.windsurf/2048/accounts/views.py', 'r') as f:
    content = f.read()

# Add public debug function
new_function = '''
def public_users_view(request):
    """Public view to check users - no login required."""
    from accounts.models import User
    
    users = User.objects.all().order_by('-date_joined')
    admin_users = User.objects.filter(role='ADMIN')
    
    user_list = []
    for user in users[:10]:  # Show first 10 users
        user_list.append({
            'email': user.email,
            'name': f"{user.first_name} {user.last_name}",
            'role': user.role,
            'phone': user.phone,
            'is_staff': user.is_staff,
            'is_superuser': user.is_superuser,
            'is_active': user.is_active,
            'date_joined': str(user.date_joined),
            'items_count': user.reported_items.count()
        })
    
    admin_list = []
    for admin in admin_users:
        admin_list.append({
            'email': admin.email,
            'name': f"{admin.first_name} {admin.last_name}",
            'role': admin.role,
            'is_staff': admin.is_staff,
            'is_superuser': admin.is_superuser,
            'is_active': admin.is_active
        })
    
    return JsonResponse({
        'total_users': users.count(),
        'admin_users_count': admin_users.count(),
        'recent_users': user_list,
        'admin_users': admin_list,
        'tess_user_found': User.objects.filter(email='tess@gmail.com').exists(),
        'mmuadmin_user_found': User.objects.filter(email='mmuadmin@lostfound.com').exists()
    })
'''

# Add the new function at the end
lines = content.split('\n')
lines.append(new_function)

# Write back to file
with open('c:/Users/hp/.windsurf/2048/accounts/views.py', 'w') as f:
    f.write('\n'.join(lines))

print("Public debug view added successfully!")
