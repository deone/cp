# Cedi

def cedi_payment_info(transaction_id):
    return '{}{}{}'.format('amount=2.0&amount_after_charge=1.5&charge=0.5&currency=GHS&message=Successful transaction.&metadata[order_id]=', transaction_id, '&metadata[product_description]=GHS to NGN&metadata[product_name]=Money transfer&payment_date=2019-12-27 11:32:51 UTC&processor_transaction_id=33FS5ZCPJWQ311&reference=33FS5ZCPJWQ311&source[number]=0542751610&source[object]=mobile_money&source[processor_transaction_id]=33FS5ZCPJWQ311&source[reference]=33FS5ZCPJWQ311&source[type]=mtn_gh&status=successful&status_code=100&tokenized=false&transaction_uuid=7514d18035a91b7ccd54a17539be90ed')

def cedi_payment_update(transaction_id):
    return {
        'amount': 1258.0,
        'metadata': {
            'order_id': transaction_id, 'product_name': 'Money transfer', 'product_description': 'GHS to NGN'
        }, 'currency': 'GHS', 'amount_after_charge': '1226.55', 'reference': '54C6JDQ3WANH16',
        'processor_transaction_id': '54C6JDQ3WANH16', 'charge': '31.45',
        'source': {
            'object': 'mobile_money', 'number': '0242110110', 'reference': '54C6JDQ3WANH16',
            'processor_transaction_id': '54C6JDQ3WANH16', 'type': 'mtn_gh'
        }, 'customer_remarks': '', 'id': '28ab1980cd9742', 'first_name': 'Duke', 'last_name': 'Martin',
        'email': 'dukeofori@gmail.com', 'tokenized': False,
        'status': 'successful', 'status_code': '100', 'transaction_uuid': '38b9489cc9d2ab560706e8b33db9cbd4',
        'payment_date': '2020-12-07 16:53:53 UTC', 'message': 'Successful transaction.', 'error_fields': []
    }

def cedi_transfer_update(transaction_id):
    return {
        'transaction_id': '53ANHU71E8LX9',
        'amount': '2.96',
        'failure_code': None,
        'balance': '13.7864',
        'previous_balance': '16.776',
        'currency': 'GHS',
        'remarks': 'NGN to GHS',
        'failure_message': None,
        'charge': '0.0296',
        'metadata': {
            'user_id': 1,
            'transaction_id': transaction_id
        },
        'url': '/payouts/9625243d-b53c-4b79-bc68-36111b3ac33d',
        'id': '9625243d-b53c-4b79-bc68-36111b3ac33d',
        'created_at': '2020-02-21T09:53:46.583Z',
        'status_code': '100',
        'status': 'SUCCESS'
    }

def cedi_transfer_update_failed(transaction_id):
    return {
        'transaction_id': '53ANHU71E8LX9',
        'amount': '2.96',
        'failure_code': None,
        'balance': '13.7864',
        'previous_balance': '16.776',
        'currency': 'GHS',
        'remarks': 'NGN to GHS',
        'failure_message': None,
        'charge': '0.0296',
        'metadata': {
            'user_id': 1,
            'transaction_id': transaction_id
        },
        'url': '/payouts/9625243d-b53c-4b79-bc68-36111b3ac33d',
        'id': '9625243d-b53c-4b79-bc68-36111b3ac33d',
        'created_at': '2020-02-21T09:53:46.583Z',
        'status_code': '100',
        'status': 'FAILED'
    }

def naira_payment_info(transaction_id):
    return {
        'resp': ['{}{}{}'.format('{"name":"vbvcomplete","data":{"transactionobject":{"id":294322659,"txRef":"97","orderRef":"URF_6FE8689989BABDDCD9_9020668","flwRef":"FLW290320532","redirectUrl":"http://127.0.0","device_fingerprint":"7acc5ad3da62c2966a93331a26ab12b8","settlement_token":null,"cycle":"one-time","amount":200,"charged_amount":200,"appfee":2.8,"merchantfee":0,"merchantbearsfee":1,"chargeResponseCode":"00","raveRef":null,"chargeResponseMessage":"Pending, Validation","authModelUsed":"noauth-saved-card","currency":"NGN","IP":"102.176.2.227","narration":"Incisia Company Limited","status":"successful","modalauditid":"c25acc39122f92898986b91ae87ba67b","vbvrespmessage":"Approved","authurl":"https://coreflutterwaveprod.com/flwmpgs/trxauth?hid=FLW03f9f08ab06f49d0b79daa174f75aa34","vbvrespcode":"00","acctvalrespmsg":null,"acctvalrespcode":"021711201599","paymentType":"card","paymentPlan":null,"paymentPage":null,"paymentId":"4506866","fraud_status":"ok","charge_type":"normal","is_live":0,"retry_attempt":null,"getpaidBatchId":null,"createdAt":"2020-08-04T11:03:40.000Z","updatedAt":"2020-08-04T11:04:19.000Z","deletedAt":null,"customerId":218654868,"AccountId":70515},"name":"vbvcomplete","data":{"status":"successful","txRef":"97","amount":"200"},"respcode":"00","respmsg":"Approved"},"respcode":"00","tx":{"id":294322659,"txRef":"', transaction_id, '","orderRef":"URF_6FE8689989BABDDCD9_9020668","flwRef":"FLW290320532","redirectUrl":"http://127.0.0","device_fingerprint":"7acc5ad3da62c2966a93331a26ab12b8","settlement_token":null,"cycle":"one-time","amount":200,"charged_amount":200,"appfee":2.8,"merchantfee":0,"merchantbearsfee":1,"chargeResponseCode":"00","raveRef":null,"chargeResponseMessage":"Pending, Validation","authModelUsed":"noauth-saved-card","currency":"NGN","IP":"102.176.2.227","narration":"Incisia Company Limited","status":"successful","modalauditid":"c25acc39122f92898986b91ae87ba67b","vbvrespmessage":"Approved","authurl":"https://coreflutterwaveprod.com/flwmpgs/trxauth?hid=FLW03f9f08ab06f49d0b79daa174f75aa34","vbvrespcode":"00","acctvalrespmsg":null,"acctvalrespcode":"021711201599","paymentType":"card","paymentPlan":null,"paymentPage":null,"paymentId":"4506866","fraud_status":"ok","charge_type":"normal","is_live":0,"retry_attempt":null,"getpaidBatchId":null,"createdAt":"2020-08-04T11:03:40.000Z","updatedAt":"2020-08-04T11:04:19.000Z","deletedAt":null,"customerId":218654868,"AccountId":70515},"respmsg":"Approved"}')]
    }

def naira_payment_update_card(transaction_id):
    return {
        'id': 294449391, 'txRef': transaction_id, 'flwRef': 'FLW290608146',
        'orderRef': 'URF_6FE868A9D9BAF7FEBE_1643877', 'paymentPlan': None,
        'paymentPage': None, 'createdAt': '2020-08-04T20:07:23.000Z', 'amount': 200,
        'charged_amount': 200, 'status': 'successful', 'IP': '197.251.182.157',
        'currency': 'NGN', 'appfee': 2.8, 'merchantfee': 0, 'merchantbearsfee': 1,
        'customer': {
            'id': 218654868, 'phone': '+233542751610', 'fullName': 'Anonymous customer',
            'customertoken': None, 'email': 'alwaysdeone@gmail.com',
            'createdAt': '2020-08-04T09:28:46.000Z', 'updatedAt': '2020-08-04T09:28:46.000Z',
            'deletedAt': None, 'AccountId': 70515
        },
        'entity': {
            'card6': '539983', 'card_last4': '9335'
        },
        'event.type': 'CARD_TRANSACTION'
    }

def naira_transfer_update(transaction_id):
    return {
        'event.type': 'Transfer',
        'transfer': {
            'id': 2700919, 'account_number': '0009432630', 'bank_code': '058',
            'fullname': 'OSIKOYA, OLADAYO JOSHUA',
            'date_created': '2020-08-04T19:25:40.000Z', 'currency': 'NGN',
            'debit_currency': None, 'amount': 127, 'fee': 10.75,
            'status': 'SUCCESSFUL',
            'reference': transaction_id,
            'meta': None,
            'narration': 'GHS to NGN', 'approver': None,
            'complete_message': 'Transaction was successful',
            'requires_approval': 0, 'is_approved': 1, 'bank_name': 'GTBANK PLC',
            'proof': '110002200804202546000068560851'
        }
    }

"""
Naira transfer update failed
{'event.type': 'Transfer', 'transfer': {'id': 4898213, 'account_number': '1015082319', 'bank_code': '057', 'fullname': 'UNIQUANTUM SOLUTIONS LIMITED', 'date_created': '2020-12-07T16:55:06.000Z', 'currency': 'NGN', 'debit_currency': None, 'amount': 96031, 'fee': 53.75, 'status': 'FAILED', 'reference': 'SMNY201207165305', 'meta': None, 'narration': 'GHS to NGN', 'approver': None, 'complete_message': 'DISBURSE FAILED: Insufficient funds in customer wallet', 'requires_approval': 0, 'is_approved': 1, 'bank_name': 'ZENITH BANK PLC'}}
""" 

def btc_payment_update(transaction_id, user_id):
    return {
        'id': '0f0008fb-9aca-452c-a355-74b1c526dda3',
        'callback_url': 'http://localhost:8000/t/handle-btc-payment-update',
        'success_url': 'http://localhost:8000',
        'status': 'paid',
        'order_id': transaction_id,
        'user_id': user_id,
        'description': 'BTC to NGN',
        'price': '100000',
        'fee': '0',
        'auto_settle': '0',
        'hashed_order': '3d1ee193b12bf9b3343e69b31dccc8787c0278cc4e8897f021640a5e9d12fe40'
    }