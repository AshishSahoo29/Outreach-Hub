from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializer import User, UserSerializer, UserLoginSerializer


class UserSignupView(APIView):
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"status": "success", "message": "User signup sucessfully."},
            status=status.HTTP_201_CREATED,
        )


class UserLoginView(APIView):
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        data = {**serializer.data, **serializer.validated_data.get("tokens")}

        return Response(
            {
                "status": "success",
                "message": "Login successful.",
                "data": data,
            },
            status=status.HTTP_200_OK,
        )
