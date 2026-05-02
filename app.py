from flask import Flask, render_template, request, jsonify
import csv
import urllib.request
from io import StringIO
import unicodedata
import time
import os

app = Flask(__name__)

SHEET_ID = "1TaDywZhawAkCIbqysq-7J68vKOWBEd7UjkRjU9mh2SQ"
SHEET_NAME = "Respostas"


@app.route("/")
def index():
    return render_template("index.html")


def normalizar_texto(texto):
    """
    Remove acentos, espaços extras e deixa tudo minúsculo.
    Isso ajuda a comparar código e nomes de colunas.
    """
    if texto is None:
        return ""

    texto = str(texto).strip().lower()

    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(
        caractere for caractere in texto
        if unicodedata.category(caractere) != "Mn"
    )

    texto = " ".join(texto.split())

    return texto


def limpar_valor(valor):
    """
    Transforma textos como:
    'R$ 300', '300', '2.000', '2000', '1.500,50'
    em número float.
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
    O cache_buster evita pegar dados antigos.
    """
    try:
        cache_buster = int(time.time())

        csv_url = (
            f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq"
            f"?tqx=out:csv&sheet={SHEET_NAME}&cache={cache_buster}"
        )

        with urllib.request.urlopen(csv_url) as resposta:
            dados = resposta.read().decode("utf-8")

        arquivo_csv = StringIO(dados)
        leitor = csv.DictReader(arquivo_csv)

        return list(leitor)

    except Exception as erro:
        print("Erro ao buscar planilha:", erro)
        return []


def pegar_valor(linha, nomes_possiveis):
    """
    Pega o valor de uma coluna mesmo se o nome tiver acento,
    espaço a mais ou pequenas diferenças.
    """
    for chave, valor in linha.items():
        chave_normalizada = normalizar_texto(chave)

        for nome in nomes_possiveis:
            if normalizar_texto(nome) == chave_normalizada:
                return valor

    return ""


def encontrar_usuario_por_codigo(codigo):
    codigo_digitado = normalizar_texto(codigo)
    linhas = buscar_dados_planilha()

    for linha in linhas:
        codigo_planilha = pegar_valor(linha, [
            "Código de identificação",
            "Codigo de identificacao",
            "Código",
            "Codigo",
            "ID",
            "Identificação",
            "Identificacao"
        ])

        if normalizar_texto(codigo_planilha) == codigo_digitado:
            return linha

    return None


def gerar_resumo_financeiro(dados):
    nome = pegar_valor(dados, ["Nome"]) or "Usuário"

    renda = limpar_valor(pegar_valor(dados, [
        "Renda mensal aproximada"
    ]))

    renda_extra = limpar_valor(pegar_valor(dados, [
        "Valor da renda extra",
        "Valor da renda extra "
    ]))

    moradia = limpar_valor(pegar_valor(dados, [
        "Gasto mensal com moradia"
    ]))

    alimentacao = limpar_valor(pegar_valor(dados, [
        "Gasto mensal com alimentação",
        "Gasto mensal com alimentacao"
    ]))

    transporte = limpar_valor(pegar_valor(dados, [
        "Gasto mensal com transporte"
    ]))

    internet = limpar_valor(pegar_valor(dados, [
        "Gasto mensal com internet, celular e assinaturas"
    ]))

    saude = limpar_valor(pegar_valor(dados, [
        "Gasto mensal com saúde",
        "Gasto mensal com saude"
    ]))

    lazer = limpar_valor(pegar_valor(dados, [
        "Gasto mensal com lazer e compras pessoais",
        "Gasto mensal com lazer e compras pessoais "
    ]))

    dividas = limpar_valor(pegar_valor(dados, [
        "Valor aproximado das dívidas",
        "Valor aproximado das dividas"
    ]))

    objetivo = pegar_valor(dados, [
        "Principal objetivo financeiro"
    ]) or "Organizar melhor o dinheiro"

    guardar = limpar_valor(pegar_valor(dados, [
        "Quanto gostaria de guardar por mês?",
        "Quanto gostaria de guardar por mes?"
    ]))

    prazo = pegar_valor(dados, [
        "Prazo para alcançar o objetivo",
        "Prazo para alcançar o objetivo ",
        "Prazo para alcancar o objetivo"
    ]) or "Não informado"

    perfil = pegar_valor(dados, [
        "Como você se considera financeiramente?",
        "Como voce se considera financeiramente?"
    ]) or "Não informado"

    cartao = pegar_valor(dados, [
        "Você usa cartão de crédito?",
        "Voce usa cartao de credito?"
    ]) or "Não informado"

    anota = pegar_valor(dados, [
        "Você anota seus gastos?",
        "Voce anota seus gastos?"
    ]) or "Não informado"

    preocupacao = pegar_valor(dados, [
        "Maior preocupação financeira agora",
        "Maior preocupação financeira agor",
        "Maior preocupacao financeira agora"
    ]) or "Não informado"

    renda_total = renda + renda_extra
    gastos_totais = moradia + alimentacao + transporte + internet + saude + lazer
    saldo = renda_total - gastos_totais

    porcentagem_gastos = 0

    if renda_total > 0:
        porcentagem_gastos = (gastos_totais / renda_total) * 100

    dicas = []

    if saldo < 0:
        dicas.append("Seus gastos estão maiores que sua renda. O primeiro passo é reduzir gastos variáveis e evitar novas dívidas.")
    elif guardar > 0 and saldo < guardar:
        dicas.append("Você ainda não consegue guardar o valor desejado todo mês. Comece com uma meta menor e aumente aos poucos.")
    else:
        dicas.append("Você tem possibilidade de guardar dinheiro mensalmente. Separe esse valor assim que receber sua renda.")

    if dividas > 0:
        dicas.append("Como existem dívidas, priorize quitar ou renegociar essas dívidas antes de assumir novos compromissos.")

    if "sim" in normalizar_texto(cartao):
        dicas.append("Use o cartão de crédito com limite controlado. Evite parcelamentos longos e acompanhe a fatura toda semana.")

    if "nao" in normalizar_texto(anota) or "as vezes" in normalizar_texto(anota):
        dicas.append("Comece anotando todos os gastos por 7 dias. Isso ajuda a enxergar para onde o dinheiro está indo.")

    return {
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
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=True)