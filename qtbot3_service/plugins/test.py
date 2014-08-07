import json

import requests

from util import irc
from util.handler_utils import get_target, fetch_all, get_master_nick, cmdhook, msghook
from util.message import Message


@cmdhook('host (?P<nick>.*)')
def get_host(message: Message, match, nick: str) -> str:
    """just parrot the host associated with a nick"""

    print("get_host() was called")

    try:
        target = get_target(message, nick)
        n = match['nick'].strip()
        if ' ' in n:
            n = n.split(' ', 1)[0]

        storage = fetch_all()

        for k, v in storage.items():
            if v == n:
                return irc.chat_message(target, "{v}'s host is {k}".format(k=k.split('_', 1)[1], v=v))
        return irc.chat_message(target, "I don't know {n}'s host yet".format(n=n))

    except Exception as ex:
        print(ex)


@cmdhook('master')
def get_master(message: Message, match, nick: str) -> str:
    try:
        target = get_target(message, nick)
        return irc.chat_message(target, "my master is " + get_master_nick() or "unknown to me")
    except Exception as ex:
        print(ex)


@msghook('(?P<amount>\d*\.\d+|\d+)'
         '\s+'
         '(?P<currency1>[a-zA-Z]+)'
         '\s+in\s+'
         '(?P<currency2>[a-zA-Z]+)')
def currency_convert(message: Message, match, nick: str) -> str:
    try:
        print("converting currency...")
        url = "http://rate-exchange.appspot.com/currency?from={currency1}&to={currency2}"

        currency1 = match['currency1'].upper()
        currency2 = match['currency2'].upper()

        result = json.loads(requests.get(url.format(currency1=currency1,
                                                    currency2=currency2)).text)
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