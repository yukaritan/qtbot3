def chat_message(target: str, message: str) -> str:
    message = message.replace('\r\n', '')
    return 'PRIVMSG {target} :{message}'.format(target=target, message=message)


def join_channel(channel) -> str:
    return 'JOIN ' + channel


def part_channel(channel) -> str:
    return 'PART ' + channel
