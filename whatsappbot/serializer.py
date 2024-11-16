import os
from rest_framework import serializers
from .models import CampaignKnowledge


class CampaignKnowledgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampaignKnowledge
        fields = ("user", "file")

    def validate(self, data):
        request = self.context.get("request")
        files = request.FILES.getlist("files")

        if not files:
            raise serializers.ValidationError({"error": "Upload knowldge base files."})

        if any(file.size > 5 * 1024 * 1024 for file in files):
            raise serializers.ValidationError(
                {"error": "File must not be exceeded 5MB"}
            )

        valid_extenstion = [".doc", ".docx", ".pdf", ".txt"]
        for file in files:
            ext = os.path.splitext(file.name)[1]
            if ext.lower() not in valid_extenstion:
                serializers.ValidationError(
                    {
                        "error": "Unsupported file extension. Only doc, docx and pdf are allowed."
                    }
                )
        return data

    def create(self, validated_data):
        request = self.context.get("request")
        files = [
            CampaignKnowledge(user=validated_data["user"], file=file)
            for file in request.FILES.getlist("files")
        ]
        ck = CampaignKnowledge.objects.bulk_create(files)
        return ck[0]
