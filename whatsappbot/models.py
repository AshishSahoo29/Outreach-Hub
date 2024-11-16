from django.db import models
from core.models import User


class CampaignKnowledge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    file = models.FileField(upload_to="kb", null=True)
