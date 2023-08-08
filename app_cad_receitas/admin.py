from django.contrib import admin
from django import forms
from .models import Receitas, Ingredientes

class ReceitasForm(forms.ModelForm):
    class Meta:
        model = Receitas
        fields = '__all__'
        widgets = {
            'nome': forms.TextInput(attrs={'style': 'width: 200px;'}),
        }

class IngredienteInlineForm(forms.ModelForm):
    class Meta:
        model = Ingredientes
        fields = '__all__'
        widgets = {
            'nome': forms.TextInput(attrs={'style': 'width: 200px;'}),
        }

class IngredienteInline(admin.TabularInline):
    model = Ingredientes
    form = IngredienteInlineForm
    extra = 1

@admin.register(Receitas)
class ReceitasAdmin(admin.ModelAdmin):
    inlines = [IngredienteInline]
    form = ReceitasForm

@admin.register(Ingredientes)
class IngredientesAdmin(admin.ModelAdmin):
    pass