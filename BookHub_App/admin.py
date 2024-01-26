from django.contrib import admin
from . models import Authors,Books,Admin_log


# Register your models here.

admin.site.register(Authors)
admin.site.register(Books)
admin.site.register(Admin_log)

