from datetime import timedelta

from django.core.mail import send_mail
from django.utils import timezone
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import PasswordResetOTP, Users
from .serializers import (
    ForgetPasswordSerializer,
    ResetPasswordSerializer,
    UserSerializers,
)


# Create your views here.
class UserCreateAPIView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializers
    queryset = Users.objects.all()

    def create(self, request,*args,**kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        return Response(
            {
                "success": True,
                "msg": "User successfully created.",
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        ) 


class UserRetrieveAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializers
    permission_classes = [IsAuthenticated]

    def retrieve(self, request,*args,**kwargs):
        user = request.user

        serializer = self.get_serializer(user)
        return Response({
            "success": True,
            "msg":"User Retrieved",
            "data":serializer.data
        },status=status.HTTP_200_OK
        )

    def update(self, request,*args,**kwargs):
         user = request.user

         if 'password' in request.data:
             return Response({
                 "success": True,
                 "msg": "You cannot update your pasword here. Please use the password reset endpoint."
             },status=status.HTTP_400_BAD_REQUEST)

         serializer = self.get_serializer(
              instance=user,
              data=request.data,
              partial=True
        )
         serializer.is_valid(raise_exception=True)


         self.perform_update(serializer)

         return Response({
              "success":True,
              "msg":"Update succesfully done",
              "data": serializer.data
         },status=status.HTTP_200_OK
         )
         

    def destroy(self,request,*args,**kwargs):
            user = request.user
    
            self.perform_destroy(user)
    
            return Response({
                "success": True,
                "msg": "User deleted successfully"
            },status=status.HTTP_200_OK)



class PasswordResetAPIView(APIView):
     permission_classes = [AllowAny]
     
     def post(self,request,*args,**kwargs):
        serializer = ForgetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]

        try:
             user = Users.objects.filter(email=email)
        except Users.DoesNotExist:
             return Response({
                  "success": False,
                  "msg":"User with this email does not exist"
             },
             status=status.HTTP_404_NOT_FOUND
             )

        code = "123456"

        PasswordResetOTP.objects.filter(
             user=user,
             is_used=False
        ).update(
             is_used=True
        )

        PasswordResetOTP.objects.create(
             user=user,
             code=code,
             expires_at=timezone.now() + timedelta(minutes=10)
        )

        send_mail(
            subject="Cardbook Project Reset Password",
            message=f"The message code {code}",
            from_email=None,
            recipient_list=[user.email]
        )

        return Response({
             "success": True,
             "msg": "Password has being succesfully being to sent to the email"
        },
        status=status.HTTP_200_OK)



class ResetPasswordAPIView(APIView):
     permission_classes = [AllowAny]

     def post(self,request,*args,**kwargs):
          # get the serializers
          serializer = ResetPasswordSerializer(data=request.data)

          # validate the serializer
          serializer.is_valid(raise_exception=True)

          email = serializer.validated_data["email"]
          submitted_code = serializer.validated_data["submitted_code"]
          new_password = serializer.validated_data["new_password"]

          # checking for the user
          try:
            user = Users.objects.get(email=email)
          except Users.DoesNotExist:
            return Response({
                "success": False,
                "msg": "User does not exist"
            }, status=status.HTTP_404_NOT_FOUND)

          # checking for the verification code
          try:
            code = PasswordResetOTP.objects.get(
                user=user,
                is_used=False
                )
          except PasswordResetOTP.DoesNotExist:
              return Response({
                  "success": False,
                  "msg": "Code does not exists"
              },status=status.HTTP_404_NOT_FOUND)


          # checking to see code has being used
          if timezone.now() > code.expires_at:
              return Response({
                  "success": False,
                  "msg": "Code has expired, kindly request for a new code"
              },status=status.HTTP_400_BAD_REQUEST)


          if submitted_code != code.code:
              return Response({
                  "success": False,
                  "msg": "Invalid Code, Try again"
              },status=status.HTTP_400_BAD_REQUEST)


          user.set_password(new_password)
          user.save()

          return Response({
              "success": True,
              "msg": "You have succesfuly changed your pasword"
          },status=status.HTTP_200_OK)
              


        

          
            

          

         
            
          
            


