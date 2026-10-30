import json

import pytest

from security_utils import (
    anonimizar_nome,
    extrair_json_modelo,
    html_seguro,
    sanitizar_texto_lgpd,
    validar_resposta_modelo,
    validar_webhook_seguro,
)


def test_anonimizar_nome_mascara_nome():
    assert anonimizar_nome("Mariana Costa") == "M*** C***"
    assert anonimizar_nome("") == "Cliente Anônimo"
    assert anonimizar_nome("Mariana") == "M***"


def test_sanitizacao_mascara_cpf_email_telefone():
    original = "CPF 123.456.789-01, email pessoa@example.com, telefone (11) 91234-5678"
    sanitized = sanitizar_texto_lgpd(original)
    assert "123.456.789-01" not in sanitized
    assert "pessoa@example.com" not in sanitized
    assert "91234-5678" not in sanitized
    assert "[CPF OCULTO]" in sanitized
    assert "[EMAIL OCULTO]" in sanitized
    assert "[TELEFONE OCULTO]" in sanitized


def test_sanitizacao_mascara_numero_de_cartao():
    original = "Cartão de teste 4111 1111 1111 1111"
    sanitized = sanitizar_texto_lgpd(original)
    assert "4111 1111 1111 1111" not in sanitized
    assert "[DADO DE CARTÃO OCULTO]" in sanitized


def test_sanitizacao_limita_tamanho():
    assert len(sanitizar_texto_lgpd("x" * 2000)) <= 1000


def test_html_seguro_escapa_conteudo_nao_confiavel():
    assert html_seguro('<script>alert("x")</script>') == "&lt;script&gt;alert(&quot;x&quot;)&lt;/script&gt;"


def valid_payload():
    return {
        "categoria": "Item Faltante",
        "sentimento": "Negativo",
        "resumo_causa": "Batata não entregue",
        "resposta_cliente": "Lamentamos o ocorrido.",
        "acao_operacional": "Investigar o pedido",
    }


def test_validar_resposta_modelo_aceita_esquema_valido():
    result = validar_resposta_modelo(valid_payload())
    assert result["categoria"] == "Item Faltante"
    assert result["sentimento"] == "Negativo"


def test_validar_resposta_modelo_rejeita_categoria_nao_permitida():
    payload = valid_payload()
    payload["categoria"] = "Executar reembolso"
    with pytest.raises(ValueError):
        validar_resposta_modelo(payload)


def test_validar_resposta_modelo_rejeita_campo_extra():
    payload = valid_payload()
    payload["comando"] = "executar"
    with pytest.raises(ValueError):
        validar_resposta_modelo(payload)


def test_extrair_json_modelo_aceita_json_em_bloco_markdown():
    text = "```json\n" + json.dumps(valid_payload(), ensure_ascii=False) + "\n```"
    assert extrair_json_modelo(text)["categoria"] == "Item Faltante"


@pytest.mark.parametrize(
    "url",
    [
        "http://hook.us1.make.com/abc",
        "https://localhost/abc",
        "https://127.0.0.1/abc",
        "https://evil.example/hook",
        "https://make.com.evil.example/hook",
        "https://user:pass@hook.us1.make.com/abc",
        "https://hook.us1.make.com:8443/abc",
    ],
)
def test_webhook_rejeita_destinos_nao_permitidos(url):
    assert not validar_webhook_seguro(url, resolver_dns=False)


@pytest.mark.parametrize(
    "url",
    [
        "https://hook.us1.make.com/abc",
        "https://meu-workspace.n8n.cloud/webhook/abc",
    ],
)
def test_webhook_aceita_formato_de_provedor_permitido(url):
    assert validar_webhook_seguro(url, resolver_dns=False)
