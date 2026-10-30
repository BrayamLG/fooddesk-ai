"""Helpers de segurança do FoodDesk AI; controles demonstrativos, não certificação."""
from __future__ import annotations

import html
import ipaddress
import json
import re
import socket
from urllib.parse import urlparse

CATEGORIAS = {"Logística / Atraso", "Qualidade da Comida", "Item Faltante", "Embalagem", "Elogio"}
SENTIMENTOS = {"Crítico", "Negativo", "Neutro", "Positivo"}
MAX_COMENTARIO_CHARS = 1000
MAX_OUTPUT_CHARS = 1200


def anonimizar_nome(nome_completo: str) -> str:
    """Mascara o nome de forma parcial; não é anonimização irreversível."""
    if not isinstance(nome_completo, str) or not nome_completo.strip():
        return "Cliente Anônimo"
    partes = nome_completo.strip().split()
    if len(partes) == 1:
        return partes[0][:1] + "***"
    return f"{partes[0][:1]}*** {partes[-1][:1].upper()}***"


def sanitizar_texto_lgpd(texto: str) -> str:
    """Mascara padrões comuns de PII; não garante anonimização completa."""
    if not isinstance(texto, str):
        return ""
    texto = texto[:MAX_COMENTARIO_CHARS]
    texto = re.sub(r"(?<!\d)(?:\d[ -]?){12,18}\d(?!\d)", "[DADO DE CARTÃO OCULTO]", texto)
    texto = re.sub(r"(?<!\d)\d{3}\.?\d{3}\.?\d{3}-?\d{2}(?!\d)", "[CPF OCULTO]", texto)
    texto = re.sub(r"(?i)(?<![\w.+-])[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}(?![\w.-])", "[EMAIL OCULTO]", texto)
    texto = re.sub(r"(?<!\d)(?:\+?55[\s.-]*)?(?:\(?\d{2}\)?[\s.-]*)?9?\d{4}[\s.-]?\d{4}(?!\d)", "[TELEFONE OCULTO]", texto)
    return texto


def html_seguro(valor: object) -> str:
    """Escapa texto dinâmico antes de inseri-lo em um bloco HTML."""
    return html.escape(str(valor), quote=True)


def validar_webhook_seguro(url: str, *, resolver_dns: bool = True) -> bool:
    """Aceita apenas HTTPS em domínios conhecidos do Make/n8n Cloud."""
    if not isinstance(url, str) or len(url) > 2048:
        return False
    try:
        parsed = urlparse(url.strip())
        if parsed.scheme.lower() != "https" or not parsed.hostname:
            return False
        if parsed.username or parsed.password or parsed.port not in (None, 443):
            return False
        host = parsed.hostname.rstrip(".").lower()
        suffixes = ("make.com", "make.eu", "make.us", "n8n.cloud")
        if not any(host == suffix or host.endswith("." + suffix) for suffix in suffixes):
            return False
        try:
            ipaddress.ip_address(host.strip("[]"))
            return False
        except ValueError:
            pass
        if resolver_dns:
            infos = socket.getaddrinfo(host, 443, type=socket.SOCK_STREAM)
            if not infos:
                return False
            for info in infos:
                ip = ipaddress.ip_address(info[4][0].split("%")[0])
                if not ip.is_global:
                    return False
        return True
    except (ValueError, OSError, socket.gaierror):
        return False


def validar_resposta_modelo(payload: object) -> dict:
    """Valida o esquema e os valores permitidos na saída do modelo."""
    if not isinstance(payload, dict):
        raise ValueError("A resposta do modelo não é um objeto JSON.")
    required = {"categoria", "sentimento", "resumo_causa", "resposta_cliente", "acao_operacional"}
    if set(payload.keys()) != required:
        raise ValueError("A resposta contém campos ausentes ou inesperados.")
    if not isinstance(payload["categoria"], str) or payload["categoria"] not in CATEGORIAS:
        raise ValueError("Categoria não permitida.")
    if not isinstance(payload["sentimento"], str) or payload["sentimento"] not in SENTIMENTOS:
        raise ValueError("Sentimento não permitido.")
    clean = {"categoria": payload["categoria"], "sentimento": payload["sentimento"]}
    for key in ("resumo_causa", "resposta_cliente", "acao_operacional"):
        value = payload[key]
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"Campo inválido: {key}")
        clean[key] = value.strip()[:MAX_OUTPUT_CHARS]
    return clean


def extrair_json_modelo(texto: str) -> dict:
    """Converte JSON emitido pelo modelo e valida sua estrutura."""
    if not isinstance(texto, str) or not texto.strip():
        raise ValueError("Resposta vazia ou inválida.")
    cleaned = re.sub(r"^\s*```(?:json)?\s*|\s*```\s*$", "", texto.strip(), flags=re.I)
    return validar_resposta_modelo(json.loads(cleaned))
