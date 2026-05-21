# deliverys/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Delivery
from .forms import RegisterForm, LoginForm, DeliveryForm

# أضفها مع باقي الـ imports في الأعلى
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .serializers import DeliverySerializer




# Mixin للتحقق من الصلاحيات
class ManagerRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        # تحقق إذا المستخدم في مجموعة managers
        if not request.user.groups.filter(name='managers').exists() and not request.user.is_superuser:
            messages.error(request, 'ليس لديك صلاحية للقيام بهذه العملية!')
            return redirect('/deliverys/')
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
            return redirect('/deliverys/')
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
            return redirect('/deliverys/')
        return render(request, 'auth/login.html', {'form': form})





class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'تم تسجيل الخروج بنجاح')
        return redirect('/login/')





class DeliveryListView(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request):
        deliverys = Delivery.objects.all()
        return render(request, 'delivery/list.html', {'deliverys': deliverys})


 
class DeliveryAddView(LoginRequiredMixin, ManagerRequiredMixin, View):
    login_url = '/login/'
    def get(self, request):
        form = DeliveryForm()
        return render(request, 'delivery/add.html', {'form': form})

    def post(self, request):
        form = DeliveryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم إضافة الطلب بنجاح!')
            return redirect('/deliverys/')
        return render(request, 'delivery/add.html', {'form': form})



class DeliveryUpdateView(LoginRequiredMixin, ManagerRequiredMixin, View):
    login_url = '/login/'
    def get(self, request, pk):
        delivery = get_object_or_404(Delivery, pk=pk)
        form = DeliveryForm(instance=delivery)
        return render(request, 'delivery/update.html', {'form': form, 'delivery': delivery})

    def post(self, request, pk):
        delivery = get_object_or_404(Delivery, pk=pk)
        form = DeliveryForm(request.POST, instance=delivery)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم تعديل الطلب بنجاح!')
            return redirect('/deliverys/')
        return render(request, 'delivery/update.html', {'form': form, 'delivery': delivery})



class DeliveryDeleteView(LoginRequiredMixin, ManagerRequiredMixin, View):
    login_url = '/login/'
    def get(self, request, pk):
        delivery = get_object_or_404(Delivery, pk=pk)
        delivery.delete()
        messages.success(request, 'تم حذف الطلب بنجاح!')
        return redirect('/deliverys/')
    # ============================================================
# ====================== API VIEWS ===========================
# ============================================================

# def delivery_api_list(request):
#     if request.method == 'GET':
#         deliveries = Delivery.objects.all()
#         serializer = DeliverySerializer(deliveries, many=True)
#         return JsonResponse(serializer.data, safe=False)

class DeliveryAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        deliveries = Delivery.objects.all()
        serializer = DeliverySerializer(deliveries, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DeliverySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeliveryAPIDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        delivery = get_object_or_404(Delivery, pk=pk)
        serializer = DeliverySerializer(delivery)
        return Response(serializer.data)

    def put(self, request, pk):
        delivery = get_object_or_404(Delivery, pk=pk)
        serializer = DeliverySerializer(delivery, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        delivery = get_object_or_404(Delivery, pk=pk)
        delivery.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)