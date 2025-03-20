from django.db import models


class RechargeEnergyMixin(models.Model):
    def recharge_energy(self, amount):
        self.energy = min(100, self.energy + amount)
        self.save()


    class Meta:
        abstract = True
