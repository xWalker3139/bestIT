from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('despre/', views.about, name='about'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('contact/', views.contact, name='contact'),
    path('contul-meu/', views.my_account, name='my_account'),
    path('termeni-si-conditii/', views.termeni_si_conditii, name='terms'),
    path('politica-cookies/', views.politica_de_cookie, name='cookies'),
    path('politica-confidentialitate/', views.politica_de_confidentialitate, name='privacy'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('lesson/complete/', views.mark_lesson_completed, name='lesson_complete'),
]