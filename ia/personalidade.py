import random


class Personalidade:

    def __init__(self):

        self.frases = {

            "ABRIR_GOOGLE": [
                "Claro. Abrindo o Google.",
                "Tudo certo. Abrindo o Google.",
                "Pode deixar. Abrindo o Google agora.",
                "Google sendo iniciado."
            ],

            "ABRIR_YOUTUBE": [
                "Abrindo o YouTube.",
                "Tudo pronto. YouTube iniciado.",
                "Pode aproveitar. Abrindo o YouTube."
            ],

            "ABRIR_CALCULADORA": [
                "Abrindo a calculadora.",
                "Calculadora iniciada.",
                "Tudo certo. Calculadora aberta."
            ],

            "SALVAR_NOME": [
                "Prazer em conhecer você.",
                "Vou lembrar disso.",
                "Informação salva com sucesso.",
                "Pode deixar, não vou esquecer."
            ],

            "ERRO": [
                "Não consegui realizar essa ação.",
                "Algo deu errado.",
                "Tive um problema ao executar esse comando."
            ]
        }

    def responder(self, chave: str) -> str:

        if chave not in self.frases:
            return ""

        return random.choice(
            self.frases[chave]
        )


personalidade = Personalidade()