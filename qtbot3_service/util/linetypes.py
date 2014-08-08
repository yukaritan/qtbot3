import re


LINE_TYPES = [
    # this is the response to a WHOIS
    # {host1}!{host2}
    ('identity', re.compile(':[^\s]+'
                            ' 311'
                            ' (?P<nick>[^\s]+)'
                            ' (?P<user>[^\s]+)'
                            ' (?P<host1>[^\s]+)'
                            ' (?P<host2>[^\s]+)'
                            ' \*'
                            ' :(?P<realname>[^\s]+)')),

    # Whenever someone /me's
    ('action', re.compile(':(?P<nick>[^\s]+)'
                          '!(?P<user>[^\s]+)'
                          ' PRIVMSG'
                          ' (?P<target>[^\s]+)'
                          ' :\x01ACTION (?P<action>.+)\x01')),

    # Whenever a message is sent
    ('message', re.compile(':(?P<nick>[^\s]+)'
                           '!(?P<user>[^\s]+)'
                           ' PRIVMSG'
                           ' (?P<target>[^\s]+)'
                           ' :(?P<message>.+)')),

    # Whenever anyone joins a channel
    ('join', re.compile(':(?P<nick>[^\s]+)'
                        '!(?P<user>[^\s]+)'
                        ' JOIN'
                        ' (?P<target>[^\s]+)')),

    # Whenever anyone leaves a channel
    ('part', re.compile(':(?P<nick>[^\s]+)'
                        '!(?P<user>[^\s]+)'
                        ' PART'
                        ' (?P<target>[^\s]+)'
                        '( :(?P<message>.*))?')),

    # Whenever anyone leaves a server
    ('quit', re.compile(':(?P<nick>[^\s]+)'
                        '!(?P<user>[^\s]+)'
                        ' QUIT'
                        '( :(?P<message>.*))?')),

    # Whenever anyone changes modes, this fires. users only
    ('mode', re.compile(':(?P<nick>[^\s]+)'
                        '!(?P<user>[^\s]+)'
                        ' MODE'
                        ' (?P<target>[^\s]+)'
                        ' (?P<mode>[^\s]+)'
                        ' (?P<targetnick>[^\s]+)')),

    # Whenever anyone changes their nick, this fires
    ('nick', re.compile(':(?P<oldnick>[^\s]+)'
                        '!(?P<user>[^\s]+)'
                        ' NICK'
                        ' :?(?P<newnick>[^\s]+)')),

    # When the bot first joins, this is sent by the server
    ('server_mode', re.compile(':(?P<nick>[^\s]+)'
                               ' MODE'
                               ' \\1'
                               ' :\+i')),


    # Catches notices sent by the server
    ('notice', re.compile(':(?P<nick>[^\s]+)'
                          '!(?P<user>[^\s]+)'
                          ' NOTICE'
                          ' (?P<target>[^\s]+)'
                          ' :(?P<message>.*)')),

    # Catches most things I've missed with the regexes above
    ('unknown', re.compile(':(?P<nick>[^\s]+)'
                           '!(?P<user>[^\s]+)'
                           ' (?P<command>[^\s]+)'
                           ' (?P<target>[^\s]+)'))]


def test():
    types = dict(LINE_TYPES)
    part = types['part']

    if c:
        print(c.groupdict())


if __name__ == '__main__':
    test()