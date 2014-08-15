# Just a toy example, it doesn't actually work.
#
# from util.handler_utils import prehook
# from util.message import Message
# from util.settings import get_setting
#
#
# @prehook('.*')
# def record_prehook(message: Message, match: dict, nick: str):
#     try:
#         if get_setting("bot_blog_recording"):  # this is an int
#             text = match.string  # this is the raw text
#             store(text, somewhere)  # this probably would've stored the raw text somewhere if it was implemented
#
#     except Exception as ex:
#         print("record_prehook failed:", ex)
#
