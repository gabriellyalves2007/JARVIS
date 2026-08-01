import re

from core.intencoes import identificar_intencao


class Planejador:
    """
    Cria planos com uma ou várias etapas.

    Exemplos:
    - "abra o Google"
    - "abra o Google e abra o YouTube"
    - "abra a calculadora, depois diga as horas"
    """

    def dividir_comando(self, comando: str) -> list[str]:
        comando = comando.strip()

        if not comando:
            return []

        partes = re.split(
            r"\s*(?:,|;|\be depois\b|\bdepois\b|\be\b)\s*",
            comando,
            flags=re.IGNORECASE
        )

        return [
            parte.strip()
            for parte in partes
            if parte.strip()
        ]

    def criar_plano(
        self,
        intencao,
        comando: str
    ) -> dict:
        comando = comando.strip()

        comandos = self.dividir_comando(comando)

        if not comandos:
            return {
                "comando_original": comando,
                "etapas": []
            }

        etapas = []

        for indice, comando_etapa in enumerate(comandos):
            # Se houver somente uma etapa, reaproveita
            # a intenção já identificada pelo Core.
            if len(comandos) == 1:
                intencao_etapa = intencao
            else:
                intencao_etapa = identificar_intencao(
                    comando_etapa
                )

            etapas.append(
                {
                    "numero": indice + 1,
                    "tipo": "executar_intencao",
                    "intencao": intencao_etapa,
                    "comando": comando_etapa,
                }
            )

        return {
            "comando_original": comando,
            "etapas": etapas
        }


planejador = Planejador()