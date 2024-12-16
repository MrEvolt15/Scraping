from scrapy_selenium import SeleniumRequest
from scrapy import Spider
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

class GoogleFlightsSpider(Spider):
    name = "custom_flights"
    allowed_domains = ["google.com"]
    start_urls = [
        "https://www.google.com/travel/explore?tfs=CBwQAxopEgoyMDI0LTEyLTE1ag0IAhIJL20vMDFkdHExcgwIBBIIL20vMDJqNzEaKRIKMjAyNS0wMS0xOWoMCAQSCC9tLzAyajcxcg0IAhIJL20vMDFkdHExQAFIAXABggELCP___________wGYAQGyAQQYASAB&tfu=GioaKAoSCZn9-G-mNlJAEd0_zPzdHh3AEhIJNlbVDJJBIcARAJ4ZEOkgZUA&hl=en&tcfs=IhgKCjIwMjQtMTItMTUSCjIwMjUtMDEtMTlSBGABeAE",  # North America
        "https://www.google.com/travel/explore?tfs=CBwQAxopEgoyMDI0LTEyLTE1ag0IAhIJL20vMDFkdHExcgwIBBIIL20vMDJqNzEaKRIKMjAyNS0wMS0xOWoMCAQSCC9tLzAyajcxcg0IAhIJL20vMDFkdHExQAFIAXABggELCP___________wGYAQGyAQQYASAB&tfu=GioaKAoSCYovmhGlilFAEVEMjNKDOVJAEhIJB_8YMusYQ0ARuc7PtXDyMsA&hl=en&tcfs=IhgKCjIwMjQtMTItMTUSCjIwMjUtMDEtMTlSBGABeAE",  # Europe
        "https://www.google.com/travel/explore?tfs=CBwQAxopEgoyMDI0LTEyLTE1ag0IAhIJL20vMDFkdHExcgwIBBIIL20vMDJqNzEaKRIKMjAyNS0wMS0xOWoMCAQSCC9tLzAyajcxcg0IAhIJL20vMDFkdHExQAFIAXABggELCP___________wGYAQGyAQQYASAB&tfu=GioaKAoSCZHWB4d6IlNAEThIy1EHlGPAEhIJFew7T0dwFUARQL6lccWuM0A&hl=en&tcfs=IhgKCjIwMjQtMTItMTUSCjIwMjUtMDEtMTlSBGABeAE",  # Asia
        "https://www.google.com/travel/explore?tfs=CBwQAxopEgoyMDI0LTEyLTE1ag0IAhIJL20vMDFkdHExcgwIBBIIL20vMDJqNzEaKRIKMjAyNS0wMS0xOWoMCAQSCC9tLzAyajcxcg0IAhIJL20vMDFkdHExQAFIAXABggELCP___________wGYAQGyAQQYASAB&tfu=GioaKAoSCTA3lOobnkJAEci3NK4YCmBAEhIJKiR1wElbTsAR3yAtRx2wS8A&hl=en&tcfs=IhgKCjIwMjQtMTItMTUSCjIwMjUtMDEtMTlSBGABeAE",  # Africa
        "https://www.google.com/travel/explore?tfs=CBwQAxopEgoyMDI0LTEyLTE1ag0IAhIJL20vMDFkdHExcgwIBBIIL20vMDJqNzEaKRIKMjAyNS0wMS0xOWoMCAQSCC9tLzAyajcxcg0IAhIJL20vMDFkdHExQAFIAXABggELCP___________wGYAQGyAQQYASAB&tfu=GioaKAoSCf-LT6oOfTlAEUC-pXHFQzVAEhIJgTdP64ayUMAROEjLUadNZMA&hl=en&tcfs=IhgKCjIwMjQtMTItMTUSCjIwMjUtMDEtMTlSBGABeAE"   # Oceania
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield SeleniumRequest(
                url=url,
                callback=self.parse,
                wait_time=60,  # Esperar suficiente tiempo
                wait_until=EC.presence_of_element_located((By.CSS_SELECTOR, "ol.SD4Ugf"))
            )

    def parse(self, response):
        # Guardar el HTML completo de la página para depuración
        with open("debug_page.html", "w", encoding="utf-8") as f:
            f.write(response.text)
    
        # Aquí puedes ajustar el selector y verificar si obtienes los vuelos
        flights = response.css('.Dy1Pdc .lPyEac')  # Ajusta este selector según la estructura HTML

        if not flights:
            self.logger.error("No se encontraron elementos de vuelos. Verifica el selector.")

        for flight in flights:
            # Simular la selección de cada item
            flight_element = flight.css('::attr(data-id)').get()
            if flight_element:
                self.logger.info(f"Seleccionando vuelo con ID: {flight_element}")
                # Aquí puedes agregar la lógica para interactuar con el elemento, por ejemplo, hacer clic en él
                # response.meta['driver'].find_element_by_css_selector(f"[data-id='{flight_element}']").click()
            yield {
                'price': flight.css('.QB2Jof > span::text').get(),  # Precio del vuelo
                'airline': flight.css('.W6bZuc::text').get(),  # Aerolínea
                'departure_time': datetime.now().strftime("%a, %b %d"),  # Fecha actual
                'arrival_time': "Sun, Jan 19",  # Fecha específica
                'duration': flight.css('.Xq1DAb::text').get(),  # Duración
                'stops': flight.css('.nx0jzf::text').get()  # Escalas
            }
