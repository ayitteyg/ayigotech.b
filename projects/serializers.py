from rest_framework import serializers
from .models import Project, ProjectScreenshot
        

class ProjectScreenshotSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    demo_video = serializers.SerializerMethodField()

    class Meta:
        model = ProjectScreenshot
        fields = ["id", "image", "demo_video", "order"]

    def get_image(self, obj):
        return obj.image.url if obj.image else None

    def get_demo_video(self, obj):
        return obj.demo_video.url if obj.demo_video else None    
        
        

class ProjectSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    screenshots = ProjectScreenshotSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = "__all__"
    
    
    def get_image(self, obj):
        if obj.image:
            return obj.image.url  # Always returns the Cloudinary URL
        return None
