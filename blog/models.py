from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User,verbose_name='Writer',on_delete=models.CASCADE)
    count = models.IntegerField("Views on Post",default=1)
    viewersIDs = models.CharField(max_length=10000,blank=True)
    uniqueCount = models.IntegerField("Unique Count",default=1)
    checked = models.BooleanField("Mark if Passes Community Guidelines", default=False)
    Likes = models.CharField(max_length=10000,blank=True)
    Hates = models.CharField(max_length=10000,blank=True)

    def __str__(self):
        if self.checked == False:
            return self.title+' : Pending'
        return self.title+' : Approved'

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
class reviewsData(models.Model):
    user = models.ForeignKey(User,verbose_name='Writer',on_delete=models.CASCADE)
    review = models.TextField(blank=False)
    timeStamp = models.DateTimeField('Date & Time',default=timezone.now)

    def __str__(self):
        return self.user.username+"'s Review"
    class Meta:
        verbose_name='Reviews'
        verbose_name_plural='Reviews'

class reportPost(models.Model):
    reportedPostID = models.IntegerField("Post ID",blank=False)
    reportedByUser = models.IntegerField("User ID",blank=False)
    note = models.CharField("Description",max_length=500,blank=True)
    status = models.BooleanField("Mark as read",default=False)

    def __str__(self):
        if self.status == False:
            return 'Post '+str(self.reportedPostID)+' reported by User ID '+str(self.reportedByUser)+' -> UnSeen'
        return 'Post '+str(self.reportedPostID)+' reported by User ID '+str(self.reportedByUser)+' -> Seen'
    class Meta:
        verbose_name = 'Reported Post'
        verbose_name_plural = 'Reported Post'
class Comments(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    text = models.TextField(max_length=500,blank=False)
    timeStamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.user)+'\'s comment'
    
    class Meta:
        verbose_name = 'Comments'
        verbose_name_plural = 'Comments'