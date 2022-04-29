from re import L
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
    serializer = UserSerializer(data=request.data, context={"request": request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    if request.user.is_authenticated and request.user.is_employee:
        return Response(serializer.data, HTTP_201_CREATED)
    data = dict(serializer.data)
    data["token"] = Token.objects.get(user=data["id"]).key
    return Response(data=data, status=HTTP_201_CREATED)


@api_view(["POST"])
def user_logout_view(request):
    request.user.auth_token.delete()
    logout(request)
    return Response(data={"Logout Succesful"}, status=HTTP_200_OK)


@api_view(["PUT", "PATCH"])
@permission_classes([IsAuthenticated, IsEmployee])
def user_update_view(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response({"error": "invalid user id"}, HTTP_404_NOT_FOUND)
    serializer = UserUpdateSerializer(user, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, HTTP_200_OK)


@api_view(["PUT"])
def user_password_change(request):
    user = request.user
    serializer = PasswordChangeSerializer(data=request.data)

    serializer.is_valid(raise_exception=True)
    if not user.check_password(serializer.data.get("old_password")):
        return Response({"old_password": "wrong password"}, HTTP_400_BAD_REQUEST)
    user.set_password(serializer.data.get("new_password"))
    user.save()
    return Response({"success": "password changed"}, HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated, IsEmployee])
def user_view_all(request):
    queryset = User.objects.all()
    data = UserSerializer(queryset, many=True).data
    return Response(data, HTTP_200_OK)


@api_view(["GET"])
def user_view_self(request):
    user = User.objects.get(id=request.user.id)
    data = UserSerializer(user).data
    return Response(data, HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated, IsEmployee])
def user_view_by_id(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        Response({"message": "No User found with this id"}, HTTP_404_NOT_FOUND)

    Response(UserSerializer(user).data, HTTP_200_OK)


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


@api_view(["GET"])
@permission_classes([IsAuthenticated, IsCustomer])
def transaction_between_dates(request):
    start_date = request.GET["start"]
    end_date = request.GET["end"]
    customer_id = request.user.id
    queryset_r = Transaction.objects.filter(r_account__account_holder=customer_id)
    queryset_s = Transaction.objects.filter(s_account__account_holder=customer_id)
    queryset_range = Transaction.objects.filter(
        timestamp__date__range=(start_date, end_date)
    )
    queryset = queryset_range.intersection(queryset_r.union(queryset_s))
    data = TransactionSerializer(queryset, many=True).data
    return Response(data, HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated, IsEmployee])
def account_add_view(request):
    serializer = AccountSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(data=serializer.data, status=HTTP_201_CREATED)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated, IsEmployee])
def account_delete_view(request, account_id):
    try:
        account = Account.objects.get(pk=account_id)
    except Account.DoesNotExist:
        Response({"message": "No account found with this id"}, HTTP_404_NOT_FOUND)
    if request.user.branch != account.account_holder.branch:
        Response(
            {"message": "Only same branch accounts can be deleted"},
            HTTP_401_UNAUTHORIZED,
        )
    data = account.delete()
    Response(data, HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated, IsEmployee])
def account_list_all(request):
    queryset = Account.objects.all()
    data = AccountSerializer(queryset, many=True).data
    return Response(data, HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated, IsCustomer])
def account_list_current_user(request):
    queryset = Account.objects.filter(account_holder=request.user)
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


@api_view(["POST"])
@permission_classes([IsAuthenticated, IsCustomer])
def disable_account(request, account_id):
    try:
        account = Account.objects.get(account_id=account_id)
    except Account.DoesNotExist:
        return Response({"error": "invalid account_id"}, HTTP_400_BAD_REQUEST)
    if request.user != account.account_holder:
        return Response({"error": "permission denied"}, HTTP_401_UNAUTHORIZED)
    if account.pin != request.data.get("pin"):
        return Response({"error": "incorrect pin"}, HTTP_400_BAD_REQUEST)
    account.disabled = True
    account.save()
    return Response({"success": "Account disabled"}, HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated, IsCustomer])
def enable_account(request, account_id):
    try:
        account = Account.objects.get(account_id=account_id)
    except Account.DoesNotExist:
        return Response({"error": "invalid account_id"}, HTTP_400_BAD_REQUEST)
    if request.user != account.account_holder:
        return Response({"error": "permission denied"}, HTTP_401_UNAUTHORIZED)
    if account.pin != request.data.get("pin"):
        return Response({"error": "incorrect pin"}, HTTP_400_BAD_REQUEST)
    account.disabled = False
    account.save()
    return Response({"success": "Account enabled"}, HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated, IsEmployee])
def customer_list_branch(request, branch_id):
    queryset = User.objects.filter(is_customer=True, branch=branch_id)
    data = UserSerializer(queryset, many=True).data
    return Response(data, HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated, IsEmployee])
def branch_list(request):
    queryset = Branch.objects.all()
    data = BranchSerializer(queryset, many=True).data
    return Response(data, HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated, IsEmployee])
def branch_add(request):
    serializer = BranchSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, HTTP_201_CREATED)
