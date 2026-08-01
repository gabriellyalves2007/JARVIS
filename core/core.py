from assistente.memoria import salvar_conversa

from core.contexto import contexto
from core.executor import executar_intencao
from core.intencoes import identificar_intencao


def processar_entrada(texto: str) -> str:
    """
    Identifica a intenção do usuário, executa a ação correspondente,
    atualiza o contexto da conversa e salva o histórico.
    """

    texto = texto.strip()

    if not texto:
        return "Digite um comando para eu processar."

    print("\n========== JARVIS ==========")

    try:
        print(f"👤 Entrada: {texto}")

        intencao = identificar_intencao(texto)

        print(f"🧠 Intenção: {intencao.name}")

        resposta = executar_intencao(
            intencao,
            texto
        )

        if not resposta:
            resposta = "Não consegui processar esse comando."

        contexto.atualizar(
            intencao=intencao,
            comando=texto,
            resposta=resposta
        )

        print(f"🤖 Resposta: {resposta}")

        salvar_conversa(
            texto,
            resposta
        )

        print("💾 Conversa salva")
        print("============================\n")

        return resposta

    except Exception as erro:
        print(
            f"❌ Erro ao processar entrada: {erro}"
        )

        print("============================\n")

        return "Ocorreu um erro ao processar o comando."