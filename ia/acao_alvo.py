import re
from dataclasses import dataclass
from typing import Optional

from ia.interpretador import interpretador


@dataclass
class AcaoAlvo:
    """
    Representa uma ação identificada
    e o alvo sobre o qual ela será executada.
    """

    acao: str
    alvo: str


class AnalisadorAcaoAlvo:
    """
    Identifica ações relacionadas a programas
    e janelas e extrai o respectivo alvo.
    """

    PADROES = (
        (
            (
                r"^(?:abra|abrir|abre|inicie|iniciar|"
                r"execute|executar|acesse|acessar)"
                r"\s+(?:o|a)?\s*(.+)$"
            ),
            "abrir",
        ),
        (
            (
                r"^(?:feche|fechar|fecha|encerre|encerrar|"
                r"finalize|finalizar)"
                r"\s+(?:o|a)?\s*(.+)$"
            ),
            "fechar",
        ),
        (
            (
                r"^(?:reinicie|reiniciar|reabra|reabrir)"
                r"\s+(?:o|a)?\s*(.+)$"
            ),
            "reiniciar",
        ),
        (
            (
                r"^(?:maximize|maximizar)"
                r"\s+(?:o|a)?\s*(.+)$"
            ),
            "maximizar",
        ),
        (
            (
                r"^(?:minimize|minimizar)"
                r"\s+(?:o|a)?\s*(.+)$"
            ),
            "minimizar",
        ),
        (
            (
                r"^(?:restaure|restaurar)"
                r"\s+(?:o|a)?\s*(.+)$"
            ),
            "restaurar",
        ),
        (
            (
                r"^(?:traga|trazer|foque|focar|mostre|mostrar)"
                r"\s+(?:o|a)?\s*(.+?)"
                r"\s+(?:para frente|em primeiro plano)$"
            ),
            "focar",
        ),
    )

    def analisar(
        self,
        comando: str
    ) -> Optional[AcaoAlvo]:
        texto_original = str(comando).strip()

        if not texto_original:
            return None

        texto = interpretador.interpretar(
            texto_original
        )

        for padrao, acao in self.PADROES:
            resultado = re.fullmatch(
                padrao,
                texto,
                flags=re.IGNORECASE
            )

            if resultado is None:
                continue

            alvo = resultado.group(1).strip()

            if not alvo:
                return None

            return AcaoAlvo(
                acao=acao,
                alvo=alvo
            )

        return None

    def eh_comando_programa(
        self,
        comando: str
    ) -> bool:
        return self.analisar(comando) is not None


analisador = AnalisadorAcaoAlvo()

# Mantém compatibilidade com o nome
# utilizado pela primeira implementação.
analisador_acao_alvo = analisador