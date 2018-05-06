# todo implement proper logging

def mpv_log_handler(log_lvl, component, message) -> None:
    """
    Defines the log handler for the mpv player.

    :param log_lvl: The log level
    :param component: The component
    :param message: The message to log
    :return:
    """

    print("[{}] {}: {}".format(log_lvl, component, message))
