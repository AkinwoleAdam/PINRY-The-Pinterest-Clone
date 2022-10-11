from django.shortcuts import render,redirect
from .models import *
from .forms import PinForm,EditProfileForm,UserUpdateForm,BoardForm,CommentForm,SaveToBoardForm,EditPinForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
# Create your views here

def home(request):
  pins = Pin.objects.all()
  context = {'pins':pins}
  return render(request,'pin/home.html',context)
 
def search(request):
  pins = Pin.objects.all()
  boards = Board.objects.filter(status='public')
  if request.method == 'GET':
    query = request.GET.get('q')
    submitbutton = request.GET.get('submit')
    if query is not None:
      lookups = Q(name__icontains=query) | Q(description__icontains=query)
      results = Pin.objects.filter(lookups).distinct()
      context={'results': results,'submitbutton': submitbutton}
      return render(request, 'pin/search.html', context)
    else:
      return render(request, 'pin/search.html')
  else:
    return render(request, 'pin/search.html')
 
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
def editPin(request,pk):
  try:
    pin = Pin.objects.get(id=pk,user=request.user)
  except:
    return render(request, 'pin/404.html')
  form = EditPinForm(instance=pin)
  if request.method == "POST":
    form = EditPinForm(request.POST,instance=pin)
    if form.is_valid():
      instance = form.save(commit=False)
      instance.user = request.user
      instance.save()
      return redirect(request.META.get('HTTP_REFERER'))
  context = {'pin':pin,'form':form}
  return render(request,'pin/edit_pin.html',context)

@login_required(login_url='login')  
def deletePin(request,pk):
  try:
    pin = Pin.objects.get(id=pk,user=request.user)
  except:
    return render(request,'pin/404.html')
  if request.method == "POST":
    pin.delete()
    return redirect('home')
  context = {'pin':pin}
  return render(request,'pin/delete_pin.html',context)

@login_required(login_url='login')  
def DeleteComment(request,pk):
  pin = Pin.objects.get(id=pk)
  comment = Comment.objects.get(id=pk)
  if request.method == "POST":
    comment.delete()
    return redirect('pin_detail',comment.pin.id)
  context = {'obj':comment,'pin':pin}
  return render(request,'pin/delete.html',context)

@login_required(login_url='login') 
def AllBoards(request):
  boards = Board.objects.filter(status='public')
  context = {'boards':boards}
  return render(request,'pin/boards.html',context)
  
@login_required(login_url='login')
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
 
@login_required(login_url='login')  
def editBoard(request,pk):
  try:
    board = Board.objects.get(id=pk,user=request.user)
  except:
    return render(request, 'pin/404.html')
  form = BoardForm(instance=board)
  if request.method == "POST":
    form = BoardForm(request.POST,request.FILES,instance=board)
    if form.is_valid():
      board = form.save(commit=False)
      board.user = request.user
      board.save()
      return redirect('all_boards')
  context = {'board':board,'form':form}
  return render(request,'pin/edit_board.html',context)

@login_required(login_url='login')  
def deleteBoard(request,pk):
  try:
    board = Board.objects.get(id=pk,user=request.user)
  except:
    return render(request,'pin/404.html')
  if request.method == "POST":
    board.delete()
    return redirect('all_boards')
  context = {'board':board}
  return render(request,'pin/delete_board.html',context)  
  
@login_required(login_url='account_login')  
def UserProfile(request,pk):
  profile = Profile.objects.get(id=pk)
  user = User.objects.get(profile=pk)
  pins = Pin.objects.filter(user=profile.user)
  pins_count = pins.count()
  boards = Board.objects.filter(user=profile.user)
  public_boards = Board.objects.filter(status='public',user=profile.user)
  public_boards_count = public_boards.count()
  boards_count = boards.count()
  context = {'profile':profile,'user':user,'boards':boards,'boards_count':boards_count,'pins':pins,'pins_count':pins_count,'public_boards':public_boards,'public_boards_count':public_boards_count}
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
  
def error_404(request, exception):
  return render(request, 'pin/404.html')  