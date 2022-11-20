from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from rest_framework import status

from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated

from .models import Follow
from .serializers import CustomUserSerializer

User = get_user_model()

from api.pagination import CustomPageNumberPagination


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = CustomPageNumberPagination
    permission_classes = (IsAuthenticated, )

    @action(
        detail=False,
        methods=['get'],
    )
    def subscriptions(self, request):
        user = request.user
        queryset = self.queryset.filter(
            following__user=user
        )
        pages = self.paginate_queryset(queryset)
        serializer = CustomUserSerializer(
            pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @action(
        methods=[
            'post',
            'delete'
        ],
        detail=True,
    )
    def subscribe(self, request, id):
        print(request, id)
        user = self.request.user
        author = get_object_or_404(User, id=id)
        subscribe = Follow.objects.filter(user=user, author=author)
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if request.method == 'POST':
            if subscribe.exists():
                data = {
                    'errors': ('Ошибка')
                }
                return Response(
                    data=data,
                    status=status.HTTP_400_BAD_REQUEST
                )
            Follow.objects.create(
                user=user,
                author=author
            )
            serializer = CustomUserSerializer(
                author,
                context={
                    'request': request
                }
            )
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        elif request.method == 'DELETE':
            if not subscribe.exists():
                data = {
                    'errors': 'Вы не подписаны на данного автора.'
                }
                return Response(
                    data=data,
                    status=status.HTTP_400_BAD_REQUEST
                )
            subscribe.delete()
            return Response(
                status=status.HTTP_204_NO_CONTENT
            )
