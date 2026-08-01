from assistente.memoria import salvar_conversa

from core.contexto import contexto
from core.executor import executar_plano
from core.intencoes import identificar_intencao

from ia.planejador import planejador
from ia.resolvedor import resolvedor


class Pipeline:

    def executar(self, texto: str) -> str:
        texto_original = str(texto).strip()

        if not texto_original:
            return "Digite um comando."

        print("\n========== PIPELINE ==========")

        try:
            print(f"👤 Entrada: {texto_original}")

            comando = resolvedor.resolver(
                texto_original
            )

            if comando != texto_original:
                print(
                    f"🔗 Contexto: {comando}"
                )

            intencao = identificar_intencao(
                comando
            )

            print(
                f"🧠 Intenção inicial: "
                f"{intencao.name}"
            )

            plano = planejador.criar_plano(
                intencao,
                comando
            )

            etapas = plano.get(
                "etapas",
                []
            )

            print(
                f"📋 Plano: {len(etapas)} etapa(s)"
            )

            for etapa in etapas:
                print(
                    f"   {etapa['numero']}. "
                    f"{etapa['intencao'].name} → "
                    f"{etapa['comando']}"
                )

            resposta = executar_plano(
                plano
            )

            if not resposta:
                resposta = (
                    "Não consegui processar "
                    "esse comando."
                )

            resposta = str(resposta).strip()

            ultima_intencao = (
                etapas[-1]["intencao"]
                if etapas
                else intencao
            )

            contexto.adicionar(
                pergunta=texto_original,
                resposta=resposta,
                intencao=ultima_intencao
            )

            salvar_conversa(
                texto_original,
                resposta
            )

            print(f"🤖 Resposta: {resposta}")
            print("💾 Contexto atualizado")
            print("==============================\n")

            return resposta

        except Exception as erro:
            print(
                f"❌ Erro no pipeline: {erro}"
            )

            print("==============================\n")

            return (
                "Ocorreu um erro ao processar "
                "o comando."
            )


pipeline = Pipeline()