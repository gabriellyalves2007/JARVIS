import re

from core.intencoes import identificar_intencao


class Planejador:
    """
    Planejador inteligente.

    Recebe um comando do usuário e transforma
    em um plano composto por uma ou várias etapas.
    """

    SEPARADORES = (
        r"\be depois\b",
        r"\bdepois\b",
        r"\bem seguida\b",
        r"\bentão\b",
        r"\bentao\b",
        r"\blogo após\b",
        r"\blogo apos\b",
        r"\bpor fim\b",
        r"\be\b",
        ",",
        ";",
    )

    def dividir_comando(
        self,
        comando: str
    ) -> list[str]:

        comando = comando.strip()

        regex = "|".join(self.SEPARADORES)

        partes = re.split(
            regex,
            comando,
            flags=re.IGNORECASE
        )

        resultado = []

        for parte in partes:

            parte = parte.strip()

            if parte:
                resultado.append(parte)

        return resultado

    def criar_plano(
        self,
        intencao,
        comando: str
    ) -> dict:

        etapas = []

        comandos = self.dividir_comando(
            comando
        )

        for indice, trecho in enumerate(comandos):

            if len(comandos) == 1:
                intencao_etapa = intencao

            else:
                intencao_etapa = identificar_intencao(
                    trecho
                )

            etapas.append(
                {
                    "numero": indice + 1,
                    "comando": trecho,
                    "intencao": intencao_etapa,
                    "executado": False,
                }
            )

        return {
            "comando_original": comando,
            "total": len(etapas),
            "etapas": etapas,
        }


planejador = Planejador()