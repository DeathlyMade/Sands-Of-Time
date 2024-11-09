from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .forms import MyUserCreationForm
from django.contrib import messages
from .models import User,Code
from datetime import datetime, timedelta
d = {
    "g_mess_board": 100,
    "g_mug_rack": 100,
    "v_mph_tire": 1000,
    "g_filter_gym": 100,
    "v_mph_taps": 100,
    "t_foosball": "t6",
    "g_ramp_dance": 100,
    "g_sac_room": 100,
    "t_firee_place": "t6",
    "g_trophy_cabinet": 100,
    "g_tuck_wall": 100,
    "g_lamp_27": 100,
    "g_fire_safety": 100,
    "t_sec_cabin": "t6",
    "g_baclony_minro": 100,
    "g_violet_flowers": 100,
    "g_r103_bench": 100,
    "g_staircase_underneath": 100,
    "t_fountain_back": "t6",
    "g_rock_pit": 100,
    "g_washroom_cabinet": 100,
    "g_bulletin_boards": 100,
    "g_electronic_waste": 100,
    "g_corner_3lifts": 100,
    "g_pipes_ramanujan": 100,
    "g_basement_way": 100,
    "g_plants_ramanujan": 100,
    "t_wenty_one": "t6",
    "g_sports_backdoor": 100,
    "v_star_guest": 1000,
    "g_welcome_board": 100,
    "g_gate_left": 100,
    "g_pond_rock": 100,
    "g_direction_board": 100,
    "g_fire_extinguisher_arya": 100,
    "g_shed_opp_pond": 100,
    "g_tree_dustbin": 100,
    "t_light_post": "t6",
    "v_bridge_under": 1000,
    "g_1000m": 100,
    "v_baby_art": 1000,
    "g_harry_p_cupboard": 100,
    "g_flower_power": 100,
    "g_601_a": 100,
    "g_lamp_lighter": 100,
    "g_bench_rest": 100,
    "g_sports_glory": 100,
    "g_attendance_dread": 100,
    "t_highness_seed": "t6",
    "g_pickle_tickle": 100,
    "t_time_keeper": "t6",
    "g_paper_guard": 100,
    "g_back_brick": 100,
    "g_laundry_steps": 100,
    "g_ev_station": 100,
    "v_map_misplaced": 1000,
    "g_pride_flag": 100,
    "g_bhaskara_back": 100,
    "g_vend_stairs": 100,
    "g_fear_street": 100,
    "g_throw_memory": 100,
    "g_kitchen_sneak": 100,
    "v_bury_gold": 1000,
    "t_arch_welcome": "t6",
    "g_power_mitoch": 100,
    "g_betala_bald_spot": 100,
    "g_ew_gross": 100,
    "g_math_genius": 100,
    "g_ten_feet": 100,
    "g_one_above_all": 100,
    "t_closeted": "t6",
    "g_monke_time": 100,
    "g_bat_alley": 100,
    "g_emotional_support": 100,
    "g_guardian_grid": 100,
    "g_pda_haven": 100,
    "g_sir_lundry": 100,
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
