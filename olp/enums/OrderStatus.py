from enum import Enum

class OrderStatus(Enum):
    FAILED = 'Failed'
    PENDING = 'Pending'
    COMPLETED = 'Completed'