from django.urls import path, include
from .views import SensorList, SensorDetail, StationList, StationDetail, \
    SourceList, SourceDetail, MeteoDataList, MeteoDataDetail, ProfileList, ProfileDetail, AccessView, AccessDetail
# from rest_framework.authtoken.views import obtain_auth_token
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from django.contrib.auth import authenticate, login, logout


# class LoginView(APIView):
#     def post(self, request):
#         username = request.data.get('username')
#         password = request.data.get('password')
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return Response({'detail': 'Authentication successful.'})
#         else:
#             return Response({'detail': 'Invalid credentials.'})
#
#
# class LogoutView(APIView):
#     def post(self, request):
#         logout(request)
#         return Response({'detail': 'Logout successful.'})


urlpatterns = [
    path('sensors/', SensorList.as_view(), name='sensor_list'),
    path('sensors/<int:pk>/', SensorDetail.as_view(), name='sensor_detail'),
    path('stations/', StationList.as_view(), name='station_list'),
    path('stations/<int:pk>/', StationDetail.as_view(), name='station_detail'),
    path('sources/', SourceList.as_view(), name='source_list'),
    path('sources/<int:pk>/', SourceDetail.as_view(), name='source_detail'),
    path('meteodata/', MeteoDataList.as_view(), name='meteo_data_list'),
    path('meteodata/<int:pk>/', MeteoDataDetail.as_view(), name='meteo_data_detail'),
    path('profiles/', ProfileList.as_view(), name='profile_list'),
    path('profiles/<int:pk>/', ProfileDetail.as_view(), name='profile_detail'),
    # path('login/', LoginView.as_view(), name='api_login'),
    # path('logout/', LogoutView.as_view(), name='api_logout'),
    path('access/', AccessView.as_view(), name='access_login'),
    path('access/<int:pk>/', AccessDetail.as_view(), name='access_logout'),
    path('auth/', include('rest_registration.api.urls')),
]