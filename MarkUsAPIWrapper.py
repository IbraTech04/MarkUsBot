from Exceptions import *
import markusapi
from dotenv import load_dotenv
load_dotenv("tokens.env")
import os

class MarkUs():
    """
    MarkUs API Abstraction Layer

    === Attributes ===
    _courseid: course id of the course
    _markus_instance_url: url of the markus instance
    _markus_api: markus api object

    ====== Representation Invariants ======
    _courseid must be a valid course id
    """

    _courseid: str
    _markus_instance_url: str
    _markus_api: markusapi.Markus

    def __init__(self, courseid: str, instance_url: str) -> None:
        """
        Initialize a Webscraper object
        """

        self._courseid = courseid
        self._markus_instance_url = instance_url
        self._markus_api = markusapi.Markus(self._markus_instance_url, os.getenv("MARKUS_API_KEY"))


    def get_assignments(self) -> list[dict]:
        """
        Scrapes MarkUs and returns a list of assignments
        """
        return self._markus_api.get_assignments(self._courseid)
        