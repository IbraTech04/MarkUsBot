import datetime
from Webscraper import Webscraper
from Assignment import Assignment

class Notifier:
    """
    Class which keeps track of MarkUs Assignments and notifies the user when an assignment is due
    
    === Attributes ===
    _assignments: list of assignments
    _webscraper: webscraper object used to scrape MarkUs
    _channel_id: channel id of the Discord channel to send notifications to
    _role_id: role id of the Discord role to mention when sending notifications
    ====== Representation Invariants ======
    _channel_id must be a valid channel id
    _role_id must be a valid role id
    """
    
    _assignments: dict[str, Assignment]
    _webscraper: Webscraper
    _channel_id: int
    _role_id: int
    
    def __init__(self, username: str, password: str, courseid: str, channel_id: int, role_id: int) -> None:
        """
        Initialize a Notifier object
        """
        self._assignments = {}
        self._webscraper = Webscraper(username, password, courseid)
        self._channel_id = channel_id
        self._role_id = role_id
        self._update_assignments(False)
    
    def _update_assignments(self, default_announced = False) -> None:
        """
        Update the list of assignments
        """
        assignmnets = self._webscraper.get_assignments()
        for assignment in assignmnets:
            if assignment['Assessment'] not in self._assignments:
                # Make a new assignment object to add to the dictionary
                name = assignment['Assessment']
                due_date = datetime.datetime.strptime(assignment['Due date'][:-4], "%A, %B %d, %Y, %I:%M:%S %p")
                is_released = assignment['Results'] == 'Results'
                self._assignments[name] = Assignment(name, due_date, is_released, default_announced)
        
            # If it's already in the dictionary, update the due date and released status
            else:
                is_released = assignment['Results'] == 'Results'
                self._assignments[assignment['Assessment']].set_released(is_released)
    
    def get_released_assignments(self) -> list[Assignment]:
        """
        Loops through the assignments and returns a list of released assignments that have not been announced
        """
        self._update_assignments()
        to_announce = []
        for assignment in self._assignments.values():
            if assignment.get_released() and not assignment.is_announced():
                assignment.set_announced(True)
                to_announce.append(assignment)
        
        return to_announce
        
        