from datetime import timedelta
from django.http import HttpResponse

def cookie_expire(time: float) -> float:
    expires = timedelta(days=time).total_seconds()
    return expires

class ThemeMiddleware:
    """
    Middleware odpowiedzialny za ustawianie domyślnego motywu (ciemny lub jasny) dla użytkownika na podstawie ciasteczka.
    Jeśli ciasteczko 'theme' nie istnieje, ustawia je na wartość 'light' przez określony czas (7 dni domyślnie).
    """
    def __init__(self, get_response):   # Konstrutktor middleware
        self.get_response = get_response

    def __call__(self, request):    # Wywołanie przy żądaniu 
        if not request.COOKIES.get('theme'):
            response = self.get_response(request)
            response.set_cookie('theme', 'light', cookie_expire(7))
            return response
        return self.get_response(request)