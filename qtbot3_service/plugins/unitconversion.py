import json
import requests
from util import irc
from util.handler_utils import msghook, get_target
from util.message import Message
from pint import UnitRegistry, DimensionalityError, UndefinedUnitError

ureg = UnitRegistry()


def currency_convert(value: float, unit1: str, unit2: str) -> float:
    try:
        print("converting currency...")
        template = "http://rate-exchange.appspot.com/currency?from={currency1}&to={currency2}"

        url = template.format(currency1=unit1,
                              currency2=unit2)

        result = json.loads(requests.get(url).text)
        if 'err' in result:
            return None

        rate = float(result['rate'])
        converted = value * rate
        return converted

    except Exception as ex:
        print(ex)


def unit_convert(value: float, unit1: str, unit2: str) -> str:
    # noinspection PyProtectedMember
    units = ureg._units

    if unit1 in units and unit2 in units:
        u1 = ureg.__getattr__(unit1)
        u2 = ureg.__getattr__(unit2)

        try:
            result = str(u1.to(u2) * value)
            return result
        except (DimensionalityError, UndefinedUnitError) as e:
            print(e)
            return None


@msghook('(?P<value>\d*\.\d+|\d+)'
         '\s+'
         '(?P<unit1>[a-zA-Z_]+)'
         '\s+in\s+'
         '(?P<unit2>[a-zA-Z_]+)')
def handle_unit_convert(message: Message, match, nick: str) -> str:
    target = get_target(message, nick)
    value, unit1, unit2 = float(match['value']), match['unit1'].lower(), match['unit2'].lower()

    # try to convert between units
    result = unit_convert(value, unit1, unit2)
    if result:
        output = "{value} {unit1} is {result}"
        return irc.chat_message(target, output.format(value=value,
                                                      result=result,
                                                      unit1=unit1))

    # try to convert currency
    result = currency_convert(value, unit1, unit2)
    if result:
        output = "{value} {unit1} is {result} {unit2}"
        return irc.chat_message(target, output.format(value=value,
                                                      result=result,
                                                      unit1=unit1,
                                                      unit2=unit2))

    # well, that failed.
    output = "couldn't convert {unit1} to {unit2} ;__;".format(unit1=unit1, unit2=unit2)
    print(output)
    return irc.chat_message(target, output)
