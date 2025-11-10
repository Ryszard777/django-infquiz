from django.urls import path
from hello import views

urlpatterns = [
    path("", views.home, name="home"),
    path("learn/", views.learn, name="learn"),
    path("contact/", views.contact, name="contact"),
    path("inf02/", views.inf02, name="inf02"),
    path("inf03/", views.inf03, name="inf03"),
    path("inf04/", views.inf04, name="inf04"),
    path("egzamin/40_pytan/<str:category>", views.pick_40_questions, name="40_questions"),
    path("egzamin/wszystkie_pytania/<str:category>", views.pick_all_questions, name="all_questions"),
    path("egzamin/wyniki/<str:category>/", views.results_view, name="results"),
]