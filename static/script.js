const btnComecar = document.getElementById("btnComecar");
const btnAbrirChat = document.getElementById("btnAbrirChat");
const btnGerarResumo = document.getElementById("btnGerarResumo");
const btnReiniciar = document.getElementById("btnReiniciar");

const inicioArea = document.getElementById("inicioArea");
const formularioArea = document.getElementById("formularioArea");
const chatArea = document.getElementById("chatArea");
const codigoInput = document.getElementById("codigoInput");
const confirmacaoInput = document.getElementById("confirmacaoInput");
const resultado = document.getElementById("resultado");

const btnFeedback = document.getElementById("btnFeedback");
const btnAcessibilidade = document.getElementById("btnAcessibilidade");
const btnIdioma = document.getElementById("btnIdioma");
const btnAdmin = document.getElementById("btnAdmin");

const feedbackModal = document.getElementById("feedbackModal");
const adminModal = document.getElementById("adminModal");
const accessPanel = document.getElementById("accessPanel");
const languagePanel = document.getElementById("languagePanel");

const btnEnviarFeedback = document.getElementById("btnEnviarFeedback");
const feedbackNome = document.getElementById("feedbackNome");
const feedbackMensagem = document.getElementById("feedbackMensagem");
const feedbackStatus = document.getElementById("feedbackStatus");

const btnEsqueciSenha = document.getElementById("btnEsqueciSenha");
const forgotBox = document.getElementById("forgotBox");

let currentLang = localStorage.getItem("assistenteIdioma") || "pt";

const translations = {
    pt: {
        badge: "Assistente Financeiro com IA",
        aiChip: "Análise inteligente em tempo real",
        heroTitle: "Organize sua vida financeira com ajuda personalizada",
        heroSubtitle: "Responda o formulário, informe seu código de identificação e receba um resumo financeiro baseado nas suas respostas.",
        terminal1: "lendo respostas financeiras...",
        terminal2: "calculando renda, gastos e saldo...",
        terminal3: "preparando recomendações personalizadas...",
        startButton: "Começar organização financeira",
        privacyNote: "Seus dados são usados apenas para gerar o resumo financeiro. Para acessar, será necessário informar o código e a confirmação de segurança.",
        formTitle: "1. Responda o formulário",
        formText: "Preencha com atenção. Anote seu Código de identificação e sua Confirmação de segurança. Eles serão necessários para abrir seu resumo.",
        chatTitle: "2. Chat financeiro",
        chatMessage: "Olá! Digite o mesmo Código de identificação e a Confirmação de segurança que você colocou no formulário.",
        codePlaceholder: "Código de identificação",
        securityPlaceholder: "Confirmação de segurança",
        generateButton: "Gerar resumo",
        restartButton: "Reiniciar e voltar ao início",
        openChatButton: "Já respondi, abrir chat",
        versionLabel: "Versão",
        feedbackTitle: "Enviar feedback",
        feedbackText: "Conte o que você achou ou o que precisa melhorar.",
        feedbackNamePlaceholder: "Seu nome, opcional",
        feedbackMessagePlaceholder: "Digite seu feedback",
        sendFeedbackButton: "Enviar feedback",
        adminTitle: "Acesso Admin",
        adminText: "Área restrita para manutenção do sistema.",
        adminUserPlaceholder: "Usuário admin",
        adminPasswordPlaceholder: "Senha admin",
        adminLoginButton: "Entrar",
        forgotPasswordButton: "Esqueci minha senha",
        forgotTitle: "Recuperar acesso admin",
        forgotText: "Por segurança, a senha do admin não fica salva visível no site. Para redefinir, altere a variável ADMIN_PASSWORD no Google Cloud Run.",
        forgotCommandText: "Use este comando no terminal:",
        forgotFinalText: "Depois faça login novamente usando o usuário admin e a nova senha.",
        accessTitle: "Acessibilidade",
        increaseFont: "A+ Aumentar fonte",
        decreaseFont: "A- Diminuir fonte",
        contrast: "Alto contraste",
        lightMode: "Modo claro",
        reduceMotion: "Reduzir animações",
        resetAccess: "Resetar",
        languageTitle: "Idioma",
        loadingSummary: "Buscando seus dados e gerando resumo...",
        errorCode: "Digite seu Código de identificação.",
        errorSecurity: "Digite sua Confirmação de segurança.",
        summaryTitle: "Resumo financeiro de",
        totalIncome: "Renda total",
        totalExpenses: "Gastos mensais aproximados",
        balance: "Saldo estimado",
        commitment: "Porcentagem da renda comprometida",
        objective: "Objetivo financeiro",
        saveAmount: "Valor que deseja guardar",
        deadline: "Prazo informado",
        profile: "Perfil financeiro",
        concern: "Maior preocupação",
        guidance: "Orientações iniciais",
        feedbackSending: "Enviando feedback...",
        feedbackEmpty: "Digite uma mensagem antes de enviar.",
        feedbackSuccess: "Feedback enviado com sucesso. Obrigado!",
        feedbackError: "Erro ao enviar feedback agora.",
        summaryGenericError: "Ocorreu um erro ao gerar o resumo. Verifique se a planilha está pública e se os dados foram digitados corretamente."
    },
    en: {
        badge: "AI Financial Assistant",
        aiChip: "Real-time intelligent analysis",
        heroTitle: "Organize your financial life with personalized support",
        heroSubtitle: "Answer the form, enter your identification code, and receive a financial summary based on your answers.",
        terminal1: "reading financial answers...",
        terminal2: "calculating income, expenses and balance...",
        terminal3: "preparing personalized recommendations...",
        startButton: "Start financial organization",
        privacyNote: "Your data is used only to generate the financial summary. To access it, you must enter your code and security confirmation.",
        formTitle: "1. Answer the form",
        formText: "Fill it out carefully. Save your identification code and security confirmation. They will be required to open your summary.",
        chatTitle: "2. Financial chat",
        chatMessage: "Hello! Enter the same identification code and security confirmation you used in the form.",
        codePlaceholder: "Identification code",
        securityPlaceholder: "Security confirmation",
        generateButton: "Generate summary",
        restartButton: "Restart and go back to start",
        openChatButton: "I answered, open chat",
        versionLabel: "Version",
        feedbackTitle: "Send feedback",
        feedbackText: "Tell us what you think or what needs improvement.",
        feedbackNamePlaceholder: "Your name, optional",
        feedbackMessagePlaceholder: "Type your feedback",
        sendFeedbackButton: "Send feedback",
        adminTitle: "Admin Access",
        adminText: "Restricted area for system maintenance.",
        adminUserPlaceholder: "Admin user",
        adminPasswordPlaceholder: "Admin password",
        adminLoginButton: "Sign in",
        forgotPasswordButton: "I forgot my password",
        forgotTitle: "Recover admin access",
        forgotText: "For security, the admin password is not visibly stored on the site. To reset it, update the ADMIN_PASSWORD variable in Google Cloud Run.",
        forgotCommandText: "Use this command in the terminal:",
        forgotFinalText: "Then log in again using the admin user and the new password.",
        accessTitle: "Accessibility",
        increaseFont: "A+ Increase font",
        decreaseFont: "A- Decrease font",
        contrast: "High contrast",
        lightMode: "Light mode",
        reduceMotion: "Reduce animations",
        resetAccess: "Reset",
        languageTitle: "Language",
        loadingSummary: "Searching your data and generating summary...",
        errorCode: "Enter your identification code.",
        errorSecurity: "Enter your security confirmation.",
        summaryTitle: "Financial summary for",
        totalIncome: "Total income",
        totalExpenses: "Approximate monthly expenses",
        balance: "Estimated balance",
        commitment: "Income commitment percentage",
        objective: "Financial goal",
        saveAmount: "Amount you want to save",
        deadline: "Reported deadline",
        profile: "Financial profile",
        concern: "Main concern",
        guidance: "Initial guidance",
        feedbackSending: "Sending feedback...",
        feedbackEmpty: "Type a message before sending.",
        feedbackSuccess: "Feedback sent successfully. Thank you!",
        feedbackError: "Error sending feedback now.",
        summaryGenericError: "An error occurred while generating the summary. Check if the spreadsheet is public and if the data was typed correctly."
    }
};

function t(key) {
    return translations[currentLang][key] || translations.pt[key] || key;
}

function aplicarIdioma(lang) {
    currentLang = lang;
    localStorage.setItem("assistenteIdioma", lang);

    const htmlRoot = document.getElementById("htmlRoot");

    if (htmlRoot) {
        htmlRoot.setAttribute("lang", lang === "pt" ? "pt-BR" : "en");
    }

    document.querySelectorAll("[data-i18n]").forEach((elemento) => {
        const chave = elemento.getAttribute("data-i18n");
        elemento.textContent = t(chave);
    });

    document.querySelectorAll("[data-i18n-placeholder]").forEach((elemento) => {
        const chave = elemento.getAttribute("data-i18n-placeholder");
        elemento.setAttribute("placeholder", t(chave));
    });
}

aplicarIdioma(currentLang);

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
    const confirmacao = confirmacaoInput.value.trim();

    resultado.classList.remove("hidden");
    resultado.classList.remove("erro");
    resultado.innerHTML = `<p>${t("loadingSummary")}</p>`;

    if (!codigo) {
        resultado.classList.add("erro");
        resultado.innerHTML = `<p><strong>${t("errorCode")}</strong></p>`;
        return;
    }

    if (!confirmacao) {
        resultado.classList.add("erro");
        resultado.innerHTML = `<p><strong>${t("errorSecurity")}</strong></p>`;
        return;
    }

    try {
        const resposta = await fetch("/gerar-resumo", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                codigo,
                confirmacao,
                idioma: currentLang
            })
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
            <h3>${t("summaryTitle")} ${dados.nome}</h3>

            <p><strong>${t("totalIncome")}:</strong> ${rendaFormatada}</p>
            <p><strong>${t("totalExpenses")}:</strong> ${gastosFormatados}</p>
            <p><strong>${t("balance")}:</strong> ${saldoFormatado}</p>
            <p><strong>${t("commitment")}:</strong> ${dados.porcentagem_gastos}%</p>

            <hr>

            <p><strong>${t("objective")}:</strong> ${dados.objetivo}</p>
            <p><strong>${t("saveAmount")}:</strong> ${guardarFormatado}</p>
            <p><strong>${t("deadline")}:</strong> ${dados.prazo}</p>
            <p><strong>${t("profile")}:</strong> ${dados.perfil}</p>
            <p><strong>${t("concern")}:</strong> ${dados.preocupacao}</p>

            <h4>${t("guidance")}</h4>
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
                <strong>${t("summaryGenericError")}</strong>
            </p>
        `;
    }
});

btnReiniciar.addEventListener("click", () => {
    window.location.href = "/";
});

codigoInput.addEventListener("keydown", (evento) => {
    if (evento.key === "Enter") {
        confirmacaoInput.focus();
    }
});

confirmacaoInput.addEventListener("keydown", (evento) => {
    if (evento.key === "Enter") {
        btnGerarResumo.click();
    }
});

btnFeedback.addEventListener("click", () => {
    feedbackModal.classList.remove("hidden");
});

btnAdmin.addEventListener("click", () => {
    adminModal.classList.remove("hidden");
});

btnAcessibilidade.addEventListener("click", () => {
    accessPanel.classList.toggle("hidden");
    languagePanel.classList.add("hidden");
});

btnIdioma.addEventListener("click", () => {
    languagePanel.classList.toggle("hidden");
    accessPanel.classList.add("hidden");
});

document.querySelectorAll("[data-lang]").forEach((botao) => {
    botao.addEventListener("click", () => {
        const lang = botao.getAttribute("data-lang");
        aplicarIdioma(lang);
        languagePanel.classList.add("hidden");
    });
});

if (btnEsqueciSenha && forgotBox) {
    btnEsqueciSenha.addEventListener("click", () => {
        forgotBox.classList.toggle("hidden");
    });
}

document.querySelectorAll(".modal-close").forEach((botao) => {
    botao.addEventListener("click", () => {
        const modalId = botao.getAttribute("data-close");
        document.getElementById(modalId).classList.add("hidden");
    });
});

document.querySelectorAll(".modal").forEach((modal) => {
    modal.addEventListener("click", (evento) => {
        if (evento.target === modal) {
            modal.classList.add("hidden");
        }
    });
});

btnEnviarFeedback.addEventListener("click", async () => {
    const nome = feedbackNome.value.trim();
    const mensagem = feedbackMensagem.value.trim();

    feedbackStatus.textContent = t("feedbackSending");

    if (!mensagem) {
        feedbackStatus.textContent = t("feedbackEmpty");
        return;
    }

    try {
        const resposta = await fetch("/feedback", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                nome,
                mensagem
            })
        });

        const dados = await resposta.json();

        if (!resposta.ok) {
            feedbackStatus.textContent = dados.erro || t("feedbackError");
            return;
        }

        feedbackStatus.textContent = t("feedbackSuccess");
        feedbackMensagem.value = "";

    } catch (erro) {
        console.error(erro);
        feedbackStatus.textContent = t("feedbackError");
    }
});

document.getElementById("btnAumentarFonte").addEventListener("click", () => {
    document.body.classList.remove("font-small");
    document.body.classList.add("font-large");
});

document.getElementById("btnDiminuirFonte").addEventListener("click", () => {
    document.body.classList.remove("font-large");
    document.body.classList.add("font-small");
});

document.getElementById("btnContraste").addEventListener("click", () => {
    document.body.classList.toggle("high-contrast");
});

document.getElementById("btnModoClaro").addEventListener("click", () => {
    document.body.classList.toggle("light-mode");
});

document.getElementById("btnReducaoAnimacao").addEventListener("click", () => {
    document.body.classList.toggle("reduce-motion");
});

document.getElementById("btnResetAcessibilidade").addEventListener("click", () => {
    document.body.classList.remove(
        "font-large",
        "font-small",
        "high-contrast",
        "light-mode",
        "reduce-motion"
    );
});

function formatarMoeda(valor) {
    if (currentLang === "en") {
        return Number(valor).toLocaleString("en-US", {
            style: "currency",
            currency: "BRL"
        });
    }

    return Number(valor).toLocaleString("pt-BR", {
        style: "currency",
        currency: "BRL"
    });
}