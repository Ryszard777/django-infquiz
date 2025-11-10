from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import CheckConstraint, Q
from datetime import datetime

QUESTION_TYPES = [
    ('INF 02', 'INF 02'),
    ('INF 03', 'INF 03'),
    ('INF 04', 'INF 04'),
]

# Create your models here.
class QuestionTypes(models.Model):
    """
    Model reprezentujący typy pytań egzaminacyjnych (np. INF 02, INF 03, INF 04).
    Zawiera listę dostępnych typów pytań.
    """
    question_type = models.CharField(
        choices=QUESTION_TYPES,
        max_length=10,
        default='INF 03'
    )

    def __str__(self):
        return self.question_type

class Questions(models.Model):
    """
    Model reprezentujący pytania egzaminacyjne.
    Zawiera pytanie, odpowiedzi oraz typ pytania (powiązany z `QuestionTypes`).
    """
    question = models.TextField()
    answer_a = models.TextField()
    answer_b = models.TextField()
    answer_c = models.TextField()
    answer_d = models.TextField()
    answer_correct = models.CharField(max_length=1)
    img = models.TextField()
    question_type = models.ForeignKey(QuestionTypes, on_delete=models.PROTECT)

    class Meta:
        indexes = [
            models.Index(fields=['id', 'question_type']),
            models.Index(fields=['question_type'])
        ]

    def __str__(self):
        return self.question

class Scores(models.Model):
    """
    Model reprezentujący wynik egzaminu.
    Zawiera wynik, datę egzaminu, liczbę pytań, oraz typ egzaminu.
    """
    score = models.FloatField(validators=[MaxValueValidator(100), MinValueValidator(0)])
    exam_date = models.DateTimeField(auto_now_add=True)
    class Meta:
        constraints = (
            CheckConstraint(
                check=Q(score__gte=0) & Q(score__lte=100),
                name='scores_score_range'
            ),
        )

        indexes = [
            models.Index(fields=['exam_type'])
        ]

    exam_type = models.ForeignKey(QuestionTypes, on_delete=models.PROTECT)
    amount_of_questions = models.IntegerField(default=40)

    def __str__(self):
        return float(self.score)
