from django.conf import settings
from django.contrib import messages
from django.utils import timezone
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_protect

from rest_framework import status as s
from rest_framework.response import Response
from rest_framework.decorators import api_view

from transaction import outflows
from .models import Transaction

import json
import requests

def get_transaction_id(ref):
    if '_' in ref:
        return ref.split('_')[0]
    return ref

""" api_view(['POST', 'GET'])
def save_naira_payment_info(request):
    print('** Naira payment info - GET **')
    print(request.GET)

    print('** Naira payment info - POST **')
    print(request.POST)

    ref = request.GET.get('txref', '')
    if ref == '':
        ref = json.loads(request.GET['resp'])['tx']['txRef']
    transaction = Transaction.objects.get(transaction_id=get_transaction_id(ref))

    cancelled = request.GET.get('cancelled', '')
    if cancelled:
        transaction.status = 'Cancelled'
        transaction.save()
    else:
        try:
            tx = json.loads(request.POST['resp'])['tx']
        except KeyError:
            tx = json.loads(request.GET['resp'])['tx']
        inflow = transaction.inflow
        inflow.reference = tx['flwRef']
        inflow.updated_at = timezone.now()
        inflow.save()

    return redirect(reverse_lazy('customer:index')) """

# api_view(['POST', 'GET'])
# @csrf_protect
""" def save_naira_payment_info(request):
    print('** Naira payment info - GET **')
    print(request.GET)

    # print('** Naira payment info - POST **')
    # print(request.POST)

    transaction_id = get_transaction_id(request.GET.get('txref', ''))
    flw_ref = request.GET.get('flwref')

    transaction = Transaction.objects.get(transaction_id=transaction_id)
    cancelled = request.GET.get('cancelled', '')
    if cancelled:
        transaction.status = 'Cancelled'
        transaction.save()
    else:
        inflow = transaction.inflow
        inflow.reference = flw_ref
        inflow.updated_at = timezone.now()
        inflow.save()
    return redirect(reverse_lazy('customer:index')) """

from django.http import HttpResponse
@csrf_protect
def save_naira_payment_info(request):
    print('** Naira payment info - GET **')
    print(request.GET)
    return HttpResponse('Redirection Successful')

@api_view(['POST'])
def handle_naira_update(request):
    data = request.data
    # Payment
    if data['event.type'] == 'CARD_TRANSACTION':
        print('** Naira payment update - card **')
        print(request.data)
        transaction = Transaction.objects.get(
            transaction_id=get_transaction_id(data['txRef']))

        inflow = transaction.inflow
        if inflow.is_complete == False:
            if data['status'] == 'successful':
                inflow.source_account_provider = 'card'
                inflow.source_account_number = '{}{}{}'.format(
                    data['entity']['card6'], '******', data['entity']['card_last4'])
                inflow.updated_at = timezone.now()
                inflow.is_complete = True
                inflow.save()

                # initiate cedi transfer
                # outflows.initiate_cedi_transfer(transaction, "NGN to GHS")
                return Response({'message': 'Success'}, status=s.HTTP_200_OK)
            return Response({'message': 'Error'}, status=s.HTTP_500_INTERNAL_SERVER_ERROR)
    elif data['event.type'] == 'BANK_TRANSFER_TRANSACTION':
        """
        {'id': 321588591, 'txRef': 'SMNY201025143737', 'flwRef': '000013201025160012000217290614', 'orderRef': 'URF_1603637754544_1052035', 'paymentPlan': None, 'paymentPage': None, 'createdAt': '2020-10-25T15:03:31.000Z', 'amount': 200, 'charged_amount': 200, 'status': 'successful', 'IP': '::ffff:127.0.0.1', 'currency': 'NGN', 'appfee': 2.8, 'merchantfee': 0, 'merchantbearsfee': 1, 'customer': {'id': 229508916, 'phone': None, 'fullName': 'Anonymous customer', 'customertoken': None, 'email': 'alwaysdeone@gmail.com', 'createdAt': '2020-10-25T14:55:54.000Z', 'updatedAt': '2020-10-25T14:55:54.000Z', 'deletedAt': None, 'AccountId': 70515}, 'entity': {'account_number': '0009432630', 'first_name': 'OLADAYO JOSHUA', 'last_name': 'OSIKOYA'}, 'event.type': 'BANK_TRANSFER_TRANSACTION'}
        """
        print('** Naira payment update - bank transfer **')
        print(request.data)
        transaction = Transaction.objects.get(
            transaction_id=get_transaction_id(data['txRef']))

        inflow = transaction.inflow
        if inflow.is_complete == False:
            if data['status'] == 'successful':
                inflow.source_account_provider = 'bank transfer'
                inflow.source_account_number = data['entity']['account_number']
                inflow.source_account_name = '{} {}'.format(data['entity']['first_name'], data['entity']['last_name'])
                inflow.updated_at = timezone.now()
                inflow.is_complete = True
                inflow.save()

                # initiate cedi transfer
                outflows.initiate_cedi_transfer(transaction, "NGN to GHS")
                return Response({'message': 'Success'}, status=s.HTTP_200_OK)
            return Response({'message': 'Error'}, status=s.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        print('** Naira transfer update **')
        print(request.data)

        transaction = Transaction.objects.get(
            transaction_id=get_transaction_id(data['transfer']['reference']))
        if data['transfer']['status'] == 'SUCCESSFUL':
            transaction.outflow.updated_at = timezone.now()
            transaction.outflow.is_complete = True
            transaction.outflow.save()

            transaction.status = 'Successful'
            transaction.is_complete = True
            transaction.save()
            return Response({'message': 'Success'}, status=s.HTTP_200_OK)

        return Response({'message': 'Error'}, status=s.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def handle_cedi_transfer_update(request):
    print('** Cedi transfer update **')
    print(request.data)
    data = request.data
    status = data['status']

    transaction = Transaction.objects.get(
        transaction_id=data['metadata']['transaction_id'])
    if transaction.outflow.is_complete == False:
        if status == 'SUCCESS':
            transaction.outflow.reference = data['transaction_id']
            transaction.outflow.is_complete = True
            transaction.outflow.updated_at = timezone.now()
            transaction.outflow.save()

            transaction.status = 'Successful'
            transaction.is_complete = True
            transaction.save()
            return Response({'message': 'Success'}, status=s.HTTP_200_OK)
    return Response({'message': 'Already created.'}, status=s.HTTP_201_CREATED)

@api_view(['GET'])
def save_cedi_payment_info(request):
    print('** Cedi payment info **')
    print(request.data)
    data = request.GET
    transaction = Transaction.objects.get(
        transaction_id=data['metadata[order_id]'])
    inflow = transaction.inflow
    inflow.reference = data['reference']
    inflow.source_account_provider = data['source[type]']
    inflow.source_account_number = data['source[number]']
    inflow.updated_at = timezone.now()
    inflow.save()

    return redirect(reverse_lazy('customer:index'))

@api_view(['POST'])
def handle_cedi_payment_update(request):
    print('** Cedi payment update **')
    print(request.data)
    data = request.data
    transaction = Transaction.objects.get(
        transaction_id=data['metadata']['order_id'])
    inflow = transaction.inflow
    if inflow.is_complete == False:
        if data['status'] == 'successful':
            inflow.updated_at = timezone.now()
            inflow.is_complete = True
            inflow.save()

            # initiate naira transfer
            outflows.initiate_naira_transfer(transaction)

            return Response({'message': 'Success'}, status=s.HTTP_200_OK)
        return Response({'message': 'Error'}, status=s.HTTP_500_INTERNAL_SERVER_ERROR)