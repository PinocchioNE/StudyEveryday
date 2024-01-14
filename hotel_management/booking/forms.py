from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django import forms
from .models import Emergency
from .models import Review
from .models import Booking, Room
from django.forms.widgets import SelectDateWidget
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('id_card', 'phone_number', 'gender', 'age')

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class LoginForm_USER(forms.Form):
    id_card = forms.CharField(required=True)
    phone_number = forms.CharField(required=True)


    class Meta:
        fields = ['id_card', 'phone_number']


# class BookingForm(forms.ModelForm):
#     class Meta:
#         model = Booking
#         fields = ['room', 'start_date', 'end_date']


class BookingForm(forms.ModelForm):
    room = forms.ModelChoiceField(queryset=Room.objects.all(), empty_label="Choose a room")
    start_date = forms.DateField(widget=SelectDateWidget())
    end_date = forms.DateField(widget=SelectDateWidget())
    price = forms.CharField(widget=forms.HiddenInput(), required=False)
    class Meta:
        model = Booking
        fields = ['room', 'start_date', 'end_date']

class EmergencyForm(forms.ModelForm):
    class Meta:
        model = Emergency
        fields = ['room_number', 'emergency_type', 'description']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['comment', 'rating']


class CheckInForm(forms.ModelForm):
    username = forms.CharField()
    id_card = forms.CharField(max_length=18, required=True)
    phone_number = forms.CharField(max_length=15, required=True)
    start_date = forms.DateField(widget=SelectDateWidget())
    end_date = forms.DateField(widget=SelectDateWidget())
    # ... 其他用户个人信息的字段 ...

    class Meta:
        model = Booking
        fields = ['room', 'start_date', 'end_date']
        # 你可以添加更多的预订相关字段

    def save(self, commit=True):
        # 使用身份证号和电话号码获取或创建用户
        user, created = CustomUser.objects.get_or_create(
            id_card=self.cleaned_data['id_card'],
            defaults={'phone_number': self.cleaned_data['phone_number']})

        # 添加用户个人信息的处理逻辑

        booking = super(CheckInForm, self).save(commit=False)
        booking.user = user
        if commit:
            booking.save()
        return booking