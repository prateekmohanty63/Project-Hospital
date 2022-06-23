
from django.contrib import admin


from main.models import User,Doctor,Hospital



# Register your models here.
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('id', 'Username', 'Email')
    
admin.site.register( Doctor)

admin.site.register(User)

admin.site.register(Hospital)
