from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.models import User
from items.models import Item
from claims.models import Claim
from reports.models import Report


def admin_required(view_func):
    """Decorator that checks if user is an admin."""
    @login_required
    def wrapper(request, *args, **kwargs):
        if request.user.role != 'ADMIN':
            messages.error(request, 'You do not have permission to access this page.')
            return redirect('/dashboard/')
        return view_func(request, *args, **kwargs)
    return wrapper


@admin_required
def admin_overview(request):
    """Main admin dashboard with system-wide stats."""
    total_users = User.objects.count()
    total_items = Item.objects.count()
    total_recovered = Item.objects.filter(status='recovered').count()
    total_active = Item.objects.filter(status='active').count()
    total_reported = Item.objects.filter(status='found').count()
    total_disputes = Claim.objects.filter(status='disputed').count()
    total_reports = Report.objects.count()

    # Recent activity — last 10 items updated
    recent_items = Item.objects.select_related('reporter').order_by(
        '-updated_at')[:10]

    # Items by category counts
    category_stats = []
    for value, label in Item.CATEGORY_CHOICES:
        count = Item.objects.filter(category=value).count()
        category_stats.append({'label': label, 'count': count})

    context = {
        'total_users': total_users,
        'total_items': total_items,
        'total_recovered': total_recovered,
        'total_active': total_active,
        'total_reported': total_reported,
        'total_disputes': total_disputes,
        'total_reports': total_reports,
        'recent_items': recent_items,
        'category_stats': category_stats,
    }
    return render(request, 'admin_panel/overview.html', context)


@admin_required
def admin_users(request):
    """Manage all users — view, search, change roles."""
    search = request.GET.get('search', '').strip()
    role_filter = request.GET.get('role', 'all')

    users = User.objects.all().order_by('-date_joined')

    if search:
        users = users.filter(
            first_name__icontains=search
        ) | users.filter(
            last_name__icontains=search
        ) | users.filter(
            email__icontains=search
        )

    if role_filter != 'all':
        users = users.filter(role=role_filter.upper())

    # Handle role change
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        new_role = request.POST.get('new_role')
        if user_id and new_role in ['STUDENT', 'STAFF', 'ADMIN']:
            target_user = get_object_or_404(User, id=user_id)
            target_user.role = new_role
            target_user.save()
            messages.success(
                request,
                f'{target_user.get_full_name()} role changed to {new_role}.'
            )
        return redirect('/admin-panel/users/')

    context = {
        'users': users,
        'search': search,
        'role_filter': role_filter,
        'total_count': User.objects.count(),
    }
    return render(request, 'admin_panel/users.html', context)


@admin_required
def admin_items(request):
    """View and manage all items across all users."""
    status_filter = request.GET.get('status', 'all')
    search = request.GET.get('search', '').strip()

    items = Item.objects.select_related('reporter').order_by('-created_at')

    if status_filter != 'all':
        items = items.filter(status=status_filter.upper())

    if search:
        items = items.filter(name__icontains=search) | \
                items.filter(reporter__first_name__icontains=search) | \
                items.filter(reporter__email__icontains=search)

    # Handle status change
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        new_status = request.POST.get('new_status')
        valid_statuses = ['ACTIVE', 'FOUND', 'CLAIM_PENDING',
                          'RECOVERED', 'DEACTIVATED']
        if item_id and new_status in valid_statuses:
            item = get_object_or_404(Item, id=item_id)
            item.status = new_status
            item.save()
            messages.success(
                request,
                f'"{item.name}" status changed to {new_status}.'
            )
        return redirect('/admin-panel/items/')

    context = {
        'items': items,
        'status_filter': status_filter,
        'search': search,
        'status_choices': Item.STATUS_CHOICES,
    }
    return render(request, 'admin_panel/items.html', context)


@admin_required
def admin_disputes(request):
    """Handle disputed claims."""
    disputes = Claim.objects.filter(
        status='disputed'
    ).select_related('item', 'claimant').order_by('-created_at')

    # Handle dispute resolution
    if request.method == 'POST':
        claim_id = request.POST.get('claim_id')
        action = request.POST.get('action')
        claim = get_object_or_404(Claim, id=claim_id)

        if action == 'resolve':
            claim.status = 'collected'
            claim.save()
            claim.item.status = 'recovered'
            claim.item.save()
            messages.success(
                request,
                f'Dispute resolved — "{claim.item.name}" marked as recovered.'
            )
        elif action == 'reject':
            claim.status = 'rejected'
            claim.save()
            claim.item.status = 'found'
            claim.item.save()
            messages.warning(
                request,
                f'Claim rejected — "{claim.item.name}" returned to reported.'
            )
        return redirect('/admin-panel/disputes/')

    context = {'disputes': disputes}
    return render(request, 'admin_panel/disputes.html', context)
