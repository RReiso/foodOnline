from django.http import HttpResponse
from django.shortcuts import redirect, render
from .forms import UserForm
from .models import User
from django.contrib import messages

# Create your views here.


def registerUser(request):
    if request.method == 'POST':
        print(request.POST)
        form = UserForm(request.POST)
        # if form is valid sav in db:
        if form.is_valid():
            # comes from clean method in UserForm (built in method)
            password = form.cleaned_data['password']
            # form is ready to be saved and data is assigned to user var:
            user = form.save(commit=False)
            user.set_password(password)  # hash the password
            user.role = User.CUSTOMER
            user.save()
            messages.success(
                request, 'You have been successfully registered!')

            # alternative way to create a user - using create_user method:
            # first_name = form.cleaned_data['first_name']
            # last_name = form.cleaned_data['last_name']
            # username = form.cleaned_data['username']
            # email = form.cleaned_data['email']
            # password = form.cleaned_data['password']
            # user = User.objects.create_user(
            #     first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            # user.role = User.CUSTOMER
            # user.save()
            return redirect('registerUser')
        else:
            print('Invalid form')
            print(form.errors)
    else:
        form = UserForm()

    context = {'form': form}
    return render(request, 'accounts/registerUser.html', context)
