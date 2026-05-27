from django.contrib.auth.decorators import login_required
from django.db.models import Count, Avg, Q
from django.shortcuts import render, redirect, get_object_or_404
from .models import Talent, CastingProject, Application, AuditionSchedule, RoleRequirement
from .forms import TalentForm, CastingProjectForm, ApplicationForm, AuditionScheduleForm, RoleRequirementForm


def home(request):
    latest_projects = CastingProject.objects.filter(status='open')[:6]
    return render(request, 'casting/home.html', {'latest_projects': latest_projects})

@login_required
def dashboard(request):
    stats = {
        'talents': Talent.objects.count(),
        'projects': CastingProject.objects.count(),
        'applications': Application.objects.count(),
        'avg_score': round(Application.objects.aggregate(v=Avg('score'))['v'] or 0, 1),
    }
    by_status = Application.objects.values('status').annotate(total=Count('id')).order_by('status')
    active_projects = CastingProject.objects.annotate(total_applications=Count('applications')).order_by('-start_date')[:10]
    return render(request, 'casting/dashboard.html', {'stats': stats, 'by_status': by_status, 'active_projects': active_projects})

@login_required
def talent_list(request):
    q = request.GET.get('q', '')
    talents = Talent.objects.all()
    if q:
        talents = talents.filter(Q(full_name__icontains=q) | Q(city__icontains=q) | Q(skills__icontains=q))
    return render(request, 'casting/talent_list.html', {'talents': talents, 'q': q})

@login_required
def talent_create(request):
    form = TalentForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('talent_list')
    return render(request, 'casting/form.html', {'form': form, 'title': 'Добавление таланта'})

@login_required
def project_list(request):
    projects = CastingProject.objects.annotate(total_applications=Count('applications'))
    return render(request, 'casting/project_list.html', {'projects': projects})

@login_required
def project_create(request):
    form = CastingProjectForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        obj = form.save(commit=False)
        obj.manager = request.user
        obj.save()
        return redirect('project_list')
    return render(request, 'casting/form.html', {'form': form, 'title': 'Создание кастинга'})

@login_required
def project_detail(request, pk):
    project = get_object_or_404(CastingProject, pk=pk)
    return render(request, 'casting/project_detail.html', {'project': project})

@login_required
def role_create(request, project_id):
    project = get_object_or_404(CastingProject, pk=project_id)
    form = RoleRequirementForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        role = form.save(commit=False)
        role.project = project
        role.save()
        return redirect('project_detail', pk=project.id)
    return render(request, 'casting/form.html', {'form': form, 'title': f'Роль для кастинга: {project.title}'})

@login_required
def application_list(request):
    status = request.GET.get('status', '')
    applications = Application.objects.select_related('talent', 'project', 'role')
    if status:
        applications = applications.filter(status=status)
    return render(request, 'casting/application_list.html', {'applications': applications, 'status': status})

@login_required
def application_create(request):
    form = ApplicationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('application_list')
    return render(request, 'casting/form.html', {'form': form, 'title': 'Регистрация заявки'})

@login_required
def application_update_status(request, pk, status):
    application = get_object_or_404(Application, pk=pk)
    if status in dict(Application.STATUS_CHOICES):
        application.status = status
        application.save(update_fields=['status'])
    return redirect('application_list')

@login_required
def schedule_list(request):
    schedule = AuditionSchedule.objects.select_related('application', 'application__talent', 'application__project')
    return render(request, 'casting/schedule_list.html', {'schedule': schedule})

@login_required
def schedule_create(request):
    form = AuditionScheduleForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('schedule_list')
    return render(request, 'casting/form.html', {'form': form, 'title': 'Назначение пробы'})
