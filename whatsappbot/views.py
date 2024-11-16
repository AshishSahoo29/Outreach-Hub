from django.http import HttpResponse
from django.core.cache import cache
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from twilio.twiml.messaging_response import MessagingResponse
from .query import Gen
from .models import CampaignKnowledge
from .serializer import CampaignKnowledgeSerializer


class ClientReplyView(APIView):

    def post(self, request):
        client_message = request.data.get("Body")
        response = MessagingResponse()
        response.message("Thank you for contacting via whatsapp!")
        return HttpResponse(
            str(response), content_type="application/xml", status=status.HTTP_200_OK
        )


class BotResponseView(APIView):
    def post(self, request):
        query = request.data.get("query", None)
        if not query:
            return Response(
                {"error": "query is required field"}, status=status.HTTP_400_BAD_REQUEST
            )
        cached_res = cache.get(query)
        if cached_res:
            return Response(
                {"status": "success", "response": cached_res}, status=status.HTTP_200_OK
            )
        response = "This context is out of bound."
        if query is not None:
            app = Gen()
            app.input_knowledge()
            response = app.query(query)
            cache.set(query, response, timeout=300)

        return Response(
            {"status": "success", "response": response}, status=status.HTTP_200_OK
        )


class CampaignKnowledgeView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CampaignKnowledgeSerializer

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)

        return Response(
            {"status": "success", "message": "Knowledge upload successfully."},
            status=status.HTTP_200_OK,
        )

    def get(self, request):
        ckb_obj = CampaignKnowledge.objects.filter(user=request.user)
        serializer = self.serializer_class(ckb_obj, many=True)
        return Response(
            {
                "status": "success",
                "message": "Knowledge files retrieve successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )
