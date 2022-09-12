from django.http import HttpResponse
from django.shortcuts import redirect, render
from .forms import UserForm
from .models import User


# Create your views here.

def registerUser(request):
    if request.method == 'POST':
        print(request.POST)
        form = UserForm(request.POST)
        # if form is valid sav in db
        if form.is_valid():
            # form is ready to be saved and data is assigned to user var
            user = form.save(commit=False)
            user.role = User.CUSTOMER
            user.save()
            print('USSSER', user)
            return redirect('registerUser')
    else:
        form = UserForm()

    context = {'form': form}
    return render(request, 'accounts/registerUser.html', context)
