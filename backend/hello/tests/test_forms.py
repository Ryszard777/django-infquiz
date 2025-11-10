from django.test import TestCase
from hello.forms import QuestionFormAll, QuestionForm_40
from hello.models import Questions, QuestionTypes

class QuestionFormTests(TestCase):
    def setUp(self):
        self.category = QuestionTypes.objects.create(question_type="INF 02")
        for i in range(50):
            Questions.objects.create(
                question=f"Question {i}",
                answer_a="A",
                answer_b="B",
                answer_c="C",
                answer_d="D",
                answer_correct="A",
                img="",
                question_type=self.category
            )

    def test_form_all_generates_fields(self):
        form = QuestionFormAll(category="INF 02")
        self.assertTrue(len(form.fields) >= 1)
        first_field = list(form.fields.keys())[0]
        self.assertTrue(first_field.startswith("question_"))

    def test_form_40_requires_enough_questions(self):
        ids = list(Questions.objects.values_list("id", flat=True))[:40]
        form = QuestionForm_40(category="INF 02", selected_question_ids=ids)
        self.assertEqual(len(form.fields), 40)

    def test_form_40_raises_if_too_few_questions(self):
        with self.assertRaises(ValueError):
            QuestionForm_40(category="INF 02", selected_question_ids=[1, 2])