from django.shortcuts import render, redirect
from .models import *

# Create your views here.

def quiz(request):
    quizs = Quiz.objects.all()
    context = {'quizs': quizs}
    return render(request, 'quiz.html', context)

def quizCreate(request):

    if request.method == 'POST':
        quiz_name = request.POST.get('quiz-name')
        quiz_duration = request.POST.get('quiz-duration')
        quiz_required_score = request.POST.get('quiz-required-score')
        quiz_difficulty = request.POST.get('quiz-difficulty')

        if quiz_duration:
            quiz = Quiz.objects.create(name=quiz_name, duration=quiz_duration, difficulty=quiz_difficulty,
                                        host=request.user,required_score=quiz_required_score)
        else:
            quiz = Quiz.objects.create(name=quiz_name, host=request.user, required_score=quiz_required_score,
                                       difficulty=quiz_difficulty)

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

    for question in questions:
        for a in Answer.objects.filter(question=question):
            answers.append(a)

    context = {'quiz': quiz, 'questions': questions, 'answers': answers, 'number_of_questions': number_of_questions}

    return render(request, 'quiz-each.html', context)

