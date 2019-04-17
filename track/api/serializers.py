from rest_framework import serializers
from track.models import Track, Course, Unit, Lecture, CourseMember, \
						 Category, Article, Practice

class TrackSerializer(serializers.ModelSerializer):
	class Meta:
		model = Track
		fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
	class Meta:
		model = Course
		fields = '__all__'

class UnitSerializer(serializers.ModelSerializer):
	class Meta:
		model = Unit
		fields = '__all__'

class LectureSerializer(serializers.ModelSerializer):
	class Meta:
		model = Lecture
		fields = '__all__'

class CourseMemberSerializer(serializers.ModelSerializer):
	class Meta:
		model = CourseMember
		fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = Category
		fields = '__all__'


class ArticleSerializer(serializers.ModelSerializer):
	class Meta:
		model = Article
		fields = '__all__'

class PracticeSerializer(serializers.ModelSerializer):
	class Meta:
		model = Practice
		fields = '__all__'
