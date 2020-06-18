from datetime import datetime
import re


def time_now():
    return datetime.now().strftime('%d-%b-%Y %H:%M:%S')


def edit_cmd(command):
    """
    Принимает сообщение пользователя с командой
    и отрезает команду от остальной строки.
    Например, от строки '/open http://url.com'
    останется только 'http://url.com'
    """
    pattern = r"\/\w+ "
    match = re.findall(pattern, command)
    return command.replace(match[0], "")
