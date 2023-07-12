from django.db import models


class TurbineData(models.Model):
    """Model definition for TurbineData."""

    created_at = models.DateTimeField(auto_now_add=True)

    temperature = models.IntegerField()
    exhaust_mass = models.IntegerField()
    fuel_consumed = models.IntegerField()
    rotations_per_second = models.IntegerField()

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        """Unicode representation of TurbineData."""
        return ",".join(
            [
                str(self.temperature),
                str(self.exhaust_mass),
                str(self.fuel_consumed),
                str(self.rotations_per_second),
            ]
        )
