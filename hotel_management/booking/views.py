from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm, LoginForm, LoginForm_USER
from .forms import BookingForm
from .models import Room, Booking
from django.urls import reverse
from .backends import CustomUserBackend
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from .forms import BookingForm
from django.contrib.auth.decorators import login_required
from .forms import EmergencyForm
from .forms import ReviewForm
from .models import CustomUser
from .forms import CheckInForm
from .models import Emergency
def login_choice(request):
    return render(request, 'booking/login_choice.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'booking/register.html', {'form': form})

def staff_register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = True  # 标记为员工，使用Django内置的is_staff字段
            user.save()
            # 添加任何员工特定的逻辑，比如发送欢迎邮件等
            return redirect(reverse('staff_login'))  #
    else:
        form = CustomUserCreationForm()
    return render(request, 'booking/staff_register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm_USER(request.POST)
        if form.is_valid():
            id_card = form.cleaned_data.get('id_card')
            phone_number = form.cleaned_data.get('phone_number')
            # password = form.cleaned_data.get('password')
            user = authenticate(request, id_card=id_card, phone_number=phone_number)
            if user is not None:
                login(request, user)
                return redirect('book_room')  # 或其他适当的重定向
            else:
                form.add_error(None, "Invalid ID card or phone number")
    else:
        form = LoginForm_USER()
    return render(request, 'booking/login.html', {'form': form})


def staff_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            # 检查用户是否存在并且是否是员工
            if user is not None and user.is_staff:
                login(request, user)
                return redirect('staff_home')  # 假设您有一个专门为员工的主页
            else:
                form.add_error(None, "Invalid username or password, or not a staff account")
    else:
        form = LoginForm()

    return render(request, 'booking/staff_login.html', {'form': form})


# @login_required
def book_room(request):
    selected_room = None
    price = None
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()
            return redirect('booking_list')  # 假设有一个预订成功的页面
    else:
        form = BookingForm()
        if 'room' in request.GET:  # 检查请求中是否有房间信息
            selected_room = request.GET['room']
            try:
                room = Room.objects.get(pk=selected_room)
                price = room.price  # 获取所选房间的价格
            except Room.DoesNotExist:
                pass  # 如果没有找到房间，忽略错误

    return render(request, 'booking/book_room.html', {'form': form, 'selected_room': selected_room, 'price': price})

# @login_required
def edit_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            return redirect('booking_list')  # Redirect to the list of bookings
    else:
        form = BookingForm(instance=booking)
    return render(request, 'booking/edit_booking.html', {'form': form, 'booking_id': booking.id})

# @login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    if request.method == 'POST':
        booking.delete()
        return redirect('booking_list')  # 重定向到用户的预订列表页面
    return render(request, 'booking/cancel_booking.html', {'booking': booking})

# @login_required
def booking_list(request):
    # 获取当前登录用户的所有预订
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'booking/booking_list.html', {'bookings': bookings})

# @login_required
def report_emergency(request):
    if request.method == 'POST':
        form = EmergencyForm(request.POST)
        if form.is_valid():
            emergency = form.save(commit=False)
            emergency.user = request.user
            emergency.save()
            return redirect('book_room')  # 重定向到突发状况申报成功页面
    else:
        form = EmergencyForm()

    return render(request, 'booking/report_emergency.html', {'form': form})

# @login_required
def submit_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('book_room')  # 重定向到评价成功页面
    else:
        form = ReviewForm()

    return render(request, 'booking/submit_review.html', {'form': form})

# @login_required
def user_list(request):
    users = CustomUser.objects.all()  # 获取所有用户信息
    return render(request, 'booking/user_list.html', {'users': users})

def staff_home(request):
    return render(request, 'booking/staff_home.html')


def check_in(request):
    selected_room = None
    price = None

    if request.method == 'POST':
        form = CheckInForm(request.POST)
        if form.is_valid():
            booking = form.save()
            return redirect('check_in_success')  # 替换为入住登记成功的页面
    else:
        form = CheckInForm()
        if 'room' in request.GET:
            selected_room = request.GET.get('room')
            try:
                room = Room.objects.get(pk=selected_room)
                price = room.price
            except Room.DoesNotExist:
                pass  # 如果没有找到房间，忽略错误

    return render(request, 'booking/check_in.html', {'form': form, 'selected_room': selected_room, 'price': price})

def check_in_success(request):
    return render(request, 'booking/check_in_success.html')

def staff_manage_bookings(request):
    bookings = Booking.objects.all()  # 获取所有预订
    return render(request, 'booking/staff_manage_bookings.html', {'bookings': bookings})

def staff_cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    if request.method == 'POST':
        booking.delete()
        return redirect('staff_home')  # 重定向到用户的预订列表页面
    return render(request, 'booking/staff_cancel_booking.html', {'booking': booking})

def emergency_reports(request):
    emergencies = Emergency.objects.all().select_related('user')
    return render(request, 'booking/emergency_reports.html', {'emergencies': emergencies})