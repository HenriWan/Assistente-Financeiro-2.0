from flask import Flask, render_template, request, jsonify
import csv
import urllib.request
from io import StringIO

app = Flask(__name__)

# Link original da sua planilha:
# https://docs.google.com/spreadsheets/d/1TaDywZhawAkCIbqysq-7J68vKOWBEd7UjkRjU9mh2SQ/edit?usp=sharing

SHEET_ID = "1TaDywZhawAkCIbqysq-7J68vKOWBEd7UjkRjU9mh2SQ"
SHEET_NAME = "Respostas"

# Link CSV da aba Respostas
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"


@app.route("/")
def index():
    return render_template("index.html")


def limpar_valor(valor):
    """
    Transforma textos como:
    'R$ 300', '300', '2.000', '2000' em número float.
    """
    if not valor:
        return 0.0

    valor = str(valor)
    valor = valor.replace("R$", "")
    valor = valor.replace("r$", "")
    valor = valor.replace(".", "")
    valor = valor.replace(",", ".")
    valor = valor.strip()

    partes = valor.split()

    for parte in partes:
        try:
            return float(parte)
        except ValueError:
            continue

    try:
        return float(valor)
    except ValueError:
        return 0.0


def buscar_dados_planilha():
    """
    Busca os dados da Planilha Google em formato CSV.
    """
    try:
        with urllib.request.urlopen(CSV_URL) as resposta:
            dados = resposta.read().decode("utf-8")

        arquivo_csv = StringIO(dados)
        leitor = csv.DictReader(arquivo_csv)

        return list(leitor)

    except Exception as erro:
        print("Erro ao buscar planilha:", erro)
        return []


def encontrar_usuario_por_codigo(codigo):
    """
    Procura uma pessoa pelo Código de identificação.
    """
    codigo = codigo.strip().lower()
    linhas = buscar_dados_planilha()

    for linha in linhas:
        codigo_planilha = linha.get("Código de identificação", "").strip().lower()

        if codigo_planilha == codigo:
            return linha

    return None


def gerar_resumo_financeiro(dados):
    nome = dados.get("Nome", "Usuário")

    renda = limpar_valor(dados.get("Renda mensal aproximada", "0"))
    renda_extra = limpar_valor(dados.get("Valor da renda extra ", "0"))

    moradia = limpar_valor(dados.get("Gasto mensal com moradia", "0"))
    alimentacao = limpar_valor(dados.get("Gasto mensal com alimentação", "0"))
    transporte = limpar_valor(dados.get("Gasto mensal com transporte", "0"))
    internet = limpar_valor(dados.get("Gasto mensal com internet, celular e assinaturas", "0"))
    saude = limpar_valor(dados.get("Gasto mensal com saúde", "0"))
    lazer = limpar_valor(dados.get("Gasto mensal com lazer e compras pessoais ", "0"))
    dividas = limpar_valor(dados.get("Valor aproximado das dívidas", "0"))

    objetivo = dados.get("Principal objetivo financeiro", "Organizar melhor o dinheiro")
    guardar = limpar_valor(dados.get("Quanto gostaria de guardar por mês?", "0"))
    prazo = dados.get("Prazo para alcançar o objetivo ", "Não informado")
    perfil = dados.get("Como você se considera financeiramente?", "Não informado")
    cartao = dados.get("Você usa cartão de crédito?", "Não informado")
    anota = dados.get("Você anota seus gastos?", "Não informado")
    preocupacao = dados.get("Maior preocupação financeira agor", "Não informado")

    renda_total = renda + renda_extra
    gastos_totais = moradia + alimentacao + transporte + internet + saude + lazer
    saldo = renda_total - gastos_totais

    porcentagem_gastos = 0
    if renda_total > 0:
        porcentagem_gastos = (gastos_totais / renda_total) * 100

    dicas = []

    if saldo < 0:
        dicas.append("Seus gastos estão maiores que sua renda. O primeiro passo é cortar ou reduzir gastos variáveis, principalmente lazer, compras pessoais e assinaturas.")
    elif saldo < guardar:
        dicas.append("Você ainda não consegue guardar o valor desejado todo mês. Comece com uma meta menor e aumente aos poucos.")
    else:
        dicas.append("Você tem possibilidade de guardar dinheiro mensalmente. O ideal é separar esse valor assim que receber sua renda.")

    if dividas > 0:
        dicas.append("Como existem dívidas, priorize quitar as dívidas antes de assumir novos compromissos financeiros.")

    if str(cartao).strip().lower() in ["sim", "s"]:
        dicas.append("Use o cartão de crédito com limite controlado. Evite parcelamentos longos e acompanhe a fatura toda semana.")

    if "não" in str(anota).lower() or "as vezes" in str(anota).lower() or "às vezes" in str(anota).lower():
        dicas.append("Comece anotando todos os gastos por 7 dias. Isso já ajuda a enxergar para onde o dinheiro está indo.")

    resumo = {
        "nome": nome,
        "renda_total": renda_total,
        "gastos_totais": gastos_totais,
        "saldo": saldo,
        "porcentagem_gastos": round(porcentagem_gastos, 2),
        "objetivo": objetivo,
        "guardar": guardar,
        "prazo": prazo,
        "perfil": perfil,
        "preocupacao": preocupacao,
        "dicas": dicas
    }

    return resumo


@app.route("/gerar-resumo", methods=["POST"])
def gerar_resumo():
    dados_requisicao = request.get_json()
    codigo = dados_requisicao.get("codigo", "")

    if not codigo.strip():
        return jsonify({
            "erro": "Digite seu Código de identificação."
        }), 400

    usuario = encontrar_usuario_por_codigo(codigo)

    if usuario is None:
        return jsonify({
            "erro": "Código não encontrado. Confira se você digitou igual ao que colocou no formulário."
        }), 404

    resumo = gerar_resumo_financeiro(usuario)

    return jsonify(resumo)


if __name__ == "__main__":
    import os

    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=True)