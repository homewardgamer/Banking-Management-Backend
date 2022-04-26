from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import *

from base.serializers import UserSerializer


@api_view(["POST"])
@permission_classes([AllowAny])
def user_register_view(request):
    serializer = UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    data = dict(serializer.data)
    data["token"] = Token.objects.get(user=data["id"]).key
    return Response(data=data, status=HTTP_201_CREATED)
