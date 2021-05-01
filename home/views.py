from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import login

from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics, permissions, status
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView

from .models import Task
from .serializers import TaskSerializer, UserSerializer, RegisterSerializer


# Registation API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user":
            UserSerializer(user, context=self.get_serializer_context()).data,
            "token":
            AuthToken.objects.create(user)[1]
        })


# Login API
class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)


@api_view(['GET',])
@permission_classes((IsAuthenticated, ))
def home(request):

    api_urls = {
        'register   :   /register',
        'login      :   /login',
        'logout     :   /logout',
        'moderator  :   /moderator',
        'detail     :   /detail',
        'create     :   /create',
        'update     :   /update/<str:slug>/',
        'delete     :   /delete/<str:slug>/',
    }
    return Response(api_urls)


# For Moderator to do tasks check
@api_view(['GET',])
@permission_classes((IsAuthenticated, ))
def moderator(request):

    try:
        tasks = Task.objects.all()
    except Task.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)


# For Customer to view there own tasks
@api_view(['GET',])
@permission_classes((IsAuthenticated, ))
def detail(request):

    try:
        tasks = Task.objects.filter(user=request.user)
    except Task.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)


# For creating new task
@api_view(['POST',])
@permission_classes((IsAuthenticated, ))
def create(request):

    task = Task(user=request.user)

    serializer = TaskSerializer(task, data=request.data)
    data = {}
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Update the task (Moderator and Customer both)
@api_view(['PUT',])
@permission_classes((IsAuthenticated, ))
def update(request, slug):

    try:
        task = Task.objects.get(id=slug)
    except Task.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = TaskSerializer(instance=task, data=request.data)
    data = {}
    if serializer.is_valid():
        serializer.save()
        data["success"] = "update successful"
        return Response(data=data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Delete task (Only Customer)
@api_view(['DELETE',])
@permission_classes((IsAuthenticated, ))
def delete(request, slug):

    try:
        task = Task.objects.get(id=slug)
    except Task.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = request.user
    if task.user != user:
        return Response({'response': "Yout don't have permission"})

    oparation = task.delete()
    data = {}
    if oparation:
        data["success"] = "delete successful"
    else:
        data["failure"] = "delete failed"
    return Response(data=data)
