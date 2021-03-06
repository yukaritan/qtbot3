import re
import json

import requests

from util import irc
from util.handler_utils import cmdhook, authenticate, get_target
from qtbot3_common.types.message import Message


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


@cmdhook('4chan (?P<board>[^\s]+) (?P<filtertext>.+)')
@authenticate
def handle_scrape(message: Message, match, nick: str):
    board = match['board']
    filtertext = match['filtertext']

    print("searching 4chan's {board} board for {filtertext}...".format(**match))
    baseurl = "http://boards.4chan.org/{board}/thread/{number}/{semantic_url}"

    lines = []
    for number, thread in scrape(board, filtertext):
        title = (thread['sub'] + ': ' + baseurl).format(number=number, board=board, **thread)
        lines.append(title + ' - ' + thread['teaser'])

    target = get_target(message, nick)

    return [irc.chat_message(target, line) for line in lines[:3]]
