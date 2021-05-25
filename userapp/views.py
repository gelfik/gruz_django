from .forms import *
from myapp.views import *

# Create your views here.
def login(request):
    arguments = {}
    arguments.update(csrf(request))
    arguments.update(form=UserLoginForm)
    if request.user.is_authenticated:
        return redirect(reverse('main_url'))
    if request.method == 'GET':
        arguments.update(next=request.GET['next'] if request.GET and 'next' in request.GET else '')
        return render(request, 'userapp/login.html', {'arguments': arguments})
    elif request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        userdata = auth.authenticate(username=username, password=password)
        try:
            usersearch = User.objects.get(username=username)
        except:
            usersearch = None
        if userdata is not None:
            auth.login(request, userdata)
            next_url = request.POST.get('next', '')
            if next_url != '':
                return redirect(next_url)
        elif usersearch is not None:
            arguments.update(error='Не верный пароль!')
            return render(request, 'userapp/login.html', {'arguments': arguments})
        else:
            arguments.update(error='Пользователь не найден!')
            return render(request, 'userapp/login.html', {'arguments': arguments})
    else:
        return HttpResponse('405 Method Not Allowed', status=405)


def logout(request):
    auth.logout(request)
    return redirect('/')

def register(request):
    arguments = {}
    arguments.update(csrf(request))
    arguments.update(form=UserRegisterForm)
    if request.user.is_authenticated:
        return redirect(reverse('main_url'))
    if request.method == 'GET':
        arguments.update(next=request.GET['next'] if request.GET and 'next' in request.GET else '')
        return render(request, 'userapp/register.html', {'arguments': arguments})
    elif request.method == 'POST':
        newuser_form = UserRegisterForm(request.POST)
        if newuser_form.is_valid():
            userform = newuser_form.save()
            userform.refresh_from_db()
            userform.groups.clear()
            userform.groups.add(newuser_form.cleaned_data.get('group_data'))
            userform.set_password(newuser_form.cleaned_data['password2'])
            userform.save()
            auth.login(request, userform)
            next_url = request.POST.get('next', '')
            if next_url != '':
                return redirect(next_url)
            return redirect(reverse('main_url'))
        else:
            arguments.update(form=UserRegisterForm(request.POST))
            arguments.update(error='Форма заполнена не корректно!')
            return render(request, 'userapp/register.html', {'arguments': arguments})
    else:
        return HttpResponse('405 Method Not Allowed', status=405)