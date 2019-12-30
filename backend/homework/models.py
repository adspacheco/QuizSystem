from django.db import models
from users.models import Teacher
from django.core.validators import MaxValueValidator, MinValueValidator

class Quiz(models.Model):
    title = models.CharField(max_length=180)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    

    def __str__(self):
        return self.title

class Question(models.Model):

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    questionNumber = models.PositiveIntegerField()
    content = models.CharField(max_length=400)
    correct_answer = models.PositiveIntegerField(default=1, validators=[
        MaxValueValidator(6),
        MinValueValidator(1)
    ])

    def __str__(self):
        return 'question {} for {}'.format(self.questionNumber, self.quiz.title )

class Choice(models.Model):
    text = models.CharField(max_length=200)
    choiceID = models.PositiveIntegerField(default=1, validators=[
        MaxValueValidator(6),
        MinValueValidator(1)
    ])

    question = models.ForeignKey(Question, on_delete=models.CASCADE)\

    def __str__(self):
        return  'Choice {} for question {} from {}'.format(self.choiceID, self.question.questionNumber, self.question.quiz.title)


