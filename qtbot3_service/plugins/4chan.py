import re
import json

import requests

from util.handler_utils import cmdhook, authenticate, message_hooks

from util.message import Message


print("loading 4chan plugin")


def scrape(board: str, filtertext: str):
    try:
        data = requests.get("http://boards.4chan.org/{board}/catalog".format(board=board)).text
        match = re.match(".*var catalog = (?P<catalog>\{.*\});.*", data)
        if not match:
            print("Couldn't scrape catalog")
        catalog = json.loads(match.group('catalog'))

        for number, thread in catalog['threads'].items():
            sub, teaser = thread['sub'], thread['teaser']
            if filtertext in sub.lower() or filtertext in teaser.lower():
                yield(number, thread)

    except Exception as ex:
        print("scraping exception:", ex)


@cmdhook('4chan (?P<board>[a-z]{1,3}) (?P<filtertext>[.+])')
@authenticate
def handle_scrape(message: Message, match, nick: str):
    board = match['board']
    filtertext = match['filtertext']

    print("searching 4chan's {board} board for {filtertext}...".format(**match))

    for result in scrape(board, filtertext):
        print(result)

print(message_hooks)