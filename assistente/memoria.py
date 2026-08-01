import json
import os

ARQUIVO = os.path.join(os.path.dirname(__file__), "memoria.json")


def carregar_memoria():
    try:
        if not os.path.exists(ARQUIVO):
            return {}

        with open(ARQUIVO, "r", encoding="utf-8") as f:
            return json.load(f)

    except:
        return {}


def salvar_memoria(memoria):
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(memoria, f, indent=4, ensure_ascii=False)


def lembrar(chave, valor):
    memoria = carregar_memoria()
    memoria[chave] = valor
    salvar_memoria(memoria)


def obter(chave):
    memoria = carregar_memoria()
    return memoria.get(chave)


def salvar_conversa(pergunta, resposta):
    memoria = carregar_memoria()

    if "chat" not in memoria:
        memoria["chat"] = []

    memoria["chat"].append({
        "pergunta": pergunta,
        "resposta": resposta
    })

    memoria["chat"] = memoria["chat"][-30:]

    salvar_memoria(memoria)


def obter_conversa():
    memoria = carregar_memoria()
    return memoria.get("chat", [])

def obter_contexto(limit=10):
    memoria = carregar_memoria()
    chat = memoria.get("chat", [])
    return chat[-limit:]