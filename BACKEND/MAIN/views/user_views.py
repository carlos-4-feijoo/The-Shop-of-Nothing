from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from MAIN.serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import User
from rest_framework import status


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUser(request):
    type = request.query_params.get("type")
    pk = request.query_params.get("pk")
    if type == "admin":
        if user.is_staff:
            user = User.objects.get(id=pk)
            serializer = UserSerializer(user, many=False)
            return Response(serializer.data)
        else:
            message = {
                "message": "Stop trying to spy on other User you sneaky bastard"}
            return Response(message, status=status.HTTP_403_FORBIDDEN)
    elif type == "normal":
        user = request.user
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)

    message = {"message": "What the heck"}
    return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUsers(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def editUser(request):
    data = request.data
    type = request.query_params.get("type")
    pk = request.query_params.get("pk")
    if type == "admin":
        if user.is_staff:
            user = User.objects.get(id=pk)
            user.username = data["username"]
            user.email = data["email"]
            user.first_name = data["first_name"]
            user.save()
            serializer = UserSerializer(user, many=False)
            return Response(serializer.data)
        else:
            message = {"message": "Hacking is bad my friend"}
            return Response(message, status=status.HTTP_403_FORBIDDEN)
    elif type == "normal":
        user = request.user
        user.username = data["username"]
        user.email = data["email"]
        user.first_name = data["first_name"]
        if data['password'] != '':
            user.password = make_password(data['password'])
        user.save()
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)


@api_view(['POST'])
def registerUser(request):
    data = request.data
    try:
        user = User.objects.create(
            first_name=data['name'],
            username=data['email'],
            email=data['email'],
            password=make_password(data['password'])
        )
        serializer = UserSerializerWithToken(user, many=False)
        return Response(serializer.data)
    except:
        message = {
            "message": "This email already has a User here, we hope no one is trying to steal your identity"}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteUser(request):
    pk = request.query_params.get("pk")
    user = User.objects.get(id=pk)
    user.delete()
    message = {"message": "User was succesfully exterminated"}
    return Response(message)
