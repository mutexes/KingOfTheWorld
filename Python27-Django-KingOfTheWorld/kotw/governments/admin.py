from governments.models import Government, effects
from django.contrib import admin

class effectsInline(admin.TabularInline):
    model = effects

class GovernmentAdmin(admin.ModelAdmin):
    fields = ['type']
    inlines = [effectsInline]

admin.site.register(Government, GovernmentAdmin)
