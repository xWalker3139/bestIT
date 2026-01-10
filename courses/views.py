from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Course, Enrollment, Lesson
from .forms import ContactForm

def home(request):
    courses = Course.objects.filter(is_active=True)[:6]
    return render(request, 'home.html', {'courses': courses})

def about(request):
    return render(request, 'about.html')

def termeni_si_conditii(request):
    return render(request, 'termeni_si_conditii.html')

def politica_de_confidentialitate(request):
    return render(request, 'politica_de_confidentialitate.html')

def politica_de_cookie(request):
    return render(request, 'politica_de_cookie.html')

def user_login(request):
    if request.user.is_authenticated:
        return redirect('my_account')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Autentificare reușită!')
            return redirect('my_account')
        else:
            messages.error(request, 'Nume utilizator sau parolă incorectă!')
    
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    messages.success(request, 'Deconectare reușită!')
    return redirect('home')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mesajul dvs. a fost trimis cu succes! Vă vom contacta în cel mai scurt timp.')
            return redirect('contact')
    else:
        form = ContactForm()
    
    return render(request, 'contact.html', {'form': form})

@login_required
def my_account(request):
    enrollments = Enrollment.objects.filter(user=request.user).select_related('course')
    return render(request, 'my_account.html', {'enrollments': enrollments})

@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id, is_active=True)

    # verificăm dacă userul este înscris
    enrollment = Enrollment.objects.filter(
        user=request.user,
        course=course
    ).first()

    if not enrollment:
        return render(request, 'courses/not_enrolled.html', {
            'course': course
        })

    lessons = course.lessons.all().order_by('order')

    # prima lecție (default)
    active_lesson = lessons.first()

    return render(request, 'courses/course_detail.html', {
        'course': course,
        'lessons': lessons,
        'active_lesson': active_lesson,
        'enrollment': enrollment
    })

from django.http import JsonResponse
from .models import LessonProgress

@login_required
def mark_lesson_completed(request):
    lesson_id = request.POST.get('lesson_id')
    lesson = Lesson.objects.get(id=lesson_id)

    LessonProgress.objects.update_or_create(
        user=request.user,
        lesson=lesson,
        defaults={'completed': True}
    )

    return JsonResponse({'status': 'ok'})
