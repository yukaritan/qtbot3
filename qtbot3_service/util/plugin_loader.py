from util.handler_utils import cmdhook, authenticate
from util.message import Message


def load_plugin(name: str) -> bool:
    """name is the name of a file under qtbot3_service/plugins/, without the file extension"""
    name = name.replace('.', '')

    try:
        # print("loading plugin:", name)
        __import__("plugins." + name)
        return True

    except Exception as ex:
        print("failed to load plugin:", ex)
        return False


@cmdhook('load_plugin (?P<plugin>[^\s]+)')
@authenticate
def handle_loadplugin(message: Message, match, nick: str):
    print("loading plugin {plugin}".format(**match))
    load_plugin(match['plugin'])
    print("plugin {plugin} loaded".format(**match))
