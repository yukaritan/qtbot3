import json
import requests
from util import irc
from util.handler_utils import msghook, get_target
from util.message import Message


@msghook('(?P<amount>\d*\.\d+|\d+)'
         '\s+'
         '(?P<currency1>[a-zA-Z]+)'
         '\s+in\s+'
         '(?P<currency2>[a-zA-Z]+)')
def currency_convert(message: Message, match, nick: str) -> str:
    try:
        print("converting currency...")
        template = "http://rate-exchange.appspot.com/currency?from={currency1}&to={currency2}"

        currency1 = match['currency1'].upper()
        currency2 = match['currency2'].upper()

        url = template.format(currency1=currency1,
                              currency2=currency2)

        print(url)

        result = json.loads(requests.get(url).text)
        target = get_target(message, nick)

        if 'err' in result:
            output = "couldn't convert {currency1} to {currency2} ;__;"
            print(output)
            return irc.chat_message(target, output.format(currency1=currency1,
                                                          currency2=currency2))

        amount = float(match['amount'])
        rate = float(result['rate'])
        converted = amount * rate

        output = "{amount} {currency1} is {converted} {currency2}".format(amount=amount,
                                                                          converted=converted,
                                                                          currency1=currency1,
                                                                          currency2=currency2)
        print(output)
        return irc.chat_message(target, output)
    except Exception as ex:
        print(ex)