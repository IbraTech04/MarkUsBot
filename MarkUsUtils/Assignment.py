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
    _assignment_id: int
    _due_date: datetime.date
    _announced: bool
    
    def __init__(self, name: str, due_date: datetime.date, assignment_id: int, is_announced = False) -> None:
        """
        Initialize an Assignment object
        """
        self._name = name
        self._due_date = due_date
        self._announced = is_announced
        self._assignment_id = assignment_id
    
    def get_name(self) -> str:
        return self._name
    
    def get_due_date(self) -> datetime.date:
        return self._due_date
    
    def is_announced(self) -> bool:
        return self._announced
    
    def set_announced(self, is_announced: bool) -> None:
        self._announced = is_announced
    
    def is_due(self) -> bool:
        """
        Return whether the assignment is due
        """
        return datetime.date.today() >= self._due_date

    def get_time_until_due(self) -> datetime.timedelta:
        """
        Return the time until the assignment is due
        """
        return self._due_date - datetime.date.today()
    
    def get_grade_release_status(self) -> bool:
        """
        Return whether the assignment's grades have been released
        """
        raise NotImplementedError("GradeSpy has not been implemented yet")  