import requests
from bs4 import BeautifulSoup
from Exceptions import *

class Webscraper():
    """
    Class used to scrape the MarkUs website for assignments

    === Attributes ===
    _username: username of the user
    _password: password of the user
    _courseid: course id of the course

    ====== Representation Invariants ======
    _username must be a valid UTORID
    _password must be the associated password of the UTORID
    _courseid must be a valid course id
    """

    _username: str
    _password: str
    _courseid: str

    def __init__(self, username: str, password: str, courseid: str) -> None:
        """
        Initialize a Webscraper object
        """
        self._username = username
        self._password = password
        self._courseid = courseid

    def _gen_cookie(self):
        """
        Log into MarkUs and return the token cookie
        Precondition: _username and _password must be valid
        """

        cookies = {
            '_markus_23s': 'tG6%2BI%2BkB4kJoguE7NCYr7%2FH2A6p%2BYQfFIa644X12wygCgxuod2b%2FJjCKaFWkmcXkw9RQZxIfEhNY%2Bcqz%2FjtBEP9%2Ff4C74zwbaeQ8hbTEkB3Yo%2BSVMc6anFoAOch6Du3eV0Fmc6jR3aw%2B7WictMEksyCcAVvkfwAfvdU8znOfwv6x7i47KLBH8f9zNCfzjqBCf6tr6n7FU4uqlgiItc0LO0ZrGlXmu2kM9vYL9SlsChlA3TXFMbCRbqIxL8PQ2t%2F%2FZysY79BckMsWefkUXyLVYEF3jz41KvspaVgVMQiuw0E0CxBZoN24YGWYMvs%2FZdCnjXxAEemyHKUhmxNNsnoL9xT%2FY8w1pPfkeN6W4bhhAHNau1rf8Hfm48A%3D--WvFPSQ9nOhAnSKEJ--eDoTT8OcofJpwzgf5LUI4A%3D%3D',
        }

        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Origin': 'https://mcsmarks.utm.utoronto.ca',
            'Prefer': 'safe',
            'Referer': 'https://mcsmarks.utm.utoronto.ca/markus23s/',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.63',
            'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Microsoft Edge";v="110"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }

        params = {
            'locale': 'en',
        }

        data = {
            'authenticity_token': 'opn9QbOvsRv_SynqveR3v4V-DXY26NYzuXodNj2yFHmuBafH6JAxkyGMUwJjE3sedr_G5RJWI3RgMX2TGD6_wA',
            'user_login': f'{self._username}',
            'user_password': f'{self._password}',
            'commit': 'Log in',
        }
        response = requests.post('https://mcsmarks.utm.utoronto.ca/markus23s/', params=params, cookies=cookies, headers=headers, data=data)
        
        if "Login failed." in response.text:
            raise LoginFailed
        if "You do not have permission to access this page." in response.text:
            raise InvalidCourseID
    
        return response.headers['Set-Cookie'].split(";")[0].split("=")[1]

    def get_assignments(self) -> list[dict]:
        """
        Scrapes MarkUs and returns a list of assignments
        Precondition: _username and _password must be valid
        """
        
        try:
            cookie = self._gen_cookie()
        except LoginFailed:
            raise LoginFailed
        
        cookies = {
        '_markus_23s': cookie,
        }

        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'DNT': '1',
            'If-None-Match': 'W/"cd36bdcd81f6541bb016047f5acbd216-gzip"',
            'Prefer': 'safe',
            'Referer': 'https://mcsmarks.utm.utoronto.ca/markus23s/courses',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.63',
            'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Microsoft Edge";v="110"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }

        response = requests.get(f'https://mcsmarks.utm.utoronto.ca/markus23s/courses/{self._courseid}/assignments', cookies=cookies, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
    
        table = soup.find('table')

        rows = table.tbody.find_all('tr')

        # Extract the header row and get the column names
        header_row = table.thead.tr
        columns = [col.text.strip() for col in header_row.find_all('th')]

        # Create an empty list to store the data
        data = []

        # Loop through each row and extract the data into a dictionary
        for row in rows:
            row_data = {}
            # Find all columns in the row
            cols = row.find_all('td')
            # Loop through each column and add the data to the row_data dictionary
            for i in range(len(columns)):
                row_data[columns[i]] = cols[i].text.strip()
            # Add the row data to the data list
            data.append(row_data)
        return data
