from django.shortcuts import render, redirect
import requests
import api.file_crypto as fc

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User,Group
from django.views.decorators.csrf import csrf_protect

from django.contrib.auth import authenticate, login as djangoLogin, logout as djangoLogout
from django.contrib.auth.decorators import login_required

from allauth.account.decorators import verified_email_required

from .forms import *
from .models import *
from django.contrib.auth.models import Group, Permission
from api.models import File
def format_bytes(size):
    # 2**10 = 1024
    power = 2**10
    n = 0
    power_labels = {0: '', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
    while size > power:
        size /= power
        n += 1
    return size, power_labels[n]+'B'



@login_required(login_url='/login')
def home(request):
    if request.user.is_superuser:
        return redirect("/admin")
    user = request.user
    profile = Profile.objects.filter(user=user).first()

    x = requests.get('http://127.0.0.1:3000/api/file',
    params={'profile': profile.id, 'is_Auth': request.user.is_authenticated})
    files = x.json()
    count_property = 0
    count_identity = 0
    count_other = 0
    for file in files:
        if file['category'] == "Property":
            count_property +=1
        elif file['category'] == "Identity":
            count_identity  += 1
        else :
            count_other += 1
    str(count_property)
    str(count_identity)
    str(count_other)
    
    context = {'is_Auth': request.user.is_authenticated, 
                'count_property':count_property,
                'count_identity':count_identity,
                'count_other':count_other,
                'user': user, 
            }
    return render(request, 'main/home.html', context)

@login_required(login_url='/login')
def drive_page(request):
    if request.user.is_superuser:
        return redirect("/admin")
    user = request.user
    profile = Profile.objects.filter(user=user).first()
    print(profile)
    x = requests.get('http://127.0.0.1:3000/api/file',
    params={'profile': profile.id, 'is_Auth': request.user.is_authenticated})
    files = x.json()
    for file in files:
        size = format_bytes(file['file_size'])
        temp = file['created_at'][0:10]
        temp = temp.split('-')
        temp = temp[::-1]
        temp = '/'.join(temp)
        file['created_at'] = temp
        file['file_size'] = str("{:.2f}".format(size[0])) + " " + str(size[1])
    context = {'user': user, 'profile': profile, 'files': files, 'is_Auth': request.user.is_authenticated}
    return render(request, 'main/drive.html', context)
 


@login_required(login_url='/login')
def trustee(request):
    if request.user.is_superuser:
        return redirect("/admin")
    form = TrusteeForm()
    group =""
    context={}
    if request.method == "POST":
        form = TrusteeForm(request.POST)
        if form.is_valid():
            
            user = request.user
            profile = Profile.objects.filter(user=user)[0]
            x = requests.get('http://127.0.0.1:3000/api/file',
            params={'profile': profile.id, 'is_Auth': request.user.is_authenticated})
            files = x.json()

            custom_groupname = files[0]['owner_id'] 
            if Group.objects.filter(name=custom_groupname).exists():
               group = Group.objects.get(name=custom_groupname)

            else:
                Group.objects.create(name=custom_groupname)
            
                uname = form.cleaned_data['username']
                userToAdd = User.objects.get(username = uname)
                # user_set = User.objects.all()

                group = Group.objects.get(name=custom_groupname)
                userToAdd.groups.add(group)

                part = Group.objects.filter(name=custom_groupname).first()
                a = File.objects.filter(owner_id = part)
                context['trustee'] = a
                form.save()
    context['form'] = form
    context['is_Auth'] = request.user.is_authenticated
    print(context)

        #return redirect("/thanks/")
    return render(request,'main/trustee.html',context)

def delete_file(request, id):
    x = requests.delete('http://127.0.0.1:3000/api/file/'+id)

    return redirect('/drive')


def view_file(request, id):

    x = requests.get('http://127.0.0.1:3000/api/file/'+id)
    file = x.json()
    data = file['file_data'][2:-1].encode('utf-8')

    user = request.user
    profile = Profile.objects.filter(user=user).first()
    print(profile, profile.cryptoKey)
    profilekey = bytes(profile.cryptoKey[2:-1], 'utf-8')

    decrypted = fc.decrypt(data, profilekey)
    
    return HttpResponse(decrypted, content_type=file['file_content_type'])


@csrf_protect
def register(request):
    if request.method == 'POST':
        data = request.POST
        user = User.objects.create_user(username=data['username'], email=data['email'],
                                        password=data['password'], first_name=data['first_name'], last_name=data['last_name'])
        user.save()
        profile = Profile(user=user)
        profile.save()
        user = authenticate(
            request, username=data['username'], password=data['password'])
        djangoLogin(request, user)
        return redirect('/drive')
    return render(request, 'main/login.html')


@csrf_protect
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            djangoLogin(request, user)
            return redirect('/drive')
        else:
            return redirect('/login')
    
    return render(request, 'main/login.html')


def logout(request):
    djangoLogout(request)
    return redirect("/")
def thanks(request):
    return render(request,"main/thanks.html")