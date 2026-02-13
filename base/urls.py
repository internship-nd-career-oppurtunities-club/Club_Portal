from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # path('UnderDevelopment/', views.devPage, name='dev' ),

    path('', views.home, name='home' ),
    path('profile/<str:pk>/', views.profile, name='profile'),
     path('update-profile/', views.updateProfile, name='update-profile' ),

    path('login/', views.loginPage, name='login' ),     
    path('logout/', views.logoutPage, name='logout' ),
    path('register/', views.registerPage, name='register' ),

    path('members/', views.membersPage, name='members' ),
    path('quickview/<str:pk>/', views.quickview, name='quickview'),

    path('activities/', views.activitiesPage, name='activities' ),
    path('activity/<str:pk>/', views.activity, name='activity'),
    path('newActivity/', views.newActivity, name='newActivity' ),

    path('resources/', views.resourcesPage, name='resources' ),
    path('saveResource/<str:pk>/', views.saveResource, name='save-resource'),
    path('addResource/', views.addResource, name='add-resource'),

    path('forum/', views.devPage, name='forum' ),
    path('contact-us/', views.contactUsPage, name='contact-us' ),
]