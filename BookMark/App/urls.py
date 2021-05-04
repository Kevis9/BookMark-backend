from django.urls import path
from . import views

urlpatterns=[
    path('login',views.login),
    path('register',views.register),
    path('checklogin',views.check_login),
    path('searchBookWithISBN',views.searchBookWithISBN),
    path('searchaKeyWords',views.searchaKeyWords),
    path('searchBookName',views.searchBookName),
    path('getEntriesWithBookandPage',views.getEntriesWithBookandPage),
    path('getHomePageEntries',views.getHomePageEntries),
    path('createEntry',views.createEntry),
    path('updateEntry',views.updateEntry),
    path('removeEntry',views.removeEntry),
    path('likeAction',views.likeAction),
    path('dislikeAction',views.dislikeAction),
    # path('getMyMsg',views.getMyMsg),
    # path('deleteMsg',views.deleteMsg),
    path('getMyEntries',views.getMyEntries),
]