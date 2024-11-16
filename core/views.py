from django.contrib.auth.decorators import login_required
from django.shortcuts import render , redirect
from django.contrib.auth import authenticate, login ,logout
from django.contrib import messages
from .models import CustomUser as User

@login_required
def index(request):
    context = {}
    return render(request,'index.html',context)


def signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if not email or not username or not password1 or not password2:
            messages.error(request, 'All fields are required.')
        elif password1 != password2:
            messages.error(request, 'Passwords do not match.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already in use.')
        else:
            # Create user
            user = User.objects.create_user(username=username, email=email, password=password1)
            login(request, user)
            messages.success(request, 'Welcome to our platform! 🎉')
            return redirect('core:index')

    return render(request, 'signup.html')


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Welcome User ')
            # Get the next URL from the request
            # next_url = request.POST.get('next') or request.GET.get('next') or '/'
            return redirect('core:index')
        else:
            messages.error(request, 'Invalid Password or Username')

            return render(request, 'login.html', {'error_message': 'Invalid Password or Username'})

    # If GET request or login unsuccessful
    success_message = None
    return render(request, 'login.html')

def logout_view(request):

    logout(request)

    return redirect('core:index')


from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
import google.generativeai as genai
import os 

@login_required
def chatbot(request):
    return render(request,'chat.html')

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import logging

# Configure logging
logger = logging.getLogger(__name__)

@login_required
def chatbot(request):
    messages.success(request,"Welcome to Level up chatbot ")
    return render(request, 'chat.html')

@csrf_exempt
@login_required
def chat_with_bot(request):
    if request.method == 'POST':
        try:
            # Parse the JSON payload
            data = json.loads(request.body)
            user_message = data.get('message')

            if not user_message:
                return JsonResponse({'error': 'Message content is missing.'}, status=400)

            # Configure GenAI
            genai.configure(api_key=os.environ.get('GOOGLE_API_KEY'))
            model = genai.GenerativeModel(model_name="gemini-pro")

            # Generate bot response
            prompt = (
                "You are a sports professional, professor,coach . Respond to "
                "the following question posed by a someone who wants to exercise or be a professional athlete, in English. If the question "
                "is unrelated to sports, state that you don't know the answer and also don't be too formal: "
                f"{user_message}"
            )
            response = model.generate_content(prompt)
            bot_message = response.text

            return JsonResponse({'response': bot_message})

        except Exception as e:
            logger.error(f"Error processing chatbot request: {e}", exc_info=True)
            return JsonResponse({'error': 'An error occurred while processing your request.'}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=400)


def profile(request):
    return render(request,'profile.html')


#! Clans Logic from .models import Clan
from django.shortcuts import render
from .models import Clan 
def clans(request):
    clans = Clan.objects.all()  
    q = request.GET.get('q')  
    if q:
        clans = clans.filter(name__icontains=q) 
    return render(request, 'clans.html', {'clans': clans}) 
