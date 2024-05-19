from django.urls import path 
from . import views

urlpatterns = [
    path('home/', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('main/', views.main_view, name='main'),

    path('start/<int:test_id>/', views.start_test, name='start_test'), 
    path('question/<int:test_id>/', views.show_question, name='question'),
    
    path('listening-start/<int:test_id>/', views.start_listening_test, name='start_listening_test'),
    path('audio/<int:test_id>/', views.show_listening_question, name='audio_test'),
    
    path('grammar-start/<int:test_id>/', views.grammar_start_test, name='start_grammar_test'),
    path('grammar/<int:test_id>/', views.grammar_show_question, name='grammar_test'),
]
