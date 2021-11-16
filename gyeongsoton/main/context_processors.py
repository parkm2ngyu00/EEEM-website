from .models import notification

def getNotification(request):
    allnotification=notification.objects.filter(user=request.user.id)
    return{
        "notifications":allnotification
    }