from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Word, Question, Test, Category, ListeningWord, ListeningQuestion, ListeningTest, GrammarTest
from django.http import JsonResponse
from django.urls import reverse
import random
from django.utils.text import slugify


def index(request):
    vocab_test = Test.objects.first()
    grammar_test = GrammarTest.objects.first()
    listening_test = ListeningTest.objects.first()

    context = {
        'vocab_test': vocab_test,
        'grammar_test': grammar_test,
        'listening_test': listening_test,
    }
    return render(request, 'index.html', context)

def register(request):
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.create_user(username=username, email=email, password=password)
        return redirect('/home/') 
    else:
        return render(request, 'register.html')  
    
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/home/') 
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
            return redirect('/login/')
    else:
        return render(request, 'login.html') 
    
def logout_view(request):
    logout(request)
    return redirect('/home/')

def main_view(request):
    tests = Test.objects.all()
    categories = Category.objects.all()
    audio_tests = ListeningTest.objects.all()
    grammar_tests = GrammarTest.objects.all()
    
    context = {
        'tests':tests,
        'categories':categories,
        'audio_tests': audio_tests,
        'grammar_tests': grammar_tests
    }
    return render(request, 'main.html', context)
 
@login_required
def start_test(request, test_id=None):
    if test_id:
        test = get_object_or_404(Test, id=test_id, user=request.user)
        test.completed = False
        test.current_question = 0
        for question in test.questions.all():
            question.completed = False
            question.correct = False  
            question.save()
        test.save()
    else:
        test = Test.objects.create(user=request.user)
        questions = [Question.objects.create(word=word) for word in Word.objects.all()]
        test.questions.set(questions)
        test.save()

    return redirect('question', test_id=test.id)




@login_required
def show_question(request, test_id):
    test = Test.objects.get(id=test_id, user=request.user)
    questions = list(test.questions.all())
    if test.current_question >= len(questions):
        test.completed = True
        test.save()
        return JsonResponse({'correct': True})

    question = questions[test.current_question]
    distractors = question.word.get_distractors_list()
    possible_answers = [question.word.english_word] + distractors
    random.shuffle(possible_answers)
    message = None
    retry = False
    
    if request.method == 'POST':
        selected_answer = request.POST.get('answer')
        if selected_answer == question.word.english_word:
            question.correct = True
            test.current_question += 1
            question.save()
            test.save()
            if test.current_question >= len(questions):
                test.completed = True
                test.save()
                return JsonResponse({'correct': True, 'particleCount': 1000})
            return JsonResponse({'correct': True, 'particleCount': 1000, 'next_url': reverse('question', args=[test.id])})
        else:
            return JsonResponse({'correct': False})

    return render(request, 'question.html', {
        'question': question,
        'test': test,
        'answers': possible_answers,
        'message': message,
        'retry': retry
    })

@login_required
def show_listening_question(request, test_id):
    test = get_object_or_404(ListeningTest, id=test_id, user=request.user)
    questions = list(test.questions.all())
    if test.current_question >= len(questions):
        test.completed = True
        test.save()
        return JsonResponse({'correct': True})

    question = questions[test.current_question]
    possible_answers = [question.word.word] + question.word.get_distractors_list()
    random.shuffle(possible_answers)
    retry = False

    if not question.word.audio_file:
        question.word.save() 

    if request.method == 'POST':
        selected_answer = request.POST.get('answer')
        if selected_answer == question.word.word:
            question.correct = True
            test.current_question += 1
            question.save()
            test.save()
            if test.current_question >= len(questions):
                test.completed = True
                test.save()
                return JsonResponse({'correct': True})
            return JsonResponse({'correct': True, 'next_url': reverse('audio_test', args=[test.id])})
        else:
            return JsonResponse({'correct': False})

    return render(request, 'audio_test.html', {
        'question': question,
        'test': test,
        'answers': possible_answers,
        'retry': retry,
        'audio_url': question.word.audio_file.url if question.word.audio_file else None
    })


@login_required
def start_listening_test(request, test_id=None):
    if test_id:
        test = get_object_or_404(ListeningTest, id=test_id, user=request.user)
        test.completed = False
        test.current_question = 0
        for question in test.questions.all():
            question.completed = False
            question.correct = False
            question.save()
        test.save()
    else:
        test = ListeningTest.objects.create(user=request.user)
        questions = [ListeningQuestion.objects.create(word=word) for word in ListeningWord.objects.all()]
        test.questions.set(questions)
        test.save()

    return redirect('audio_test', test_id=test.id)

@login_required
def grammar_start_test(request, test_id):
    test = get_object_or_404(GrammarTest, id=test_id, user=request.user)
    test.completed = False
    test.current_question = 0
    test.save()
    questions = list(test.questions.all())
    if not questions:
        return render(request, 'error.html', {'message': 'No questions in this test.'})
    return redirect('grammar_test', test_id=test.id)

@login_required
def grammar_show_question(request, test_id):
    test = get_object_or_404(GrammarTest, id=test_id, user=request.user)
    questions = list(test.questions.all())

    if request.method == 'POST':
        selected_answer = request.POST.get('answer')
        current_question = questions[test.current_question]

        if selected_answer == current_question.correct_answer:
            if test.current_question + 1 < len(questions):
                test.current_question += 1
                test.save()
                return JsonResponse({'correct': True, 'next_url': reverse('grammar_test', args=[test_id])})
            else:
                test.completed = True
                test.save()
                return JsonResponse({'correct': True})
        else:
            return JsonResponse({'correct': False})

    current_question = questions[test.current_question]
    return render(request, 'grammar_test.html', {
        'test': test,
        'question': current_question,
        'answers': current_question.options.all(),
        'retry': False
    })



