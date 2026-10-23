from django.db import models


class Client(models.Model):
    class ClientType(models.TextChoices):
        INDIVIDUAL = "individual", "Persoană fizică"
        COMPANY = "company", "Persoană juridică"

    client_type = models.CharField(
        "Tip client", max_length=20, choices=ClientType.choices, default=ClientType.INDIVIDUAL,
    )
    name = models.CharField("Nume / Denumire", max_length=200)
    idno = models.CharField("IDNO / IDNP", max_length=13, blank=True)
    email = models.EmailField("Email", blank=True)
    phone = models.CharField("Telefon", max_length=20, blank=True)
    address = models.CharField("Adresă", max_length=255, blank=True)
    notes = models.TextField("Note", blank=True)
    created_at = models.DateTimeField("Creat la", auto_now_add=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Client"
        verbose_name_plural = "Clienți"

    def __str__(self):
        return self.name
