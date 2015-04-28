from countries.models import Country, Build, Army, Resource, Tech
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.contrib import admin

class BuildInline(admin.TabularInline):
    model=Build
    can_delete=False

class ArmyInline(admin.TabularInline):
    model=Army
    can_delete=False

class ResrcInline(admin.TabularInline):
    model=Resource
    can_delete=False

class TechInline(admin.TabularInline):
    model=Tech
    can_delete=False

class CountryAdmin(admin.ModelAdmin):
    fields = ['name', 'government']
    list_display = ('name', 'government')
    inlines = [BuildInline, ArmyInline, ResrcInline, TechInline]

class CountryInline(admin.TabularInline):
	model = Country
	can_delete=False

class UserAdmin(UserAdmin):
	inlines=(CountryInline,)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Country, CountryAdmin)
