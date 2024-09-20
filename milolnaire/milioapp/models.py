from django.db import models

# Create your models here.
class Questions(models.Model):
    LEVEL_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
        ('impossible', 'Impossible'),
    ]
    CORRECT_ANSWER = [
        ('answer_a', 'A'),
        ('answer_b', 'B'),
        ('answer_c', 'C'),
        ('answer_d', 'D'),
    ]
    QUESTION_TYPE = [
        ('esport', 'Esport'),
        ('game', 'Game'),
        ('lore', 'Lore'),
    ]
    question = models.TextField()
    answer_a = models.CharField(max_length=100)
    answer_b = models.CharField(max_length=100)
    answer_c = models.CharField(max_length=100)
    answer_d = models.CharField(max_length=100)
    level = models.CharField(max_length=100, choices=LEVEL_CHOICES, default='easy')
    correct_answer = models.CharField(max_length=100, choices=CORRECT_ANSWER, default='answer_a', null='false')
    question_type = models.CharField(max_length=100, choices=QUESTION_TYPE, default='game', null='false')

    image = models.FileField(upload_to="project_images/", blank=True)

class FriendAnswers(models.Model):
    ANSWER_TYPE = [
        ('certain', 'Certain'),
        ('not_sure', 'Not sure'),
        ('dont_know', 'IDK'),
    ]

    answer = models.TextField()
    answer_type = models.CharField(max_length=100, choices=ANSWER_TYPE, default='certain')
