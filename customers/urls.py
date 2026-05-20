# customers/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/',    views.LoginView.as_view(),    name='login'),
    path('logout/',   views.LogoutView.as_view(),   name='logout'),

    # Customers CRUD
    path('customers/',                    views.CustomerListView.as_view(),   name='customer-list'),
    path('customers/add/',                views.CustomerAddView.as_view(),    name='customer-add'),
    path('customers/update/<int:pk>/',    views.CustomerUpdateView.as_view(), name='customer-update'),
    path('customers/delete/<int:pk>/',    views.CustomerDeleteView.as_view(), name='customer-delete'),

     # API
    path('api/customers/',              views.CustomerAPIView.as_view(),       name='api-customer-list'),
    path('api/customers/<int:pk>/',     views.CustomerAPIDetailView.as_view(), name='api-customer-detail'),
]