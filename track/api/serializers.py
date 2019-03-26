from rest_framework import serializers
from track.models import Track, Course

class TrackSerializer(serializers.ModelSerializer):
	class Meta:
		model = Track
		fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
	class Meta:
		model = Course
		fields = '__all__'