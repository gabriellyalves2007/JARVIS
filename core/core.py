from assistente.memoria import salvar_conversa

from core.contexto import contexto
from core.executor import executar_plano
from core.intencoes import identificar_intencao

from ia.planejador import planejador
from ia.resolvedor import resolvedor


def processar_entrada(texto: str) -> str:
    """
    Fluxo principal do JARVIS:

    1. recebe o texto;
    2. resolve referências ao contexto;
    3. identifica a intenção inicial;
    4. cria um plano de execução;
    5. executa todas as etapas;
    6. registra a conversa.
    """

    texto_original = str(texto).strip()

    if not texto_original:
        return "Digite um comando para eu processar."

    print("\n========== JARVIS ==========")

    try:
        print(f"👤 Entrada: {texto_original}")

        comando_resolvido = resolvedor.resolver(
            texto_original
        )

        if comando_resolvido != texto_original:
            print(
                "🔗 Comando resolvido: "
                f"{comando_resolvido}"
            )

        intencao_inicial = identificar_intencao(
            comando_resolvido
        )

        print(
            "🧠 Intenção inicial: "
            f"{intencao_inicial.name}"
        )

        plano = planejador.criar_plano(
            intencao=intencao_inicial,
            comando=comando_resolvido
        )

        etapas = plano.get("etapas", [])

        print(
            f"📋 Etapas do plano: {len(etapas)}"
        )

        for etapa in etapas:
            print(
                f"   {etapa['numero']}. "
                f"{etapa['intencao'].name} → "
                f"{etapa['comando']}"
            )

        resposta = executar_plano(plano)

        if not resposta:
            resposta = (
                "Não consegui processar esse comando."
            )

        resposta = str(resposta).strip()

        ultima_intencao = (
            etapas[-1]["intencao"]
            if etapas
            else intencao_inicial
        )

        contexto.adicionar(
            pergunta=texto_original,
            resposta=resposta,
            intencao=ultima_intencao
        )

        print(f"🤖 Resposta: {resposta}")

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