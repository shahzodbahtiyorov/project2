from collections import defaultdict
from datetime import datetime

from django.contrib.auth.hashers import make_password
from django.db.models import Sum, Q
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from v1.helper import helper, sms_messages
from v1.gateway import shina_gateway
from v1.services.permission_check import HasChartPermission
from v1.models import Users, ClientInfo, ClientIABSAccount, MFO, DocHistories, ClientCertificate
from v1.serializers import CompanySerializer, UserSerializer, AccoutsSerializer, ChartSerializer, ClientSerializer, \
    ClientAccountSerializer, MFOSerializer, AllAccoutsSerializer


class CompanyView(GenericAPIView):
    company_serializer_class = CompanySerializer
    staff_serializer_class = UserSerializer

    @swagger_auto_schema(
        operation_description="Retrieve a company and its associated workers, or list all companies",
        responses={
            200: openapi.Response('Company and workers retrieved successfully or list of companies'),
            404: openapi.Response('Company not found')
        }
    )
    def get(self, request, pk=None):
        if pk:
            company = ClientInfo.objects.get(pk=pk)
            workers = Users.objects.filter(workspace=company)

            company_serializer = self.company_serializer_class(company)
            workers_serializer = self.staff_serializer_class(workers, many=True)

            response_data = {
                "company": company_serializer.data,
                "workers": workers_serializer.data
            }

            return Response({"success": response_data}, status=status.HTTP_200_OK)

        data = ClientInfo.objects.all()
        serializer = self.company_serializer_class(data, many=True)
        return Response({"success": serializer.data})



class AccountView(GenericAPIView):
    company_serializer_class = CompanySerializer
    account_serializer_class = AccoutsSerializer

    @swagger_auto_schema(
        operation_description="Retrieve a company and its associated workers, or list all companies",
        responses={
            200: openapi.Response('Company and workers retrieved successfully or list of companies'),
            404: openapi.Response('Company not found')
        }
    )
    def get(self, request, pk=None):
        if pk:
            company = ClientInfo.objects.get(pk=pk)
            accounts = ClientIABSAccount.objects.select_related('client').filter(company=company)

            company_serializer = self.company_serializer_class(company)
            account_serializer = self.account_serializer_class(accounts, many=True)

            response_data = {
                "company": company_serializer.data,
                "accounts": account_serializer.data
            }

            return Response({"success": response_data}, status=status.HTTP_200_OK)

        data = ClientInfo.objects.all()
        serializer = CompanySerializer(data, many=True)
        return Response({"success": serializer.data})

    def put(self, request, pk=None):
        account = ClientIABSAccount.objects.get(pk=pk)
        if not account:
            return Response({"error": "Account not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.account_serializer_class(data=request.data, partial=True, instance=account)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

        return Response({"success": serializer.data})


class ChartView(GenericAPIView):
    serializer_class = ChartSerializer

    # permission_classes = [HasChartPermission]

    def get(self, request, pk=None):
        details = DocHistories.objects.all()
        print(details)

        total_credit = details.aggregate(total_credit=Sum('credit_amount'))['total_credit'] or 0
        total_debit = details.aggregate(total_debit=Sum('debit_amount'))['total_debit'] or 0

        mfo_totals = defaultdict(lambda: {'credit_amount': 0, 'debit_amount': 0})
        mfo_name = {
            '01186': 'Оплата труда',
            '00440': 'Финансовые расходы',
            '00014': 'Таможня',
            '01176': 'Налоги',
            '00421': 'Другие'
        }

        for item in details:
            mfo = item.receiver_mfo
            mfo_totals[mfo]['credit_amount'] += item.credit_amount or 0
            mfo_totals[mfo]['debit_amount'] += item.debit_amount or 0

        mfo_totals_response = [{
            "receiver_mfo": mfo,
            "name": mfo_name.get(mfo, 'Unknown'),
            "total_credit": totals['credit_amount'],
            "total_debit": totals['debit_amount']
        } for mfo, totals in mfo_totals.items()]

        total_balance = total_credit - total_debit

        return Response(
            {
                "success": mfo_totals_response,
                "total_credit": total_credit,
                "total_debit": total_debit,
                "total_balance": round(total_balance, 2)
            }
        )


class GetOrCreateBankClient(GenericAPIView):
    def get(self, request, pk):
        endpoint = f'1.0.0/get-customer/{pk}'
        result = shina_gateway.post("GET", endpoint)
        print(result)
        if 'responseBody' in result:
            return Response({"result": result['responseBody']['response']})
        return Response({"error": result}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        data = request.data
        user_requirements = ['username', 'phone_number', 'password', 'full_name', 'email', 'role_id', 'direction_code',
                             'director', 'accountant']
        for field in user_requirements:
            value = request.data.get(field)
            if field not in request.data or not value.strip():
                return Response({'required': field}, status=status.HTTP_400_BAD_REQUEST)

        user = Users.objects.filter(username=data['username']).first()
        if user:
            return Response({"error": "User already exists"})

        client = ClientInfo.objects.filter(client_code=data['client_code']).first()
        if client:
            return Response({"error": "Client already exists"})
        try:
            contract_date = datetime.strptime(data['contract_date'], "%d.%m.%Y").date()
        except ValueError:
            return Response({"error": "Invalid date format. It must be in DD.MM.YYYY format."},
                            status=status.HTTP_400_BAD_REQUEST)

        if not helper.is_valid_password(data['password']):
            return Response({
                "error": "Password is invalid. It must be at least 8 characters long and contain letters, numbers, and symbols."},
                status=status.HTTP_400_BAD_REQUEST)
        full_name = data.get('full_name', '').strip()
        name_parts = full_name.split(' ')
        user_data = {
            "username": data['username'],
            "password": make_password(data['password']),
            "email": data['email'],
            "phone_number": data['phone_number'],
            "first_name": name_parts[0] if len(name_parts) > 0 else '',
            "last_name": name_parts[1] if len(name_parts) > 1 else '',
            "role_id": data['role_id'],
        }

        client_info_data = {
            'branch_code': data['branch_code'],
            'branch_name': data['branch_name'],
            'devision_code': data['devision_code'],
            'devision_name': data['devision_name'],
            'client_code': data['client_code'],
            'client_name': data['client_name'],
            'direction_code': data['direction_code'],
            'direction_name': data['direction_name'],
            'contract_date': contract_date,
            'contract_number': data['contract_number'],
            'director': data['director'],
            'accountant': data['accountant'],
            'address': data['address'],
            'country': data['country'],
            'locality': data['locality'],
            'org_unit': data['org_unit'],
            'state': data['state'],
            'tin': data['inn']

        }

        user = Users.objects.create(**user_data)

        client_info_data['user'] = user

        client = ClientInfo.objects.create(**client_info_data)
        ClientCertificate.objects.create(client=client)
        helper.sms_client_pass(data['phone_number'], data['password'])
        return Response({"success": True})


class GetClient(GenericAPIView):
    serializer_class = ClientSerializer

    @swagger_auto_schema(
        operation_summary="Retrieve a client by ID",
        responses={
            200: openapi.Response('Client data', ClientSerializer),
            404: "Client does not exist"
        }
    )
    def get(self, request, pk=None):
        if pk:
            try:
                client = ClientInfo.objects.get(pk=pk)
                serializer = self.serializer_class(client)
                return Response(serializer.data)
            except ClientInfo.DoesNotExist:
                return Response({"error": "Client does not exist"}, status=404)

        clients = ClientInfo.objects.select_related('user').all()
        serializer = self.serializer_class(clients, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Update a client by ID",
        request_body=ClientSerializer,
        responses={
            200: openapi.Response('Client updated successfully', ClientSerializer),
            404: "Client does not exist",
            400: "Invalid data"
        }
    )
    def put(self, request, pk):
        data = request.data
        try:
            client = ClientInfo.objects.get(pk=pk)
        except ClientInfo.DoesNotExist:
            return Response({"error": "Client does not exist"}, status=404)
        user_data = data.get('user', None)
        if user_data:
            new_username = user_data.get('username')
            if new_username:
                if Users.objects.filter(username=new_username).exists():
                    user_data.pop('username', None)
        serializer = self.serializer_class(client, data=data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        serializer.save()
        return Response({"success": serializer.data})


class GetClientAccounts(GenericAPIView):
    def get(self, request, pk):
        if not pk:
            return Response({"error": "client id is required"}, status=400)
        client_id = ClientInfo.objects.filter(id=pk).first()
        if not client_id:
            return Response({"error": "Client does not exists"}, status=400)
        endpoint = f'1.0.0/get-active-accounts/{client_id.client_code}'
        result = shina_gateway.post("GET", endpoint)
        print(result)

        if result.get('code') != 0:
            return Response({"error": result.get('msg', 'An error occurred.')}, status=400)

        accounts = result.get('responseBody', {}).get('response', [])
        if not accounts:
            return Response({"error": "No accounts found."}, status=404)

        for account_data in accounts:
            account_id = account_data['id']
            account_number = account_data['account']
            code_filial = account_data['codeFilial']

            detail_endpoint = f'1.0.0/get-account-details?account={account_number}&code={code_filial}&id={account_id}'
            detail_result = shina_gateway.post("GET", detail_endpoint)
            print(detail_result)

            if 'responseBody' in detail_result:
                inn = detail_result['responseBody']['inn']
                if not ClientIABSAccount.objects.filter(number=account_number, iabs_id=account_id).exists():
                    ClientIABSAccount.objects.create(
                        client_id=client_id.id,
                        number=account_number,
                        name=account_data['nameAcc'],
                        inn=inn,
                        mfo=code_filial,
                        iabs_id=account_id,
                        balance=account_data['saldo'],
                        currency_code=account_data['codeCurrency'],
                        codeCoa=account_data['codeCoa']
                    )
                else:
                    print(f"Duplicate account found: {account_number} with ID: {account_id}. Skipping.")

        return Response({"success": "Accounts processed successfully."}, status=200)

    def post(self, request):
        data = request.data
        client_id = data['client_id']
        account_number = data['account_number']
        code_filial = data['mfo']
        iabs_id = data['iabs_id']

        detail_endpoint = f'1.0.0/get-account-details?account={account_number}&code={code_filial}&id={iabs_id}'
        result = shina_gateway.post("GET", detail_endpoint)

        if 'code' in result and result['code'] == 2:
            return Response({"error": result})

        if 'responseBody' in result:
            result = result['responseBody']

            ClientIABSAccount.objects.create(
                client_id=client_id,
                number=result['account'],
                name=result['nameAcc'],
                inn=result['inn'],
                mfo=result['codeFilial'],
                iabs_id=iabs_id,
                balance=result['saldo'],
                currency_code=result['codeCurrency'],
                codeCoa=result['codeCoa']
            )

            return Response({"success": "Accounts processed successfully."})

        return Response({"error": "Unexpected response format."}, )


class GetExistingAcc(GenericAPIView):
    serializer_class = ClientAccountSerializer

    def get(self, request, pk):
        existing_accounts = ClientIABSAccount.objects.select_related('client').filter(
            client_id=pk).all().order_by('id')

        serializer = self.serializer_class(existing_accounts, many=True)
        return Response({"success": serializer.data})

    def put(self, request, pk):
        acc_id = ClientIABSAccount.objects.filter(id=pk).first()
        if not acc_id:
            return Response({"error": "Account does not exists"}, status=404)

        seralizer = self.serializer_class(acc_id, data=request.data, partial=True)
        if seralizer.is_valid(raise_exception=True):
            seralizer.save()
            return Response({"success": "Account updated successfully."})

        return Response({"error": seralizer.errors}, status=400)


class GetMfo(GenericAPIView):
    serializer_class = MFOSerializer

    def get(self, request):
        filial_codes = MFO.objects.all()
        serializer = self.serializer_class(filial_codes, many=True)
        directions = {
            1: "Бухгалтер -> Банк",
            2: "Бухгалтер -> Директор -> Бухгалтер -> Банк",
            3: "Бухгалтер -> Директор -> Банк",
            4: "Бухгалтер -> Главный -> Бухгалтер -> Банк"
        }
        devision = {
            "123456": "отделение",
            "789012": "клиент",
            "345678": "счет",
            "234567": "кредит",
            "456789": "депозит",
            "567890": "услуга",
            "678901": "операция",
            "890123": "финансирование",
            "901234": "платеж",
            "345123": "консультация"
        }
        return Response({"success": serializer.data, "directions": directions, "devision": devision})


class GetAccountHistory(GenericAPIView):

    def get(self, request, pk, begin=None, end=None, tr_id=None):
        if not pk:
            return Response({"error": "account not found"}, status=404)

        accounts = ClientIABSAccount.objects.filter(id=pk).first()
        if not accounts:
            return Response({"message": "Account does not exist"}, status=404)
        if tr_id:
            transaction = DocHistories.objects.filter(tr_id=tr_id).first()
            if not transaction:
                return Response({"message": "Transaction does not exist"}, status=404)

            if transaction.receiver_company_account == accounts.number:
                return Response({
                    'tr_id': transaction.tr_id,
                    'ext_id': transaction.ext_id,
                    'receiver_company_account': transaction.receiver_company_account,
                    'receiver_name': transaction.receiver_name,
                    'sender_mfo': transaction.sender_company_mfo,
                    'sender_inn': transaction.sender_company_inn,
                    'receiver_mfo': transaction.receiver_mfo,
                    'receiver_inn': transaction.receiver_inn,
                    'details': transaction.details,
                    'status': transaction.status,
                    'sender_company_account': transaction.sender_company_account,
                    'sender_company': transaction.sender_company,
                    'credit_amount': transaction.credit_amount or 0
                })
            if transaction.sender_company_account == accounts.number:
                return Response({
                    'tr_id': transaction.tr_id,
                    'ext_id': transaction.ext_id,
                    'sender_company_account': transaction.sender_company_account,
                    'sender_company': transaction.sender_company,
                    'sender_mfo': transaction.sender_company_mfo,
                    'sender_inn': transaction.sender_company_inn,
                    'receiver_mfo': transaction.receiver_mfo,
                    'receiver_inn': transaction.receiver_inn,
                    'details': transaction.details,
                    'status': transaction.status,
                    'receiver_company_account': transaction.receiver_company_account,
                    'receiver_name': transaction.receiver_name,
                    'debit_amount': transaction.debit_amount or 0
                })

        transactions = DocHistories.objects.filter(
            Q(sender_company_account=accounts.number) | Q(receiver_company_account=accounts.number)
        )

        if begin:
            try:
                start_date = datetime.strptime(begin, '%d-%m-%Y').date()
                transactions = transactions.filter(transaction_date__gte=start_date)
            except ValueError:
                return Response({"message": "Invalid start_date format. Use DD-MM-YYYY."}, status=400)

        if end:
            try:
                end_date = datetime.strptime(end, '%d-%m-%Y').date()
                transactions = transactions.filter(transaction_date__lte=end_date)
            except ValueError:
                return Response({"message": "Invalid end_date format. Use DD-MM-YYYY."}, status=400)

        result = []
        for transaction in transactions:
            transaction_data = {
                'transaction_date': transaction.transaction_date,
            }

            if transaction.receiver_company_account == accounts.number:
                transaction_data.update({
                    'tr_id': transaction.tr_id,
                    'ext_id': transaction.ext_id,
                    'receiver_company_account': transaction.receiver_company_account,
                    'receiver_name': transaction.receiver_name,
                    'sender_mfo': transaction.sender_company_mfo,
                    'sender_inn': transaction.sender_company_inn,
                    'receiver_mfo': transaction.receiver_mfo,
                    'receiver_inn': transaction.receiver_inn,
                    'details': transaction.details,
                    'status': transaction.status,
                    'sender_company_account': transaction.sender_company_account,
                    'sender_company': transaction.sender_company,
                    'credit_amount': transaction.credit_amount or 0
                })
            if transaction.sender_company_account == accounts.number:
                transaction_data.update({
                    'tr_id': transaction.tr_id,
                    'ext_id': transaction.ext_id,
                    'sender_company_account': transaction.sender_company_account,
                    'sender_company': transaction.sender_company,
                    'sender_mfo': transaction.sender_company_mfo,
                    'sender_inn': transaction.sender_company_inn,
                    'receiver_mfo': transaction.receiver_mfo,
                    'receiver_inn': transaction.receiver_inn,
                    'details': transaction.details,
                    'status': transaction.status,
                    'receiver_company_account': transaction.receiver_company_account,
                    'receiver_name': transaction.receiver_name,
                    'debit_amount': transaction.debit_amount or 0
                })

            if 'receiver_company_account' in transaction_data or 'sender_company_account' in transaction_data:
                result.append(transaction_data)

        total_debit = transactions.filter(sender_company_account=accounts.number).aggregate(Sum('debit_amount'))[
                          'debit_amount__sum'] or 0
        total_credit = transactions.filter(receiver_company_account=accounts.number).aggregate(Sum('credit_amount'))[
                           'credit_amount__sum'] or 0

        return Response({
            "result": {
                "total_debit": total_debit,
                "total_credit": total_credit,
                "operations": result
            }
        })


class ClientAccounts(GenericAPIView):
    serializer_class = AllAccoutsSerializer

    def get(self, request):
        accounts = ClientIABSAccount.objects.select_related('client').all().order_by('id')
        serializer = self.serializer_class(accounts, many=True)
        return Response({"success": serializer.data})


class GetTransactions(GenericAPIView):
    def get(self, request, pk):
        endpoint = f'1.0.0/transactions/{pk}'
        result = shina_gateway.post("GET", endpoint)
        return Response({"success": result})

