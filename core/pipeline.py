from assistente.comandos import pesquisar as pesquisar_conhecimento
from assistente.memoria import salvar_conversa

from core.contexto import contexto
from core.executor import executar_plano
from core.intencoes import identificar_intencao
from core.router import Destino, router

from ia.corretor import corretor
from ia.planejador import planejador
from ia.resolvedor import resolvedor


class Pipeline:
    """
    Coordena o fluxo completo de processamento do JARVIS.
    """

    def antes_processar(
        self,
        texto: str
    ) -> str:
        return str(texto).strip()

    def antes_interpretar(
        self,
        comando: str
    ) -> str:
        comando_corrigido = corretor.corrigir(
            comando
        )

        if (
            comando_corrigido.lower()
            != comando.lower()
        ):
            print(
                "✏️ Comando corrigido: "
                f"{comando_corrigido}"
            )

        return resolvedor.resolver(
            comando_corrigido
        )

    def depois_planejar(
        self,
        plano: dict
    ) -> dict:
        return plano

    def depois_executar(
        self,
        resposta: str
    ) -> str:
        resposta = str(resposta).strip()

        if not resposta:
            return "Não consegui produzir uma resposta."

        return resposta

    def executar_por_destino(
        self,
        destino: Destino,
        plano: dict,
        comando: str
    ) -> str:
        """
        Encaminha o comando para o destino
        escolhido pelo Router.
        """

        if destino == Destino.EXECUTOR:
            return executar_plano(plano)

        if destino == Destino.INTERNET:
            return pesquisar_conhecimento(
                comando
            )

        if destino == Destino.MEMORIA:
            return (
                "O módulo específico de memória "
                "ainda não está disponível."
            )

        if destino == Destino.IA:
            return (
                "O módulo de inteligência artificial "
                "ainda não foi integrado."
            )

        if destino == Destino.PLUGIN:
            return (
                "O sistema de plugins ainda não "
                "foi integrado."
            )

        return (
            "Não encontrei um destino adequado "
            "para esse comando."
        )

    def executar(
        self,
        texto: str
    ) -> str:
        texto_original = self.antes_processar(
            texto
        )

        if not texto_original:
            return "Digite um comando."

        print("\n========== PIPELINE ==========")

        try:
            print(
                f"👤 Entrada: {texto_original}"
            )

            comando = self.antes_interpretar(
                texto_original
            )

            if (
                comando.lower()
                != texto_original.lower()
            ):
                print(
                    "🔗 Comando processado: "
                    f"{comando}"
                )

            intencao_inicial = identificar_intencao(
                comando
            )

            print(
                "🧠 Intenção inicial: "
                f"{intencao_inicial.name}"
            )

            destino = router.decidir(
                intencao=intencao_inicial,
                comando=comando
            )

            print(
                f"🧭 Destino: {destino.value}"
            )

            plano = planejador.criar_plano(
                intencao_inicial,
                comando
            )

            plano = self.depois_planejar(
                plano
            )

            etapas = plano.get(
                "etapas",
                []
            )

            print(
                f"📋 Plano: {len(etapas)} etapa(s)"
            )

            for etapa in etapas:
                numero = etapa.get(
                    "numero",
                    "?"
                )

                intencao_etapa = etapa.get(
                    "intencao"
                )

                comando_etapa = etapa.get(
                    "comando",
                    ""
                )

                nome_intencao = (
                    intencao_etapa.name
                    if intencao_etapa is not None
                    else "DESCONHECIDA"
                )

                print(
                    f"   {numero}. "
                    f"{nome_intencao} → "
                    f"{comando_etapa}"
                )

            resposta = self.executar_por_destino(
                destino=destino,
                plano=plano,
                comando=comando
            )

            resposta = self.depois_executar(
                resposta
            )

            ultima_intencao = (
                etapas[-1].get("intencao")
                if etapas
                else intencao_inicial
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

            print(
                f"🤖 Resposta: {resposta}"
            )

            print("💾 Contexto atualizado")
            print("==============================\n")

            return resposta

        except Exception as erro:
            print(
                "❌ Erro no Pipeline: "
                f"{erro}"
            )

            print("==============================\n")

            return (
                "Ocorreu um erro ao processar "
                "o comando."
            )


pipeline = Pipeline()