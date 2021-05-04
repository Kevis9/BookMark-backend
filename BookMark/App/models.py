from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
# Create your models here.
salt = 'wobuzhidaoyongshenmejiamisuanfabijiaohaozLPQ'

class User(AbstractUser):

    nick_name = models.CharField('昵称', max_length=128, null=True)
    profile_img = models.CharField('头像', max_length=128, null=True)
    email = models.EmailField("邮件",max_length=128,null=True)

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
    def __str__(self):
        return "{}".format(self.username)
    def get_absolute_url(self):
        return reverse('用户', args=[self.id])
    def getDic(self):
        dic = {}
        dic["uid"] = self.id
        dic["name"] = self.nick_name
        dic["img_link"] = self.profile_img
        dic["publish_num"] = len(Entry.objects.filter(users_write=self.id))
        return dic

class Book(models.Model):

    ISBN = models.CharField("ISBN",max_length=1200,primary_key=True)
    publisher = models.CharField('出版商', max_length=128, null=True)
    pubdate = models.DateField("出版日期",null=True)
    image_medium = models.CharField('书的图像(中)', max_length=1200, null=True)
    image_large = models.CharField('书的图像(大)', max_length=1000, null=True)
    author = models.CharField('作者', max_length=200, null=True)
    subTitle = models.CharField('副标题', max_length=1000, null=True)
    mainTitle = models.CharField('主标题', max_length=1000, null=True)
    summary =  models.CharField('总结', max_length=2000, null=True)
    pages = models.IntegerField("页数",null=True)
    class Meta:
        verbose_name = '书籍'
        verbose_name_plural = verbose_name
    def __str__(self):
        return "{}".format(self.mainTitle)
    def get_absolute_url(self):
        return reverse('书籍', args=[self.id])
    def getDic(self):
        dic = {}
        dic["result"] = {}
        dic["result"]["ISBN"] = self.ISBN
        dic["result"]["publisher"] = self.publisher
        dic["result"]["pubdate"] = self.pubdate
        dic["result"]["image_medium"] = self.image_medium
        dic["result"]["image_large"] = self.image_large
        dic["result"]["author"] = self.author
        dic["result"]["subTitle"] = self.subTitle
        dic["result"]["title"] = self.mainTitle
        dic["result"]["summary"] = self.summary
        dic["result"]["pages"] = self.pages
        dic["result"]["entry_num"] = len(Entry.objects.filter(book=self))
        return dic




class Entry(models.Model):
    conception = models.CharField("概念",max_length=200,null=True)
    explanation = models.CharField("解释",max_length=2000,null=True)
    example = models.CharField("举例",max_length=2000,null=True)
    resemblence = models.CharField("类似的概念",max_length=2000,null=True)
    QA = models.CharField("自问自答",max_length=2000,null=True)
    page = models.IntegerField("所在页面",null=True)
    time = models.DateField(auto_now_add=True,null=True)
    like_num = models.IntegerField("点赞数",default=0,null=True)
    book = models.ForeignKey(Book,verbose_name="所在书名",on_delete=models.DO_NOTHING,null=True,related_name="所含词条")
    users_write = models.ForeignKey(User,verbose_name="词条作者",null=True,on_delete=models.CASCADE,related_name="user_write")

    class Meta:
        verbose_name = '词条'
        verbose_name_plural = verbose_name
    def __str__(self):
        return "{}".format(self.conception)
    def get_absolute_url(self):
        return reverse('词条', args=[self.id])

    def checkisliked(self,request):
        uid = request.get_signed_cookie('loginCookie', salt=salt, default=None)
        if uid:
            info = likeInfo.objects.filter(user_like=uid,entry=self.id)
            if(len(info)>0):
                return 1
            else:
                return 0
        else:
            return 0

    def getDic(self,request):
        dic = {}
        dic["conception"] = self.conception
        dic["book_name"] = self.book.mainTitle
        dic["user_name"] = self.users_write.nick_name
        dic["explanation"] = self.explanation
        dic["example"] = self.example
        dic["resemblence"] = self.resemblence
        dic["QA"] = self.QA
        dic["page"] = self.page
        dic["time"] = self.time
        dic["like_num"] = self.like_num
        dic["id"] = self.id
        dic["img_link"] = self.users_write.profile_img
        dic["isliked"] = self.checkisliked(request)
        dic["uid"] = self.users_write.id
        return dic

    def update(self,dic):
        objlist = dir(self)
        for key in dic:
            if key in objlist:
                setattr(self,key,dic[key])
        self.save()




class likeInfo(models.Model):
    #点赞信息(Django的逻辑就是一张中间表)
    user_like = models.ForeignKey(User,verbose_name="点赞者",null=True,on_delete=models.DO_NOTHING,related_name="userlike")
    entry = models.ForeignKey(Entry,verbose_name="点赞的词条",null=True,on_delete=models.DO_NOTHING)
    user_liked = models.ForeignKey(User,verbose_name="被点赞者",null=True,on_delete=models.DO_NOTHING,related_name="userliked")
    time = models.DateField(auto_now_add=True,null=True)
    class Meta:
        verbose_name = '点赞信息'
        verbose_name_plural = verbose_name
    def __str__(self):
        return "{}".format(self.id)
    def get_absolute_url(self):
        return reverse('点赞信息', args=[self.id])
    def getDic(self):
        dic = {}
        dic["user_like"] = self.user_like.nick_name
        dic["entry"] = self.entry.getDic()
        dic["time"] = self.time
        dic["mid"] = self.id
        return dic





