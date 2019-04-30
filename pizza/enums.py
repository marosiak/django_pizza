from enum import Enum

class StateEnum(Enum):   # A subclass of Enum
    # TODO: Django Enum
    Rejected = "Odrzucone"
    Canceled = "Anulowane"
    NotApproved = "Oczekuje akceptacji"
    Preparing = "Trwa przygotowanie"
    Traveling = "W drodze"
    Delivered = "Dostarczone"