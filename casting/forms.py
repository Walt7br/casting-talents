from django import forms
from .models import Talent, CastingProject, RoleRequirement, Application, AuditionSchedule

class TalentForm(forms.ModelForm):
    class Meta:
        model = Talent
        fields = ['full_name', 'birth_date', 'gender', 'city', 'phone', 'email', 'height_cm', 'skills', 'portfolio_link']
        widgets = {'birth_date': forms.DateInput(attrs={'type': 'date'}), 'skills': forms.Textarea(attrs={'rows': 3})}

class CastingProjectForm(forms.ModelForm):
    class Meta:
        model = CastingProject
        fields = ['title', 'client', 'description', 'start_date', 'end_date', 'location', 'status']
        widgets = {'start_date': forms.DateInput(attrs={'type': 'date'}), 'end_date': forms.DateInput(attrs={'type': 'date'}), 'description': forms.Textarea(attrs={'rows': 4})}

class RoleRequirementForm(forms.ModelForm):
    class Meta:
        model = RoleRequirement
        fields = ['role_name', 'gender', 'min_age', 'max_age', 'required_skills', 'payment']

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['talent', 'project', 'role', 'status', 'score', 'comment']
        widgets = {'comment': forms.Textarea(attrs={'rows': 3})}

class AuditionScheduleForm(forms.ModelForm):
    class Meta:
        model = AuditionSchedule
        fields = ['application', 'audition_time', 'room', 'result_note']
        widgets = {'audition_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}), 'result_note': forms.Textarea(attrs={'rows': 3})}
