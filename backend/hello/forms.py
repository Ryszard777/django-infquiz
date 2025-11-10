from django import forms
from .models import Questions
from random import shuffle

class QuestionFormAll(forms.Form):
    """
    Formularz do obsługi wszystkich pytań z wybranej kategorii.
    Formuje pola formularza na podstawie pytań z bazy danych związanych z określoną kategorią.
    """
    def __init__(self, *args, category=None, **kwargs):
        super().__init__(*args, **kwargs)   # Wywołanie konstruktora klasy

        if category is None:    # Jeśli kategoria nie została wybrana, zwróć błąd
            raise ValueError("Kategoria jest wymagana")
        
        allQuestions = Questions.objects.filter(question_type__question_type = category)
        if len(allQuestions) <= 0:      # Jeśli nie udało się znaleźć żadnych pytań, zwróć błąd
            raise RuntimeError("Nie udało się załadować pytań")
        
        for question in sorted(allQuestions, key=lambda q: q.id):   # Dla każdego pytania z tej kategorii, dodaj pole do formularza
            field_name = f"question_{question.id}"  # Tworzenie unikalnej nazwy pola w formularzu
            choices = [
                    ('A', question.answer_a),
                    ('B', question.answer_b),
                    ('C', question.answer_c),
                    ('D', question.answer_d)]
            
            self.fields[field_name] = forms.ChoiceField(    # Dodanie pola wyboru (RadioSelect) do formularza
                    help_text=question.id,          # Dodanie ID pytania w formie help_text
                    label=question.question,        # Tekst pytania wyświetlany w formularzu
                    choices=choices,                # Dostępne odpowiedzi
                    widget=forms.RadioSelect,       # Użycie widgetu do wyświetlania jako radio buttons
                    required=True)                  # Pole jest wymagane do wypełnienia
            
class QuestionForm_40(forms.Form):
    """
    Formularz do obsługi 40 pytań wybranych losowo na podstawie kategorii.
    Formuje pola formularza na podstawie pytań, które zostały losowo wybrane.
    """
    def __init__(self, *args, category=None, selected_question_ids=None, **kwargs):
        super().__init__(*args, **kwargs)

        if category is None:
            raise ValueError("Kategoria jest wymagana")
        
        if selected_question_ids is None or len(selected_question_ids) < 40:
            raise ValueError("Błąd: Nie znaleziono wystarczającej liczby pytań.")
        
        allQuestions = Questions.objects.filter(id__in=selected_question_ids)   # Pobieranie pytań na podstawie przekazanych id

        for question in sorted(allQuestions, key=lambda q: q.id):
            field_name = f"question_{question.id}"
            choices = [
                    ('A', question.answer_a),
                    ('B', question.answer_b),
                    ('C', question.answer_c),
                    ('D', question.answer_d)]
            
            self.fields[field_name] = forms.ChoiceField(
                    help_text=question.id,
                    label=question.question,
                    choices=choices,
                    widget=forms.RadioSelect,
                    required=True)

