from django.urls import path
from . import views 


urlpatterns = [
  path('',views.home,name='home'),
  
  path('profile/<str:pk>',views.UserProfile,name='profile'),
  
  path('profile/edit/<str:pk>',views.editProfile,name='edit_profile'),
  
  path('boards/',views.AllBoards,name='all_boards'),
  
  path('board/create/',views.CreateBoard,name='create_board'),
  
  path('board/<str:pk>',views.BoardDetail,name='board'),
  
  path('pin/create/',views.createPin,name='create'),
  
  path('pin_detail/<str:pk>',views.pinDetail,name='pin_detail'),
  
  path('comment/delete/<str:pk>',views.DeleteComment,name='delete'),
  ]