from django.shortcuts import render, redirect,  get_object_or_404
from .models import Receitas, Ingredientes
from decimal import Decimal
from django.contrib.auth.decorators import login_required


@login_required
def home(request):
    return render(request, 'home.html')


@login_required
def criar_receitas(request):
    return render(request, 'criar_receitas.html')


@login_required
def ver_cardapio(request):
    receitas = Receitas.objects.filter(usuario=request.user)
    return render(request, 'ver_cardapio.html', {'receitas': receitas})


@login_required
def cadastrar_receita(request):
    if request.method == 'POST':
        nome_receita = request.POST.get('nome_receita')
        taxa_extra = float(request.POST.get('taxa_extra', 0))
        porcoes = int(request.POST.get('porcoes', 1))
        preco_venda = float(request.POST.get('preco_venda', 0))

        receita = Receitas(nome=nome_receita, taxa_extra=taxa_extra, porcoes=porcoes, preco_venda=preco_venda)
        receita.usuario = request.user
        receita.save()

        ingredientes = request.POST.getlist('nome_ingrediente[]')
        tipo_medida = request.POST.getlist('tipo_medida[]')
        valor_gasto = [float(val) for val in request.POST.getlist('valor_gasto[]')]
        qnt_comprada = [float(val) for val in request.POST.getlist('qnt_comprada[]')]
        qnt_utilizada = [float(val) for val in request.POST.getlist('qnt_utilizada[]')]

        custo_total = Decimal(0)
        for i in range(len(ingredientes)):
            custo_ingrediente = (Decimal(valor_gasto[i]) / Decimal(qnt_comprada[i])) * Decimal(qnt_utilizada[i])
            custo_total += custo_ingrediente

            ingrediente = Ingredientes(receita=receita, nome=ingredientes[i], tipo_medida=tipo_medida[i],
                                       valor_gasto=valor_gasto[i], qnt_comprada=qnt_comprada[i],
                                       qnt_utilizada=qnt_utilizada[i], custo=custo_ingrediente)

            ingrediente.save()

        receita.custo_total = custo_total
        receita.save()

        return redirect('home')

    return render(request, 'cad_receitas.html')


@login_required
def calcular_lucro(request):
    if request.method == 'POST':
        receita_id = request.POST.get('receita_id')
        preco_venda = request.POST.get('preco_venda')
        try:
            receita = Receitas.objects.get(id_receita=receita_id)
            receita.preco_venda = float(preco_venda)
            receita.save()
        except Receitas.DoesNotExist:
            pass

    return redirect('ver_cardapio')


@login_required
def excluir_receita(request, id_receita):
    receita = get_object_or_404(Receitas, id_receita=id_receita)

    if request.method == 'POST':
        receita.delete()
        return redirect('ver_cardapio') 

    return render(request, 'excluir_receita.html', {'receita': receita})


@login_required
def editar_receita(request, receita_id):
    receita = get_object_or_404(Receitas, id_receita=receita_id)
    if request.method == 'POST':
        if receita:
            receita.nome = request.POST.get('nome_receita')
            receita.taxa_extra = int(request.POST.get('taxa_extra'))
            receita.porcoes = int(request.POST.get('porcoes'))

            receita.save()

        return redirect('ver_cardapio')

    return render(request, 'app/editar_receita.html', {'receita': receita})


@login_required
def editar_ingrediente(request, id_ingrediente):
    ingrediente = get_object_or_404(Ingredientes, id_ingrediente=id_ingrediente)
    if request.method == 'POST':
        ingrediente.nome = request.POST.get('nome_ingrediente')
        ingrediente.tipo_medida = request.POST.get('tipo_medida')
        ingrediente.valor_gasto = float(request.POST.get('valor_gasto'))
        ingrediente.qnt_comprada = float(request.POST.get('qnt_comprada'))
        ingrediente.qnt_utilizada = float(request.POST.get('qnt_utilizada'))

        ingrediente.save()

        receita = ingrediente.receita
        custo_total = Decimal(0)
        for ing in receita.ingredientes.all():
            custo_total += ing.custo
        receita.custo_total = custo_total
        receita.save()

        return redirect('ver_cardapio')

    return render(request, 'app/editar_ingrediente.html', {'ingrediente': ingrediente})
