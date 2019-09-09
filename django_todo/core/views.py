from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.http import Http404
from django.shortcuts import get_object_or_404

from .models import Todo
from .serializers import TodoSerializer
import datetime



class APIRoot(APIView):
    """
    API root view listing all routes.
    """
    def get(self, request):
        return Response({
            'todos': reverse('todo-list-view', request=request)
        })


class TodoList(APIView):
    """
    List all to-dos or create a new one.
    """
    def get(self, request, format=None):
        todos = Todo.objects.all()
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        print(request.data)
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TodoItem(APIView):
    """
    Retrieve, delete, update or update partially a to-do instance.
    """
    def get(self, request, pk, format=None):
        todo = get_object_or_404(Todo, id=pk)
        serializer = TodoSerializer(todo)
        return Response(serializer.data)

    def patch(self, request, pk, format=None):
        todo = get_object_or_404(Todo, id=pk)
        todo.conclused_at = datetime.date.today()
        serializer = TodoSerializer(todo, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        todo = get_object_or_404(Todo, id=pk)
        todo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk, format=None):
        todo = get_object_or_404(Todo, id=pk)
        serializer = TodoSerializer(todo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
