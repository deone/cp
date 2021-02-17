from django.conf import settings
from django.contrib import messages
from django.utils import timezone
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt

from rest_framework import status as s
from rest_framework.response import Response
from rest_framework.decorators import api_view

from transaction import outflows
from .models import Transaction
from .utils import (
    get_transaction_id, update_inflow 
)

import json
import requests

api_view(['POST', 'GET'])
@csrf_exempt
def save_naira_payment_info(request):
    print('** Naira payment info - GET **')
    print(request.GET)

    print('** Naira payment info - POST **')
    print(request.POST)

    transaction_id = get_transaction_id(request.GET.get('txref', ''))
    flw_ref = request.GET.get('flwref')

    transaction = Transaction.objects.get(transaction_id=transaction_id)
    cancelled = request.GET.get('cancelled', '')
    if cancelled:
        transaction.status = 'Cancelled'
        transaction.save()
    else:
        inflow = transaction.inflow
        update_inflow(inflow, **{'reference': flw_ref})
    return redirect(reverse_lazy('customer:activity'))

@api_view(['POST'])
def handle_naira_update(request):
    data = request.data
    transaction_type = data.get('event.type', None)

    # Payment
    if transaction_type is None or transaction_type == 'CARD_TRANSACTION':
        print('** Naira payment update - card **')
        print(request.data)
        transaction = Transaction.objects.get(
            transaction_id=get_transaction_id(data['txRef']))

        inflow = transaction.inflow
        if inflow.is_complete == False:
            if data['status'] == 'successful':
                is_card = data.get('entity', None).get('card6', None)
                if is_card:
                    inflow_data = {
                        'reference': data['flwRef'],
                        'source_account_provider': 'card',
                        'source_account_number': '{}{}{}'.format(
                            data['entity']['card6'], '******', data['entity']['card_last4'])
                    }
                else:
                    inflow_data = {
                        'reference': data['flwRef'],
                        'source_account_provider': 'bank transfer',
                        'source_account_number': data['entity']['account_number'],
                        'source_account_name': '{} {}'.format(
                            data['entity']['first_name'], data['entity']['last_name'])
                    }

                update_inflow(inflow, **inflow_data)
                outflows.initiate_cedi_transfer(transaction, "NGN to GHS")
                return Response({'message': 'Success'}, status=s.HTTP_200_OK)
            return Response({'message': 'Error'}, status=s.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({'message': 'Already created.'}, status=s.HTTP_201_CREATED)

    elif transaction_type == 'BANK_TRANSFER_TRANSACTION':
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
                inflow_data = {
                    'reference': data['flwRef'],
                    'source_account_provider': 'bank transfer',
                    'source_account_number': data['entity']['account_number'],
                    'source_account_name': '{} {}'.format(
                        data['entity']['first_name'], data['entity']['last_name'])
                }
                update_inflow(inflow, **inflow_data)

                # initiate cedi transfer
                outflows.initiate_cedi_transfer(transaction, "NGN to GHS")
                return Response({'message': 'Success'}, status=s.HTTP_200_OK)
            return Response({'message': 'Error'}, status=s.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        print('** Naira transfer update **')
        print(request.data)

        transaction = Transaction.objects.get(
            transaction_id=get_transaction_id(data['transfer']['reference']))
        outflow = transaction.outflow
        if outflow.is_complete == False:
            if data['transfer']['status'] == 'SUCCESSFUL':
                outflow.is_complete = True
                outflow.updated_at = timezone.now()
                outflow.save()

                transaction.status = 'Successful'
                transaction.is_complete = True
                transaction.save()
                return Response({'message': 'Success'}, status=s.HTTP_200_OK)
        return Response({'message': 'Already created.'}, status=s.HTTP_201_CREATED)

@api_view(['POST'])
def handle_cedi_transfer_update(request):
    print('** Cedi transfer update **')
    print(request.data)
    data = request.data
    status = data['status']

    transaction = Transaction.objects.get(
        transaction_id=data['metadata']['transaction_id'])

    outflow = transaction.outflow
    if outflow.is_complete == False:
        if status == 'SUCCESS':
            outflow.reference = data['transaction_id']
            outflow.updated_at = timezone.now()
            outflow.is_complete = True
            outflow.save()

            transaction.status = 'Successful'
            transaction.is_complete = True
            transaction.save()
            return Response({'message': 'Success'}, status=s.HTTP_200_OK)
    return Response({'message': 'Already created.'}, status=s.HTTP_201_CREATED)

@api_view(['GET'])
@csrf_exempt
def save_cedi_payment_info(request):
    print('** Cedi payment info **')
    print(request.GET)
    data = request.GET
    transaction = Transaction.objects.get(
        transaction_id=data['metadata[order_id]'])
    inflow = transaction.inflow
    inflow_data = {
        'reference': data['reference'],
        'source_account_provider': data['source[type]'],
        'source_account_number': data['source[number]']
    }
    update_inflow(inflow, **inflow_data)
    return redirect(reverse_lazy('customer:activity'))

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
            update_inflow(inflow, **{})

            # initiate naira transfer
            outflows.initiate_naira_transfer(transaction)

            return Response({'message': 'Success'}, status=s.HTTP_200_OK)
        return Response({'message': 'Error'}, status=s.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response({'message': 'Already created.'}, status=s.HTTP_201_CREATED)

@api_view(['POST'])
def handle_BTC_payment_update(request):
    print('** BTC payment update **')
    print(request.POST)
    transaction = Transaction.objects.get(
        transaction_id=get_transaction_id(request.POST['order_id']))

    status = request.POST['status']
    if status == 'paid':
        update_inflow(transaction.inflow, **{'reference': request.POST['id']})

        # initiate dest amount transfer - GHS or NGN
        if transaction.outflow.currency == 'GHS':
            outflows.initiate_cedi_transfer(transaction, message='BTC to GHS')
        else:
            outflows.initiate_naira_transfer(transaction, narration='BTC to NGN')
    else:
        pass
        # do something if status is not 'paid'
        # maybe redirect to activity page so that
        # user can see status of transaction
        # because we cannot initiate transfer if
        # invoice is not paid

    content = {'message': 'Success'}
    return Response(content, status=s.HTTP_200_OK)