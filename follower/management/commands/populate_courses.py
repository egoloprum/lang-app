import json
import string
import random
from faker import Faker
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

from course.models import Course, Content
from quiz.models import Quiz, Question, Answer

class Command(BaseCommand):
  help = "Populate courses from a JSON file"

  def handle(self, *args, **options):
    with open("data/sample_course.json", "r") as json_file:
      course_data = json.load(json_file)
      created_courses = []

      # course 
      for data in course_data:
        course_name = data['name']
        course_tag = data['tag']
        course_pts = data['pts']
        course_exp = data['exp']
        course_start = data['start_date']
        course_end = data['end_date']
        course_public = True if data['publication'] == 'True' else False
        course_contents = data['contents']
        course_quizs = data['quizs']

        try:
          hosts = User.objects.filter(is_superuser=True)
          host = hosts[random.randint(0, len(hosts) - 1)]

        except User.DoesNotExist:
          host = User.objects.get_or_create(username='admin', password='admin', 
                                      is_superuser=True, is_staff=True, is_active=True)

        fake = Faker()
        Faker.seed(0)

        fake_body = []
        course_body = ''

        for _ in range(random.randint(7, 14)):
          fake_body.append(fake.sentences())

        for data in fake_body:
          for body in data:
            course_body += body + ' '

        try:
          course = Course.objects.get(name=course_name)
          course.delete()

          course, created = Course.objects.get_or_create(
            name=course_name, body=course_body, pts=course_pts, exp=course_exp, start_date=course_start,
            end_date=course_end, publication=course_public, host=host, tag=course_tag
          )

        except Course.DoesNotExist:
          course, created = Course.objects.get_or_create(
            name=course_name, body=course_body, pts=course_pts, exp=course_exp, start_date=course_start,
            end_date=course_end, publication=course_public, host=host, tag=course_tag
          )

        if created:
          self.stdout.write(
            self.style.SUCCESS(f"Created course: {course.name}")
          )
          created_courses.append(course.name)

        else:
          self.stdout.write(
            self.style.WARNING(f"Course already exists: {course.name}")
          )
        
        created_contents = []
        created_course_quizs = []

        # course contents
        for content in course_contents:
          content_name = content['name']
          content_public = True if content['publication'] == 'True' else False
          content_quiz = content['quizs']

          fake = Faker()
          Faker.seed(0)

          fake_body = []
          content_body = ''

          for _ in range(random.randint(7, 14)):
            fake_body.append(fake.sentences())

          for data in fake_body:
            for body in data:
              content_body += body + ' '

          content, created = Content.objects.get_or_create(
            course=course, name=content_name, body=content_body, publication=content_public
          )

          if created:
            self.stdout.write(
              self.style.SUCCESS(f"Created content: {content.name}")
            )
            created_contents.append(content.name)

          else:
            self.stdout.write(
              self.style.WARNING(f"Content already exists: {content.name}")
            )

          created_quizs = []

          # content quizs
          for data in content_quiz:
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
          
            quiz, created = Quiz.objects.get_or_create(
              name=quiz_name, duration=quiz_duration, start_date=quiz_start,
              end_date=quiz_end, required_score=quiz_score, difficulty=quiz_difficulty,
              pts=quiz_points, exp=quiz_exp, publication=quiz_public, host=host, content=content
            )

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
        
        self.stdout.write(
          self.style.SUCCESS(f"Successfully populated {len(created_contents)} contents")
        )

        for quiz in course_quizs:
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

          quiz, created = Quiz.objects.get_or_create(
            name=quiz_name, duration=quiz_duration, start_date=quiz_start,
            end_date=quiz_end, required_score=quiz_score, difficulty=quiz_difficulty,
            pts=quiz_points, exp=quiz_exp, publication=quiz_public, host=host, course=course
          )

          if created:
            self.stdout.write(
              self.style.SUCCESS(f"Created course quiz: {quiz.name}")
            )
            created_quizs.append(quiz.name)

          else:
            self.stdout.write(
              self.style.WARNING(f"Course quiz already exists: {quiz.name}")
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
                self.style.SUCCESS(f"Created course question: {question.id}")
                )
              created_questions.append(question.id)

            else:
              self.stdout.write(
                self.style.WARNING(f"Course question already exists: {question.id}")
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
                  self.style.SUCCESS(f"Created course answer: {answer.id}")
                  )
                created_answers.append(answer.id)

              else:
                self.stdout.write(
                  self.style.WARNING(f"Course answer already exists: {answer.id}")
                )

            self.stdout.write(
              self.style.SUCCESS(f"Successfully populated {len(created_answers)} answers")
            )

          self.stdout.write(
            self.style.SUCCESS(f"Successfully populated {len(created_questions)} questions")
          )

        self.stdout.write(
          self.style.SUCCESS(f"Successfully populated {len(created_course_quizs)} quizs")
        )

      self.stdout.write(
        self.style.SUCCESS(f"Successfully populated {len(created_courses)} courses")
      )
