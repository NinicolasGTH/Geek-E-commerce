import sqlite3

import main


def test_banco_temporario_recebe_dados_iniciais(banco_temporario):
    conn = sqlite3.connect(main.DB_PATH)
    try:
        conn.row_factory = sqlite3.Row
        produtos = conn.execute("SELECT * FROM produtos ORDER BY nome").fetchall()
    finally:
        conn.close()

    assert [produto["nome"] for produto in produtos] == ["mouse", "teclado"]
    assert produtos[0]["preco"] == 100.0
    assert produtos[1]["estoque"] == 10


def test_banco_temporario_e_isolado_por_teste(client):
    produtos = client.get("/api/produtos").json()
    teclado = next(produto for produto in produtos if produto["nome"] == "teclado")

    assert teclado["estoque"] == 10
