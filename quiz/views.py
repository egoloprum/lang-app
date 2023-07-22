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
        quiz_number_of_question = request.POST.get('quiz-number-of-question')
        quiz_required_score = request.POST.get('quiz-required-score')
        quiz_difficulty = request.POST.get('quiz-difficulty')

        if quiz_duration:
            quiz = Quiz.objects.create(name=quiz_name, duration=quiz_duration, difficulty=quiz_difficulty,
                                       number_of_questions=quiz_number_of_question, host=request.user,
                                       required_score=quiz_required_score)
        else:
            quiz = Quiz.objects.create(name=quiz_name, host=request.user, required_score=quiz_required_score,
                                       difficulty=quiz_difficulty, number_of_questions=quiz_number_of_question)

        x = 1
        
        while(True):
            if request.POST.get('question-body-' + str(x)):
                question_body = request.POST.get('question-body-' + str(x))
                question = Question.objects.create(body=question_body, quiz=quiz)
                x += 1
            else:
                break
        

        # while(True):
        #     if request.POST.get('question-body-' + str(x)):
        #         question_body = request.POST.get('question-body-' + str(x))
        #         question = Question.objects.create(body=question_body, quiz=quiz)
        #         while(True):
        #             if request.POST.get('answer-body-' + str(y)):
        #                 answer_body = request.POST.get('answer-body-' + str(x) + '-' + str(y))
        #                 answer_correct = request.POST.get('answer-correct-' + str(x) + '-' + str(y))
        #                 answer = Answer.objects.create(body=answer_body, correct=answer_correct, question=question)
        #                 y += 1
        #             else:
        #                 break
        #         x += 1
        #     else:
        #         break

        return redirect('quiz')

    context = {}
    return render(request, 'quiz-create.html', context)
