from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages


def sign_up(request):
    """The function checks if a user with similar data does not already exist,
    if not creating a new user."""

    if request.method == "POST":
        username = request.POST["username"]

        if User.objects.filter(username=username).exists():
            messages.error(
                request,
                "User with given username already exists, use another username.",
            )
            return render(request, "registration/sign_up.html")

        email = request.POST["email"]

        if User.objects.filter(email=email).exists():
            messages.error(
                request,
                "User with given emails already exists, use another email address.",
            )
            return render(request, "registration/sign_up.html")

        password_1 = request.POST["pass1"]
        password_2 = request.POST["pass2"]

        if password_1 != password_2:
            messages.error(
                request,
                """Verification of your passwords failed because the passwords are different.
                Try re-entering passwords.""",
            )
            return render(request, "registration/sign_up.html")

        my_user = User.objects.create_user(username, email, password_1)

        my_user.save()

        messages.success(request, "Your account has been successfully created.")

        return redirect("home")

    return render(request, "registration/sign_up.html")
