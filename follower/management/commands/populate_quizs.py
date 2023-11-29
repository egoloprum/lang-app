import json
import string
import random
import datetime
from faker import Faker
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model

from quiz.models import Quiz, Question, Answer

class Command(BaseCommand):
  help = "Populate quizs from a JSON file"

  def handle(self, *args, **options):
    with open("data/sample_quiz.json", "r") as json_file:
      quiz_data = json.load(json_file)

      User = get_user_model()
      created_quizs = []

      for data in quiz_data:
        quiz_name = data['name']
        quiz_duration = data['duration']
        quiz_start = data['start_date']
        quiz_end = data['end_date']
        quiz_score = data['minimum']
        quiz_difficulty = data['difficulty']
        quiz_points = data['points']
        quiz_exp = data['experience']
        quiz_public = data['publication']
        quiz_questions = data['questions']

        try:
          hosts = User.objects.filter(is_staff=True)
          host = hosts[random.randint(0, len(hosts))]

        except User.DoesNotExist:
          host = User.objects.get_or_create(username='host', password=make_password('admin'), 
                                            is_staff=True, is_active=True)
          
        fake = Faker()

        try:
          Quiz.objects.get(name=quiz_name).delete() 
        except Quiz.DoesNotExist:
          ...

        quiz, created = Quiz.objects.get_or_create(
          name=quiz_name, duration=quiz_duration,
          required_score=quiz_score, difficulty=quiz_difficulty,
          pts=quiz_points, exp=quiz_exp, publication=quiz_public, host=host
        )

        quiz.start_date = fake.date_between(start_date=datetime.date(2023, 9, 1), end_date=datetime.date(2023, 12, 31))
        quiz.end_date = fake.date_between(start_date=quiz.start_date, end_date=datetime.date(2024, 1, 24))
        quiz.save()

        if created:
          self.stdout.write(
            self.style.SUCCESS(f"Created quiz: {quiz.name}")
          )
          created_quizs.append(quiz.name)

        else:
          self.stdout.write(
            self.style.WARNING(f"Quiz already exists: {quiz.name}")
          )

        created_questions = []
        for question in quiz_questions:
          question_body = question['body']
          question_explanation = question['explanation']
          question_answers = question['answers']

          question, created = Question.objects.get_or_create(
            body=question_body, explanation=question_explanation, quiz=quiz
          )

          if created:
            self.stdout.write(
              self.style.SUCCESS(f"Created question: {question.id}")
              )
            created_questions.append(question.id)

          else:
            self.stdout.write(
              self.style.WARNING(f"Question already exists: {question.id}")
            )

          created_answers = []
          for answer in question_answers:
            answer_body = answer['body']
            answer_correct = True if answer['correct'] == 'True' else False

            answer, created = Answer.objects.get_or_create(
              body=answer_body, correct=answer_correct, question=question
            )

            if created:
              self.stdout.write(
                self.style.SUCCESS(f"Created answer: {answer.id}")
                )
              created_answers.append(answer.id)

            else:
              self.stdout.write(
                self.style.WARNING(f"Answer already exists: {answer.id}")
              )

          self.stdout.write(
            self.style.SUCCESS(f"Successfully populated {len(created_answers)} answers")
          )

        self.stdout.write(
          self.style.SUCCESS(f"Successfully populated {len(created_questions)} questions")
        )

      self.stdout.write(
        self.style.SUCCESS(f"Successfully populated {len(created_quizs)} quizs")
      )
