from django.db import models
from decimal import Decimal
from django.contrib.auth.models import User

class Receitas(models.Model):
    id_receita = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nome = models.TextField(max_length=250)
    custo_total = models.DecimalField(max_digits=1000, decimal_places=2, null=True)
    taxa_extra = models.IntegerField(default=0)
    custo_total_com_extra = models.DecimalField(max_digits=1000, decimal_places=2, default=0, null=True)
    porcoes = models.IntegerField(default=0)
    custo_por_porcao = models.DecimalField(max_digits=1000, decimal_places=2, default=0)
    custo_por_porcao_com_extra = models.DecimalField(max_digits=1000, decimal_places=2, default=0)
    preco_venda = models.DecimalField(max_digits=1000, decimal_places=2, null=True)

    def save(self, *args, **kwargs):
        if self.custo_total:
            taxa_extra_decimal = Decimal(self.taxa_extra) / 100
            self.custo_total_com_extra = Decimal(self.custo_total) + (Decimal(self.custo_total) * taxa_extra_decimal)
            self.custo_por_porcao = self.custo_total / Decimal(self.porcoes)
            self.custo_por_porcao_com_extra = self.custo_total_com_extra / Decimal(self.porcoes)
        super().save(*args, **kwargs)


    def calcular_lucro(self):
        return self.preco_venda - self.custo_por_porcao_com_extra

    def __str__(self):
        return self.nome


class Ingredientes(models.Model):
    MEDIDATIPOS = [
        ('unidade', 'Unidade'),
        ('gramas', 'Gramas'),
        ('mililitros', 'Mililitros'),
    ]

    receita = models.ForeignKey(Receitas, on_delete=models.CASCADE, related_name='ingredientes')
    id_ingrediente = models.AutoField(primary_key=True)
    nome = models.TextField(max_length=250)
    tipo_medida = models.CharField(max_length=50, choices=sorted(MEDIDATIPOS))
    valor_gasto = models.DecimalField(max_digits=1000, decimal_places=2)
    qnt_comprada = models.DecimalField(max_digits=1000, decimal_places=2)
    qnt_utilizada = models.DecimalField(max_digits=1000, decimal_places=2)
    custo = models.DecimalField(max_digits=1000, decimal_places=2, null=True)

    def save(self, *args, **kwargs):
        self.custo = (self.valor_gasto / self.qnt_comprada) * self.qnt_utilizada
        super().save(*args, **kwargs)