from util.message import Message


def chat_message(target: str, message: str):
    message = message.replace('\r\n', '')
    return 'PRIVMSG {target} :{message}'.format(target=target, message=message)


def join_channel(channel):
    return 'JOIN ' + channel


def part_channel(channel):
    return 'PART ' + channel


def is_mentioned(message: Message, nick: str) -> bool:
    lownick = nick.lower()
    lowmsg = message.message.lower()
    return lownick in lowmsg or ('-' in nick and lownick.split('-', 1)[0] in lowmsg)
