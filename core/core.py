from assistente.memoria import salvar_conversa

from core.contexto import contexto
from core.executor import executar_intencao
from core.intencoes import identificar_intencao

from ia.planejador import planejador
from ia.resolvedor import resolvedor


def processar_entrada(texto: str) -> str:
    """
    Fluxo principal do JARVIS:

    1. recebe o texto;
    2. resolve referências ao contexto;
    3. identifica a intenção;
    4. cria um plano;
    5. executa o plano;
    6. registra a conversa no contexto e no histórico.
    """

    texto_original = str(texto).strip()

    if not texto_original:
        return "Digite um comando para eu processar."

    print("\n========== JARVIS ==========")

    try:
        print(f"👤 Entrada: {texto_original}")

        # Completa comandos que dependem da conversa anterior.
        comando_resolvido = resolvedor.resolver(
            texto_original
        )

        if comando_resolvido != texto_original:
            print(
                "🔗 Comando resolvido: "
                f"{comando_resolvido}"
            )

        # O intencoes.py já utiliza o interpretador
        # para normalizar e analisar o texto.
        intencao = identificar_intencao(
            comando_resolvido
        )

        print(f"🧠 Intenção: {intencao.name}")

        plano = planejador.criar_plano(
            intencao=intencao,
            comando=comando_resolvido
        )

        print(
            f"📋 Etapas do plano: "
            f"{len(plano['etapas'])}"
        )

        resposta = executar_intencao(
            plano["intencao"],
            plano["comando"]
        )

        if not resposta:
            resposta = (
                "Não consegui processar esse comando."
            )

        resposta = str(resposta).strip()

        # Guarda a interação na memória temporária.
        contexto.adicionar(
            pergunta=texto_original,
            resposta=resposta,
            intencao=intencao
        )

        print(f"🤖 Resposta: {resposta}")

        # Guarda a conversa na memória permanente.
        salvar_conversa(
            texto_original,
            resposta
        )

        print("💾 Conversa salva")
        print("============================\n")

        return resposta

    except Exception as erro:
        print(
            "❌ Erro ao processar entrada: "
            f"{erro}"
        )

        print("============================\n")

        return (
            "Ocorreu um erro ao processar "
            "o comando."
        )