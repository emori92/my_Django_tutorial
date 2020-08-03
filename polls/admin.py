from django.contrib import admin
from .models import Question, Choice


# 管理サイトに表示
# admin.site.register(Question)
# admin.site.register(Choice)


# 管理サイトでpub_dateの表示を先にする
# class QuestionAdmin(admin.ModelAdmin):
#     fields = ['pub_date', 'question_text']


# フィールドのタイトルを追加
# class QuestionAdmin(admin.ModelAdmin):
#     fieldsets = [
#         (None,               {'fields': ['question_text']}),
#         ('Date information', {'fields': ['pub_date']}),
#     ]

# admin.site.register(Question, QuestionAdmin)


# QuestionとChoiceを同時に登録
class ChoiceInline(admin.TabularInline):
# class ChoiceInline(admin.StackedInline):  # ページが長くなるので、Tabularに変更
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    # question_text, pub_dateなどを追加して表示
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']

admin.site.register(Question, QuestionAdmin)
