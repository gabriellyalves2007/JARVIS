import re
import unicodedata


class Interpretador:
    """
    Responsável por preparar qualquer frase antes
    que ela seja analisada pelo núcleo do sistema.
    """

    def normalizar(self, texto: str) -> str:

        texto = texto.lower().strip()

        texto = unicodedata.normalize(
            "NFD",
            texto
        )

        texto = "".join(
            caractere
            for caractere in texto
            if unicodedata.category(caractere) != "Mn"
        )

        texto = re.sub(
            r"[^\w\s]",
            "",
            texto
        )

        texto = " ".join(
            texto.split()
        )

        return texto

    def interpretar(
        self,
        comando: str
    ) -> str:

        return self.normalizar(comando)


interpretador = Interpretador()