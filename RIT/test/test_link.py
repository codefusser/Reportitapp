import selenium as sm
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import unittest


class TestHyperlink(unittest.TestCase):
    # def __init__(self) -> None:
    #    self.browser = None

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self) -> None:
        # self.browser.implicitly_wait(10)
        self.browser.close()
        # return super().tearDown()

    def test_hyperlink(self):
        department = 'it service desk'
        self.browser.get("http://127.0.0.1:8000/RIT/dashboard/")
        department = str.upper(department)
        web_element = self.browser.find_element_by_partial_link_text(department)
        web_element.click()
        global visited 
        visited = self.browser.current_url
        self.assertIn(visited, "http://127.0.0.1:8000/RIT/dashboard/"+department+"/")
        # Select(web_element).select_by_visible_text(department)
    
    def test_hyperlink_visit(self):        
        self.browser.get(visited)
        # test visited link that it contains a table col with at least one table data
        count_td = self.browser.find_elements_by_class_name("incident_department")
        self.assertGreaterEqual(len(count_td), 1)
        pass

    def test_table_content(self):
        table_element = self.browser.find_element_by_tag_name("table")
        table_content = table_element.find_elements_by_tag_name("td")
        self.assertNotIn("No Incidents!" in table_content)
        
        pass

def main():
    test_link = TestHyperlink()
    test_link.test_hyperlink()
    test_link.test_hyperlink_visit()
    test_link.test_table_content()

if __name__ == '__main__':
    unittest.main()