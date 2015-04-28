from military.models import Military
from django.contrib import admin

class MilitaryAdmin(admin.ModelAdmin):
    fields = [ 'unit', 'offense', 'defense','fuel' ]
    list_display = ('unit', 'offense', 'defense','fuel')

admin.site.register(Military, MilitaryAdmin)
