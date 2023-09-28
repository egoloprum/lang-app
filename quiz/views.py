from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from django.http import HttpResponse, JsonResponse
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator 
from django.contrib import messages
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
    question_cor_num = []
    answers = []
    answer_correct = []

    for question in questions:
        answers.extend(Answer.objects.filter(question=question).select_related('question'))
        question_cor_num.append(models.Count(Answer.objects.filter(question=question, correct=True).select_related('question')))

    paginator = Paginator(questions, 5)
    page_number = request.GET.get("page")  
    page_obj = paginator.get_page(page_number)

    if request.method == 'POST':
        y = 1
        for x in range(1, len(questions) + 1):
            ans = []
            while(request.POST.get('answer-body-' + str(x) + '-' + str(y))):
                ans.append(True if request.POST.get('answer-' + str(x) + '-' + str(y)) == 'on' else False)
                y += 1
        
            answer_correct.append(ans)

        print(len(answer_correct))

        for x in range(0, len(answer_correct)):
            for y in range(0, len(answer_correct[x])):
                pass
    

    context = {
        'quiz': quiz,
        'questions': page_obj,
        'answers': answers,
    }
    return render(request, 'quiz-each.html', context)

# @login_required(login_url='login')
# def quizEach(request, pk):
#     quiz = Quiz.objects.get(id=pk)
#     questions = Question.objects.filter(quiz=quiz)
#     number_of_questions = len(questions)
#     answers = []
#     answers_correct_num = []

#     for question in questions:
#         count = 0
#         for a in Answer.objects.filter(question=question).select_related('question'):
#             answers.append(a)
#             if a.correct is True:
#                 count += 1
        
#         answers_correct_num.append(count)

#     context = {'quiz': quiz, 'questions': questions, 'answers': answers, 'number_of_questions': range(number_of_questions)}

#     if request.method == 'POST':
#         quiz_answers = []
#         result = 0

#         for answer in answers:
#             if request.POST.get('answer-' + str(answer.id)) == 'on':
#                 quiz_answers.append(True)
#                 Selected_Answer.objects.create(answer=answer, correct=True)
#             else:
#                 quiz_answers.append("")
#                 Selected_Answer.objects.create(answer=answer, correct=False)
    
#         temp_quiz = quiz_answers.copy()
#         temp_answers = answers.copy()
#         length_answers = len(answers_correct_num)

#         for question in questions:
#             count = 0
#             for n in range(len(question.get_answers())):
#                 if temp_answers[n].correct is temp_quiz[n]:
#                     count += 1

#             for n in range(len(question.get_answers())):
#                 temp_quiz.pop(0)
#                 temp_answers.pop(0)

#             try:
#                 result += count / answers_correct_num[0]
#             except ZeroDivisionError:
#                 result = result

#             answers_correct_num.pop(0)
        
#         result = (result / length_answers) * 100

#         quiz_result = Result.objects.create(quiz=quiz, user=request.user, score=result)

#         return redirect('quiz-result', quiz.id)

#     return render(request, 'quiz-each.html', context)

# @login_required(login_url='login')
# def quizEdit(request, pk):
#     quiz = Quiz.objects.get(id=pk)
#     questions = Question.objects.filter(quiz=quiz)
#     number_of_questions = len(questions)
#     answers = []

#     for question in questions:
#         for a in Answer.objects.filter(question=question).select_related('question'):
#             answers.append(a)

#     if request.method == "POST":
#         quiz_name = request.POST.get('quiz-name')
#         quiz_duration = request.POST.get('quiz-duration')
#         quiz_required = request.POST.get('quiz-required')
#         quiz_diff = request.POST.get('quiz-difficulty')

#         quiz.name = quiz_name
#         if quiz_duration:
#             quiz.duration = quiz_duration
#         if quiz_required:
#             quiz.required_score = quiz_required
#         if quiz_diff:
#             quiz.difficulty = quiz_diff

#         for question in questions:
#             question_body = request.POST.get('question-body-' + str(question.id))
#             question.body = question_body

#             for answer in answers:
#                 if answer.question.id == question.id:
#                     answer_body = request.POST.get('answer-body-' + str(question.id) + '-' + str(answer.id))
#                     answer.body = answer_body
#                     answer_correct = request.POST.get('answer-correct-' + str(question.id) + '-' + str(answer.id))
#                     if answer_correct == 'on':
#                         answer.correct = True
#                     else:
#                         answer.correct = False
#                     answer.save()
#             question.save()

#         quiz.save()

#         return redirect('/quiz/%d'%quiz.id)

#     context = {'quiz': quiz, 'questions': questions, 'answers': answers, 'number_of_questions': range(number_of_questions)}

#     return render(request, 'quiz-edit.html', context)

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

