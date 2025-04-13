from enum import Enum, auto


class ConversationStates(Enum):
    # Menu
    MENU = auto()

    # Registration
    ENTER_PROFILE_NAME = auto()
    ENTER_PROFILE_COUNTRY = auto()
    ENTER_PROFILE_CITY = auto()

    # Edit profile
    EDIT_PROFILE_NAME = auto()
    EDIT_PROFILE_CITY = auto()
    EDIT_PROFILE_COUNTRY = auto()

    # Session creation
    GAME_NAME = auto()
    IS_ONLINE = auto()
    COUNTRY = auto()
    CITY = auto()
    MAX_PLAYERS = auto()
    START_DATE = auto()
    START_TIME = auto()
    DURATION_HOURS = auto()
