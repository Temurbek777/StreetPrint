from django.http import JsonResponse
from django.utils.timezone import now


def qr_scan_handler(request):
    user_id = request.GET.get('user_id')

    if not user_id:
        return JsonResponse({'status': 'error', 'message': 'Missing user_id'}, status=400)

    # Simulate saving scan info
    print(f"✅ QR scanned: user_id = {user_id} at {now()}")

    # Optionally, you could save this to a model here

    return JsonResponse({
        'status': 'success',
        'message': f'Scan received for user {user_id}',
        'timestamp': now().isoformat()
    })
