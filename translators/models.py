from django.conf import settings
from django.db import models


class Domain(models.TextChoices):
    """Domeniul textului. Îl folosim și la traducători, și la comenzi."""
    GENERAL = "general", "General"
    LEGAL = "legal", "Juridic"
    MEDICAL = "medical", "Medical"
    TECHNICAL = "technical", "Tehnic"
    ECONOMIC = "economic", "Economic"


class Language(models.Model):
    code = models.CharField("Cod", max_length=10, unique=True)   # ro, en, fr, ru
    name = models.CharField("Denumire", max_length=50)

    class Meta:
        ordering = ["name"]
        verbose_name = "Limbă"
        verbose_name_plural = "Limbi"

    def __str__(self):
        return self.name


class LanguagePair(models.Model):
    source = models.ForeignKey(
        Language, on_delete=models.PROTECT,
        related_name="pairs_as_source", verbose_name="Limba sursă",
    )
    target = models.ForeignKey(
        Language, on_delete=models.PROTECT,
        related_name="pairs_as_target", verbose_name="Limba țintă",
    )
    price_per_page = models.DecimalField("Preț / pagină (MDL)", max_digits=8, decimal_places=2)

    class Meta:
        verbose_name = "Pereche de limbi"
        verbose_name_plural = "Perechi de limbi"
        constraints = [
            models.UniqueConstraint(fields=["source", "target"], name="unique_language_pair"),
        ]

    def __str__(self):
        return f"{self.source.code.upper()} → {self.target.code.upper()}"


class Translator(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name="translator_profile", verbose_name="Utilizator",
    )
    language_pairs = models.ManyToManyField(
        LanguagePair, related_name="translators", verbose_name="Perechi de limbi",
    )
    specialization = models.CharField(
        "Specializare", max_length=20, choices=Domain.choices, default=Domain.GENERAL,
    )
    max_pages_per_day = models.PositiveIntegerField("Max. pagini / zi", default=10)
    is_available = models.BooleanField("Disponibil", default=True)
    notes = models.TextField("Note", blank=True)

    class Meta:
        verbose_name = "Traducător"
        verbose_name_plural = "Traducători"

    def __str__(self):
        return self.user.get_full_name() or self.user.username