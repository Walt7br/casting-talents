from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Talent(models.Model):
    GENDER_CHOICES = [('female', 'Женский'), ('male', 'Мужской'), ('other', 'Другое')]
    full_name = models.CharField('ФИО', max_length=160)
    birth_date = models.DateField('Дата рождения')
    gender = models.CharField('Пол', max_length=20, choices=GENDER_CHOICES)
    city = models.CharField('Город', max_length=80)
    phone = models.CharField('Телефон', max_length=40)
    email = models.EmailField('Email', blank=True)
    height_cm = models.PositiveIntegerField('Рост, см', null=True, blank=True)
    skills = models.TextField('Навыки')
    portfolio_link = models.URLField('Портфолио', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['full_name']
        verbose_name = 'Талант'
        verbose_name_plural = 'Таланты'

    def __str__(self):
        return self.full_name

class CastingProject(models.Model):
    STATUS_CHOICES = [('draft', 'Черновик'), ('open', 'Открыт'), ('closed', 'Закрыт')]
    title = models.CharField('Название кастинга', max_length=180)
    client = models.CharField('Заказчик', max_length=160)
    description = models.TextField('Описание')
    start_date = models.DateField('Дата начала')
    end_date = models.DateField('Дата окончания')
    location = models.CharField('Локация', max_length=160)
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='draft')
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Менеджер')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-start_date']
        verbose_name = 'Кастинг'
        verbose_name_plural = 'Кастинги'

    def __str__(self):
        return self.title

class RoleRequirement(models.Model):
    project = models.ForeignKey(CastingProject, on_delete=models.CASCADE, related_name='roles')
    role_name = models.CharField('Роль', max_length=120)
    gender = models.CharField('Требуемый пол', max_length=20, blank=True)
    min_age = models.PositiveIntegerField('Возраст от', validators=[MinValueValidator(1), MaxValueValidator(100)])
    max_age = models.PositiveIntegerField('Возраст до', validators=[MinValueValidator(1), MaxValueValidator(100)])
    required_skills = models.CharField('Ключевые навыки', max_length=250)
    payment = models.DecimalField('Гонорар', max_digits=10, decimal_places=2, default=0)

    class Meta:
        verbose_name = 'Требование к роли'
        verbose_name_plural = 'Требования к ролям'

    def __str__(self):
        return f'{self.project.title}: {self.role_name}'

class Application(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('review', 'На рассмотрении'),
        ('invited', 'Приглашен'),
        ('rejected', 'Отклонен'),
        ('approved', 'Утвержден'),
    ]
    talent = models.ForeignKey(Talent, on_delete=models.CASCADE, related_name='applications')
    project = models.ForeignKey(CastingProject, on_delete=models.CASCADE, related_name='applications')
    role = models.ForeignKey(RoleRequirement, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField('Статус заявки', max_length=20, choices=STATUS_CHOICES, default='new')
    score = models.PositiveIntegerField('Оценка', default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    comment = models.TextField('Комментарий', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('talent', 'project', 'role')
        ordering = ['-created_at']
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'

    def __str__(self):
        return f'{self.talent} — {self.project}'

class AuditionSchedule(models.Model):
    application = models.OneToOneField(Application, on_delete=models.CASCADE, related_name='audition')
    audition_time = models.DateTimeField('Время пробы')
    room = models.CharField('Зал/кабинет', max_length=80)
    result_note = models.TextField('Результат', blank=True)

    class Meta:
        ordering = ['audition_time']
        verbose_name = 'Расписание пробы'
        verbose_name_plural = 'Расписание проб'

    def __str__(self):
        return f'{self.application} — {self.audition_time:%d.%m.%Y %H:%M}'
