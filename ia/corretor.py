import re
import unicodedata


class CorretorTexto:
    """
    Corrige erros comuns de digitação e de reconhecimento de voz
    antes que o comando seja interpretado pelo JARVIS.
    """

    def __init__(self):
        self.correcoes = {
            # Ações
            "abri": "abra",
            "abririr": "abrir",
            "abreir": "abrir",
            "pesquiza": "pesquise",
            "pesquisae": "pesquise",
            "procura": "procure",

            # Aplicações e serviços
            "gugou": "google",
            "gugol": "google",
            "googol": "google",
            "youtubi": "youtube",
            "iutube": "youtube",
            "calculadoura": "calculadora",
            "calculadoraa": "calculadora",

            # Horário
            "orario": "horario",
            "horarrio": "horario",
        }

    @staticmethod
    def remover_acentos(texto: str) -> str:
        texto_normalizado = unicodedata.normalize(
            "NFD",
            texto
        )

        return "".join(
            caractere
            for caractere in texto_normalizado
            if unicodedata.category(caractere) != "Mn"
        )

    def corrigir(self, texto: str) -> str:
        texto = str(texto).strip()

        if not texto:
            return ""

        palavras = re.findall(
            r"\w+|[^\w\s]",
            texto,
            flags=re.UNICODE
        )

        resultado = []

        for palavra in palavras:
            palavra_comparacao = self.remover_acentos(
                palavra.lower()
            )

            palavra_corrigida = self.correcoes.get(
                palavra_comparacao,
                palavra
            )

            resultado.append(palavra_corrigida)

        texto_corrigido = " ".join(resultado)

        # Remove espaços antes de pontuação.
        texto_corrigido = re.sub(
            r"\s+([,.!?;:])",
            r"\1",
            texto_corrigido
        )

        return texto_corrigido


corretor = CorretorTexto()