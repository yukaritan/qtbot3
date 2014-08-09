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
