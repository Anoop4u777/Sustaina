from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect


from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"] 
        password = request.POST["password"]
        existing_user = authenticate(request=request, username=username, password=password)
        if existing_user:
            login(request, existing_user)
            print("Logged In !!!")
            return redirect('/')
    return render(request, "auth/login.html", {})

def register_view(request):
    if request.method == "POST":
        username = request.POST["username"] 
        email = request.POST["email"] 
        password = request.POST["password"]
        try:
            new_user = User.objects.create_user(username=username, email=email, password=password)
            if new_user:
                login(request, new_user)
                print("Logged In !!!")
                return redirect('/')
        except:
            pass
    return render(request, "auth/register.html", {})