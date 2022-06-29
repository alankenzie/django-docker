from django.db import models


# Create your models here.
class Animal(models.Model):
    name = models.CharField(max_length=50)
    age = models.FloatField()
    weight = models.FloatField()
    sex = models.CharField(max_length=15, blank=True)

    group = models.ForeignKey(
        "groups.Group", related_name="animals", on_delete=models.CASCADE
    )

    characteristics = models.ManyToManyField(
        "characteristics.characteristic", related_name="animals"
    )

    def __repr__(self):
        return f"<Animal {self.id} - {self.name}>"
