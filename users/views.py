from django.contrib.auth import authenticate
from rest_framework import generics, permissions, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from users.models import Person, Company, User, Job, Application
from users.serializers import PersonSerializer, CompanySerializer, PersonUpdateSerializer, CompanyUpdateSerializer, LoginSerializer, JobSerializer, ApplicationSerializer, ApplicationListSerializer, JobUpdateSerializer
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated 
from users.permissions import IsCompany, IsOwner

class PersonSignUp(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = PersonSerializer


class CompanySignUp(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = CompanySerializer


class Login(generics.CreateAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username, password)
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {'token': token},
            status=200
        )


class ProfileUpdate(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
    authentication_classes = [TokenAuthentication]

    def get_object(self):
        try:
            Person.objects.get(user=self.request.user)
            return self.request.user.person
        except:
            return self.request.user.company

    def get_serializer_class(self):
        try:
            Person.objects.get(user=self.request.user)
            return PersonUpdateSerializer
        except:
            return CompanyUpdateSerializer


class PersonList(generics.ListCreateAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonUpdateSerializer
    authentication_classes = [TokenAuthentication]


class CompanyList(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    authentication_classes = [TokenAuthentication]



class JobList(generics.ListAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]
    ordering_fields = ['create_date', 'salary', 'field']
    search_fields = ['title']
    authentication_classes = [TokenAuthentication]


class JobCreate(generics.CreateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated, IsCompany]
    authentication_classes = [TokenAuthentication]


class JobUpdate(generics.RetrieveUpdateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobUpdateSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    authentication_classes = [TokenAuthentication]


class Apply(generics.CreateAPIView):
    queryset = Job.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request, *args, **kwargs):
        job = Job.objects.get(pk=request.data['job'])
        if timezone.now().date() < job.expire_date:
            submit, created = Application.objects.get_or_create(person=request.user.person, job=job)
            submit.save()
            return Response("Application Added Successfully", status=status.HTTP_200_OK)
        return Response("Job was expired", status=status.HTTP_400_BAD_REQUEST)


class ApplicationList(generics.ListAPIView):
    serializer_class = ApplicationListSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        return Application.objects.filter(job__company=self.request.user.company)

