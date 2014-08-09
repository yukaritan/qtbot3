def chat_message(target: str, message: str):
    message = message.replace('\r\n', '')
    return 'PRIVMSG {target} :{message}'.format(target=target, message=message)


def join_channel(channel):
    return 'JOIN ' + channel


def part_channel(channel):
    return 'PART ' + channel
