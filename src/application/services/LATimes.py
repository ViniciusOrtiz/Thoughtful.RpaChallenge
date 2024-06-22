from RPA.Browser.Selenium import Selenium
from robocorp import storage

class LATimesAutomation():
    def __init__(self) -> None:
        self._browser = Selenium()
        
        self._search_input = "//input[@placeholder='Please enter search term']"
        self._search_button = "//div[contains(@class, 'search-results-module-query')]/button[span[text()='Search']]"
        self._loading_icon = "//div[contains(@class, 'loading-icon')]"
        
    def open(self):
        url = storage.get_text("LaTimesUrl")
        self._browser.open_available_browser(url=url)
        
    def search(self, search_term: str):
        """
        Search for a term in the LA Times website

        Args:
            search_term (str): Term to be searched
        """
        self._browser.wait_until_element_is_visible(locator=self._search_input)
        self._browser.input_text(locator=self._search_input, text=search_term)
        self._browser.click_element(locator=self._search_button)
        self._browser.wait_until_element_is_visible(locator=self._loading_icon)
        self._browser.wait_until_element_is_not_visible(locator=self._loading_icon)