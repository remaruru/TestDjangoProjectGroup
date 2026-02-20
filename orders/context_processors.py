def notifications_processor(request):
    if request.user.is_authenticated:
        return {
            'notifications': request.user.notifications.filter(is_read=False)[:5]
        }
    return {'notifications': []}
