from django.contrib import admin
from django.utils.html import format_html
from .models import *

##
admin.site.register(Content)
##


class TrackAdmin(admin.ModelAdmin):
    list_filter = ('created_at', 'status')
    list_display = ('title', 'status')
    list_editable = ('status',)
    search_fields = ('title', 'content')
    # change_list_template = 'admin/change_list.html'
    prepopulated_fields = {"slug": ("title",)}
    class Meta:
        model = Track

admin.site.register(Track, TrackAdmin)


class CourseAdmin(admin.ModelAdmin):
    list_filter = ('created_at', 'status')
    list_display = ('title', 'status')
    list_editable = ['status']
    search_fields = ('title', 'content')
    # change_list_template = 'admin/change_list.html'
    prepopulated_fields = {"slug": ("title",)}
    class Meta:
        model = Course

admin.site.register(Course, CourseAdmin)


class UnitAdmin(admin.ModelAdmin):
    list_filter = ('created_at', 'status')
    list_display = ['title', 'status']
    list_editable = ['status']
    search_fields = ('title', 'content')
    # change_list_template = 'admin/change_list.html'
    prepopulated_fields = {"slug": ("title",)}
    class Meta:
        model = Unit

admin.site.register(Unit, UnitAdmin)

class LectureAdmin(admin.ModelAdmin):
    list_filter = ('created_at', 'status')
    list_display = ['title', 'status']
    list_editable = ['status']
    search_fields = ('title', 'content')
    # change_list_template = 'admin/change_list.html'
    prepopulated_fields = {"slug": ("title",)}
    class Meta:
        model = Lecture

admin.site.register(Lecture, LectureAdmin)


class ArticleAdmin(admin.ModelAdmin):
    list_filter = ('created_at', 'tags', 'status')
    list_display = ('title', 'created_at', 'status')
    list_editable = ['status']
    search_fields = ('title', 'content')
    # change_list_template = 'admin/change_list.html'
    prepopulated_fields = {"slug": ("title",)}
    class Meta:
        model = Article

admin.site.register(Article, ArticleAdmin)


class PracticeAdmin(admin.ModelAdmin):
    list_filter = ('created_at', 'status')
    list_display = ('title', 'created_at', 'status')
    list_editable = ['status']
    search_fields = ('title', 'content')
    # change_list_template = 'admin/change_list.html'
    prepopulated_fields = {"slug": ("title",)}
    class Meta:
        model = Practice

admin.site.register(Practice, PracticeAdmin)

class CourseMemberAdmin(admin.ModelAdmin):
    list_filter = ('course', 'profile',)
    list_display = ('course', 'profile',)
    search_fields = ('course', 'profile',)
    class Meta:
        model = CourseMember

admin.site.register(CourseMember, CourseMemberAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}
    class Meta:
        model = Category
admin.site.register(Category, CategoryAdmin)


####### content

class VideoAdmin(admin.ModelAdmin):
    list_filter = ('created_at',)
    list_display = ['created_at', 'title',]
    list_editable = ['title']
    search_fields = ('title', 'content')

    class Meta:
        model = Video

admin.site.register(Video, VideoAdmin)


class ImageAdmin(admin.ModelAdmin):
    list_filter = ('created_at',)
    list_display = ['created_at', 'title',]
    list_editable = ['title']
    search_fields = ('title', 'content')

    class Meta:
        model = Image

admin.site.register(Image, ImageAdmin)


class FileAdmin(admin.ModelAdmin):
    list_filter = ('created_at',)
    list_display = ['created_at', 'title',]
    list_editable = ['title']
    search_fields = ('title', 'content')

    class Meta:
        model = File

admin.site.register(File, FileAdmin)


class TextAdmin(admin.ModelAdmin):
    list_filter = ('created_at',)
    list_display = ['created_at', 'title',]
    list_editable = ['title']
    search_fields = ('title', 'content')

    class Meta:
        model = Text

admin.site.register(Text, TextAdmin)