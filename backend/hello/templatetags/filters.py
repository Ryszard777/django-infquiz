from django import template
from typing import Any
register = template.Library()

@register.filter
def get_answer(answers: dict, key: int):
    try:
        answer = answers[str(key)]['userAnswer']
        return answer
    except (IndexError, ValueError, TypeError):
        return None
    
@register.filter
def calculate_score(score:int ,question_amount: int) -> str:
    try:
        result = round((int(score)*100)/int(question_amount), 1)
        return str(result).removesuffix('.0')
    except(ValueError, TypeError, ZeroDivisionError):
        return None
    
@register.filter
def get_cookie(request, cookie_name: str) -> Any:
    return request.COOKIES.get(cookie_name)

@register.filter
def name_without_space(name):
    returned_value = str(name)
    return returned_value.replace(' ', '-')