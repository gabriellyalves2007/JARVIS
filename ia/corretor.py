import re
import unicodedata
from difflib import get_close_matches


class CorretorTexto:
    """
    Corrige erros comuns de digitação e reconhecimento de voz.

    Primeiro usa correções exatas.
    Depois tenta encontrar palavras parecidas.
    """

    def __init__(self):
        self.correcoes_exatas = {
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

        self.palavras_conhecidas = (
            "abra",
            "abrir",
            "abre",
            "acesse",
            "acessar",
            "entre",
            "entrar",
            "inicie",
            "iniciar",
            "execute",
            "executar",
            "pesquise",
            "pesquisar",
            "procure",
            "buscar",
            "busque",
            "google",
            "youtube",
            "calculadora",
            "horario",
            "hora",
            "horas",
            "nome",
            "repita",
            "novamente",
        )

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

    def corrigir_palavra(self, palavra: str) -> str:
        palavra_normalizada = self.remover_acentos(
            palavra.lower()
        )

        # Correção manual primeiro.
        if palavra_normalizada in self.correcoes_exatas:
            return self.correcoes_exatas[
                palavra_normalizada
            ]

        # Se já for conhecida, mantém.
        if palavra_normalizada in self.palavras_conhecidas:
            return palavra

        # Ignora palavras muito curtas para evitar
        # correções erradas como "e", "o", "a".
        if len(palavra_normalizada) < 4:
            return palavra

        correspondencias = get_close_matches(
            palavra_normalizada,
            self.palavras_conhecidas,
            n=1,
            cutoff=0.72
        )

        if correspondencias:
            return correspondencias[0]

        return palavra

    def corrigir(self, texto: str) -> str:
        texto = str(texto).strip()

        if not texto:
            return ""

        partes = re.findall(
            r"\w+|[^\w\s]",
            texto,
            flags=re.UNICODE
        )

        resultado = []

        for parte in partes:
            if re.fullmatch(r"\w+", parte):
                parte = self.corrigir_palavra(parte)

            resultado.append(parte)

        texto_corrigido = " ".join(resultado)

        texto_corrigido = re.sub(
            r"\s+([,.!?;:])",
            r"\1",
            texto_corrigido
        )

        return texto_corrigido


corretor = CorretorTexto()