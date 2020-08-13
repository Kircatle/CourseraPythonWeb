from bs4 import BeautifulSoup
from decimal import Decimal


def convert(amount, cur_from, cur_to, date, requests):
    amount = Decimal(amount)
    response = requests.get("https://www.cbr.ru/scripts/XML_daily.asp",
                            params={
                                    "date_req": date
                                    }
                            )
    soup = BeautifulSoup(response.content, "xml")
    if cur_from != "RUR":
        cur_from = soup.find("CharCode", text=cur_from)
        cur_from_nominal = int(cur_from.find_next_sibling("Nominal").string)
        cur_from_value = cur_from.find_next_sibling("Value").string
        cur_from_value = cur_from_value.replace(",", ".")
        cur_from_value = Decimal(cur_from_value)
        rub = (amount/cur_from_nominal)*cur_from_value
    else:
        rub = amount
    if cur_to != "RUR":
        cur_to = soup.find("CharCode", text=cur_to)
        cur_to_nominal = int(cur_to.find_next_sibling("Nominal").string)
        cur_to_value = cur_to.find_next_sibling("Value").string
        cur_to_value = cur_to_value.replace(",", ".")
        cur_to_value = Decimal(cur_to_value)
        result = Decimal(rub/cur_to_value) * cur_to_nominal
    else:
        result = rub
    return result.quantize(Decimal("1.0000"))
