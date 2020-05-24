from django.shortcuts import render,redirect
from .models import Post,reviewsData,Comments
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from .forms import ReviewDataForm,ReportPostForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from users.models import MessageData,Notifications,Following,Followers,Profile
# Create your views here.


def home(request):
    dataSet = list(MessageData.objects.filter(recieverID=request.user.id))
    dataSet.reverse()
    flag = False
    for data in dataSet:
        if data.seen == False:
            flag = True
            break
    notice= False
    if request.user.is_authenticated:
        dataSet = list(Notifications.objects.filter(user=request.user))
        notice= False
        dataSet.reverse()
        if dataSet:
            if dataSet[0].seen == False:
                notice = True
    dataSet = Post.objects.all().filter(checked=True).order_by('-date_posted')
    for data in dataSet:
        data.content = data.content[0:200]
    context = {
         'posts' : dataSet,
         'flag' : flag,
         'notice': notice
         }
    return render(request,'blog/home.html',context)

class PostListView(ListView):
    model = Post 
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Post 
    success_url = '/'
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post 
    fields = ['title','content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Post 
    fields = ['title','content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

@login_required
def about(request):
    userSet = list(User.objects.all())
    dataSet = list(Following.objects.filter(user=request.user).values('friends'))
    copyUser = []
    try:
        for data in dataSet:
            copyUser.append(Profile.objects.get(id=data.get('friends')).user)
    except:
        print('Some Error Occured')
    return render(request,'blog/allUsers.html', {'userSet' : userSet,'copyUser':copyUser})

@login_required
def postDetail(request, pk):
    if request.method  == 'POST':
        text = request.POST.get('commentText')
        postID = request.POST.get('postID')
        print(text)
        print(postID)
        dataObject = Comments(user=request.user,post=Post.objects.get(id=postID),text=text)
        dataObject.save()
        NotificationsObject = Notifications(user=Post.objects.get(id=postID).author,notice=str(User.objects.get(id=request.user.id).profile.name)+' commented on your Post.',seen=False)
        NotificationsObject.save()
        print('POST')
    obj = Post.objects.get(pk=pk)
    likeCount = len(obj.Likes.split("_")[:-1])
    hateCount = len(obj.Hates.split("_")[:-1])
    metaData = ''
    if str(request.user.id) in obj.Likes.split("_")[:-1]:
        metaData = 'Liked Post'
    if str(request.user.id) in obj.Hates.split("_")[:-1]:
        metaData = 'Disliked Post'
    if not obj.author==request.user:
        obj.count +=1
    obj.save()
    viwersIDs = obj.viewersIDs.split("_")[:-1]
    flag = True
    for IDs in viwersIDs:
        if int(IDs)==request.user.id:
            flag = False
    if flag==True:
        newString = obj.viewersIDs+str(request.user.id)+str('_')
        number = obj.uniqueCount
        number+=1
        Post.objects.filter(pk=pk).update(viewersIDs=newString)
        Post.objects.filter(pk=pk).update(uniqueCount=number)
    commentsData = Comments.objects.filter(post=Post.objects.get(id=pk)).values()
    for data in commentsData:
        userProfile = User.objects.get(id=data.get('user_id'))
        data['user_id'] = userProfile
    context = {
        'object':obj,
        'likes':likeCount,
        'hates':hateCount,
        'metaData':metaData,
        'commentsData': list(commentsData)
        }
    return render(request,'blog/post_detail.html',context)

@login_required
def trendingPost(request):
    obj = Post.objects.all().order_by('-uniqueCount')[0]
    return render(request,'blog/post_detail.html',{'object':obj})

def getReviews(request):
    dataSet = reviewsData.objects.all().order_by('-timeStamp')
    return render(request,'blog/reviews.html',{'dataSet':dataSet})

@login_required
def postReviews(request):
    if request.method=='POST':
        formData = ReviewDataForm(request.POST)
        if formData.is_valid():
            dataSaved = formData.save(commit=False)
            dataSaved.user = request.user
            dataSaved.save()
            messages.success(request, 'Review has been saved')
            return redirect('reviews')
    else:
        form = ReviewDataForm()
        return render(request,'blog/addReview.html',{'form':form})

@login_required
def reportPost(request,pk):
    if request.method == 'GET':
        form = ReportPostForm()
        return render(request,'blog/reportPost.html',{'form':form,'pk':pk})
    elif request.method == 'POST':
        formData = ReportPostForm(request.POST)
        note = request.POST.get('note')
        if formData.is_valid():
            dataSaved = formData.save(commit=False)
            dataSaved.reportedPostID = pk
            dataSaved.reportedByUser = request.user.id
            dataSaved.note = note
            dataSaved.save()
            messages.success(request,'Thanks for your feedback')
            return redirect('blog-home')

@login_required
def likePost(request,pk):
    postData = Post.objects.get(id=pk)
    if str(request.user.id) not in postData.Likes.split("_")[:-1] and str(request.user.id) not in postData.Hates.split("_")[:-1]:
        postData.Likes += str(request.user.id)+'_'
        messages.success(request,'Added to liked post')
        NotificationsObject = Notifications(user=User.objects.get(id=postData.author.id),notice='Congratulations! '+str(User.objects.get(id=request.user.id).profile.name)+' liked your Post.',seen=False)
        NotificationsObject.save()
    elif str(request.user.id) not in postData.Likes.split("_")[:-1] and str(request.user.id) in postData.Hates.split("_")[:-1]:
        ## write something so that hate gets removed and like gets added
        hateList = postData.Hates.split("_")[:-1]
        hateList.remove(str(request.user.id))
        newString = ''
        for data in hateList:
            newString+=(data+'_')
        postData.Hates = newString
        postData.Likes += str(request.user.id)+'_'
        messages.success(request,'Added to Liked Post')
    else:
        likeList = postData.Likes.split("_")[:-1]
        if str(request.user.id) in likeList:
            likeList.remove(str(request.user.id))
        newString = ''
        for data in likeList:
            newString += data+"_"
        postData.Likes = newString
        messages.success(request,'Removed from liked post')
    postData.save()
    return redirect('post-detail',pk)

@login_required
def hatePost(request,pk):
    postData = Post.objects.get(id=pk)
    if str(request.user.id) not in postData.Hates.split("_")[:-1] and str(request.user.id) not in postData.Likes.split("_")[:-1]:
        postData.Hates += str(request.user.id)+'_'
        messages.success(request,'Added to disliked post.')
    elif str(request.user.id) not in postData.Hates.split("_")[:-1] and str(request.user.id) in postData.Likes.split("_")[:-1]:
        ## write something so that like get removed and Hate gets added
        likeList = postData.Likes.split("_")[:-1]
        likeList.remove(str(request.user.id))
        newString = ''
        for data in likeList:
            newString+=(data+'_')
        postData.Likes = newString
        postData.Hates += str(request.user.id)+'_'
        messages.success(request,'Added to Disliked Post')
    else:
        likeList = postData.Hates.split("_")[:-1]
        if str(request.user.id) in likeList:
            likeList.remove(str(request.user.id))
        newString = ''
        for data in likeList:
            newString += data+"_"
        postData.Hates = newString
        messages.success(request,'Removed from disliked post.')
    postData.save()
    return redirect('post-detail',pk)