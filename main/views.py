from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .serializers import (Registration_response, RegistrationSerializer,
                            CardSerializer, CardGetSerializer, OrderHistorySerializer)
from .models import UserModel, CardModel, OrderHistoryModel
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
import datetime

class RegistrationView(APIView):
    @swagger_auto_schema(
        operation_id='registration',
        operation_description="Registration",
        # request_body=SmsSerializer(),
        responses={
            '200': Registration_response()
        },
        manual_parameters=[
            openapi.Parameter('name', openapi.IN_QUERY, description="first name",
                              type=openapi.TYPE_STRING),
            openapi.Parameter('last_name', openapi.IN_QUERY, description="last name",
                              type=openapi.TYPE_STRING),
            openapi.Parameter('documentCode', openapi.IN_QUERY, description="passport code",
                              type=openapi.TYPE_STRING),
            openapi.Parameter('documentDate', openapi.IN_QUERY, description="password date",
                              type=openapi.FORMAT_DATE),
        ],
    )
    def post(self, request):
        name = request.GET.get('name', False)
        last_name = request.GET.get('last_name', False)
        documentCode = request.GET.get('documentCode', False)
        if documentCode and len(documentCode) == 9:
            try:
                int(documentCode[:2])
                return Response(data={'StatusMessage':'fail', 'data':'documentCode is not correct 1'})
            except:
                pass
            try:
                int(documentCode[2:9])
                pass
            except:
                return Response(data={'StatusMessage':'fail', 'data':'documentCode is not correct 11'})

            
            passport_code = documentCode.replace(documentCode[:2], documentCode[:2].upper())
            print(passport_code)
            
        else: return Response(data={'StatusMessage':'fail', 'data':'documentCode is not correct 0'})
        documentDate = request.GET.get('documentDate', False)
        if documentDate:
            dat = documentDate.split('.')
            print(dat)
            d = datetime.date(int(dat[2]), int(dat[1]), int(dat[0]))
            
        
        user = UserModel(username=name, first_name=name, last_name=last_name, documentCode=passport_code, documentDate=d)
        user.set_password(passport_code)
        try:
            user.save()
            access_token = AccessToken().for_user(user)
            return Response(data={"StatusMessage": "success", 'Token': str(access_token)})
        except:
            return Response(data={"StatusMessage": "fail", 'data': 'username already exist'})


class RegistartionSecondView(APIView):
    @swagger_auto_schema(
        operation_id='registration',
        operation_description="Registration",
        request_body=RegistrationSerializer(),
        responses={
            '200': RegistrationSerializer()
        },
    )
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            
            return Response(data={'status': 'succes', 'data': serializer.data})
        else:
            return Response(data={'status': 'fail', 'data': serializer.errors})




class CardView(generics.ListCreateAPIView ):
    queryset = CardModel.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = CardSerializer

    @swagger_auto_schema(
        operation_id='card',
        operation_description="Card List",
        responses={
            '200': CardSerializer()
        },
    )

    def get(self, request, *args, **kwargs):
        self.queryset = CardModel.objects.filter(user=request.user)
        return self.list(request, *args, **kwargs)


    @swagger_auto_schema(
        operation_id='card_create',
        operation_description="Card Create",
        request_body=CardSerializer(),
        responses={
            '200': CardSerializer()
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    
    def get_serializer_context(self):
        print('oooooooooooooooooooooo1111111')
        context = super(CardView, self).get_serializer_context()
        context.update({"request": self.request})
        print(context)
        return context


class GetCardView(APIView):
    permission_classes = (IsAuthenticated,)
    
    @swagger_auto_schema(
        operation_id='card_get',
        operation_description="Card get List",
        responses={
            '200': CardGetSerializer()
        },
    )

    def get(self, request):
        cards = CardModel.objects.filter(user=request.user)
        ser = CardGetSerializer(cards, many=True)
        return Response(data=ser.data)


class UseCardView(APIView):
    permission_classes = (IsAuthenticated,)
    @swagger_auto_schema(
        operation_id='use_Card',
        operation_description="Use Card",

        manual_parameters=[
            openapi.Parameter('id', openapi.IN_QUERY, description="id card",
                              type=openapi.TYPE_INTEGER),
        ],
    )
    def post(self, request):
        id = request.GET.get('id', False)
        cards = CardModel.objects.all()
        cards.update(active=False)
        card = cards.get(id=id)
        card.active = True
        card.save()
        return Response(data={'status': 'success'})


class GetCurrentCardView(APIView):
    permission_classes = (IsAuthenticated,)
    @swagger_auto_schema(
        operation_id='get_current_card',
        operation_description="Get current card",
    )
    def post(self, request):
        try:
            card = CardModel.objects.get(user=request.user, active=True)
            return Response(data={'status': 'success', 'id': card.id})
        except:
            return Response(data={'status': 'fail', 'data': 'you have no active cards'})


class GetHistoryView(generics.ListAPIView):
    queryset = OrderHistoryModel.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderHistorySerializer

    @swagger_auto_schema(
        operation_id='order_history',
        operation_description="Order History",
        responses={
            '200': OrderHistorySerializer()
        },
    )

    def get(self, request, *args, **kwargs):
        self.queryset = OrderHistoryModel.objects.filter(user=request.user)
        return self.list(request, *args, **kwargs)


class AddPurchase(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        operation_id='add_purchase',
        operation_description="Add Purchase",
        # responses={
        #     '200': OrderHistorySerializer()
        # },
        manual_parameters=[
            openapi.Parameter('Price', openapi.IN_QUERY, description="Price",
                              type=openapi.TYPE_INTEGER),
            openapi.Parameter('UserDocumentCode', openapi.IN_QUERY, description="UserDocumentCode",
                              type=openapi.TYPE_STRING),
        ],
    )
    def post(self, request):
        price = request.GET.get('Price', False)
        order = OrderHistoryModel(user=request.user, date=datetime.datetime.now(),
                                price=price, location='Mirobod Tumani', market='Korzinka')
        order.save()
        return Response(data={'status': 'ok', 'userInfo': {
            "name": request.user.first_name,
            "lastname": request.user.last_name
        }})