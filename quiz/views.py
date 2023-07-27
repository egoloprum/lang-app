from django.shortcuts import render, redirect
from .models import *
from django.http import HttpResponse, JsonResponse

# Create your views here.

def quiz(request):
    quizs = Quiz.objects.all()

    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if is_ajax:
        quiz = request.GET.get('quiz')
        num_of_question = Question.objects.filter(quiz=quiz).count

        data = [{
            'id': 1,
        }]
        return JsonResponse(data, safe=False)
    
    count = Quiz.objects.annotate(child_count = models.Count('question'))

    context = {'quizs': count}
    return render(request, 'quiz.html', context)

def quizCreate(request):

    if request.method == 'POST':
        quiz_name = request.POST.get('quiz-name')
        quiz_duration = request.POST.get('quiz-duration')
        quiz_required_score = request.POST.get('quiz-required-score')
        quiz_difficulty = request.POST.get('quiz-difficulty')

            
        quiz = Quiz.objects.create(name=quiz_name, duration=quiz_duration, difficulty=quiz_difficulty,
                                        host=request.user, required_score=quiz_required_score)

        x = 1
        y = 1

        while(request.POST.get('question-body-' + str(x))):
            question_body = request.POST.get('question-body-' + str(x))
            question = Question.objects.create(body=question_body, quiz=quiz)

            y = 1

            while(request.POST.get('answer-body-' + str(x) + '-' + str(y))):
                answer_body = request.POST.get('answer-body-' + str(x) + '-' + str(y))
                answer_correct = request.POST.get('answer-correct-' + str(x) + '-' + str(y))
                if answer_correct == 'on':
                    answer_correct = True
                else:
                    answer_correct = False
                answer = Answer.objects.create(body=answer_body, correct=answer_correct, question=question)

                y += 1

            x += 1

        return redirect('quiz')

    context = {}
    return render(request, 'quiz-create.html', context)

def quizEach(request, pk):
    quiz = Quiz.objects.get(id=pk)
    questions = Question.objects.filter(quiz=quiz)
    number_of_questions = len(questions)
    answers = []
    answers_correct_num = []

    for question in questions:
        count = 0
        for a in Answer.objects.filter(question=question):
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
            else:
                quiz_answers.append("")
    
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

            result += count / answers_correct_num[0];
            answers_correct_num.pop(0);

        
        result = (result / length_answers) * 100

        quiz_result = Result.objects.create(quiz=quiz, user=request.user, score=result)

        return redirect('quiz')

    return render(request, 'quiz-each.html', context)


def quizEdit(request, pk):
    quiz = Quiz.objects.get(id=pk)
    questions = Question.objects.filter(quiz=quiz)
    number_of_questions = len(questions)
    answers = []

    for question in questions:
        for a in Answer.objects.filter(question=question):
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
                    answer.save()
            question.save()

        quiz.save()

        return redirect('/quiz/%d'%quiz.id)

    context = {'quiz': quiz, 'questions': questions, 'answers': answers, 'number_of_questions': range(number_of_questions)}

    return render(request, 'quiz-edit.html', context)

