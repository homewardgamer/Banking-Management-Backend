from django.contrib.auth import logout
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import *

from base.permissions import *
from base.serializers import *


@api_view(["POST"])
@permission_classes([AllowAny])
def user_register_view(request):
    serializer = UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    data = dict(serializer.data)
    data["token"] = Token.objects.get(user=data["id"]).key
    return Response(data=data, status=HTTP_201_CREATED)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
@permission_classes([AllowAny])
def user_logout_view(request):
    request.user.auth_token.delete()
    logout(request)
    return Response(data={"Logout Succesful"}, status=HTTP_200_OK)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated, IsEmployee])
def user_delete_view(request, user_id):
    User.objects.get(pk=user_id).delete()
    return Response(data={"message": "Deleted User succesfully"}, status=HTTP_200_OK)


def is_unauthorized(user, data):
    deposit = Transaction.TransactionTypes.DEPOSIT
    withdraw = Transaction.TransactionTypes.WITHDRAW
    transfer = Transaction.TransactionTypes.TRANSFER
    check_1 = user.is_customer and (data.get("type", "") in [deposit, withdraw])
    check_2 = user.is_employee and (data.get("type", "") == transfer)
    return check_1 or check_2


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def transaction_add_view(request):
    if is_unauthorized(request.user, request.data):
        return Response(
            {"transaction failed": "permission denied"}, HTTP_401_UNAUTHORIZED
        )
    serializer = TransactionSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(data=serializer.data, status=HTTP_201_CREATED)


@api_view(["GET"])
@permission_classes([IsAuthenticated, IsCustomer])
def all_transactions_by_customer(request):
    customer_id = request.user.id
    queryset_r = Transaction.objects.filter(r_account__account_holder=customer_id)
    queryset_s = Transaction.objects.filter(s_account__account_holder=customer_id)
    queryset = queryset_r.union(queryset_s).order_by("-timestamp")
    serializer = TransactionSerializer(queryset, many=True)
    return Response(serializer.data, HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated, IsEmployee])
def account_add_view(request):
    serializer = AccountSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(data=serializer.data, status=HTTP_201_CREATED)


@api_view(["GET"])
@permission_classes([IsAuthenticated, IsEmployee])
def account_list_all(request):
    queryset = Account.objects.all()
    data = AccountSerializer(queryset, many=True).data
    return Response(data, HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated, IsCustomer])
def account_detail_by_id(request, account_id):
    try:
        account = Account.objects.get(account_id=account_id)
    except Account.DoesNotExist:
        return Response({"error": "invalid account_id"}, HTTP_400_BAD_REQUEST)
    if request.user != account.account_holder:
        return Response({"error": "permission denied"}, HTTP_401_UNAUTHORIZED)
    return Response(AccountSerializer(account).data, HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated, IsCustomer])
def disable_account(request, account_id):
    try:
        account = Account.objects.get(account_id=account_id)
    except Account.DoesNotExist:
        return Response({"error": "invalid account_id"}, HTTP_400_BAD_REQUEST)
    if request.user != account.account_holder:
        return Response({"error": "permission denied"}, HTTP_401_UNAUTHORIZED)
    account.disabled = True
    account.save()
    return Response({"success": "Account disabled"}, HTTP_200_OK)
