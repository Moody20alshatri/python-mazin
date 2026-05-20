# customers/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Customer

# ============================================================
# فورم تسجيل مستخدم جديد
# ============================================================
class RegisterForm(UserCreationForm):
    
    # حقل الإيميل - غير موجود افتراضياً في UserCreationForm
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    # ليش؟ نضيف كلاسات Bootstrap لكل حقل عشان يكون شكله حلو
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label


# ============================================================
# فورم تسجيل الدخول
# ============================================================
class LoginForm(AuthenticationForm):
    
    # ليش نستخدم AuthenticationForm؟
    # لأنه جاهز من Django ويتحقق من اسم المستخدم وكلمة المرور تلقائياً
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label


# ============================================================
# فورم إضافة عميل
# ============================================================
class CustomerForm(forms.ModelForm):
    
    class Meta:
        model = Customer
        # الحقول اللي تظهر في الفورم
        fields = ['name', 'phone', 'address']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label