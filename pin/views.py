from django.shortcuts import render,redirect
from .models import *
from .forms import PinForm,EditProfileForm,UserUpdateForm,BoardForm,CommentForm,SaveToBoardForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here

def home(request):
  pins = Pin.objects.all()
  context = {'pins':pins}
  return render(request,'pin/home.html',context)
 
 
@login_required(login_url='login')
def createPin(request):
  form = PinForm(request.user)
  if request.method == "POST":
    form = PinForm(request.POST,request.FILES,request.user)
    if form.is_valid():
      pin = form.save(commit=False)
      pin.user = request.user
      pin.save()
      return redirect('home')
  context = {'form':form}
  return render(request,'pin/create_pin.html',context)
  
  
@login_required(login_url='account_login')
def pinDetail(request,pk):
  pin = Pin.objects.get(id=pk)
  comments = pin.comments.all()
  form = CommentForm()
  if request.method == 'POST':
    form = CommentForm(request.POST)
    if form.is_valid():
      comment = form.save(commit=False)
      comment.user = request.user
      comment.pin = pin
      comment.save()
      return redirect('pin_detail',pin.id)
  context = {'pin':pin,'comments':comments,'form':form}
  return render(request,'pin/pin_detail.html',context)

@login_required(login_url='login')  
def DeleteComment(request,pk):
  pin = Pin.objects.get(id=pk)
  comment = Comment.objects.get(id=pk)
  if request.method == "POST":
    comment.delete()
    return redirect('pin_detail',comment.pin.id)
  context = {'obj':comment,'pin':pin}
  return render(request,'pin/delete.html',context)

def AllBoards(request):
  boards = Board.objects.filter(status='public')
  context = {'boards':boards}
  return render(request,'pin/boards.html',context)
  

def CreateBoard(request):
  form = BoardForm()
  if request.method == "POST":
    form = BoardForm(request.POST,request.FILES,request.user)
    if form.is_valid():
      board = form.save(commit=False)
      board.user = request.user
      board.save()
      return redirect('home')
  context = {'form':form}
  return render(request,'pin/create_board.html',context)
  

@login_required(login_url='login')
def BoardDetail(request,pk):
  board = Board.objects.get(id=pk)
  pin = Pin.objects.get(id=pk)
  pin_board = board.pin_set.all()
  pin_board_count = pin_board.count()
  context = {'board':board,'pin_board':pin_board,'pin':pin,'pin_board_count':pin_board_count}
  return render(request,'pin/board.html',context)
  
  
@login_required(login_url='account_login')  
def UserProfile(request,pk):
  profile = Profile.objects.get(id=pk)
  user = User.objects.get(profile=pk)
  boards = Board.objects.filter(user=profile.user)
  boards_count = boards.count()
  context = {'profile':profile,'user':user,'boards':boards,'boards_count':boards_count}
  return render(request,'pin/profile.html',context)
  
  
@login_required(login_url='login')  
def editProfile(request,pk):
  profile = Profile.objects.get(id=pk)
  user = User.objects.get(profile=pk)
  form = EditProfileForm(instance=user.profile)
  user_form = UserUpdateForm(instance=user)
  if request.method == "POST":
    form = EditProfileForm(request.POST,request.FILES,instance=user.profile)
    user_form = UserUpdateForm(request.POST,instance=user)
    if form.is_valid() and user_form.is_valid():
      form.save()
      user_form.save()
      return redirect('profile',profile.id)
  context = {'profile':profile,'form':form,'user_form':user_form}
  return render(request,'pin/edit_profile.html',context)