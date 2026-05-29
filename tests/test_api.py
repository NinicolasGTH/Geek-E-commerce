import sqlite3
from unittest.mock import Mock

import main


def test_frontend_retorna_html(client):
    resposta = client.get("/")

    assert resposta.status_code == 200
    assert "GeekStore" in resposta.text
    assert "btn-comprar" in resposta.text


def test_listar_produtos_retorna_200(client):
    resposta = client.get("/api/produtos")

    assert resposta.status_code == 200
    produtos = resposta.json()
    assert isinstance(produtos, list)
    assert produtos[0].keys() >= {"nome", "preco", "estoque"}


def test_comprar_produto_com_sucesso(client):
    payload = {
        "produto": "teclado",
        "cartao": "1234",
        "cupom": "GEEK20"
    }
    resposta = client.post("/api/comprar", json=payload)

    assert resposta.status_code == 200

    dados = resposta.json()
    assert dados["status"] == "sucesso"
    assert dados["mensagem"] == "Compra aprovada!"
    assert dados["valor_pago"] == 160.0

    produtos = client.get("/api/produtos").json()
    teclado = next(produto for produto in produtos if produto["nome"] == "teclado")
    assert teclado["estoque"] == 9


def test_comprar_produto_inexistente(client):
    payload = {
        "produto": "monitor",
        "cartao": "1234",
        "cupom": ""
    }

    resposta = client.post("/api/comprar", json=payload)

    assert resposta.status_code == 404
    assert resposta.json()["detail"] == "Produto não encontrado"


def test_comprar_produto_sem_estoque(client):
    conn = sqlite3.connect(main.DB_PATH)
    try:
        conn.execute("UPDATE produtos SET estoque = 0 WHERE nome = ?", ("mouse",))
        conn.commit()
    finally:
        conn.close()

    payload = {
        "produto": "mouse",
        "cartao": "1234",
        "cupom": ""
    }

    resposta = client.post("/api/comprar", json=payload)

    assert resposta.status_code == 400
    assert resposta.json()["detail"] == "Sem estoque"


def test_comprar_com_pagamento_recusado_nao_baixa_estoque(client):
    gateway_mock = Mock()
    gateway_mock.cobrar.return_value = False
    main.app.dependency_overrides[main.get_gateway] = lambda: gateway_mock

    payload = {
        "produto": "teclado",
        "cartao": "0000",
        "cupom": ""
    }

    resposta = client.post("/api/comprar", json=payload)

    assert resposta.status_code == 400
    assert resposta.json()["detail"] == "Pagamento recusado pelo Gateway."
    gateway_mock.cobrar.assert_called_once_with("0000", 200.0)

    produtos = client.get("/api/produtos").json()
    teclado = next(produto for produto in produtos if produto["nome"] == "teclado")
    assert teclado["estoque"] == 10
