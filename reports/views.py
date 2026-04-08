from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from items.models import Item
from reports.models import Report
from notifications.services import notify_owner_item_found
import logging

logger = logging.getLogger(__name__)


def finder_page(request, item_uuid):
    """Public page — no login required."""
    try:
        item = Item.objects.get(uuid=item_uuid)
    except Item.DoesNotExist:
        return render(request, 'reports/invalid_qr.html', status=404)

    if item.status in ['recovered', 'deactivated']:
        return render(request, 'reports/already_recovered.html',
                      {'item': item})

    if request.method == 'POST':
        location_found = request.POST.get('location_found', '').strip()
        finder_name = request.POST.get('finder_name', '').strip()
        finder_email = request.POST.get('finder_email', '').strip()
        message_text = request.POST.get('message', '').strip()

        if not location_found:
            return render(request, 'reports/finder_page.html', {
                'item': item,
                'error': 'Please tell us where you found the item.',
                'values': request.POST,
            })

        Report.objects.create(
            item=item,
            location_found=location_found,
            finder_name=finder_name if finder_name else None,
            finder_email=finder_email if finder_email else None,
            message=message_text if message_text else None,
        )

        # Update item status based on current state
        if item.status == 'active':
            item.status = 'found'
            item.save()
        elif item.status == 'found':
            # If already found, mark as recovered when new report comes in
            item.status = 'recovered'
            item.save()

        try:
            notify_owner_item_found(item.reporter, item, location_found)
        except Exception as e:
            logger.error(f"Notification failed: {str(e)}")

        return render(request, 'reports/success.html',
                      {'item_name': item.name})

    return render(request, 'reports/finder_page.html', {'item': item})


@login_required
def reports_list_view(request):
    """Shows all finder reports for items owned by current user."""
    user_items = Item.objects.filter(reporter=request.user)
    reports = Report.objects.filter(
        item__in=user_items
    ).select_related('item').order_by('-created_at')
    return render(request, 'reports/reports_list.html', {
        'reports': reports,
        'total_reports': reports.count(),
    })
