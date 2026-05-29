# language: pt
Funcionalidade: Compra de Produto
    Cenário: Compra com sucesso
        Dado que existe um produto "teclado" em estoque
        Quando realizo a compra do produto "teclado" com cupom "GEEK20"
        Então a compra deve ser aprovada
        E o valor pago deve ser 160.0
