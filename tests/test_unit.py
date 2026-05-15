import pytest
from unittest.mock import mock

from main import calcular_desconto, processar_pedido

def test_calcular_desconto():
    resultado = calcular_desconto(200.0, "GEEK20")

    assert resultado == 160.0

def test_calcular_desconto_cupom_invalido():
    resultado = calcular_desconto(200.0, "INVALIDO")

    assert resultado == 200.0

def test_processar_pedido_com_gateway_aprovado():
    gateway_mock = Mock()
    gateway_mock.cobrar.return_value = True

    resultado = processar_pedido(200.0, "1234", gateway_mock)

    assert resultado == "Compra aprovada."
    gateway_mock.cobrar.assert_called_once_with("1234", 200.0)

def test_processar_pedido_com_valor_zero():
    gateway_mock = Mock()

    with pytest.raises(ValueError) as erro:
        processar_pedido(0, "1234", gateway_mock)

        assert "Pagamento recusado" in str(erro.value)
