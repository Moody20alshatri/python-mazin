# customers/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Customer
from .forms import RegisterForm, LoginForm, CustomerForm


# أضفها مع باقي الـ imports في الأعلى
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .serializers import CustomerSerializer


# Mixin للتحقق من الصلاحيات
class ManagerRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        # تحقق إذا المستخدم في مجموعة managers
        if not request.user.groups.filter(name='managers').exists() and not request.user.is_superuser:
            messages.error(request, 'ليس لديك صلاحية للقيام بهذه العملية!')
            return redirect('/customers/')
        return super().dispatch(request, *args, **kwargs)


class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'auth/register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'تم إنشاء الحساب بنجاح!')
            return redirect('/customers/')
        return render(request, 'auth/register.html', {'form': form})





class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'auth/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'مرحباً ' + user.username)
            return redirect('/customers/')
        return render(request, 'auth/login.html', {'form': form})





class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'تم تسجيل الخروج بنجاح')
        return redirect('/login/')





class CustomerListView(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request):
        customers = Customer.objects.all()
        return render(request, 'customers/list.html', {'customers': customers})


 
class CustomerAddView(LoginRequiredMixin, ManagerRequiredMixin, View):
    login_url = '/login/'
    def get(self, request):
        form = CustomerForm()
        return render(request, 'customers/add.html', {'form': form})

    def post(self, request):
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم إضافة العميل بنجاح!')
            return redirect('/customers/')
        return render(request, 'customers/add.html', {'form': form})



class CustomerUpdateView(LoginRequiredMixin, ManagerRequiredMixin, View):
    login_url = '/login/'
    def get(self, request, pk):
        customer = get_object_or_404(Customer, pk=pk)
        form = CustomerForm(instance=customer)
        return render(request, 'customers/update.html', {'form': form, 'customer': customer})

    def post(self, request, pk):
        customer = get_object_or_404(Customer, pk=pk)
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم تعديل العميل بنجاح!')
            return redirect('/customers/')
        return render(request, 'customers/update.html', {'form': form, 'customer': customer})



class CustomerDeleteView(LoginRequiredMixin, ManagerRequiredMixin, View):
    login_url = '/login/'
    def get(self, request, pk):
        customer = get_object_or_404(Customer, pk=pk)
        customer.delete()
        messages.success(request, 'تم حذف العميل بنجاح!')
        return redirect('/customers/')
    
    
    # ============================================================
# ====================== API VIEWS ===========================
# ============================================================

# def customer_api_list(request):
#     if request.method == 'GET':
#         customers = Customer.objects.all()
#         serializer = CustomerSerializer(customers, many=True)
#         return JsonResponse(serializer.data, safe=False)

class CustomerAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerAPIDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        customer = get_object_or_404(Customer, pk=pk)
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    def put(self, request, pk):
        customer = get_object_or_404(Customer, pk=pk)
        serializer = CustomerSerializer(customer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        customer = get_object_or_404(Customer, pk=pk)
        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)