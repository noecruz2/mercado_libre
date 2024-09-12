from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    # chrome_options.add_argument("--headless")  
    return webdriver.Chrome(options=chrome_options)

def remove_cookie_banner(driver):
    try:
        driver.execute_script("""
            var elements = document.getElementsByClassName('cookie-consent-banner-opt-out__container');
            if (elements.length > 0) {
                elements[0].parentNode.removeChild(elements[0]);
            }
        """)
        print("Banner de cookies eliminado.")
    except Exception as e:
        print("Error al eliminar el banner de cookies: ", e)

def main():
    driver = setup_driver()
    wait = WebDriverWait(driver, 60)

    try:
        # 1. Ingresa al sitio web
        driver.get("https://mercadolibre.com/")
        print("Página cargada: MercadoLibre")

        # 2. Cierra el banner de cookies 
        remove_cookie_banner(driver)

        # 3. Selecciona México como país
        mexico_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'México')]")))
        mexico_link.click()
        print("Redirigido a México.")

        # 4. Esperar hasta que la página de México esté completamente cargada
        time.sleep(5)

        # 5. Busca el término "playstation 5"
        search_box = wait.until(EC.presence_of_element_located((By.NAME, "as_word")))
        search_box.send_keys("playstation 5" + Keys.RETURN)
        print("Búsqueda de 'Playstation 5' realizada.")

        # 6. Eliminar nuevamente el banner de cookies antes del filtro
        remove_cookie_banner(driver)

        # 7. Filtro por condición "Nuevos"
        new_condition = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Nuevo']")))
        new_condition.click()
        print("Filtro 'Nuevos' aplicado.")

        # 8. Eliminar nuevamente el banner de cookies antes del siguiente filtro
        remove_cookie_banner(driver)

        # 9. Filtro por ubicación "Cdmx"
        cdmx_filter = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Distrito Federal')]")))
        cdmx_filter.click()
        print("Filtro 'CDMX' aplicado.")

        # 10. Eliminar nuevamente el banner de cookies antes de ordenar
        remove_cookie_banner(driver)

        # 11. Ordenar por "mayor a menor precio"
        order_dropdown = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "andes-dropdown__trigger")))
        order_dropdown.click()
        highest_price = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Mayor precio']")))
        highest_price.click()
        print("Ordenado de mayor a menor precio.")

        # 12. Espera que los productos se carguen
        wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "ui-search-result__wrapper")))
        print("Productos cargados.")

        # 13. Obtén el nombre y precio de los primeros 5 productos
        products = driver.find_elements(By.CLASS_NAME, "ui-search-result__wrapper")[:5]

        if len(products) < 5:
            print("No se encontraron suficientes productos.")
        else:
            # Imprimir los productos
            for i, product in enumerate(products, 1):
                try:
                    name = product.find_element(By.CLASS_NAME, "ui-search-item__title").text
                    try:
                        price = product.find_element(By.CLASS_NAME, "andes-money-amount__fraction").text
                    except Exception:
                        price = "Precio no disponible"
                    print(f"{i}. {name} - Precio: {price}")
                except Exception as e:
                    print(f"Error obteniendo el producto {i}: {e}")

    except Exception as e:
        print(f"Error durante la ejecución del script: {e}")

    finally:
        if driver:
            driver.quit()

if __name__ == "_main_":
    main()