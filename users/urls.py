from django.urls import path, include
from users import views
from users.views import PersonSignUp, CompanySignUp, Login, ProfileUpdate, JobList, JobCreate, JobUpdate, Apply, ApplicationList

urlpatterns = [
    path('person-signup/', PersonSignUp.as_view()),
    path('company-signup/', CompanySignUp.as_view()),
    path('login/', Login.as_view()),
    path('accounts/profile/', ProfileUpdate.as_view()),
    path('person-list/', views.PersonList.as_view()),
    path('company-list/', views.CompanyList.as_view()),
    path('job-create/', JobCreate.as_view()),
    path('job-update/<pk>/', JobUpdate.as_view()),
    path('job-list/', JobList.as_view()),
    path('apply/', Apply.as_view()),
    path('job-applications/<pk>/', ApplicationList.as_view()),
]
