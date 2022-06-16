from rest_framework.views import APIView, Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.http import Http404, HttpResponse
from django.contrib.auth.models import User, Group, Permission

import json
import requests

from .serializers import *
from .models import Address, Militant, PaymentNorm, Core, Payment


def detail(queryset, msg_error):
    if len(queryset) > 0:
        return queryset[0]
    else:
        return Response(msg_error, status=status.HTTP_404_NOT_FOUND)


class Address_APIView(APIView):
    def get_queryset(self):
        return Address.objects.all()

    def get(self, request, format=None):
        address = self.get_queryset()
        serializer = AddressSerializer(address, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = AddressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Address_APIView_Detail(APIView):
    def get_queryset(self):
        address = Address.objects.filter(pk=self.kwargs['pk'])
        return address

    def get(self, request, format=None):
        address = detail(self.get_queryset(), 'Address does not exist.')
        serializer = AddressSerializer(address)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, format=None):
        address = detail(self.get_queryset(), 'Address does not exist.')
        serializer = AddressSerializer(address, data=request.data)
        if serializer.is_valid():
            serializer.update(address, serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        address = self.get_queryset(pk)
        address.delete()
        return Response({'detail': 'Address deleted'}, status=status.HTTP_200_OK)


class DeclarationDate_APIView(APIView):
    def get_queryset(self):
        return DeclarationDate.objects.all()

    def get(self, request, format=None):
        declaration_date = self.get_queryset()
        serializer = DeclarationDateSerializer(declaration_date, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = DeclarationDateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeclarationDate_APIView_Detail(APIView):
    def get_queryset(self):
        declaration_date = DeclarationDate.objects.filter(pk=self.kwargs['pk'])
        return declaration_date

    def put(self, request, format=None):
        declaration_date = detail(
            self.get_queryset(), 'Declaration date does not exist.')
        serializer = DeclarationDateSerializer(
            declaration_date, data=request.data)
        if serializer.is_valid():
            serializer.update(declaration_date, serializer.data)
        return Response(serializer.errors, status=status.HTTP_200_OK)

    def delete(self, request, pk, format=None):
        declaration_date = self.get_queryset(pk)
        declaration_date.delete()
        return Response({'detail': 'Declaration date deleted'}, status=status.HTTP_200_OK)


class PaymentDate_APIView(APIView):
    def get_queryset(self):
        return PaymentDate.objects.all()

    def get(self, request, format=None):
        serializer = PaymentDateSerializer(
            self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = PaymentDateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentDate_APIView_Detail(APIView):
    def get_queryset(self):
        return PaymentDate.objects.filter(pk=self.kwargs['pk'])

    def put(self, request, pk, format=None):
        payment_date = detail(self.get_queryset(),
                              'Payment date does not exist')
        serializer = PaymentDateSerializer(payment_date, data=request.data)
        if serializer.is_valid():
            serializer.update(payment_date, serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        core = get_object_or_404(Core, pk=pk)
        core.delete()
        return HttpResponse({'detail': 'Payment date deleted'}, status=status.HTTP_204_NO_CONTENT)


class Core_APIView(APIView):
    def get_queryset(self):
        return Core.objects.all()

    def get(self, request, format=None):
        cores = self.get_queryset()
        serializer_cores = CoreSerializer(cores, many=True)
        return Response(serializer_cores.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = CoreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Core_APIView_Detail(APIView):
    def get_queryset(self):
        return Core.objects.filter(pk=self.kwargs['pk'])

    def get(self, request, pk, format=None):
        core = detail(self.get_queryset(), 'Core does not exist.')
        serializer = CoreDetailSerializer(core)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        core = self.get_queryset(pk)
        serializer = CoreSerializer(core, data=request.data)
        if serializer.is_valid():
            serializer.update(core, serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        core = get_object_or_404(Core, pk=pk)
        core.delete()
        return HttpResponse({'detail': 'Core deleted'}, status=status.HTTP_204_NO_CONTENT)


class Militant_APIView(APIView):
    def get_queryset(self):
        militant = Militant.objects.all()
        return militant

    def get(self, request, format=None, *args, **kwargs):
        militant = self.get_queryset()
        serializer = MilitantSerializer(militant, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = MilitantPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Militant_APIView_Detail(APIView):
    def get_queryset(self):
        militant = Militant.objects.filter(pk=self.kwargs['pk'])
        return militant

    def get(self, request, pk, format=None):
        militant = detail(self.get_queryset(), 'Militant does not exist')
        serializer = MilitantDeclarationsSerializer(militant)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        militant = detail(self.get_queryset(), 'Militant does not exist')
        serializer = MilitantDeclarationsSerializer(
            militant, data=request.data)
        if serializer.is_valid():
            serializer.update(militant, serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        militant = self.get_queryset(pk)
        militant.delete()
        return HttpResponse({'detail': 'Militant deleted'}, status=status.HTTP_400_BAD_REQUEST)


class PaymentDeclaration_APIView(APIView):
    def get_queryset(self):
        return PaymentDeclaration.objects.all()

    def post(self, request, format=None):
        serializer = PaymentDeclarationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Payment_APIView(APIView):
    def get_queryset(self):
        return Payment.objects.all()

    def get(self, request, format=None):
        payment = self.get_queryset()
        serializer = PaymentSerializer(payment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Debts_APIView(APIView):
    def get_queryset(self):
        return Militant.objects.all()

    def get(self, request, format=None):
        arrears = MilitantDebtsSerializer.serialize(self.get_queryset(), True)
        return Response(arrears, status=status.HTTP_200_OK)


class Debts_APIViews_Detail(APIView):
    def get_queryset(self):
        return Militant.objects.none

    def get(self, request, pk, format=None):
        militant = Militant.objects.filter(pk=pk)
        if len(militant) != 0:
            if len(militant[0].arrears_fees()) == 0:
                body = {'message': 'Militant it is clean'}
                return HttpResponse(json.dumps(body), status=status.HTTP_404_NOT_FOUND, content_type='application/json')
            else:
                serializer = MilitantDebtsSerializer.serialize(militant)
                return Response(serializer, status=status.HTTP_200_OK)
        else:
            body = {'error': 'Militant do not exist'}
            return HttpResponse(json.dumps(body), status=status.HTTP_404_NOT_FOUND, content_type='application/json')


class User_APIView(APIView):
    def get_queryset(self):
        return User.objects.all()

    def get(self, request, format=None):
        serializer = UserSerializer(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class User_APIView_Detail(APIView):
    def get_queryset(self, pk):
        return get_object_or_404(User, pk=pk)

    def get(self, request, pk, format=None):
        user = self.get_queryset(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        user = self.get_queryset(pk)
        serializer = UserSerializer(user, request.data)
        if serializer.is_valid():
            serializer.update(user, serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Group_APIView(APIView):
    def get_queryset(self):
        return Group.objects.all()

    def get(self, request, format=None):
        serializer = GroupSerializer(self.get_queryset(), many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Group_APIViews_Details(APIView):
    def get_queryset(self, pk):
        Permission.objects.all()
        return get_object_or_404(Group, pk=pk)

    def get(self, request, pk, format=None):
        serializer = GroupSerializer(self.get_queryset(pk))
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        auth_group = self.get_queryset(pk)
        serializer = GroupSerializer(auth_group, data=request.data)
        if serializer.is_valid():
            serializer.update(auth_group, serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Permission_APIView(APIView):
    def get_queryset(self):
        return Permission.objects.all()

    def get(self, request, format=None):
        serializer = PermissionSerializer(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
