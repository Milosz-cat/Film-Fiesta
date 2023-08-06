from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy


class MyLoginView(LoginView):
    template_name = "registration/login.html"  # Szablon logowania
    success_url = reverse_lazy(
        "home"
    )  # URL, na który użytkownik zostanie przekierowany po zalogowaniu
