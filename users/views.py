from blog.models import Post
from django.db.models import Q
from .models import MessageData
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from django.contrib.sessions.models import Session
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import UserRegisterForm,UserUpdateForm,ProfileUpdateForm,MessageDataForm
from users.models import Notifications
from users.models import Profile,Following,Followers
from django.core.mail import send_mail
import requests
import json
# Create your views here.
# something changed

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            successMessage = 'Welcome '+username+" ! Kindly Update your profile after login."
            messages.success(request,successMessage)
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request,'users/register.html',{ 'form': form})

@login_required
def profile(request):
    messageArrived = MessageData.objects.filter(recieverID=request.user.id).values('sender','senderName').distinct()
    for data in messageArrived:
        dataSet = MessageData.objects.filter(senderName=data['senderName'],recieverID=request.user.id).values('seen')
        flag = True
        for datanew in dataSet:
            if(datanew['seen']==False):
                flag=False
        data.update({'AllRead' : flag})
    if request.user.profile.name== 'Default Name':
        messages.info(request, 'Kindly update your profile')
    posts = Post.objects.all().filter(author=request.user).order_by('-date_posted')
    return render(request,'users/profile.html',{'messageMD':messageArrived,'posts':posts})

@login_required
def update(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST,instance = request.user)
        p_form = ProfileUpdateForm(request.POST,request.FILES, instance = request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,'Profile Updated Successfully.')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance = request.user)
        p_form = ProfileUpdateForm(instance = request.user.profile)
    context = {
        'u_form':u_form,
        'p_form':p_form
    }
    return render(request,'users/updateProfile.html',context)

@login_required
def UserProfileView(request, pk):
    userData = User.objects.get(pk=pk)
    posts = Post.objects.all().filter(author=User.objects.get(id=pk)).order_by('-date_posted')
    for data in posts:
        data.content = data.content[0:200]
    return render(request, 'users/user_detail.html', {'user' : userData,'posts':posts})

@login_required
def storeMessage(request,pk):
    if request.method=='POST':
        formData = MessageDataForm(request.POST)
        if formData.is_valid():
            dataSaved = formData.save(commit=False)
            dataSaved.sender = request.user
            dataSaved.recieverID = pk
            dataSaved.senderName = request.user.profile.name
            dataSaved.seen = False
            dataSaved.save()
            recieverData = User.objects.get(id=pk)
            messages.success(request, 'Message has been send to '+recieverData.profile.name)
            return redirect('detail-message',pk)
    else:
        form = MessageDataForm()
        user = User.objects.get(id=pk)
        return render(request,'users/message.html',{'form':form,'user':user})

@login_required
def checkMessage(request):
    dataSet = MessageData.objects.filter(recieverID=request.user.id).values().order_by('-timeStamp')
    return render(request,'users/checkMessage.html',{'dataSet':dataSet})

@login_required
def detailedMessage(request,pk):
    if request.method=='POST':
        formData = MessageDataForm(request.POST)
        if formData.is_valid():
            dataSaved = formData.save(commit=False)
            dataSaved.sender = request.user
            dataSaved.recieverID = pk
            dataSaved.senderName = request.user.profile.name
            dataSaved.save()
            recieverData = User.objects.get(id=pk)
            messages.success(request, 'Message has been send to '+recieverData.profile.name)
            return redirect('detail-message',pk)
    else:
        form = MessageDataForm()
    dataSet = MessageData.objects.filter(Q(sender=pk,recieverID=request.user.id)|Q(sender=request.user.id,recieverID=pk)).values().order_by('timeStamp')
    changeData = MessageData.objects.filter(sender=pk,recieverID=request.user.id).order_by('timeStamp')
    for data in changeData:
        data.seen = True
        data.save()
    return render(request,'users/detail_message.html',{'dataSet':dataSet,'pk':pk,'form':form})

@login_required
def messageSummary(request):
    messageArrived = list(MessageData.objects.filter(recieverID=request.user.id).values('sender','senderName').order_by('-timeStamp'))
    messageArrivedCopy = []
    for data in messageArrived:
        if data not in messageArrivedCopy:
            messageArrivedCopy.append(data)
    messageArrived = messageArrivedCopy
    for data in messageArrived:
        dataSet = MessageData.objects.filter(senderName=data['senderName'],recieverID=request.user.id).values('seen')
        flag = True
        for datanew in dataSet:
            if(datanew['seen']==False):
                flag=False
        data.update({'AllRead' : flag})
    return render(request,'users/message.html',{'messageMD':messageArrived})

@login_required
def addFriend(request,pk):
    user = Followers.objects.get(user=User.objects.get(id=pk))
    user.friends.add(Profile.objects.get(user=request.user))
    user.save()
    user = Following.objects.get(user=request.user)
    friend = Profile.objects.get(user = User.objects.get(id=pk))
    user.friends.add(friend)
    user.save()
    userNote = user=User.objects.get(id=request.user.id)
    data = Notifications.objects.create(user=User.objects.get(id=pk),notice=str(userNote.profile.name)+' started following you.')
    data.save()
    messages.info(request, 'You started following '+str(friend.name))
    return redirect('blog-about')


@login_required
def myFriends(request):
    friendIDs = []
    for data in list(Following.objects.filter(user=request.user).values('friends')):
        friendIDs.append(data.get('friends'))
    usersList = []
    try:
        for i in friendIDs:
            user = Profile.objects.get(id=i).user
            usersList.append(user)
    except:
        print('Some error occured')
    return render(request,'users/myfriends.html',{'DataSet' : usersList})


@login_required
def removeFriend(request,pk):
    user = Following.objects.get(user=request.user)
    friend = Profile.objects.get(user = User.objects.get(id=pk))
    user.friends.remove(friend)
    user.save()
    messages.info(request, 'Removed Successfully')
    return redirect('my-friend')


def myNotifications(request):
    dataSet = Notifications.objects.filter(user=request.user)
    for data in dataSet:
        data.seen = True
        data.save()
    return render(request,'users/notification.html',{'dataSet':Notifications.objects.filter(user=request.user).order_by('-timeStamp')})


def search(request):
    if request.method=='POST':
        postData = list(Post.objects.filter(title__contains=request.POST.get('searchData')).values())
        userData = list(Profile.objects.filter(name__contains=request.POST.get('searchData')).values())
        return render(request,'users/search.html',{'h1':'Post Summary:','h2':'User Summary:','postData':postData,'userData': userData})
    else:
        return render(request,'users/search.html')


def myFollowers(request):
    dataSet = list(Followers.objects.filter(user=request.user).values('friends'))
    usersList = []
    for data in dataSet:
        usersList.append(Profile.objects.get(id=data.get("friends")).user)
    print(usersList)
    followingData = list(Following.objects.filter(user=request.user).values('friends'))
    print(followingData)
    idList = []
    for data in followingData:
        idList.append(data.get('friends'))
    print(idList)
    avoidList = []
    try:
        for data in idList:
            avoidList.append(Profile.objects.get(id=data).user)
    except:
        print('Some Error occured')
    print(avoidList)
    return render(request,'users/followers.html',{'DataSet' :usersList,'avoidList':avoidList})

def verify(request):
    if request.method == 'POST':
        otp = request.POST.get('OTP')
        if request.user.profile.OTP == int(otp):
            print('success')
            request.user.profile.varifiedProfile = True
            request.user.save()
            messages.success(request, 'You are a verified user now.')
            return redirect('profile')
    else:
        otp = request.user.profile.OTP
        number = request.user.profile.phoneNumber
        URL = 'https://www.way2sms.com/api/v1/sendCampaign'
        message = 'Dear '+str(request.user.profile.name)+'\n Kindly verify your account by giving the OTP as '+str(otp)+'\n Regards\n Roshan Pandey\n Team Tech Talk'
        req_params = {
            'apikey':"LJXV55YXPM4QIN75BMI6AHQA7SKTU33M",
            'secret':"7QRJWN0RFBDI0DKL",
            'usetype':"stage",
            'phone': number,
            'message': message,
            'senderid': 'ROSHAN'
            }
        requests.post(URL, req_params)
        send_mail('Tech Talk Account verification',message,'pandeyroshan556@gmail.com',[request.user.email],fail_silently=False,)
    return render(request,'users/verify.html')