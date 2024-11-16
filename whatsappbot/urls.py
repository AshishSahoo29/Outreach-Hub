from django.urls import path
from .views import ClientReplyView, BotResponseView, CampaignKnowledgeView

urlpatterns = [
    path("reply/", ClientReplyView.as_view(), name="reply-message"),
    path("response/", BotResponseView.as_view(), name="response-message"),
    path("upload_kb/", CampaignKnowledgeView.as_view(), name="upload-knowledge-files"),
]
