from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .forms import MyUserCreationForm
from django.contrib import messages
from .models import User,Code
from datetime import datetime, timedelta
d={
    'code_1':1,
    'code_2':2,
    'code_3':3,
    'code_4':4,
    'code_5':5,
    'code_6':6,
    'code_7':7,
    'code_8':8,
    'code_9':9,
    'code_10':10,
    'code_11':11,
    'code_t1':"t1",
}
k_l=list(d.keys())
v_l=list(d.values())
def loginPage(request): 
    page = 'login'
    if request.user.is_authenticated:
        return redirect('participant_home') 

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist')
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('participant_home') 
        else:
            messages.error(request, 'Email OR password does not exit') 
    context = {'page': page}
    return render(request, 'login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


def registerPage(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            if "iiitb.ac.in" in user.email: 
                user.email = user.email.lower()
                user.save()
                login(request, user)
                return redirect('participant_home')
            messages.error(request, 'Use iiitb mail id')
        else:
            messages.error(request, 'An error occurred during registration (Ensure that you are not using the same email id, this error could have been caused by that)')

    return render(request, 'login_register.html', {'form': form})

def participant_home(request):
    da=datetime.now()
    user_1= User.objects.get(email=str(request.user))
    timezone = user_1.sand.tzinfo
    da=da.replace(tzinfo=timezone)
    flag=(da<user_1.sand)
    if request.method == 'POST':
        if  not (flag):
            messages.error(request,"You can't enter code now , the contest is over")
        else:
            a=request.POST.get('text_input').strip().lower()
            passcode = list(Code.objects.filter(user=request.user).values())
            new_arr=[]
            for x in passcode:
                new_arr.append(x['data_item'])
            if a not in new_arr:
                if a in k_l:
                    Code.objects.create(
                    user=user_1,
                    data_item=a,
                    )
                    if type(d[a]) == int:
                        user_1.gold +=d[a]
                        user_1.save()
                    else:
                        return HttpResponse("Go to 8Bit and get your time increased by " + d[a][1] + "minutes")
                else:
                    messages.error(request,'Ooops Better luck next time ')
            else:
                messages.error(request,'You have already got points for submitting the above code . This is a repeat submission') 

    users=User.objects.all().order_by('-gold').values()
    context = {
        'users': users,
        'user_1':user_1,
        'curr_date_time':str(user_1.sand.month) + " " + str(user_1.sand.day) + "," + str(user_1.sand.year) + " " + str(user_1.sand.hour) + ":" + str(user_1.sand.minute) + ":" + str(user_1.sand.second),
        'flag':flag
    }
    return render(request, 'participant_home.html', context)
