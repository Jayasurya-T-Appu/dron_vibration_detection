from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import os
import joblib
from .forms import SensorInputForm

# Load trained model dynamically
model_path = os.path.join(os.path.dirname(__file__), "models", "random_forest_model.pkl")
model = joblib.load(model_path)

# Predict Drone Fault
@csrf_exempt  
def predict_fault(request):
    prediction = None
    safety_status = None

    if request.method == "POST":
        form = SensorInputForm(request.POST)
        if form.is_valid():
            # Extract sensor values
            sensor_values = [
                form.cleaned_data["sensor_a"],
                form.cleaned_data["sensor_b"],
                form.cleaned_data["sensor_c"],
                form.cleaned_data["sensor_d"],
            ]

            # Make prediction
            prediction = model.predict([sensor_values])[0]

            # Determine safety status
            if prediction < 0.4:
                safety_status = "✅ Safe"
            elif 0.4 <= prediction < 0.65:
                safety_status = "⚠️ Partially Safe"
            else:
                safety_status = "❌ Not Safe"
    else:
        form = SensorInputForm()

    return render(request, "predict_form.html", {"form": form, "prediction": prediction, "safety_status": safety_status})

# Render Register Page
def register_page(request):
    return render(request, "register.html")

# Render Login Page
def login_page(request):
    return render(request, "login.html")

# Register API
@csrf_exempt  
def register(request):
    if request.method == "POST":
        try:
            
            username =request.POST.get("username")
            email = request.POST.get("email")
            password = request.POST.get("password")
            password2 = request.POST.get("password2")

            if password != password2:
                messages.error(request, "Passwords do not match.")
                return redirect('register_page')
            
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already taken.")
                return redirect('register_page')
            
            User.objects.create_user(username=username, email=email, password=password)
            messages.error(request, "User registered Succesfully")
            return redirect('login_page')
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method. Use POST."}, status=400)

# Login API
@csrf_exempt
def login(request):
    if request.method == "POST":
        try:
            username = request.POST.get("username")
            password = request.POST.get("password")
            
            user = authenticate(username=username, password=password)

            if user:
                auth_login(request, user)
                return redirect('predict_form')
            else:
                messages.error(request, "Invalid username or password.")
                return redirect('login_page')
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method. Use POST."}, status=400)

# Logout API
def logout(request):
    auth_logout(request)
    return redirect('login_page')
