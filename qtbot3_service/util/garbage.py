#
#  Random junk
#

colors = ['\x0304', '\x0307', '\x0308', '\x0309',
          '\x0303', '\x0310', '\x0312', '\x0302',
          '\x0306', '\x0313', '\x0305']


def repeat(items) -> str:
    while True:
        for item in items:
            yield item
