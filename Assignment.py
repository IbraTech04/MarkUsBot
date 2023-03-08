import datetime

class Assignment:
    """
    Class which represents an assignment on MarkUs
    
    ========= Attributes =========
    _name: name of the assignment
    _due_date: due date of the assignment
    _released: whether the assignment is released
    _is_announced: whether the release of the assignment was announced on Discord
    ===== Representation Invariants =====
    _due_date is a valid date
    """
    
    _name: str
    _due_date: datetime.date
    _released: bool
    
    def __init__(self, name: str, due_date: datetime.date, released: bool, is_announced = False) -> None:
        """
        Initialize an Assignment object
        """
        self._name = name
        self._due_date = due_date
        self._released = released
        self._is_announced = is_announced
    
    def get_name(self) -> str:
        return self._name
    
    def get_due_date(self) -> datetime.date:
        return self._due_date
    
    def get_released(self) -> bool:
        return self._released
    
    def set_released(self, released: bool) -> None:
        self._released = released
    
    def is_announced(self) -> bool:
        return self._is_announced
    
    def set_announced(self, is_announced: bool) -> None:
        self._is_announced = is_announced
    
    def is_due(self) -> bool:
        """
        Return whether the assignment is due
        """
        return datetime.date.today() >= self._due_date