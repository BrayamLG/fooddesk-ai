"""Motor determinístico de demonstração do FoodDesk AI.

Não utiliza LLM, API, rede ou credenciais. As regras abaixo geram exemplos
reproduzíveis para demonstrar o contrato de dados esperado da análise.
"""
from __future__ import annotations

from security_utils import validar_resposta_modelo


def analisar_avaliacao_demo(nota: int, comentario: str) -> dict[str, str]:
    if isinstance(nota, bool) or not isinstance(nota, int) or not 1 <= nota <= 5:
        raise ValueError("A nota deve ser um número inteiro entre 1 e 5.")
    if not isinstance(comentario, str):
        raise TypeError("O comentário deve ser um texto.")

    texto = comentario.casefold()
    if any(p in texto for p in ("atras", "demor", "entrega", "pedido não chegou", "pedido nao chegou")):
        categoria = "Logística / Atraso"
        causa = "O comentário indica possível atraso ou problema na entrega."
        acao = "Verificar o status do pedido e orientar a equipe responsável pela entrega."
    elif any(p in texto for p in ("faltou", "falta", "item não veio", "item nao veio", "esqueceram")):
        categoria = "Item Faltante"
        causa = "O comentário indica que um ou mais itens podem não ter sido entregues."
        acao = "Conferir os itens do pedido e encaminhar o caso à equipe responsável."
    elif any(p in texto for p in ("frio", "queimad", "gosto", "comida", "qualidade")):
        categoria = "Qualidade da Comida"
        causa = "O comentário menciona uma possível questão de qualidade do alimento."
        acao = "Registrar o relato e solicitar verificação da equipe da cozinha."
    elif any(p in texto for p in ("embalagem", "vazou", "derramou", "aberta")):
        categoria = "Embalagem"
        causa = "O comentário indica possível problema na embalagem ou acondicionamento."
        acao = "Verificar o processo de embalagem e acondicionamento do pedido."
    elif nota >= 4:
        categoria = "Elogio"
        causa = "A avaliação indica uma experiência positiva."
        acao = "Registrar o feedback positivo e compartilhar com a equipe."
    else:
        categoria = "Qualidade da Comida"
        causa = "A avaliação indica insatisfação; é necessária uma verificação do relato."
        acao = "Revisar o atendimento e identificar a causa da insatisfação."

    if nota == 1:
        sentimento = "Crítico"
    elif nota == 2:
        sentimento = "Negativo"
    elif nota == 3:
        sentimento = "Neutro"
    else:
        sentimento = "Positivo"

    resposta = (
        "Sentimos muito pela experiência relatada. Vamos verificar o ocorrido "
        "com a equipe responsável e buscar uma solução."
        if nota <= 3 else
        "Agradecemos por compartilhar sua experiência! Ficamos felizes com seu feedback."
    )

    return validar_resposta_modelo({
        "categoria": categoria,
        "sentimento": sentimento,
        "resumo_causa": causa,
        "resposta_cliente": resposta,
        "acao_operacional": acao,
    })
