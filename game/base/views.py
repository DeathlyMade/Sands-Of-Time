from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .forms import MyUserCreationForm
from django.contrib import messages
from .models import User,Code
from datetime import datetime, timedelta
d = {
    "G_mess_board": 100,
    "G_mug_rack": 100,
    "V_mph_tire": 1000,
    "G_filter_gym": 100,
    "G_mph_taps": 100,
    "T_foosball": "t6",
    "G_ramp_dance": 100,
    "G_sac_room": 100,
    "T_firee_place": "t6",
    "G_trophy_cabinet": 100,
    "G_tuck_wall": 100,
    "G_lamp_27": 100,
    "G_fire_safety": 100,
    "T_sec_cabin": "t6",
    "G_baclony_minro": 100,
    "G_violet_flowers": 100,
    "G_r103_bench": 100,
    "G_staircase_underneath": 100,
    "T_fountain_back": "t6",
    "G_rock_pit": 100,
    "G_washroom_cabinet": 100,
    "G_bulletin_boards": 100,
    "G_electronic_waste": 100,
    "G_corner_3lifts": 100,
    "G_pipes_ramanujan": 100,
    "G_basement_way": 100,
    "G_plants_ramanujan": 100,
    "T_wenty_one": "t6",
    "G_sports_backdoor": 100,
    "V_star_guest": 1000,
    "G_welcome_board": 100,
    "G_gate_left": 100,
    "G_pond_rock": 100,
    "G_direction_board": 100,
    "G_fire_extinguisher_arya": 100,
    "G_shed_opp_pond": 100,
    "G_tree_dustbin": 100,
    "T_light_post": "t6",
    "V_bridge_under": 1000,
    "G_1000m": 100,
    "V_baby_art": 1000,
    "G_harry_p_cupboard": 100,
    "G_flower_power": 100,
    "G_601_A": 100,
    "G_lamp_lighter": 100,
    "G_bench_rest": 100,
    "G_sports_glory": 100,
    "G_attendance_dread": 100,
    "T_highness_seed": "t6",
    "G_pickle_tickle": 100,
    "T_time_keeper": "t6",
    "G_paper_guard": 100,
    "G_back_brick": 100,
    "G_laundry_steps": 100,
    "G_ev_station": 100,
    "V_map_misplaced": 1000,
    "G_pride_flag": 100,
    "G_bhaskara_back": 100,
    "G_vend_stairs": 100,
    "G_fear_street": 100,
    "G_throw_memory": 100,
    "G_kitchen_sneak": 100,
    "V_Bury_Gold": 1000,
    "T_arch_welcome": "t6",
    "G_power_mitoch": 100,
    "G_betala_bald_spot": 100,
    "G_ew_gross": 100,
    "G_math_genius": 100,
    "G_ten_feet": 100,
    "G_one_above_all": 100,
    "T_closeted": "t6",
    "G_monke_time": 100,
    "G_bat_alley": 100,
    "G_emotional_support": 100,
    "G_guardian_grid": 100,
    "G_PDA_Haven": 100,
    "G_sir_lundry": 100,
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
