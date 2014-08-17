import json


def get_setting(setting: str):
    """Bit wasteful.. I'll probably fix it later. Best part is that you can change certain settings while running."""
    try:
        with open('settings.json', 'r') as f:
            return json.load(f)[setting]
    except Exception as exception:
        print('failed to fetch setting "%s": %s' % (setting, exception))
        return None
