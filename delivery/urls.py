from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/',    views.LoginView.as_view(),    name='login'),
    path('logout/',   views.LogoutView.as_view(),   name='logout'),
    path('deliverys/',                    views.DeliveryListView.as_view(),   name='delivery-list'),
    path('deliverys/add/',                views.DeliveryAddView.as_view(),    name='delivery-add'),
    path('deliverys/update/<int:pk>/',    views.DeliveryUpdateView.as_view(), name='delivery-update'),
    path('deliverys/delete/<int:pk>/',    views.DeliveryDeleteView.as_view(), name='delivery-delete'),
     path('api/delivery/',               views.DeliveryAPIView.as_view(),       name='api-delivery-list'),
    path('api/delivery/<int:pk>/',      views.DeliveryAPIDetailView.as_view(), name='api-delivery-detail'),
]
