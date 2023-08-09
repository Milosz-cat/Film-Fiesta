from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def choose_list(request):
    # Render the template with the context
    return render(request, "list_management/choose_list.html")
