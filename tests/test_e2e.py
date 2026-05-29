import os

import pytest

selenium = pytest.importorskip("selenium")

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def criar_driver_headless():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1280,720")
    try:
        return webdriver.Chrome(options=options)
    except WebDriverException as exc:
        pytest.skip(f"Navegador Chrome indisponível para o teste E2E: {exc}")


def test_fluxo_de_compra_com_selenium():
    base_url = os.getenv("LIVE_SERVER_URL", "http://127.0.0.1:8000")
    driver = criar_driver_headless()

    try:
        driver.get(base_url)

        driver.find_element(By.ID, "input-produto").send_keys("teclado")
        driver.find_element(By.ID, "input-cartao").send_keys("1234")
        driver.find_element(By.ID, "input-cupom").send_keys("GEEK20")
        driver.find_element(By.ID, "btn-comprar").click()

        mensagem = WebDriverWait(driver, 10).until(
            EC.text_to_be_present_in_element(
                (By.ID, "mensagem"),
                "Compra aprovada com sucesso! Valor pago: R$ 160.00",
            )
        )

        assert mensagem is True
    finally:
        driver.quit()
