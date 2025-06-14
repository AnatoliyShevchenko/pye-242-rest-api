from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.db.models import QuerySet
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.authentication import JWTAuthentication

from chats.models import Chat, Message
from chats.serializers import ChatSerializer, ChatViewSerializer

class ChatsViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(responses={
        200: ChatViewSerializer(many=True)
    })
    def list(self, request: Request) -> Response:
        chats: QuerySet[Chat] = request.user.users_chats.all()
        serializer = ChatViewSerializer(instance=chats, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=ChatSerializer,
        responses={
            201: ChatViewSerializer,
            400: "bad request"
        }
    )
    def create(self, request: Request) -> Response:
        serializer = ChatSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        chat = serializer.save()
        response_serializer = ChatViewSerializer(instance=chat)
        return Response(data=response_serializer.data)

    @swagger_auto_schema(
        responses={
            200: ChatViewSerializer,
            404: "chat not exist"
        }
    )
    def retrieve(self, request: Request, pk: int) -> Response:
        try:
            chat: Chat = request.user.users_chats.get(pk=pk)
        except Chat.DoesNotExist:
            return Response(
                data="chat not exist",
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = ChatViewSerializer(instance=chat)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=ChatSerializer,
        responses={
            200: "chat updated",
            404: "bad request"
        }
    )
    def update(self, request: Request, pk: int) -> Response:
        chat: Chat = get_object_or_404(Chat, pk=pk, users=request.user)
        serializer = ChatSerializer(instance=chat, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data="chat updated", status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=ChatSerializer,
        responses={
            200: "chat updated",
            404: "bad request"
        }
    )
    def partial_update(self, request: Request, pk: int) -> Response:
        chat: Chat = get_object_or_404(Chat, pk=pk, users=request.user)
        serializer = ChatSerializer(instance=chat, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data="chat updated", status=status.HTTP_200_OK)

    @swagger_auto_schema(
        responses={
            200: "chat was removed",
            404: "chat not found"
        }
    )
    def destroy(self, request: Request, pk: int) -> Response:
        chat: Chat = get_object_or_404(Chat, pk=pk, users=request.user)
        chat.delete()
        return Response(data="chat was removed", status=status.HTTP_200_OK)


class MessagesViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def list(self, request: Request) -> Response:
        pass

    def create(self, request: Request) -> Response:
        pass

    def retrieve(self, request: Request, pk: int) -> Response:
        pass

    def update(self, request: Request, pk: int) -> Response:
        pass

    def partial_update(self, request: Request, pk: int) -> Response:
        pass

    def destroy(self, request: Request, pk: int) -> Response:
        pass
