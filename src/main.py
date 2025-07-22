from app.controllers.controller import start
from app.models.models import Currencies, ExchangeRates


cur = Currencies()
ex = ExchangeRates()
# cur.create("RUB", "RUB", "RUB")
# print(cur.read())
# cur.update("sign", 1, "idea")
# print(cur.read())
# cur.delete(1)
# print(cur.read())
ex.delete(1)
ex.create(20, 30, 5.5)
print(ex.read())
ex.update("rate", 1, 2.2)
print(ex.read())



start()
