from django.http import request
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import UserRegistration, UserEditForm,SampleCollectionForm, ProfileForm
from .models import SampleCollection, SampleStatus, Profile
from datetime import datetime
from django.contrib import messages
# Create your views here.

@login_required
def dashboard(request): 
    if request.method == 'POST':
        age = request.POST['age']
        date = request.POST['date']
        fever = request.POST.get('fever')
        if fever:
            fever = True
        else:
            fever = False
        drycough = request.POST.get('drycough')
        if drycough:
            drycough = True
        else:
            drycough = False
        tiredness = request.POST.get('tiredness')
        if tiredness:
            tiredness = True
        else:
            tiredness = False
        difficultybreathing = request.POST.get('difficultybreathing')
        if difficultybreathing:
            difficultybreathing = True
        else:
            difficultybreathing = False
        chestpain = request.POST.get('chestpain')
        if chestpain:
            chestpain = True
        else:
            chestpain = False
        lossofspeech = request.POST.get('lossofspeech')
        if lossofspeech:
            lossofspeech = True
        else:
            lossofspeech = False
        fname = request.user.first_name
        num = SampleStatus.objects.all().filter(user=request.user).count()
        sampleid = SampleIDCalculator(fname,date,num)
        data = SampleCollection(sampleid=sampleid, age=age, date=date, fever=fever, drycough=drycough, tiredness=tiredness, difficultybreathing=difficultybreathing, chestpain=chestpain, lossofspeech=lossofspeech)
        data.save()
        new_data = SampleStatus(user=request.user, sampleid=sampleid, status='TestingUnderProcess')
        new_data.save()

    form = SampleCollectionForm()
    recent =  SampleStatus.objects.all().filter(user=request.user).last()
    context = {
        "welcome": "Get Yourself Tested",
        "form": form,
        "recent": recent
    }
    return render(request, 'authapp/dashboard.html', context=context)

@login_required
def account(request):
    user = request.user
    context = {
        "welcome": "Welcome to your Portal",
        "user": user
    }
    return render(request, 'authapp/account.html', context=context)

def home(request):
    context = {
        
    }
    return render(request, 'home.html', context=context)


def register(request):
    if request.method == 'POST':
        
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        aadhar_number = request.POST['aadhar_number']

        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username Exists!!')
                return render(request, 'authapp/register.html')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email Exists!!')
                return render(request, 'authapp/register.html')
            elif EmailFieldChecker(email):
                messages.info(request, 'Only @gmail.com and @yahoo.com required!!')
                return render(request, 'authapp/register.html')
            elif PasswordChecker(password):
                messages.info(request, 'Password should atleast contain one small letter, one capital letter, one digit, one special character and atleast length of 8 characters!!')
                return render(request, 'authapp/register.html')
            elif PhoneNumberChecker(phone_number):
                messages.info(request, 'Enter Valid Phone Number!!')
                return render(request, 'authapp/register.html')
            elif AadharNumberChecker(aadhar_number):
                messages.info(request, 'Enter Valid Aadhar Number!!')
                return render(request, 'authapp/register.html')
            else:
                first_name = first_name.upper()
                last_name = last_name.upper()
                user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name,last_name=last_name)
                user.save()
                profile = Profile(user=user, phone_number=phone_number, aadhar_number=aadhar_number)
                profile.save()
                return render(request, 'authapp/register_done.html')

        else:
            messages.info(request, 'Password does not match!!')
            return render(request, 'authapp/register.html')

    else:
        return render(request, 'authapp/register.html')



@login_required
def history(request):
    result = SampleStatus.objects.filter(user=request.user)
    context = {
        "welcome": "Welcome to your Sample Report Portal",
        "result": result
    }
    return render(request, 'authapp/history.html', context=context)


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        if user_form.is_valid():
            user_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
    context = {
        'form': user_form,
    }
    return render(request, 'authapp/edit.html', context=context)



def SampleIDCalculator(fname, date, num):
    num += 1
    num = num % 100
    if len(fname) < 2:
        fname = 'XX'
    fname = fname[0:2]
    fname = fname.upper()
    mon = date[5:7]
    day = date[8:]
    sample_id = ""
    sample_id = sample_id+day+mon+fname
    if num < 10:
        sample_id= sample_id + '0'
    sample_id=sample_id + str(num)

    return sample_id


def EmailFieldChecker(email):
    email = str(email)
    cnt=0
    for e in email:
        if e=='@':
            break
        cnt+=1
    email = email[cnt:]

    if email == '@gmail.com' or email == '@yahoo.com':
        return False
    return True

def PasswordChecker(password):
    password=str(password)
    cnt_small=0
    cnt_large=0
    cnt_num=0
    cnt_char=0
    for p in password:
        if p>='a' and p<='z':
            cnt_small+=1
        elif p>='A' and p<='Z':
            cnt_large+=1
        elif p>='0' and p<='9':
            cnt_num+=1
        else:
            cnt_char += 1
    

    if cnt_small >= 1 and cnt_large >= 1 and cnt_num>=1 and cnt_char >= 1 and len(password)>=8:
        return False
    return True

def PhoneNumberChecker(phone_number):
    phone_number = str(phone_number)
    for ph in phone_number:
        if ph<'0' and ph>'9':
            return True
    if phone_number[0]=='0' or len(phone_number)!=10:
        return True
    return False

def AadharNumberChecker(aadhar_number):
    aadhar_number = str(aadhar_number)
    for ad in aadhar_number:
        if (ad<'0' and ad>'9') or len(aadhar_number)!=16:
            return True
    return False





    

    
    


