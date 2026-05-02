from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import csv
import urllib.request
from io import StringIO
import unicodedata
import time
import os
from datetime import datetime

app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY", "assistente-financeiro-chave-dev")

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=True
)

SHEET_ID = "1TaDywZhawAkCIbqysq-7J68vKOWBEd7UjkRjU9mh2SQ"
SHEET_NAME = "Respostas"

APP_VERSION = "2.0.15.38.26"
APP_AUTHOR = "Henrique Morais"

ADMIN_USER_PADRAO = "henrique"
ADMIN_PASSWORD_PADRAO = "Henri2026IA"


@app.after_request
def security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    return response


@app.route("/")
def index():
    return render_template(
        "index.html",
        app_version=APP_VERSION,
        app_author=APP_AUTHOR
    )


def normalizar_texto(texto):
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
    dados_requisicao = request.get_json() or {}

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


@app.route("/feedback", methods=["POST"])
def feedback():
    dados = request.get_json() or {}

    nome = str(dados.get("nome", "Anônimo")).strip()[:80]
    mensagem = str(dados.get("mensagem", "")).strip()[:1000]

    if not mensagem:
        return jsonify({"erro": "Digite uma mensagem de feedback."}), 400

    data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        arquivo_existe = os.path.exists("feedbacks.csv")

        with open("feedbacks.csv", "a", newline="", encoding="utf-8") as arquivo:
            escritor = csv.writer(arquivo)

            if not arquivo_existe:
                escritor.writerow(["data_hora", "nome", "mensagem"])

            escritor.writerow([data_hora, nome, mensagem])

        return jsonify({"mensagem": "Feedback enviado com sucesso."})

    except Exception as erro:
        print("Erro ao salvar feedback:", erro)
        return jsonify({"erro": "Não foi possível salvar o feedback agora."}), 500


def ler_feedbacks():
    feedbacks = []

    if not os.path.exists("feedbacks.csv"):
        return feedbacks

    try:
        with open("feedbacks.csv", "r", encoding="utf-8") as arquivo:
            leitor = csv.DictReader(arquivo)

            for linha in leitor:
                feedbacks.append(linha)

    except Exception as erro:
        print("Erro ao ler feedbacks:", erro)

    return list(reversed(feedbacks))


@app.route("/admin-login", methods=["POST"])
def admin_login():
    admin_user = os.environ.get("ADMIN_USER", ADMIN_USER_PADRAO)
    admin_password = os.environ.get("ADMIN_PASSWORD", ADMIN_PASSWORD_PADRAO)

    usuario = request.form.get("usuario", "")
    senha = request.form.get("senha", "")

    if usuario == admin_user and senha == admin_password:
        session["admin_logado"] = True
        return redirect(url_for("admin"))

    return render_template(
        "admin.html",
        logado=False,
        erro="Usuário ou senha incorretos.",
        feedbacks=[],
        app_version=APP_VERSION,
        app_author=APP_AUTHOR
    ), 401


@app.route("/admin")
def admin():
    if not session.get("admin_logado"):
        return render_template(
            "admin.html",
            logado=False,
            erro=None,
            feedbacks=[],
            app_version=APP_VERSION,
            app_author=APP_AUTHOR
        )

    feedbacks = ler_feedbacks()
    total_respostas = len(buscar_dados_planilha())

    return render_template(
        "admin.html",
        logado=True,
        erro=None,
        feedbacks=feedbacks,
        total_respostas=total_respostas,
        app_version=APP_VERSION,
        app_author=APP_AUTHOR,
        sheet_id=SHEET_ID,
        sheet_name=SHEET_NAME
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=True)