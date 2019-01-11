from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication
from rest_framework.response import Response
from knox.views import LoginView as KnoxLoginView


class LoginView(KnoxLoginView):
    authentication_classes = [BasicAuthentication]
    permission_classes = []


@api_view()
@permission_classes([IsAuthenticated])
def user_info(request):
    return Response({"username": request.user.username})
