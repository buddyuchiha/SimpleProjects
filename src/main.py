from app.controllers.controller import start
from app.models.models import Currencies, ExchangeRates


cur = Currencies()
ex = ExchangeRates()
# cur.create("RUB", "RUB", "RUB")
# print(cur.read())
# cur.update("sign", 1, "idea")
# print(cur.read())
cur.delete(1)
print(cur.read())
cur.create("RUB", "RUB", "RUB")
print(cur.read())
cur.update("sign", 1, "RUB")
print(cur.read())



start()
