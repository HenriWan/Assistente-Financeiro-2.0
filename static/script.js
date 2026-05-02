const btnComecar = document.getElementById("btnComecar");
const btnAbrirChat = document.getElementById("btnAbrirChat");
const btnGerarResumo = document.getElementById("btnGerarResumo");
const btnReiniciar = document.getElementById("btnReiniciar");

const inicioArea = document.getElementById("inicioArea");
const formularioArea = document.getElementById("formularioArea");
const chatArea = document.getElementById("chatArea");
const codigoInput = document.getElementById("codigoInput");
const resultado = document.getElementById("resultado");

btnComecar.addEventListener("click", () => {
    formularioArea.classList.remove("hidden");
    btnAbrirChat.classList.remove("hidden");

    formularioArea.scrollIntoView({
        behavior: "smooth",
        block: "start"
    });
});

btnAbrirChat.addEventListener("click", () => {
    inicioArea.classList.add("hidden");
    formularioArea.classList.add("hidden");
    btnAbrirChat.classList.add("hidden");

    chatArea.classList.remove("hidden");

    document.body.classList.add("chat-focused");

    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });

    setTimeout(() => {
        codigoInput.focus();
    }, 500);
});

btnGerarResumo.addEventListener("click", async () => {
    const codigo = codigoInput.value.trim();

    resultado.classList.remove("hidden");
    resultado.classList.remove("erro");
    resultado.innerHTML = "<p>Buscando seus dados e gerando resumo...</p>";

    if (!codigo) {
        resultado.classList.add("erro");
        resultado.innerHTML = "<p><strong>Digite seu Código de identificação antes de gerar o resumo.</strong></p>";
        return;
    }

    try {
        const resposta = await fetch("/gerar-resumo", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ codigo })
        });

        const dados = await resposta.json();

        if (!resposta.ok) {
            resultado.classList.add("erro");
            resultado.innerHTML = `<p><strong>${dados.erro}</strong></p>`;
            return;
        }

        resultado.classList.remove("erro");

        const saldoFormatado = formatarMoeda(dados.saldo);
        const rendaFormatada = formatarMoeda(dados.renda_total);
        const gastosFormatados = formatarMoeda(dados.gastos_totais);
        const guardarFormatado = formatarMoeda(dados.guardar);

        let dicasHtml = "";

        dados.dicas.forEach((dica) => {
            dicasHtml += `<li>${dica}</li>`;
        });

        resultado.innerHTML = `
            <h3>Resumo financeiro de ${dados.nome}</h3>

            <p><strong>Renda total:</strong> ${rendaFormatada}</p>
            <p><strong>Gastos mensais aproximados:</strong> ${gastosFormatados}</p>
            <p><strong>Saldo estimado:</strong> ${saldoFormatado}</p>
            <p><strong>Porcentagem da renda comprometida:</strong> ${dados.porcentagem_gastos}%</p>

            <hr>

            <p><strong>Objetivo financeiro:</strong> ${dados.objetivo}</p>
            <p><strong>Valor que deseja guardar:</strong> ${guardarFormatado}</p>
            <p><strong>Prazo informado:</strong> ${dados.prazo}</p>
            <p><strong>Perfil financeiro:</strong> ${dados.perfil}</p>
            <p><strong>Maior preocupação:</strong> ${dados.preocupacao}</p>

            <h4>Orientações iniciais</h4>
            <ul>${dicasHtml}</ul>
        `;

        resultado.scrollIntoView({
            behavior: "smooth",
            block: "start"
        });

    } catch (erro) {
        console.error(erro);

        resultado.classList.add("erro");
        resultado.innerHTML = `
            <p>
                <strong>
                    Ocorreu um erro ao gerar o resumo. Verifique se a planilha está pública
                    e se o código foi digitado corretamente.
                </strong>
            </p>
        `;
    }
});

btnReiniciar.addEventListener("click", () => {
    window.location.href = "/";
});

codigoInput.addEventListener("keydown", (evento) => {
    if (evento.key === "Enter") {
        btnGerarResumo.click();
    }
});

function formatarMoeda(valor) {
    return Number(valor).toLocaleString("pt-BR", {
        style: "currency",
        currency: "BRL"
    });
}