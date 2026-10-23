from django.conf import settings
from django.db import models
from django.utils import timezone

from clients.models import Client
from translators.models import Domain, LanguagePair, Translator


class Order(models.Model):
    class Status(models.TextChoices):
        NEW = "new", "Nouă"
        IN_PROGRESS = "in_progress", "În lucru"
        REVIEW = "review", "Revizuire"
        DONE = "done", "Finalizată"
        DELIVERED = "delivered", "Livrată"
        CANCELLED = "cancelled", "Anulată"

    class Urgency(models.TextChoices):
        NORMAL = "normal", "Normal"
        URGENT = "urgent", "Urgent (x1.5)"
        EXPRESS = "express", "Express (x2)"

    number = models.CharField("Nr. comandă", max_length=20, unique=True,
                              null=True, blank=True, editable=False)
    client = models.ForeignKey(Client, on_delete=models.PROTECT,
                               related_name="orders", verbose_name="Client")
    translator = models.ForeignKey(Translator, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name="orders", verbose_name="Traducător")
    language_pair = models.ForeignKey(LanguagePair, on_delete=models.PROTECT,
                                      related_name="orders", verbose_name="Pereche de limbi")
    domain = models.CharField("Domeniu", max_length=20, choices=Domain.choices, default=Domain.GENERAL)
    urgency = models.CharField("Urgență", max_length=20, choices=Urgency.choices, default=Urgency.NORMAL)
    pages = models.DecimalField("Nr. pagini", max_digits=7, decimal_places=2, default=0)
    needs_notarization = models.BooleanField("Necesită legalizare", default=False)
    cost = models.DecimalField("Cost (MDL)", max_digits=10, decimal_places=2, default=0)
    deadline = models.DateTimeField("Termen limită")
    status = models.CharField("Status", max_length=20, choices=Status.choices, default=Status.NEW)
    description = models.TextField("Descriere", blank=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                                   related_name="created_orders", verbose_name="Creată de")
    created_at = models.DateTimeField("Creată la", auto_now_add=True)
    updated_at = models.DateTimeField("Actualizată la", auto_now=True)

    class Meta:
        ordering = ["-created_at"]          # "-" = descrescător, cele mai noi primele
        verbose_name = "Comandă"
        verbose_name_plural = "Comenzi"

    def __str__(self):
        return f"{self.number} – {self.client}"

    def save(self, *args, **kwargs):
        # Prima salvare: obiectul primește un id (pk) de la PostgreSQL
        super().save(*args, **kwargs)
        # Apoi generăm numărul pe baza id-ului, ex: TOMS-2026-00001
        if not self.number:
            self.number = f"TOMS-{self.created_at.year}-{self.pk:05d}"
            super().save(update_fields=["number"])

    @property
    def is_overdue(self):
        """True dacă termenul a trecut și comanda nu e încheiată."""
        closed = {self.Status.DONE, self.Status.DELIVERED, self.Status.CANCELLED}
        return self.deadline < timezone.now() and self.status not in closed
