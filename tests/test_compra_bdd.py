from pytest_bdd import scenario, given, when, then, parsers

@scenario("features/compra.feature", "Compra com sucesso")
def test_compra_com_sucesso():
    pass

@given(parsers.parse('que existe um produto "{produto}" em estoque'))
def produto_em_estoque(produto, client):
    resposta = client.get("/api/produtos")
    produtos = resposta.json()

    nomes = [p["nome"] for p in produtos]

    assert produto in nomes

@when(
    parsers.parse('realizo a compra do produto "{produto}" com cupom "{cupom}"'),
    target_fixture="resposta_compra",
)
def realizar_compra(produto, cupom, client):
    payload = {
        "produto": produto,
        "cartao": "1234",
        "cupom": cupom
    }
    return client.post("/api/comprar", json=payload)

@then("a compra deve ser aprovada")
def compra_deve_ser_aprovada(resposta_compra):
    assert resposta_compra.status_code == 200
    assert resposta_compra.json()["status"] == "sucesso"

@then(parsers.parse("o valor pago deve ser {valor:f}"))
def valor_pago_deve_ser(resposta_compra, valor):
    assert resposta_compra.json()["valor_pago"] == valor
