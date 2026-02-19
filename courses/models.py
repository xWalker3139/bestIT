from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    title = models.CharField(max_length=200, verbose_name="Titlu")
    description = models.TextField(verbose_name="Descriere")
    image = models.ImageField(upload_to='courses/', blank=True, null=True, verbose_name="Imagine")
    duration = models.CharField(max_length=50, verbose_name="Durată")
    level = models.CharField(max_length=50, choices=[
        ('incepator', 'Începător'),
        ('intermediar', 'Intermediar'),
        ('avansat', 'Avansat')
    ], verbose_name="Nivel")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True, verbose_name="Activ")

    class Meta:
        verbose_name = "Curs"
        verbose_name_plural = "Cursuri"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class Lesson(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='lessons',
        verbose_name="Curs"
    )
    title = models.CharField(max_length=200, verbose_name="Titlu lecție")
    video = models.FileField(
        upload_to='lessons/videos/',
        verbose_name="Video"
    )

    suport_curs = models.FileField(
        upload_to='lessons/curricula/',
        verbose_name="Suport pentru curs",
        blank=True,
        null=True
    )

    duration = models.CharField(max_length=20, verbose_name="Durată", blank=True)
    order = models.PositiveIntegerField(verbose_name="Ordine")
    is_free = models.BooleanField(default=False, verbose_name="Preview gratuit")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Lecție"
        verbose_name_plural = "Lecții"
        ordering = ['order']
        unique_together = ('course', 'order')

    def __str__(self):
        return f"{self.course.title} - {self.title}"

class LessonPR(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'lesson')

class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments', verbose_name="Utilizator")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments', verbose_name="Curs")
    enrolled_at = models.DateTimeField(auto_now_add=True, verbose_name="Data înscrierii")
    completed = models.BooleanField(default=False, verbose_name="Completat")
    progress = models.IntegerField(default=0, verbose_name="Progress (%)")

    class Meta:
        verbose_name = "Înscriere"
        verbose_name_plural = "Înscrieri"
        unique_together = ['user', 'course']
        ordering = ['-enrolled_at']

    def __str__(self):
        return f"{self.user.username} - {self.course.title}"


class ContactMessage(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="Prenume")
    last_name = models.CharField(max_length=100, verbose_name="Nume")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=20, verbose_name="Telefon")
    message = models.TextField(verbose_name="Mesaj")
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False, verbose_name="Citit")

    class Meta:
        verbose_name = "Mesaj Contact"
        verbose_name_plural = "Mesaje Contact"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.created_at.strftime('%d.%m.%Y')}"

class LessonProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'lesson')
