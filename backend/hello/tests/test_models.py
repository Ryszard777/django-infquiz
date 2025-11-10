from django.test import TestCase
from hello.models import QuestionTypes, Scores

class QuestionTypesTestCase(TestCase):
    def test_question_type_creation(self):
        question_type = QuestionTypes.objects.create(question_type='INF 02')
        
        self.assertEqual(question_type.question_type, 'INF 02')
        
    def test_question_type_str(self):
        question_type = QuestionTypes.objects.create(question_type='INF 03')
        
        self.assertEqual(str(question_type), 'INF 03')

class ScoresTestCase(TestCase):
    def setUp(self):
        self.question_type = QuestionTypes.objects.create(question_type='INF 02')

    def test_scores_creation(self):
        score = Scores.objects.create(
            score=85.5,
            exam_type=self.question_type,
            amount_of_questions=40
        )

        self.assertEqual(score.score, 85.5)
        self.assertEqual(score.exam_type, self.question_type)
        self.assertEqual(score.amount_of_questions, 40)

    def test_scores_score_range(self):
        with self.assertRaises(ValueError):
            Scores.objects.create(score=-5, exam_type=self.question_type, amount_of_questions=40)
        
        with self.assertRaises(ValueError):
            Scores.objects.create(score=105, exam_type=self.question_type, amount_of_questions=40)

    def test_scores_valid_score(self):
        score = Scores.objects.create(score=75, exam_type=self.question_type, amount_of_questions=40)
        self.assertEqual(score.score, 75)

    def test_scores_str(self):
        score = Scores.objects.create(score=95, exam_type=self.question_type, amount_of_questions=40)   
        self.assertEqual(score.score, 95.0)