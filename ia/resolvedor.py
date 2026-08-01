from core.contexto import contexto

from ia.contexto import usa_contexto


class ResolvedorContexto:
    """
    Resolve comandos que dependem
    da conversa anterior.
    """

    def resolver(
        self,
        comando: str
    ) -> str:

        comando = comando.strip()

        if not usa_contexto(comando):
            return comando

        if not contexto.historico:
            return comando

        ultima = contexto.historico[-1]

        pergunta = ultima["pergunta"]

        return self.completar(
            comando,
            pergunta
        )

    def completar(
        self,
        atual: str,
        anterior: str
    ) -> str:

        atual = atual.lower()

        if atual.startswith("e "):

            return (
                anterior.split("?")[0]
                + " "
                + atual[2:]
            )

        if "novamente" in atual:

            return anterior

        return atual


resolvedor = ResolvedorContexto()