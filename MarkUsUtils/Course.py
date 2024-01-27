import datetime
from .Assignment import Assignment
import markusapi
from dotenv import load_dotenv
load_dotenv("tokens.env")
import os

class Course:
    """
    Class representing a course in the MarkUs LMS
    
    === Attributes ===
    _markus_api: markus api object
    _markus_instance_url: url of the markus instance we're using
    _course_id: course id of the course
    """
    
    _markus_api: markusapi.Markus
    _markus_instance_url: str
    _course_id: int
    _assignments: dict[int, Assignment]

    
    def __init__(self, instance_url: str, course_id: int) -> None:
        """
        Initialize a Notifier object
        """
        self._markus_instance_url = instance_url
        self._course_id = course_id
        self._markus_api = markusapi.Markus(os.getenv("MARKUS_API_KEY"), self._markus_instance_url)
        self._assignments = {}

    
    def _update_assignments(self) -> None:
        """
        Update the list of assignments. If the assignment is not in the dictionary, add it. If it is, update the due date and released status
        This method assumes all assignments that have already been released have been announced
        """
        assignments = self._markus_api.get_assignments(self._course_id)
        # We now have a massive JSON of assignments, we need to parse them and create Assignment objects to add them to our dictionary
        for assignment in assignments:
            if assignment['id'] not in self._assignments:
                # Make a new assignment object to add to the dictionary
                name = assignment['short_identifier']
                due_date = datetime.datetime.strptime(assignment['due_date'], "%Y-%m-%dT%H:%M:%S.%f%z")
                assignment_id = assignment['id']
                self._assignments[assignment_id] = Assignment(name, due_date, assignment_id)

    
    def get_new_assignments(self) -> list[Assignment]:
        """
        Returns a list of assignments which have not been announced on Discord yet
        """
        return [assignment for assignment in self._assignments.values() if not assignment.is_announced()]
        
        