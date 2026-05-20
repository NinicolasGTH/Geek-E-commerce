def test_listar_produtos_retorna_200(client):
    resposta = client.get("/api/produtos")

    assert resposta_status_code == 200
    assert isinstance(resposta.json(), list)

def comprar_produto_com_sucesso(client):
    payload = {
        "produto": "teclado",
        "cartao": "1234",
        "cupom": "GEEK20"
    }
    resposta = client.post("/api/comprar", json=payload)

    assert resposta_status_code = 200

    dados = resposta.json()
    assert dados["status"] == "sucesso"
    assert dados["valor_pago"] == 160.0

def test_comprar_produto_inexistente(client):
    payload = {
        "produto": "monitor",
        "cartao": "1234",
        "cupom": ""
    }

    resposta = client.post("/api/comprar", json=payload)

    assert resposta_status_code = 404
    assert resposta.json()["detail"] == "Produto não encontrado"
