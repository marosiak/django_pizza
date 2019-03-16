from enum import Enum

class StateEnum(Enum):   # A subclass of Enum
    # TODO: Django Enum
    Rejected = -2
    Canceled = -1
    NotApproved = 0
    Preparing = 1
    Traveling = 2
    Delivered = 3