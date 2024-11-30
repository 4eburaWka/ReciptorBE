import uuid
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.urls import reverse
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required

from app.forms import UserLoginForm, UserRegistrationForm, CallExecutionForm
from app.models import ExecutionModel, UserExecution
from app.service import finally_get_execution_result_service


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('users:call_execution'))
    else:
        form = UserLoginForm()
    context = {'form': form}
    return render(request, 'users/login.html', context)


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Вы успешно зарегистрировались!")
            return HttpResponseRedirect(reverse('users:login'))
    else:
        form = UserRegistrationForm()
    context = {'form': form}
    return render(request, 'users/register.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('users:home'))


def home(request):
    return render(request, 'app/home.html')


@login_required
def call_execution(request):
    if request.method == 'POST':
        form = CallExecutionForm(request.POST)
        if not form.is_valid():
            return HttpResponseRedirect()
        
        ingredients = ExecutionModel.sort_ingredients(form.cleaned_data['keys'])
        execution = ExecutionModel.objects.filter(keys=ingredients).first()
        if not execution:
            receipes = finally_get_execution_result_service(ingredients)
            execution = ExecutionModel.objects.create(id=uuid.uuid4(), keys=ingredients, value=receipes)
        UserExecution.objects.create(user=request.user, execution=execution)
        
        return redirect('users:history')
    else:
        form = CallExecutionForm()
        
    context = {'form': form}
    return render(request, 'app/call_execution.html', context)


@login_required
def get_history(request):
    executions = UserExecution.objects.filter(user=request.user).select_related('execution').order_by('called_at')
    
    context = {'executions': executions}
    return render(request, 'app/history.html', context)
