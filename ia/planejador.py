class Planejador:
    """
    Cria um plano de execução a partir da intenção
    identificada e do comando do usuário.

    Nesta primeira versão, cada plano possui apenas
    uma etapa. Futuramente, poderá dividir comandos
    compostos em várias ações.
    """

    def criar_plano(
        self,
        intencao,
        comando: str
    ) -> dict:
        comando = comando.strip()

        return {
            "intencao": intencao,
            "comando": comando,
            "etapas": [
                {
                    "tipo": "executar_intencao",
                    "intencao": intencao,
                    "comando": comando,
                }
            ],
        }


planejador = Planejador()