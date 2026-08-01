from core.intencoes import Intencao


class Router:
    """
    Decide qual componente deve processar uma intenção.

    Nesta primeira versão, todas as intenções existentes
    continuam sendo encaminhadas ao executor.
    """

    DESTINO_EXECUTOR = "executor"
    DESTINO_IA = "ia"
    DESTINO_MEMORIA = "memoria"
    DESTINO_DESCONHECIDO = "desconhecido"

    def decidir(
        self,
        intencao: Intencao,
        comando: str
    ) -> str:
        if intencao is None:
            return self.DESTINO_DESCONHECIDO

        intencoes_executor = {
            Intencao.ABRIR_GOOGLE,
            Intencao.ABRIR_YOUTUBE,
            Intencao.ABRIR_CALCULADORA,
            Intencao.INFORMAR_HORAS,
            Intencao.SALVAR_NOME,
            Intencao.LEMBRAR_NOME,
            Intencao.REPETIR,
            Intencao.PESQUISAR,
        }

        if intencao in intencoes_executor:
            return self.DESTINO_EXECUTOR

        return self.DESTINO_DESCONHECIDO


router = Router()