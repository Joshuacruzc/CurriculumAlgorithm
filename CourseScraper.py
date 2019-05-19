from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class CourseScrape:

    faculties_departments = {
        'ENGR': ['ICOM']
    }

    def __init__(self):
        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920x1080")
        self.driver = webdriver.Chrome(chrome_options=chrome_options, executable_path='Drivers/chromedriver')

    def scrape(self):
        self.driver.get('https://home.uprm.edu')
        username = self.driver.find_element_by_name('username')
        password = self.driver.find_element_by_name('password')
        submit = self.driver.find_element_by_name('s')
        username.send_keys('javier.bustillo')
        password.send_keys('') #TODO: USE ENVIRONMENT VARIABLE
        submit.click()
        for faculty, departments in self.faculties_departments.items():
            for department in departments:
                self.driver.get('https://home.uprm.edu/cursos/appsearch.php?l=0&a=lc&f=%s&d=%s' % (faculty, department))
                rows = self.driver.find_element_by_xpath("/html/body[@class='rea_view_body']/div[@id='container']/div[@id='body']/table[@id='ui_content_tbl']/tbody/tr/td[@id='ui_body_area']/table/tbody/tr/td/table/tbody/td[1]")
                print("hm")


if __name__ == '__main__':
    CourseScrape().scrape()
