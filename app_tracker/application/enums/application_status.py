from enum import Enum


class ApplicationStatus(Enum):
    """Status an application can be in"""

    SUBMITTED = "SUBMITTED"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"

    @classmethod
    def get_choices(cls):
        return [(v.value, v.name) for v in cls]
