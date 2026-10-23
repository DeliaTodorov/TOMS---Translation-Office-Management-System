from django.contrib import admin
from .models import Language, LanguagePair, Translator


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ("name", "code")
    search_fields = ("name", "code")


@admin.register(LanguagePair)
class LanguagePairAdmin(admin.ModelAdmin):
    list_display = ("__str__", "source", "target", "price_per_page")
    list_filter = ("source", "target")


@admin.register(Translator)
class TranslatorAdmin(admin.ModelAdmin):
    list_display = ("__str__", "specialization", "is_available", "max_pages_per_day")
    list_filter = ("specialization", "is_available")
    filter_horizontal = ("language_pairs",)   # widget comod pentru ManyToMany
