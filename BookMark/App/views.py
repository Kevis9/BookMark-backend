from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse, HttpResponse
from .models import User,Entry,Book,likeInfo
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import requests

salt = 'wobuzhidaoyongshenmejiamisuanfabijiaohaozLPQ'
AppKey = "3885330ed4c3462b67d50bd55d2e7817"
ISBNSearchURL = "http://feedback.api.juhe.cn/ISBN"

@csrf_exempt
@require_http_methods(["POST"])
def login(request):
    # 设置响应
    dic={}
    response = HttpResponse()
    if request.method=="POST":
        dic["msg"] = 1
        req = request.POST
        email=req['email']
        pwd=req['pwd']
        try:
            user_a = User.objects.get(username=email)  # 这个设置是为了更详细的检查出错误来,因为这个地方get函数不会返回none,一旦找不到,便会给一个exception
            # print(user_a.password)
            user = authenticate(username=email, password=pwd)  # 而authenticate就能返回一个none
            if user:
                #用户存在
                response.set_signed_cookie('loginCookie',user.id,salt=salt,max_age=24*3600*7)   #Cookie的有效期为7天
                dic = user.getDic()
                dic["msg"] = 1
                response.content = json.dumps(dic)
            else:
                dic["msg"] = 3  #用户密码错误
                return JsonResponse(dic)
            response.content = json.dumps(dic)
            return response
        except Exception as e:
            print(e)
            dic["msg"] = 2     #用户不存在
            return JsonResponse(dic)
    # get_token(request)  # 产生一个token 用于csrf验证
    return response

@csrf_exempt
@require_http_methods(["POST"])
def register(request):
    response = {}
    if(request.method=="POST"):
        response["msg"] = 1
        req = request.POST
        #检验用户是否存在
        user_exist = list(User.objects.filter(email=req["email"]))
        if user_exist:
            response["msg"] = 2 #用户存在
            return JsonResponse(response)
        #使用邮箱来作为用户名
        user=User.objects.create_user(username=req["email"],password=req["pwd"])
        user.email=req["email"]
        user.pwd = req["pwd"]
        user.nick_name = req["nick_name"]
        # user.profile_img = req["profile_img"]
        user.save()
        return JsonResponse(response)

@require_http_methods(["GET"])
def check_login(request):
    req = request.get_signed_cookie('loginCookie',salt=salt,default=None)
    if req is None:
        dic = {}
        dic["msg"] = 2
        return JsonResponse(dic)
    else:
        user = User.objects.get(id=req)
        dic = user.getDic()
        dic["msg"] = 1
        return JsonResponse(dic)


@require_http_methods(["GET"])
def searchBookWithISBN(request):
    res = {}
    if(request.method=="GET"):
        req = request.GET
        print(req["ISBN"])
        ISBNnum = req["ISBN"]
        #首先是本服务器搜索是否存在此ISBN的书
        try:
            #在本地找到该书
            book = Book.objects.get(ISBN=ISBNnum)
            dic = book.getDic()
            dic["error_code"] = 0
            return JsonResponse(dic)
        except Exception as e:
            #请求聚合数据的书籍资料,请求成功则创建该书
            params = {}
            params["key"] = AppKey
            params["sub"] = ISBNnum
            #本身request模块就是阻塞式请求
            response = requests.get(ISBNSearchURL,params=params)
            dic_res = json.loads(response.content.decode())
            book = Book()
            if(dic_res["error_code"]==0):
                res["msg"] = 1  #查找成功
                book.ISBN = ISBNnum
                book.author = dic_res["result"]["author"]
                book.image_large = dic_res["result"]["images_large"]
                book.image_medium = dic_res["result"]["images_medium"]
                book.mainTitle = dic_res["result"]["title"]
                book.pages = dic_res["result"]["pages"]
                book.pubdate = dic_res["result"]["pubdate"]
                book.publisher = dic_res["result"]["publisher"]
                book.subTitle = dic_res["result"]["subtitle"]
                book.summary = dic_res["result"]["summary"]
                book.save()
                dic_cp = dic_res.copy()
                dic_cp["result"]["ISBN"] = ISBNnum
                dic_cp["result"]["entry_num"] = len(Entry.objects.filter(book=book))
                return JsonResponse(dic_cp)
            else:
                res["reason"]=dic_res["reason"]
                res["error_code"] = dic_res["error_code"]
                res["msg"] = 2  #查找失败
        return JsonResponse(res)

@require_http_methods(["GET"])
def searchaKeyWords(request):
    res = {}
    if(request.method=="GET"):
        req = request.GET
        entries = list(Entry.objects.filter(conception__contains=req["keyword"]))
        if entries:
            #存在关键字
            res["entries"] = []
            for entry in entries:
                res["entries"].append(entry.getDic(request))
            res["num"] = len(res["entries"])
        else:
            res["num"] = 0
        return JsonResponse(res)

@require_http_methods(["GET"])
def searchBookName(request):
    res = {}
    if(request.method=="GET"):
        req = request.GET
        books = list(Book.objects.filter(mainTitle__contains=req["title"]))
        if books:
            #本地数据库存在书籍
            res["books"] = []
            for book in books:
                res["books"].append(book.getDic())
            res["num"] = len(res["books"])
    else:
        res["num"] = 0
    return JsonResponse(res)

@require_http_methods(["GET"])
def getEntriesWithBookandPage(request):
    res = {}
    if(request.method=="GET"):
        req = request.GET
        entries = list(Entry.objects.filter(book=req["ISBN"],page=req["page"]))
        if entries:
            res["entries"] = []
            for entry in entries:
                res["entries"].append(entry.getDic(request))
            res["num"] = len(res["entries"])
        else:
            res["num"] = 0
        return JsonResponse(res)


@require_http_methods(["GET"])
def getHomePageEntries(request):
    #返回100条比较热门的entry
    if (request.method == "GET"):
        entries = Entry.objects.all().order_by("-like_num")
        res = {}
        res["entries"] = []
        for i in range(min(100,len(entries))):
            res["entries"].append(entries[i].getDic(request))
        res["num"] = len(res["entries"])
        return JsonResponse(res)

@csrf_exempt
@require_http_methods(["POST"])
def createEntry(request):
    res = {}
    if(request.method=="POST"):
        #检查登录状态
        uid = request.get_signed_cookie('loginCookie', salt=salt, default=None)
        if uid:
            req = request.POST
            entry = Entry()
            dic = {}
            entry.book = Book.objects.get(ISBN=req["book"])
            entry.users_write = User.objects.get(id=req["users_write"])
            dic = req.copy()
            del dic["book"]
            del dic["users_write"]
            entry.update(dic)
            res["msg"] = 1
        else:
            res["msg"] = 2 #登录失效
        return JsonResponse(res)

@csrf_exempt
@require_http_methods(["POST"])
def updateEntry(request):
    res = {}
    if(request.method=="POST"):
        # 检查登录状态
        uid = request.get_signed_cookie('loginCookie', salt=salt, default=None)
        if uid:
            req = request.POST
            entry = Entry.objects.get(id=req["id"])
            entry.book = Book.objects.get(ISBN=req["book"])
            entry.users_write = User.objects.get(id=req["users_write"])
            dic = req.copy()
            del dic["book"]
            del dic["users_write"]
            entry.update(dic)
            res["msg"] = 1
        else:
            res["msg"] =2
        return JsonResponse(res)

@require_http_methods(["GET"])
def removeEntry(request):
    res = {}
    if(request.method=="GET"):
        # 检查登录状态
        uid = request.get_signed_cookie('loginCookie', salt=salt, default=None)
        if uid:
            req = request.GET
            entry = Entry.objects.get(id=req["eid"])
            entry.delete()
            res["msg"] = 1
        else:
            res["msg"] = 2
        return JsonResponse(res)

@require_http_methods(["GET"])
def likeAction(request):
    res = {}
    if(request.method=="GET"):
        # 检查登录状态
        uid = request.get_signed_cookie('loginCookie', salt=salt, default=None)
        req = request.GET
        if uid:
            res["msg"] = 1
            entry = Entry.objects.get(id=req["eid"])
            entry.like_num += 1
            user_liked = entry.users_write
            user_like = User.objects.get(id=uid)
            likeinfo = likeInfo(user_like=user_like,entry=entry,user_liked=user_liked)
            likeinfo.save()
            entry.save()
        else:
            res["msg"] = 2
        return JsonResponse(res)

@require_http_methods(["GET"])
def dislikeAction(request):
    res = {}
    if (request.method == "GET"):
        # 检查登录状态
        uid = request.get_signed_cookie('loginCookie', salt=salt, default=None)
        req = request.GET
        if uid:
            try:
                entry = Entry.objects.get(id=req["eid"])
                entry.like_num -= 1
                likeinfo = likeInfo.objects.get(user_like=uid,entry=req["eid"])
                likeinfo.delete()
                entry.save()
                res["msg"] = 1
            except Exception as e:
                print(e)
                res["msg"] = 3  #意外情况
        else:
            res["msg"] = 2 #未登录
        return JsonResponse(res)

# @require_http_methods(["GET"])
# def getMyMsg(request):
#     res = {}
#     if (request.method == "GET"):
#         # 检查登录状态
#         uid = request.get_signed_cookie('loginCookie', salt=salt, default=None)
#         req = request.POST
#         if uid:
#             msgs = list(likeInfo.objects.filter(user_liked=uid))
#             res["msgs"] = []
#             for msg in msgs:
#                 res["msgs"].append(msg.getDic())
#             res["num"] = len(res["msgs"])
#         else:
#             res["num"] = 0
#         return JsonResponse(res)
#
# @require_http_methods(["GET"])
# def deleteMsg(request):
#     res = {}
#     if(request.method=="GET"):
#         uid = request.get_signed_cookie('loginCookie', salt=salt, default=None)
#         req = request.POST
#         if uid:
#             msg = likeInfo.objects.get(id=req["mid"])
#             msg.delete()
#             res["msg"] = 1
#         else:
#             res["msg"] = 2
#
#         return JsonResponse(res)

@require_http_methods(["GET"])
def getMyEntries(request):
    res = {}
    if(request.method=="GET"):
        uid = request.get_signed_cookie('loginCookie', salt=salt, default=None)
        req = request.POST
        if uid:
            res["entries"] = []
            entries = list(Entry.objects.filter(users_write=uid))
            for entry in entries:
                res["entries"].append(entry.getDic(request))
            res["num"] = len(res["entries"])
            res["msg"] = 1
        else:
            res["msg"] = 2
            res["num"] = 0
        return JsonResponse(res)


