"""
Robot class that performs tasks to fetch scientist information.
"""
from RPA.Browser.Selenium import Selenium
from RPA.Calendar import Calendar
from typing import Tuple
from typing import Optional
import re


class Robot:
    """
    Robot class is designed to perform tasks including opening a browser,
    fetching information about scientists, and closing the browser.
    """
    def __init__(self, name, config):
        """
        Initialize the Robot with its name and configuration.
        """
        self.name = name
        self.config = config
        self.scientists = config['scientists']
        self.br = Selenium()
        self.cal = Calendar()

    def say_hello(self) -> None:
        """
        Have the robot say hello.
        """
        print(f"Hello! My name is {self.name}. " +
              "Please give me a moment while I fetch some information " +
              "about these scientists:\n" +
              f"{', '.join(self.scientists)}")

    def open_browser(self) -> None:
        """
        Have the robot open a browser instance.
        """
        self.br.open_available_browser()

    def get_scientists_information(self) -> None:
        """
        Get information about each scientist.
        """
        for scientist in self.scientists:
            self._get_info(scientist)

    def say_goodbye(self) -> None:
        """
        Have the robot say goodbye.
        """
        print("\nMy task has been completed, goodbye!")

    def close_all_browsers(self) -> None:
        """
        Have the robot gracefully close all browsers.
        Also resets browser cache.
        """
        self.br.close_all_browsers()

    def _get_info(self, scientist) -> None:
        """
        Private helper function to get information of a scientist.
        """
        print(f"\nFetching information on {scientist}...")
        scientist = scientist.replace(' ', '_')
        url = f"{self.config['wikipedia']['base_url']}{scientist}"
        self._open_webpage(url)
        birth_date, death_date = self._get_dates()
        age = self._calculate_age(birth_date, death_date)
        first_paragraph = self._get_first_paragraph()

        print(f"Scientist: {scientist}" +
              f"\nBirth Date: {birth_date}" +
              f"\nDeath Date: {death_date}" +
              f"\nAged: {age}" +
              f"\nFirst paragraph: {first_paragraph}")

    def _open_webpage(self, webpage) -> None:
        """
        Private helper function to navigate web pages.
        """
        self.br.go_to(webpage)

    def _get_dates(self) -> Tuple[str, str]:
        """
        Private helper function to get the birth date and the death date of a
        scientist.
        """
        birth_date = self._get_date(match_with_newline=True)
        death_date = self._get_date()
        return birth_date, death_date

    def _calculate_age(self, birth_date, death_date) -> int:
        """
        Private helper function to calculate the age of a scientist given
        birth date and death date.
        """
        birth_date = self.cal.create_time(birth_date,
                                          self.config['date_format'])
        death_date = self.cal.create_time(death_date,
                                          self.config['date_format'])
        return self.cal.time_difference(birth_date, death_date)['years']

    def _get_first_paragraph(self) -> str:
        """
        Private helper function to find the first paragraph on a scientists
        wikipedia page.
        """
        paragraph_elements = self.br.find_elements(
            self.config['selectors']['paragraphs'])

        for paragraph_element in paragraph_elements:
            paragraph_text = paragraph_element.text
            if paragraph_text:
                return paragraph_text.encode(
                    self.config['encoding'], errors='ignore').decode(
                    self.config['encoding'])

        return "No plaintext found."

    def _get_date(
            self,
            match_with_newline: Optional[bool] = None) -> str:
        """
        Private helper function to find find either birth date or death date
        of a scientist.
        """
        elements = self.br.find_elements(self.config['selectors']['dates'])

        for element in elements:
            if element.text:
                if match_with_newline:
                    match = re.search(
                        fr"{self.config['regex_patterns']['birth_date']}",
                        element.text,
                        re.DOTALL)
                else:
                    match = re.search(
                        fr"{self.config['regex_patterns']['death_date']}",
                        element.text)
                if match:
                    matched_date = match.group(1)
                    return matched_date

        return "No date found."
