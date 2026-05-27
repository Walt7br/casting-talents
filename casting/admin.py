from django.contrib import admin
from .models import Talent, CastingProject, RoleRequirement, Application, AuditionSchedule

class RoleInline(admin.TabularInline):
    model = RoleRequirement
    extra = 1

@admin.register(CastingProject)
class CastingProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'client', 'status', 'start_date', 'end_date', 'location')
    list_filter = ('status', 'location')
    search_fields = ('title', 'client', 'description')
    inlines = [RoleInline]

@admin.register(Talent)
class TalentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'city', 'phone', 'email', 'height_cm')
    search_fields = ('full_name', 'city', 'skills')
    list_filter = ('gender', 'city')

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('talent', 'project', 'role', 'status', 'score', 'created_at')
    list_filter = ('status', 'project')
    search_fields = ('talent__full_name', 'project__title', 'comment')

admin.site.register(RoleRequirement)
admin.site.register(AuditionSchedule)
