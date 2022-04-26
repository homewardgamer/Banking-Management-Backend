from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import *

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


def is_unauthorized(user, data):
    deposit = Transaction.TransactionTypes.DEPOSIT
    withdraw = Transaction.TransactionTypes.WITHDRAW
    transfer = Transaction.TransactionTypes.TRANSFER
    check_1 = user.is_customer and (data.get("type", "") in [deposit, withdraw])
    check_2 = user.is_employee and (data.get("type", "") == transfer)
    return check_1 or check_2


@api_view(["POST"])
def transaction_add_view(request):
    if is_unauthorized(request.user, request.data):
        return Response(
            {"transaction failed": "permission denied"}, HTTP_401_UNAUTHORIZED
        )
    serializer = TransactionSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(data=serializer.data, status=HTTP_201_CREATED)
