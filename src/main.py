from app.controllers.controller import start
from app.models.models import Currencies, ExchangeRates


cur = Currencies()
ex = ExchangeRates()
def test():
    cur.create("RUB", "RUB", "RUB")
    print(cur.read())
    cur.update("sign", 1, "idea")
    print(cur.read())

    print("\nДобавляем валюты:")
    cur.create("US Dollar", "USD", "$")
    cur.create("Euro", "EUR", "€")
    cur.create("British Pound", "GBP", "£")
    print("Добавленные валюты:", cur.read())


    print("\nДобавляем курсы:")
    ex.create(1, 2, "1.11")
    ex.create(2, 3, "5.0")
    print("Добавленные курсы:", ex.read())

# test()
start()
