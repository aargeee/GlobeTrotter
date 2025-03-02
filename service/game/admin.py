from django.contrib import admin
from .models import Destination, DestinationInfo, Game, Question

class DestinationInfoInline(admin.TabularInline):
    model = DestinationInfo
    extra = 1

class DestinationAdmin(admin.ModelAdmin):
    inlines = [DestinationInfoInline]

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1

class GameAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]

admin.site.register(Destination, DestinationAdmin)
admin.site.register(DestinationInfo)
admin.site.register(Game, GameAdmin)
admin.site.register(Question)
