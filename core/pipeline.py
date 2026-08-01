from assistente.memoria import salvar_conversa

from core.contexto import contexto
from core.executor import executar_plano
from core.intencoes import identificar_intencao
from core.router import router

from ia.corretor import corretor
from ia.planejador import planejador
from ia.resolvedor import resolvedor


class Pipeline:

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

        if comando_corrigido.lower() != comando.lower():
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
        destino: str,
        plano: dict
    ) -> str:
        """
        Encaminha o plano ao componente escolhido pelo Router.
        """

        if destino == router.DESTINO_EXECUTOR:
            return executar_plano(plano)

        if destino == router.DESTINO_MEMORIA:
            return (
                "O módulo de memória ainda não está "
                "disponível neste fluxo."
            )

        if destino == router.DESTINO_IA:
            return (
                "O módulo de inteligência artificial "
                "ainda não foi integrado."
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

            if comando.lower() != texto_original.lower():
                print(
                    f"🔗 Comando processado: {comando}"
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
                f"🧭 Destino: {destino}"
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
                print(
                    f"   {etapa['numero']}. "
                    f"{etapa['intencao'].name} → "
                    f"{etapa['comando']}"
                )

            resposta = self.executar_por_destino(
                destino=destino,
                plano=plano
            )

            resposta = self.depois_executar(
                resposta
            )

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
                f"❌ Erro no Pipeline: {erro}"
            )

            print("==============================\n")

            return (
                "Ocorreu um erro ao processar "
                "o comando."
            )


pipeline = Pipeline()