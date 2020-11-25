from datetime import datetime


# import requests
# from bs4 import BeautifulSoup
#
#
# class Rates:
'''
Класс для получения курса валют (с ним тесты не проходят)
Вроде работает нормально, хз насколько правильно реализовал
'''
#     def __init__(self):
#         self.rates = dict()
#         response = requests.get("https://www.cbr.ru/eng/currency_base/daily/")
#         soup = BeautifulSoup(response.text, 'html.parser')
#         rows = soup.find('table', {'class': 'data'}).find_all('tr')
#         for row in rows[1:len(rows)]:
#             cells = row.find_all('td')
#             self.rates[cells[1].text] = cells[4].text


class Record:
    def __init__(self, amount=0, comment="Я не помню", date=""):
        self.amount = amount
        self.comment = comment
        self.date = datetime.strptime(date, "%d.%m.%Y").date() if len(date) > 0 else datetime.today().date()


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        amount = 0
        for record in self.records:
            if record.date == datetime.today().date():
                amount += record.amount
        return amount

    def get_week_stats(self):
        amount = 0
        today = datetime.today().date()
        for record in self.records:
            if 0 <= (today - record.date).days < 7:
                amount += record.amount
        return amount


def temp():
    return 75.0


class CashCalculator(Calculator):

    # USD_RATE = Rates().rates['USD']
    # EURO_RATE = Rates().rates['EUR']
    USD_RATE = 70.0
    EURO_RATE = 80.0

    def __init__(self, limit=1000):
        super().__init__(limit)

    def get_currency(self, currency):
        if currency == "usd":
            return [self.USD_RATE, "USD"]
        elif currency == "eur":
            return [self.EURO_RATE, "Euro"]
        return [1, "руб"]

    def get_today_cash_remained(self, currency="rub"):
        cur = self.get_currency(currency)
        remainder = (self.limit - self.get_today_stats()) / cur[0]
        precision = ".1f" if (remainder - int(remainder)) == 0 else ".2f"
        if remainder > 0:
            return f"На сегодня осталось {remainder:{precision}} {cur[1]}"
        elif remainder == 0:
            return "Денег нет, держись"
        else:
            return f"Денег нет, держись: твой долг - {-remainder:{precision}} {cur[1]}"


class CaloriesCalculator(Calculator):
    def __init__(self, limit=2000):
        super().__init__(limit)

    def get_calories_remained(self):
        difference = self.limit - self.get_today_stats()
        if difference > 0:
            return f"Сегодня можно съесть что-нибудь ещё, но с общей калорийностью не более {difference} кКал"
        else:
            return "Хватит есть!"
