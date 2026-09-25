from django.shortcuts import render
from django.http import HttpResponse
from .forms import UserRegisterForm

# Create your views here.

def register_view(request):

    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_superuser = False
            user.is_staff = False
            user.save()
            return HttpResponse("Đăng ký thành công!")
    else:
        form = UserRegisterForm()

    return render(
        request, 
        'register/register.html',
            {
                'form': form
            }
        )
