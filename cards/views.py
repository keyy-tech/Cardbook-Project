from rest_framework import status
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Card
from .serializers import FullCardSerializer, ShortCardSerializer


class RetreivePersonalShortAPIView(ListAPIView):
    serializer_class=ShortCardSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Card.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        serializer = self.get_serializer(queryset,many=True)

        return Response({
            "success": True,
            "data": serializer.data
        },status=status.HTTP_200_OK)
    

class RetreivePersonalFullAPIView(RetrieveAPIView):
    serializer_class=FullCardSerializer
    queryset = Card.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Card.objects.filter(user=user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        serializer = self.get_serializer(instance)

        return Response({
            "status": True,
            "data": serializer.data
        },status=status.HTTP_200_OK)


class CreateCardAPIView(CreateAPIView):
    serializer_class = FullCardSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer=serializer)

        return Response({
            "success": True,
            "msg": "Card created successfully",
            "data": serializer.data
        },status=status.HTTP_201_CREATED)


class UpdateCardAPIView(UpdateAPIView):
    serializer_class = FullCardSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Card.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        user = self.request.user
        serializer.save(user=user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance=instance, 
            data=request.data,
            partial=True
        )

        serializer.is_valid(raise_exception=True)

        self.perform_update(serializer=serializer)

        return Response({
            "success": True,
            "msg": "You have succesfully updated this card",
            "data": serializer.data
        },status=status.HTTP_200_OK)


class DestroyCardAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Card.objects.filter(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        self.perform_destroy(instance=instance)

        return Response({
            "success": True,
            "msg": "You have successfully deleted  this card"
        },status=status.HTTP_200_OK)

