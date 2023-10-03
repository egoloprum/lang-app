from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator 
from django.contrib import messages
from django.db.models import Avg, Count, Q
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

    if request.method == 'POST':
        quiz_id = Quiz.objects.get(pk=request.POST.get('quiz-id'))
        quiz_id.delete()

    quizs = Quiz.objects.annotate(child_count=models.Count('question_quiz')).select_related('host')
    context = {'quizs': quizs}
    return render(request, 'quiz.html', context)

@login_required(login_url='login')
def quizCreate(request):
    host = request.user
    quiz = Quiz.objects.create(host=host)
    return redirect('quiz-edit', quiz.id)

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
        quiz_required_score = None if request.POST.get('quiz-score') == "" else request.POST.get('quiz-score')
        quiz_difficulty = None if request.POST.get('quiz-diff') == "" else request.POST.get('quiz-diff')
        quiz_public = True if request.POST.get('quiz-public') == 'on' else False
        quiz_start = None if request.POST.get('quiz-duration') == "" else request.POST.get('quiz-start')
        quiz_end = None if request.POST.get('quiz-duration') == "" else request.POST.get('quiz-end')

        quiz.name = quiz_name
        quiz.duration = quiz_duration
        quiz.difficulty = quiz_difficulty
        quiz.required_score = quiz_required_score
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
    
    context = {
        'quiz': quiz,
        'questions': questions,
        'answers': answers
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

    context = {
        'quiz': quiz,
        'questions': questions,
        'answers': answers,
    }

    sel_answers = [[] for _ in range(len(questions))]

    if request.method == 'POST':
        iter = 1
        q = 1

        completed_quiz = Completed_Quiz.objects.create(quiz=quiz, user=request.user)
        
        for x in range(len(questions)):
            while(request.POST.get('answer-id-' + str(iter))):
                q += 1
                answer = Answer.objects.get(id=request.POST.get('answer-id-' + str(iter)))

                if answer.question == questions[x]:
                    sel_answers[x].append(answer.id)
                    try:
                        Selected_Answer.objects.create(selected=answer, user=request.user, quiz=completed_quiz, question=questions[x])
                    except IntegrityError:
                        ...
                else:
                    break

                iter += 1

        points = 0
        for x in range(0, len(questions)):
            for y in range(0, len(cor_answers[x])):
                if len(sel_answers[x]) == len(cor_answers[x]) and sel_answers[x][y] == cor_answers[x][y].id:
                    points += 1

        result = Result.objects.create(quiz=quiz, user=request.user, score=points)

        return redirect('quiz-result', quiz.id)
    
    return render(request, 'quiz-each.html', context)

@login_required(login_url='login')
def quizResult(request, pk):
    quiz = Quiz.objects.select_related('host').get(id=pk)

    if request.user.is_staff:
        questions = Question.objects.select_related('quiz').filter(quiz=quiz)
        completed_quiz = Completed_Quiz.objects.select_related('quiz', 'user').filter(quiz=quiz, user=request.user).last()
        all_results = Result.objects.select_related('quiz', 'user').filter(quiz=quiz)
        results = all_results.filter(user=request.user).aggregate(average_score=Avg('score'))

        cor_answers = []
        sel_answers = []

        cor_ans = Answer.objects.select_related('question')
        sel_ans = Selected_Answer.objects.select_related('user', 'quiz', 'question')

        for x in range(0, len(questions)):
            cor_answers.append(cor_ans.filter(question=questions[x], correct=True))
            try:
                sel_answers.append(sel_ans.filter(user=request.user,
                                                                  quiz=completed_quiz, 
                                                                  question=questions[x]))
            except Selected_Answer.DoesNotExist:
                sel_answers.append(None)

        answers = list(zip(sel_answers, cor_answers))

        context = {
            'quiz': quiz,
            'results': results,
            'all_results': all_results,
            'questions': questions,
            'answers': answers,
        }

    else:
        questions = Question.objects.filter(quiz=quiz).select_related('quiz')
        completed_quiz = Completed_Quiz.objects.filter(quiz=quiz, user=request.user).last
        sel_answers = Selected_Answer.objects.filter(user=request.user, quiz=completed_quiz).select_related('user')
        results = Result.objects.filter(quiz=quiz, user=request.user).select_related('quiz', 'user')

        cor_answers = []
        for question in questions:
            cor_answers.extend(Answer.objects.filter(question=question, correct=True).select_related('question'))

        average_score = 0
        for result in results:
            average_score += result.score

        try:
            average_score /= results.count()
        except ZeroDivisionError:
            average_score = 0

        context = {
            'quiz': quiz,
            'results': results,
            'average_score': average_score,
            'questions': questions,
            'cor_answers': cor_answers,
            'sel_answers': sel_answers,
        }

    return render(request, 'quiz-result.html', context)

# @login_required(login_url='login')
# def quizResult(request, pk):
#     quiz = Quiz.objects.get(id=pk)
#     result = Result.objects.select_related('quiz').filter(quiz=quiz).last
#     results = Result.objects.select_related('quiz').filter(quiz=quiz).order_by('-id')
#     questions = Question.objects.select_related('quiz').filter(quiz=quiz)
#     answers = []
#     selected_answers = []

#     for question in questions:
#         for a in Answer.objects.filter(question=question).select_related('question'):
#             answers.append(a)
#             try:
#                 selected_answers.append(Selected_Answer.objects.select_related('answer').filter(answer=a).last)
#                 # Selected_Answer.objects.get(answer=a).delete()
#             except ObjectDoesNotExist:
#                 ...

#     list_answers = dict(zip(answers, selected_answers))
#     average_score = 0

#     for res in results:
#         average_score += res.score

#     try:
#         average_score = average_score / len(results)
#     except ZeroDivisionError:
#         average_score = 0

#     if Average_score.objects.filter(quiz=quiz, user=request.user).exists:
#         Average_score.objects.filter(quiz=quiz, user=request.user).delete()

#     Average_score.objects.create(quiz=quiz, user=request.user, score=average_score)

#     context = {'result': result, 'results': results, 'average_score': average_score,
#                'quiz': quiz, 'questions': questions, 'answers': list_answers, 'ans': answers}

#     return render(request, 'quiz-result.html', context)

