from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.exceptions import NotAuthenticated
from users.models import User, Person, Company, Job, Application
from django.db import transaction


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        user = User(username=validated_data['username'],)
        user.set_password(validated_data['password'])
        user.save()
        return user


class PersonSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()
    user = UserSerializer(required=True)
    username = serializers.CharField(read_only=True)
    password = serializers.CharField(read_only=True)

    class Meta:
        model = Person
        fields = ['token', 'user', 'username', 'password', 'firstname', 'lastname', 'birthday', 'gender', 'resume']

    def create(self, validated_data):
        with transaction.atomic():
            username = validated_data['user.username']
            password = validated_data['user.password']
            user = UserSerializer.create(UserSerializer(), validated_data={'username': username, 'password': password})
            person, created = Person.objects.update_or_create(user=user,
                                                              firstname=validated_data.get('firstname'),
                                                              lastname=validated_data.get('lastname'),
                                                              birthday=validated_data.get('birthday'),
                                                              gender=validated_data.get('gender'),
                                                              resume=validated_data.get('resume'))
            return person


class PersonUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['firstname', 'lastname', 'birthday', 'gender', 'field', 'resume']



class CompanySerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()
    user = UserSerializer(required=True)
    username = serializers.CharField(read_only=True)
    password = serializers.CharField(read_only=True)

    class Meta:
        model = Company
        fields = ['token', 'user', 'username', 'password', 'name', 'creation_date', 'address', 'telephone_number', 'field']

    def create(self, validated_data):
        with transaction.atomic():
            username = validated_data['user.username']
            password = validated_data['user.password']
            user = UserSerializer.create(UserSerializer(), validated_data={'username': username, 'password': password})
            company, created = Company.objects.update_or_create(user=user,
                                                                name=validated_data.get('name'),
                                                                creation_date=validated_data.get('creation_date'),
                                                                address=validated_data.get('address'),
                                                                telephone_number=validated_data.get('telephone_number'),
                                                                field=validated_data.get('field'))

            return company


class CompanyUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['name', 'creation_date', 'address', 'telephone_number', 'field']


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100, write_only=True)

    def validate(self, attrs):
        username = attrs.get("username", None)
        password = attrs.get("password", None)
        user = authenticate(username=username, password=password)
        if user is None:
            raise NotAuthenticated('This user does not exist.')
        return UserSerializer(instance=user).data

    def to_representation(self, instance):
        return instance


class JobSerializer(serializers.ModelSerializer):
    company = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = ('company', 'title', 'image', 'expire_date', 'field', 'salary', 'working_hours')

    def create(self, validated_data):
        job, created = Job.objects.update_or_create(company=self.context['request'].user.company,
                                                    title=validated_data.get('title'),
                                                    image=validated_data.get('image'),
                                                    expire_date=validated_data.get('expire_date'),
                                                    field=validated_data.get('field'),
                                                    salary=validated_data.get('salary'),
                                                    working_hours=validated_data.get('working_hours'))
        return job

    def get_company(self, obj):
        company = CompanySerializer(obj.company).data
        company.pop('user')
        return company


class JobUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ('title', 'image', 'expire_date', 'field', 'salary', 'working_hours')


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ('job')


class ApplicationListSerializer(serializers.ModelSerializer):
    job = serializers.SerializerMethodField(read_only=True)
    person = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Application
        fields = ('job', 'person')

    def get_person(self, obj):
        person = PersonSerializer(obj.person).data
        person.pop('user')
        return person

    def get_job(self, obj):
        job = JobSerializer(obj.job).data
        job.pop('company')
        return job
