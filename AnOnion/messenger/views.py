from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from messenger.models import Message
from .serializers import MessageSerializer
from django.shortcuts import redirect
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render
from django.http import HttpResponseForbidden




def chat_view(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden("You must be logged in to send a message.")

    if request.method == 'POST':
        message_text = request.POST.get('message')
        if message_text:
            Message.objects.create(text=message_text, user=request.user)

    messages = Message.objects.all()
    return render(request, 'chat.html', {'messages': messages})


class MessageList(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [JSONRenderer]# Додаємо перевірку на аутентифікацію

    def get(self, request):
        # Отримуємо всі повідомлення
        messages = Message.objects.all()
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)  # Зберігаємо з поточним користувачем
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MessageDetail(APIView):
    permission_classes = [IsAuthenticated]  # Додаємо перевірку на аутентифікацію

    def get(self, request, pk):
        try:
            message = Message.objects.get(pk=pk)
        except Message.DoesNotExist:
            return Response({"detail": "Message not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = MessageSerializer(message)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            message = Message.objects.get(pk=pk)
        except Message.DoesNotExist:
            return Response({"detail": "Message not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = MessageSerializer(message, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            message = Message.objects.get(pk=pk)
        except Message.DoesNotExist:
            return Response({"detail": "Message not found."}, status=status.HTTP_404_NOT_FOUND)

        message.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


