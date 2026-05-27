from pytest_bdd import scenario, given, when, then, parsers

@scenario("features/compra.feature", "Compra com sucesso")
def test_compra_com_sucesso():
    pass

@given.parsers.parse('que existe um produto "{produto}" em estoque')
def produto_em_estoque(produto, client):
    resposta = client.get("/api/produtos")
    produtos = resposta.json()

    nomes = [p["nome"] for p in produtos]

    assert produto in nomes

@when(parses.parse('eu realizo a compra do produto "{produto}" com o cupom "{cupom}"'))
def realizar_compra(produto, cupom, client):
    payload = {
        "produto": produto,
        "cartao": "1234",
        "cupom": cupom
    }