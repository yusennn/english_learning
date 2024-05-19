from django.contrib import admin
from django.utils.html import format_html
from .models import Word, Question, Test, Category, ListeningWord, ListeningQuestion, ListeningTest, GrammarTest, GrammarQuestion, AnswerOption

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'image_tag')  
    search_fields = ('name',)

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="300px" height="auto" />', obj.image.url)
        return "No Image"
    image_tag.short_description = 'Image'

admin.site.register(Category, CategoryAdmin)

class WordAdmin(admin.ModelAdmin):
    list_display = ('russian_word', 'english_word', 'distractors')
    search_fields = ('russian_word', 'english_word')

admin.site.register(Word, WordAdmin)

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('word', 'completed', 'correct')
    list_filter = ('completed', 'correct')
    search_fields = ('word__russian_word', 'word__english_word')

admin.site.register(Question, QuestionAdmin)

class TestAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'current_question', 'progress', 'completed')
    list_filter = ('completed', 'category')
    search_fields = ('category__name',)

admin.site.register(Test, TestAdmin)


class ListeningWordAdmin(admin.ModelAdmin):
    list_display = ('word', 'distractors')
    search_fields = ('word',)

admin.site.register(ListeningWord, ListeningWordAdmin)

class ListeningQuestionAdmin(admin.ModelAdmin):
    list_display = ('word', 'completed', 'correct')
    list_filter = ('completed', 'correct')
    search_fields = ('word__word',)

admin.site.register(ListeningQuestion, ListeningQuestionAdmin)

class ListeningTestAdmin(admin.ModelAdmin):
    list_display = ('category', 'current_question', 'progress', 'completed')
    list_filter = ('completed', 'category')
    search_fields = ('category__name',)

admin.site.register(ListeningTest, ListeningTestAdmin)

class GrammarTestAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'completed', 'current_question', 'category')
    list_filter = ('completed', 'category')
    search_fields = ('title', 'user__username')
    ordering = ('-completed', 'title')

class GrammarQuestionAdmin(admin.ModelAdmin):
    list_display = ('sentence', 'test', 'correct_answer')
    list_filter = ('test',)
    search_fields = ('sentence', 'correct_answer')

class AnswerOptionAdmin(admin.ModelAdmin):
    list_display = ('word', 'question')
    list_filter = ('question',)
    search_fields = ('word',)

admin.site.register(GrammarTest, GrammarTestAdmin)
admin.site.register(GrammarQuestion, GrammarQuestionAdmin)
admin.site.register(AnswerOption, AnswerOptionAdmin)


