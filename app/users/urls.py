from django.urls import path

from .views import CreateUserView, CreateTokenView, ManageUserView

app_name = 'users'
urlpatterns = [
    path('', ManageUserView.as_view(), name='details_and_update'),
    path('create/', CreateUserView.as_view(), name='create'),
    path('token/', CreateTokenView.as_view(), name='token'),
]
