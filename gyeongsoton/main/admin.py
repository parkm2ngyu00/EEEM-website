from django.contrib import admin
from .models import certification, newterm, communityText, communityComment, manner, product,certification,notification
# Register your models here.

admin.site.register(newterm)
admin.site.register(communityText)
admin.site.register(communityComment)
admin.site.register(manner)
admin.site.register(product)
admin.site.register(certification)
admin.site.register(notification)
