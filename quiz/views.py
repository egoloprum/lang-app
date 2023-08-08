from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist 
from django.contrib import messages
# Create your views here.

@login_required(login_url='login')
def quiz(request):

    data = [{
        'id': 1,
    }]
    # return JsonResponse(data, safe=False)

    q = request.GET.get('q') if request.GET.get('q') != None else ''

    difficulties = []

    for quiz in Quiz.objects.all():
        difficulties.append(quiz.difficulty.lower())

    difficulties = list(dict.fromkeys(difficulties))
    sort_diff = ['a', 'e', 'i',]

    difficulties.sort(key = lambda i: sort_diff.index(i[0]))     

    if request.method == 'POST':
        quiz_id = Quiz.objects.get(pk=request.POST.get('quiz-id'))
        quiz_id.delete()
    
    count = Quiz.objects.annotate(child_count = models.Count('question_quiz')).filter(difficulty__icontains=q)

    context = {'quizs': count, 'difficulties': difficulties}
    return render(request, 'quiz.html', context)

@login_required(login_url='login')
def quizCreate(request):
    if request.method == 'POST':
        quiz_name = request.POST.get('quiz-name')
        quiz_duration = request.POST.get('quiz-duration')
        quiz_required_score = request.POST.get('quiz-required-score')
        quiz_difficulty = request.POST.get('quiz-difficulty')

            
        quiz = Quiz.objects.create(name=quiz_name, duration=quiz_duration, difficulty=quiz_difficulty,
                                        host=request.user, required_score=quiz_required_score)

        x = 1

        while(request.POST.get('question-body-' + str(x))):
            question_body = request.POST.get('question-body-' + str(x))
            question = Question.objects.create(body=question_body, quiz=quiz)

            y = 1

            while(request.POST.get('answer-body-' + str(x) + '-' + str(y))):
                answer_body = request.POST.get('answer-body-' + str(x) + '-' + str(y))
                answer_correct = False

                if request.POST.get('answer-correct-' + str(x) + '-' + str(y)) == 'on':
                    answer_correct = True
                else:
                    answer_correct = False

                answer = Answer.objects.create(body=answer_body, correct=answer_correct, question=question)

                y += 1

            x += 1

        return redirect('quiz')

    context = {}
    return render(request, 'quiz-create.html', context)

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
    questions = Question.objects.filter(quiz=quiz)
    number_of_questions = len(questions)
    answers = []
    answers_correct_num = []

    for question in questions:
        count = 0
        for a in Answer.objects.filter(question=question).select_related('question'):
            answers.append(a)
            if a.correct is True:
                count += 1
        
        answers_correct_num.append(count)

    context = {'quiz': quiz, 'questions': questions, 'answers': answers, 'number_of_questions': range(number_of_questions)}

    if request.method == 'POST':
        quiz_answers = []
        result = 0

        for answer in answers:
            if request.POST.get('answer-' + str(answer.id)) == 'on':
                quiz_answers.append(True)
                Selected_Answer.objects.create(answer=answer, correct=True)
            else:
                quiz_answers.append("")
                Selected_Answer.objects.create(answer=answer, correct=False)
    
        temp_quiz = quiz_answers.copy()
        temp_answers = answers.copy()
        length_answers = len(answers_correct_num)

        for question in questions:
            count = 0
            for n in range(len(question.get_answers())):
                if temp_answers[n].correct is temp_quiz[n]:
                    count += 1

            for n in range(len(question.get_answers())):
                temp_quiz.pop(0)
                temp_answers.pop(0)

            try:
                result += count / answers_correct_num[0]
            except ZeroDivisionError:
                result = result

            answers_correct_num.pop(0)
        
        result = (result / length_answers) * 100

        quiz_result = Result.objects.create(quiz=quiz, user=request.user, score=result)

        return redirect('quiz-result', quiz.id)

    return render(request, 'quiz-each.html', context)

@login_required(login_url='login')
def quizEdit(request, pk):
    quiz = Quiz.objects.get(id=pk)
    questions = Question.objects.filter(quiz=quiz)
    number_of_questions = len(questions)
    answers = []

    for question in questions:
        for a in Answer.objects.filter(question=question).select_related('question'):
            answers.append(a)

    if request.method == "POST":
        quiz_name = request.POST.get('quiz-name')
        quiz_duration = request.POST.get('quiz-duration')
        quiz_required = request.POST.get('quiz-required')
        quiz_diff = request.POST.get('quiz-difficulty')

        quiz.name = quiz_name
        if quiz_duration:
            quiz.duration = quiz_duration
        if quiz_required:
            quiz.required_score = quiz_required
        if quiz_diff:
            quiz.difficulty = quiz_diff

        for question in questions:
            question_body = request.POST.get('question-body-' + str(question.id))
            question.body = question_body

            for answer in answers:
                if answer.question.id == question.id:
                    answer_body = request.POST.get('answer-body-' + str(question.id) + '-' + str(answer.id))
                    answer.body = answer_body
                    answer_correct = request.POST.get('answer-correct-' + str(question.id) + '-' + str(answer.id))
                    if answer_correct == 'on':
                        answer.correct = True
                    else:
                        answer.correct = False
                    answer.save()
            question.save()

        quiz.save()

        return redirect('/quiz/%d'%quiz.id)

    context = {'quiz': quiz, 'questions': questions, 'answers': answers, 'number_of_questions': range(number_of_questions)}

    return render(request, 'quiz-edit.html', context)

@login_required(login_url='login')
def quizResult(request, pk):
    quiz = Quiz.objects.get(id=pk)
    result = Result.objects.select_related('quiz').filter(quiz=quiz).last
    results = Result.objects.select_related('quiz').filter(quiz=quiz).order_by('-id')
    questions = Question.objects.select_related('quiz').filter(quiz=quiz)
    answers = []
    selected_answers = []

    for question in questions:
        for a in Answer.objects.filter(question=question).select_related('question'):
            answers.append(a)
            try:
                selected_answers.append(Selected_Answer.objects.select_related('answer').filter(answer=a).last)
                # Selected_Answer.objects.get(answer=a).delete()
            except ObjectDoesNotExist:
                ...

    list_answers = dict(zip(answers, selected_answers))
    average_score = 0

    for res in results:
        average_score += res.score

    try:
        average_score = average_score / len(results)
    except ZeroDivisionError:
        average_score = 0

    if Average_score.objects.filter(quiz=quiz, user=request.user).exists:
        Average_score.objects.filter(quiz=quiz, user=request.user).delete()

    Average_score.objects.create(quiz=quiz, user=request.user, score=average_score)

    context = {'result': result, 'results': results, 'average_score': average_score,
               'quiz': quiz, 'questions': questions, 'answers': list_answers, 'ans': answers}

    return render(request, 'quiz-result.html', context)

