import datetime

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from user.models import Completion
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator 
from django.contrib import messages
from django.db.models import Avg, Count, Q

from follower.models import NotificationList
# Create your views here.

@login_required(login_url='login')
def quiz(request):
    # q = request.GET.get('q') if request.GET.get('q') != None else ''
    # difficulties = []

    # for quiz in Quiz.objects.all():
    #     difficulties.append(quiz.difficulty.lower())

    # difficulties = list(dict.fromkeys(difficulties))
    # sort_diff = ['a', 'e', 'i',]
    # difficulties.sort(key = lambda i: sort_diff.index(i[0]))     

    context = {}
    completions = Completion.objects.filter(user=request.user, completed=True).select_related('quiz')
    list_count = NotificationList.objects.get(user=request.user).notification.all().count()

    context['completions'] = completions
    context['list_count'] = list_count

    if request.user.is_staff:
        quizs = Quiz.objects.annotate(child_count=models.Count('question_quiz')).select_related('host').filter(content=None, course=None)
        context['quizs'] = quizs
    else:
        quizs = Quiz.objects.annotate(child_count=models.Count('question_quiz')).select_related('host').filter(publication=True, content=None, course=None)
        context['quizs'] = quizs

    return render(request, 'quiz.html', context)

def searchQuiz(request):
    search_quiz = request.POST.get('search-quiz')
    search_status = request.POST.get('search-status')
    search_diff = request.POST.get('search-difficulty')
    search_date = request.POST.get('search-date')
    search_duration = request.POST.get('search-duration')

    current_time = datetime.datetime.now()
    completions = Completion.objects.filter(user=request.user, completed=True).select_related('quiz')

    context = {}
    context['completions'] = completions

    if request.user.is_staff:
        quizs = Quiz.objects.annotate(child_count=models.Count('question_quiz')).select_related('host').filter(
            content=None, course=None)
        
        if search_duration == 'Ascending':
            quizs = quizs.order_by('duration')
        elif search_duration == 'Descending':
            quizs = quizs.order_by('-duration')

        if search_date == 'Not Started':
            quizs = quizs.filter(Q(start_date__lte=current_time))
        elif search_date == 'Started':
            quizs = quizs.filter(Q(start_date__gte=current_time))
        elif search_date == 'Finished':
            quizs = quizs.filter(Q(end_date__lte=current_time))


        if search_diff == 'Difficulty':
            quizs = quizs.filter(Q(name__icontains=search_quiz))
        else:
            quizs = quizs.filter(Q(name__icontains=search_quiz, difficulty=search_diff))

        context['quizs'] = quizs
    else:
        quizs = Quiz.objects.annotate(child_count=models.Count('question_quiz')).select_related('host').filter(
            publication=True, content=None, course=None)
        
        if search_duration == 'Ascending':
            quizs = quizs.order_by('duration')
        elif search_duration == 'Descending':
            quizs = quizs.order_by('-duration')

        if search_date == 'Not Started':
            quizs = quizs.filter(Q(start_date__lte=current_time))
        elif search_date == 'Started':
            quizs = quizs.filter(Q(start_date__gte=current_time))
        elif search_date == 'Finished':
            quizs = quizs.filter(Q(end_date__lte=current_time))


        if search_diff == 'Difficulty':
            quizs = quizs.filter(Q(name__icontains=search_quiz))
        else:
            quizs = quizs.filter(Q(name__icontains=search_quiz, difficulty=search_diff))

        context['quizs'] = quizs

    return render(request, 'quiz-partial.html', context)

@login_required(login_url='login')
def quizCreate(request):
    host = request.user
    quiz = Quiz.objects.create(host=host, name='New Quiz')
    return redirect('quiz-edit', quiz.id)

@login_required(login_url='login')
def quizDelete(request, pk):
    quiz = Quiz.objects.get(id=pk)
    quiz.delete()
    return redirect('quiz')

@login_required(login_url='login')
def quizEdit(request, pk):
    quiz = Quiz.objects.get(id=pk)
    questions = Question.objects.filter(quiz=quiz).select_related('quiz')
    answers = []

    for question in questions:
        answers.extend(Answer.objects.filter(question=question).select_related('question'))

    if request.method == 'POST':
        quiz_name = request.POST.get('quiz-name')
        quiz_duration = None if request.POST.get('quiz-duration') == "" else request.POST.get('quiz-duration')
        quiz_required_score = 60 if request.POST.get('quiz-score') == "" else request.POST.get('quiz-score')
        quiz_difficulty = None if request.POST.get('quiz-diff') == "" else request.POST.get('quiz-diff')
        quiz_pts = None if request.POST.get('quiz-pts') == "" else request.POST.get('quiz-pts')
        quiz_exp = None if request.POST.get('quiz-exp') == "" else request.POST.get('quiz-exp')
        quiz_public = True if request.POST.get('quiz-public') == 'on' else False
        quiz_start = None if request.POST.get('quiz-start') == "" else request.POST.get('quiz-start')
        quiz_end = None if request.POST.get('quiz-end') == "" else request.POST.get('quiz-end')

        quiz.name = quiz_name
        quiz.duration = quiz_duration
        quiz.difficulty = quiz_difficulty
        quiz.required_score = quiz_required_score
        quiz.pts = quiz_pts
        quiz.exp = quiz_exp
        quiz.publication = quiz_public
        quiz.start_date = quiz_start
        quiz.end_date = quiz_end
        quiz.save()
        x = 1
        y = 1
        while(request.POST.get('question-' + str(x))):
            question_body = request.POST.get('question-' + str(x))
            question_id = request.POST.get('question-id-' + str(x))
            question_exp = None if request.POST.get('explanation-' + str(x)) == "" else request.POST.get('explanation-' + str(x))
            question = questions.get(id=question_id)
            question.body = question_body
            question.explanation = question_exp
            question.save()

            while(request.POST.get('answer-body-' + str(x) + '-' + str(y))):
                answer_body = request.POST.get('answer-body-' + str(x) + '-' + str(y))
                answer_id = request.POST.get('answer-id-' + str(x) + '-' + str(y))
                answer_correct = True if request.POST.get('answer-cor-' + str(x) + '-' + str(y)) == 'on' else False
                ans = Answer.objects.get(id=answer_id)
                ans.body = answer_body
                ans.correct = answer_correct
                ans.save()

                y += 1

            x += 1

        return redirect('quiz')
    
    list_count = NotificationList.objects.get(user=request.user).notification.all().count()

    context = {
        'quiz': quiz,
        'questions': questions,
        'answers': answers,
        'list_count': list_count,
    }
    return render(request, 'quiz-edit.html', context)

@login_required(login_url='login')
def add_question(request, pk):
    quiz = Quiz.objects.get(id=pk)
    question = Question.objects.create(quiz=quiz)
    return HttpResponse(question.id)

@login_required(login_url='login')
def add_answer(request, pk):
    question = Question.objects.get(id=pk)
    answer = Answer.objects.create(question=question)
    return HttpResponse(answer.id)

@login_required(login_url='login')
def delete_question(request, pk):
    question = Question.objects.get(id=pk)
    id = question.quiz.id
    question.delete()
    return HttpResponse(' ')

@login_required(login_url='login')
def delete_answer(request, pk):
    answer = Answer.objects.get(id=pk)
    id = answer.question.quiz.id
    answer.delete()
    return HttpResponse(' ')

@login_required(login_url='login')
def checkQuizName(request):
    name = request.POST.get('quiz-name')

    if Quiz.objects.filter(name=name).exists():
        return HttpResponse('<div style="color:red;">This name is already in use</div>')
    elif name == '':
        return HttpResponse('')
    else:
        return HttpResponse('<div style="color:green;">This name is available</div>')

@login_required(login_url='login')
def quizEach(request, pk):
    quiz = Quiz.objects.get(id=pk)
    questions = Question.objects.filter(quiz=quiz).select_related('quiz')
    cor_answers = []
    answers = []

    for question in questions:
        answers.extend(Answer.objects.filter(question=question).select_related('question'))
        cor_answers.append(Answer.objects.filter(question=question, correct=True).select_related('question'))

    list_count = NotificationList.objects.get(user=request.user).notification.all().count()

    context = {
        'quiz': quiz,
        'questions': questions,
        'answers': answers,
        'list_count': list_count,
    }

    sel_answers = [[] for _ in range(len(questions))]

    if request.method == 'POST':
        if request.path != "http://127.0.0.1:8000/quiz/" + str(quiz.id):
            request.path = "http://127.0.0.1:8000/quiz/" + str(quiz.id)
        iter = 1

        try:
            comp = Completion.objects.get(user=request.user, quiz=quiz)
        except:
            comp = Completion.objects.create(user=request.user, quiz=quiz)

        if not comp.completed:
            comp.completed = True
            comp.save()

        if quiz.content:
            result = Result.objects.create(quiz=quiz, user=request.user, has_content=True)
            comp.contest = quiz.contest
            comp.save()

        if quiz.course:
            result = Result.objects.create(quiz=quiz, user=request.user, has_course=True)
            comp.course = quiz.course
            comp.save()

        if not quiz.content and not quiz.course:
            result = Result.objects.create(quiz=quiz, user=request.user)

        for x in range(len(questions)):
            while(request.POST.get('answer-id-' + str(iter))):
                answer = Answer.objects.get(id=request.POST.get('answer-id-' + str(iter)))

                if answer.question == questions[x]:
                    sel_answers[x].append(answer.id)
                    Selected_Answer.objects.create(selected=answer, user=request.user, question=questions[x], result=result)
                else:
                    break

                iter += 1

        points = 0
        for x in range(0, len(questions)):
            for y in range(0, len(cor_answers[x])):
                if len(sel_answers[x]) == len(cor_answers[x]) and sel_answers[x][y] == cor_answers[x][y].id:
                    points += 1

        try:
            result.score = (points / questions.count()) * 100
        except ZeroDivisionError:
            result.score = 0
        result.save()

        return redirect('quiz-result', quiz.id)
    
    return render(request, 'quiz-each.html', context)

@login_required(login_url='login')
def quizResult(request, pk):
    quiz = Quiz.objects.select_related('host').get(id=pk)
    questions = Question.objects.select_related('quiz').filter(quiz=quiz)
    list_count = NotificationList.objects.get(user=request.user).notification.all().count()

    context = {}
    context['quiz'] = quiz
    context['questions'] = questions
    context['list_count'] = list_count

    if request.user.is_staff:
        all_results = Result.objects.select_related('quiz', 'user').filter(quiz=quiz).order_by('-created_at')
        average_score = all_results.aggregate(average_score=Avg('score'))

        context['average_score'] = average_score
        context['all_results'] = all_results

    else:
        results = Result.objects.filter(quiz=quiz, user=request.user).select_related('quiz', 'user')
        all_results = results.order_by('-created_at')
        average_score = results.aggregate(average_score=Avg('score'))

        context['results'] = results
        context['all_results'] = all_results
        context['average_score'] = average_score

    if request.META.get('HTTP_REFERER').replace("http://127.0.0.1:8000", "") == request.path.replace("/result", "").replace("/each", ""):
        result = Result.objects.filter(user=request.user).last()
        cor_answers = []
        sel_answers = []
        sel_ans = Selected_Answer.objects.filter(result=result).select_related('result', 'user', 'selected', 'question')
        for question in questions:
            cor_answers.append(question.answer_question.filter(correct=True))
            # cor_answers.append(Answer.objects.filter(question=question, correct=True).select_related('question'))
            try:
                sel_answers.append(sel_ans.filter(user=request.user, question=question))
            except Selected_Answer.DoesNotExist:
                sel_answers.append(None)

        answers = list(zip(sel_answers, cor_answers, questions))
        context['answers'] = answers

    return render(request, 'quiz-result.html', context)
