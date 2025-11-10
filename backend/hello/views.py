from django.views.decorators.cache import never_cache
from django.utils.timezone import datetime
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db.models import Q
from django import forms
from .forms import QuestionFormAll, QuestionForm_40
from .models import Questions, Scores, QuestionTypes
from random import shuffle
from typing import Any
from datetime import timedelta

EXAM_TYPES: list[str] = QuestionTypes.objects.all().values_list('question_type', flat=True)

def possible_zero_division_average(num1: float, num2: int) -> float:
    """
    Funkcja oblicza iloraz num1 i num2. 
    Jeśli num2 wynosi 0, zamiast rzucać wyjątek, funkcja zwróci 0.
    
    :param num1: Pierwsza liczba (float), dzielnik.
    :param num2: Druga liczba (int), mianownik.
    :return: Wynik dzielenia num1 przez num2 lub 0, jeśli wystąpi błąd dzielenia przez zero.
    """
    try:
        return num1/num2
    except ZeroDivisionError:
        return 0

def render_error(request, message):
    """ Pomocnicza funkcja do renderowania strony błędu. """
    return render(request, 'hello/error_handler.html', {'error': message})

def form_validation(request, category: str, form_type: forms.Form) -> tuple[bool, dict | str]:
    """
    Funkcja walidująca formularz na podstawie typu formularza i danych z requestu.
    Jeśli formularz jest poprawny, zwraca True i słownik odpowiedzi, w przeciwnym razie
    zwraca False i błędy formularza.
    """
    selected_question_ids: list[str] = request.session.get('selected_questions', []) # # Pobieranie id, które zostały losowo wybrane do formularza
    if form_type == QuestionFormAll:    # W zależności od typu formularza, tworzy odpowiedni obiekt formularza
        form: forms.Form = form_type(request.POST, category=category)
    else:
        if not selected_question_ids:
            selected_question_ids: list[str] = [key.split("_")[1] for key in request.POST.keys() if key.startswith("question_")] # W html input[radio] są nazwane question_ID dlatego zostawiamy tylko część z id
        form: forms.Form = form_type(request.POST, category=category, selected_question_ids=selected_question_ids)

    if form.is_valid():
        cleaned: dict[str, Any] = form.cleaned_data
        answers: dict[str, Any] = {
            key.split("_")[1]: value
            for key, value in cleaned.items()
            if key.startswith("question_")
        }

        return True, answers # Przekazuje czy udało się zweryfikować formularz oraz odpowiedzi użytkownika
            
    return False, form.errors

@never_cache
def pick_40_questions(request, category=None):
    """
    Funkcja wybiera 40 pytań na podstawie wybranej kategorii i wyświetla formularz.
    Obsługuje zarówno walidację formularza, jak i generowanie pytań.
    """
    if category not in EXAM_TYPES:
        return render_error(request, 'Wybrano złą kategorię')

    
    if request.method == "POST":     # Jeśli dane zostały przesłane metodą POST, funckja przechodzi do walidacji formularza
            is_valid: bool
            answers: dict[str, Any]
            is_valid, answers = form_validation(request=request, category=category, form_type=QuestionForm_40)
            if is_valid:
                return results_questions(postData=answers, request=request, category=category)      # Zapis oraz pokazywanie wyników 
            else:
                return render_error(request, 'Formularz nie przeszedł walidacji oraz wynik nie został zapisany')
        
    random_questions: list[int] = list(Questions.objects.filter(question_type__question_type=category).values_list('id', flat=True))    # Pobranie wszystkich pytań z danej kategorii
    
    if len(random_questions) < 40:
        return render_error(request, 'Nie udało się zebrać 40 pytań. Błąd zbierania pytań')    # Jeśli nie uda się zebrać 40 pytań zwraca błąd
    
    shuffle(random_questions)   #  Mieszamy pytania
    selected_question_ids: list[int] = random_questions[:40]    # Z listy losowo wybranych pytań wybieramy pierwsze 40

    request.session['selected_questions'] = selected_question_ids
    images: list[int] = Questions.objects.filter(~Q(img = ''), id__in=selected_question_ids).values_list('id',flat=True)    # Pobiera odpowiednie obrazy z bazy danych
    form: forms.Form = QuestionForm_40(category=category, selected_question_ids=selected_question_ids)
    data: dict = {
        'form': form,
        'img': images,
        'category': category.lower().replace(' ','')
    }
    return render(request, "hello/40_questions.html", data)     # Zwracamy stronę z formularzem

@never_cache
def pick_all_questions(request, category=None):
    """
    Funkcja wybiera wszystkie pytania z wybranej kategorii i wyświetla formularz.
    """
    if category not in EXAM_TYPES:
        return render_error(request, 'Wybrano złą kategorie')

    if request.method == "POST":    # Jeśli dane zostały przesłane metodą POST, funckja przechodzi do walidacji formularza
            is_valid: bool
            answers: dict[str, Any]
            is_valid, answers = form_validation(request=request, category=category, form_type=QuestionFormAll)
            if is_valid:
                return results_questions(postData=answers, request=request, category=category)  # Zapis oraz pokazywanie wyników 
            else:
                return render_error(request, 'Formularz nie przeszedł walidacji oraz wynik nie został zapisany')
    form: forms.Form = QuestionFormAll(category=category)   # Tworzenie formularza dla wybranej kategorii
    images = Questions.objects.filter(~Q(img = '')).values_list('id',flat=True)
    data: dict = {
        'form': form,
        'img': images,
        'category': category.lower().replace(' ','')
    }
    return render(request, "hello/all_questions.html", data)

def results_questions(postData, request, category: str):
    """
    Funkcja przetwarza odpowiedzi użytkownika, porównuje je z poprawnymi odpowiedziami,
    zapisuje wynik i przekazuje dane do widoku wyników.
    """
    questions: list[str] = [key for key in postData]
    exam_questions: list[dict[str, Any]] = list(Questions.objects.filter(id__in=questions).values())
    correct_dict: dict[str, Any] = {item['id']: item['answer_correct'] for item in exam_questions}
    correct: int = 0
    answers:dict[int, Any] = {}

    for key, value in postData.items():
        if key.startswith("csrf"):      # Pomijamy token csrf
            continue

        user_answer: str = value
        correct_answer: str = correct_dict.get(int(key))
        answers[int(key)] = {'userAnswer' : user_answer}
        if user_answer == correct_answer:
            correct += 1

    try:
        question_type_fk = QuestionTypes.objects.get(question_type=category)
    except ObjectDoesNotExist:
        return render_error(request, f'Nie znaleziono typu egzaminu: {category}')
    except MultipleObjectsReturned:
        return render_error(request, f'Znaleziono więcej niż jeden egzamin dla typu: {category}')
    
    exam_score: Scores = Scores(score=round((correct*100)/len(correct_dict),1), exam_type=question_type_fk, amount_of_questions=len(correct_dict))
    try:        # Próbujemy zapisa wynik i informacje o egzaminie do bazy danych
        exam_score.save()
    except Exception as e:
        return render_error(request, f'Błąd podczas zapisywania wyniku')
    
    request.session.pop('selected_questions', None)

    request.session['data'] = {         # Zapisujemy dane w sesji
        'score' : correct, 
        "questions" : exam_questions, 
        "answers" : answers, 
        "amount" : len(questions)
    }
    """  
    Przekierowujemy użytkownika na stronę z wynikami, dlatego dane są zapisane w sesji ponieważ z redirect nie możemy przekazywać danych.
    Oraz dzięki temu działamy według wzorca Post/Redirect/Get dzięki czemu użytkownik po odświeżeniu czy cofnięciu nie dodaje ciągle tego samego testu.
    Test zostaje dodany tylko raz.
    """
    return redirect('results', category)

def results_view(request, category=None):
    """
    Funkcja wyświetla wyniki egzaminu po jego zakończeniu, pokazując pytania, odpowiedzi użytkownika
    oraz punktację.
    """
    
    exam_data = request.session.get('data', None)   # Pobieramy dane zapisane w sesji po zakończeniu egzaminu

    if exam_data is None:
        return render_error(request, 'Brak danych do wyświetlenia wyników') # Jeśli dane nie są zapisane, zwracamy błąd

    score = exam_data['score']
    questions = exam_data['questions']
    answers = exam_data['answers']
    amount = exam_data['amount']

    context = {
        'score': score,
        'questions': questions,
        'answers': answers,
        'amount': amount,
        'category': category.lower().replace(' ',''),
    }

    return render(request, 'hello/questions_results.html', context)

def home(request):
    """
    Funkcja wyświetlająca stronę główną z danymi dotyczącymi wyników egzaminów.
    """
    types = QuestionTypes.objects.values('question_type')
    scores_from_last_week: list[float] = []
    scores_from_today: list[float] = []
    scores_all: list[float] = []

    try:
        if request.method == 'POST':    # Jeśli dane zostały przez POST (czyli użytkownik zastosował filtr), sprawdzamy jakie filtru zastosował
            filter_type = request.POST.get('filter')    # Zmienna filter przyjmuje wartości z tabeli QuestionTypes
            if filter_type == 'none':
                scores = Scores.objects.all()
            elif filter_type in EXAM_TYPES:
                scores = Scores.objects.filter(exam_type__question_type=filter_type)
            else:
                scores = Scores.objects.all()
        else:
            scores = Scores.objects.all()

        for score in scores:        # Przyporządkowanie wyników do trzech kategorii: dzisiaj, w ciągu ostatniego tygodnia i wszystkie wyniki”
            time_diff = datetime.now().astimezone() - score.exam_date
            if time_diff <= timedelta(weeks=1):
                scores_from_last_week.append(score.score)
            if time_diff <= timedelta(days=1):
                scores_from_today.append(score.score)
            scores_all.append(score.score)
    except Exception as e:
        return render_error(request, f'Błąd podczas przetwarzania wyników')

    data: dict = {
        'scores': scores, 
        'types': types, 
        'average_today': round(possible_zero_division_average(sum(scores_from_today), len(scores_from_today)),1), 
        'average_week': round(possible_zero_division_average(sum(scores_from_last_week), len(scores_from_last_week)),1),    # Średnie wyniki
        'average_all': round(possible_zero_division_average(sum(scores_all), len(scores_all)),1)
    }
    return render(request, "hello/index.html", data)

def learn(request):
    """ Funkcja wyświetlająca stronę z materiałami do nauki. """
    return render(request, "hello/learn.html")

def contact(request):
    """ Funkcja wyświetlająca stronę kontaktową. """
    return render(request, "hello/contact.html")

def inf_site(request, exam_type):
    """
    Funkcja wyświetla stronę z informacjami o egzaminie na podstawie podanego typu egzaminu.
    Na podstawie wartości argumentu `exam_type`, funkcja pobiera liczbę pytań
    związanych z danym egzaminem z bazy danych i renderuje odpowiednią stronę
    z informacjami o tym egzaminie.
    """
    category = exam_type.lower().replace(' ', '')
    amount = Questions.objects.filter(question_type__question_type = exam_type).count()
    return render(request, f"hello/{category}.html", {'amount': amount})

def inf02(request):
    """ Funkcja wyświetlająca strone z infromacjami oraz testami egzaminu INF 02. """
    return inf_site(request, 'INF 02')

def inf03(request):
    """ Funkcja wyświetlająca stronę z infromacjami oraz testami egzaminu INF 03. """
    return inf_site(request, 'INF 03')

def inf04(request):
    """ Funkcja wyświetlająca stronę z infromacjami oraz testami egzaminu INF 04. """
    return inf_site(request, 'INF 04')