from enum import Enum, auto

from ia.acao_alvo import analisador
from ia.interpretador import interpretador

from servicos.programas import programas


class Intencao(Enum):
    ABRIR_GOOGLE = auto()
    ABRIR_YOUTUBE = auto()
    ABRIR_CALCULADORA = auto()

    # Mantido com este nome por compatibilidade.
    # Agora também controla programas e janelas.
    ABRIR_PROGRAMA = auto()

    INFORMAR_HORAS = auto()

    SALVAR_NOME = auto()
    LEMBRAR_NOME = auto()

    REPETIR = auto()

    CONSULTAR_TAREFA = auto()
    CANCELAR_TAREFA = auto()

    PESQUISAR = auto()


def contem_alguma(
    texto: str,
    palavras: tuple[str, ...]
) -> bool:
    return any(
        palavra in texto
        for palavra in palavras
    )


def identificar_intencao(
    comando: str
) -> Intencao:
    texto = interpretador.interpretar(
        comando
    )

    if not texto:
        return Intencao.PESQUISAR

    palavras_salvar_nome = (
        "meu nome e",
        "eu me chamo",
        "pode me chamar de",
        "me chame de",
    )

    palavras_perguntar_nome = (
        "qual e meu nome",
        "qual e o meu nome",
        "qual o meu nome",
        "qual que e meu nome",
        "qual que e o meu nome",
        "voce sabe meu nome",
        "voce sabe o meu nome",
        "voce lembra meu nome",
        "voce lembra o meu nome",
        "me fala meu nome",
        "me diga meu nome",
        "como eu me chamo",
        "lembra como eu me chamo",
    )

    palavras_horario = (
        "que horas sao",
        "que hora e",
        "qual e a hora",
        "qual o horario",
        "me diga as horas",
        "me fale as horas",
        "horario agora",
        "horas agora",
    )

    palavras_abrir = (
        "abrir",
        "abra",
        "abre",
        "acessar",
        "acesse",
        "entrar",
        "entre",
        "iniciar",
        "inicie",
        "executar",
        "execute",
    )

    palavras_repetir = (
        "repita",
        "repete",
        "repita isso",
        "novamente",
        "de novo",
        "faz de novo",
        "faca de novo",
        "diga novamente",
        "fala novamente",
    )

    palavras_consultar_tarefa = (
        "qual o progresso",
        "qual e o progresso",
        "qual e o andamento",
        "qual o andamento",
        "como esta a tarefa",
        "como esta o progresso",
        "andamento da tarefa",
        "progresso da tarefa",
        "progresso atual",
        "qual tarefa esta executando",
        "qual tarefa voce esta executando",
        "o que esta executando",
        "o que voce esta executando",
        "status da tarefa",
        "estado da tarefa",
        "a tarefa terminou",
        "a tarefa foi concluida",
    )

    palavras_cancelar_tarefa = (
        "cancele a tarefa",
        "cancelar a tarefa",
        "cancele essa tarefa",
        "cancele a execucao",
        "cancelar a execucao",
        "pare a tarefa",
        "pare a execucao",
        "interrompa a tarefa",
        "interrompa a execucao",
        "interrompa",
        "cancelar",
        "cancele",
    )

    if contem_alguma(
        texto,
        palavras_salvar_nome
    ):
        return Intencao.SALVAR_NOME

    if contem_alguma(
        texto,
        palavras_cancelar_tarefa
    ):
        return Intencao.CANCELAR_TAREFA

    if contem_alguma(
        texto,
        palavras_consultar_tarefa
    ):
        return Intencao.CONSULTAR_TAREFA

    if (
        contem_alguma(
            texto,
            (
                "tarefa",
                "progresso",
                "andamento",
            )
        )
        and contem_alguma(
            texto,
            (
                "qual",
                "como",
                "status",
                "estado",
                "terminou",
                "concluida",
                "executando",
            )
        )
    ):
        return Intencao.CONSULTAR_TAREFA

    if contem_alguma(
        texto,
        palavras_repetir
    ):
        return Intencao.REPETIR

    if contem_alguma(
        texto,
        palavras_perguntar_nome
    ):
        return Intencao.LEMBRAR_NOME

    if (
        "nome" in texto
        and contem_alguma(
            texto,
            (
                "meu",
                "me chamo",
            )
        )
        and contem_alguma(
            texto,
            (
                "qual",
                "sabe",
                "lembra",
                "fala",
                "diga",
                "como",
            )
        )
    ):
        return Intencao.LEMBRAR_NOME

    if contem_alguma(
        texto,
        palavras_horario
    ):
        return Intencao.INFORMAR_HORAS

    if (
        contem_alguma(
            texto,
            (
                "hora",
                "horas",
                "horario",
            )
        )
        and contem_alguma(
            texto,
            (
                "qual",
                "que",
                "agora",
                "diga",
                "fala",
            )
        )
    ):
        return Intencao.INFORMAR_HORAS

    acao_alvo = analisador.analisar(
        comando
    )

    if acao_alvo is not None:
        # Preserva as habilidades específicas
        # para abrir Google, YouTube e calculadora.
        if acao_alvo.acao == "abrir":
            if acao_alvo.alvo in (
                "google",
                "o google",
            ):
                return Intencao.ABRIR_GOOGLE

            if acao_alvo.alvo in (
                "youtube",
                "o youtube",
            ):
                return Intencao.ABRIR_YOUTUBE

            if acao_alvo.alvo in (
                "calculadora",
                "a calculadora",
            ):
                return Intencao.ABRIR_CALCULADORA

        # Ações de janela podem funcionar mesmo
        # quando o alvo não está no catálogo.
        if acao_alvo.acao in {
            "minimizar",
            "maximizar",
            "restaurar",
            "focar",
        }:
            return Intencao.ABRIR_PROGRAMA

        if programas.existe(
            acao_alvo.alvo
        ):
            return Intencao.ABRIR_PROGRAMA

    if "google" in texto:
        return Intencao.ABRIR_GOOGLE

    if "youtube" in texto:
        return Intencao.ABRIR_YOUTUBE

    if "calculadora" in texto:
        return Intencao.ABRIR_CALCULADORA

    if (
        contem_alguma(
            texto,
            palavras_abrir
        )
        and programas.existe(texto)
    ):
        return Intencao.ABRIR_PROGRAMA

    if contem_alguma(
        texto,
        palavras_abrir
    ):
        if "navegador" in texto:
            return Intencao.ABRIR_GOOGLE

        if (
            "video" in texto
            or "videos" in texto
        ):
            return Intencao.ABRIR_YOUTUBE

        if (
            "calcular" in texto
            or "conta" in texto
        ):
            return Intencao.ABRIR_CALCULADORA

    return Intencao.PESQUISAR