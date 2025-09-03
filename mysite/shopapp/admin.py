from django.contrib import admin
from .models import Quote, Source

class QuoteAdmin(admin.ModelAdmin):
    list_display = ('text', 'source', 'weight', 'impressions', 'likes', 'dislikes')
    search_fields = ('text', 'source__name')

class SourceAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

admin.site.register(Quote, QuoteAdmin)
admin.site.register(Source, SourceAdmin)