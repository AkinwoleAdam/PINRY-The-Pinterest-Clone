from django.urls import path
from . import views 


urlpatterns = [
  path('',views.home,name='home'),
  
  path('search/',views.search,name='search'),
  
  path('profile/<str:pk>',views.UserProfile,name='profile'),
  
  path('profile/edit/<str:pk>',views.editProfile,name='edit_profile'),
  
  path('boards/',views.AllBoards,name='all_boards'),
  
  path('board/create/',views.CreateBoard,name='create_board'),
  
  path('board/<str:pk>',views.BoardDetail,name='board'),
  
  path('board/edit/<str:pk>',views.editBoard,name='edit_board'),
  
  path('board/delete/<str:pk>',views.deleteBoard,name='delete_board'),
  
  path('pin/create/',views.createPin,name='create'),
  
  path('pin_detail/<str:pk>',views.pinDetail,name='pin_detail'),
  
  path('pin/edit/<str:pk>',views.editPin,name='edit_pin'),
  
  path('pin/delete/<str:pk>',views.deletePin,name='delete_pin'),
  
  path('comment/delete/<str:pk>',views.DeleteComment,name='delete'),
  ]
  
handler404 = 'pin.views.error_404'