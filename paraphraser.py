from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os

class Paraphrase_Text():
    def __init__(self, text):
        self.WINDOW_SIZE = "1920,1080"
        self.webpage = "https://seotoolstation.com/article-rewriter"
        self.chrome_options = Options()  
        self.executable_path = os.getcwd()+"/chromedriver"
        self.text = text
        self.configure_arguments()
        self.result = self.run_chrome_driver()

    def return_paraphrased(self):
        return self.result

    def configure_arguments(self):
        self.chrome_options.add_argument("start-maximized") # open Browser in maximized mode
        self.chrome_options.add_argument("disable-infobars") # disabling infobars
        self.chrome_options.add_argument("--disable-extensions")
        self.chrome_options.add_argument("--headless")  
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument('--disable-dev-shm-usage')

    def run_chrome_driver(self):
        driver = webdriver.Chrome(self.executable_path, options=self.chrome_options)
        driver.get(self.webpage)

        search_input_box = driver.find_element_by_name("data")
        search_input_box.send_keys(self.text)

        submit = driver.find_element_by_name("submit")
        submit.click()

        output_box = driver.find_element_by_id("textArea")
        text_final = output_box.text

        driver.close()
        return text_final



#p = Paraphrase_Text("hello world")

#print(p.return_paraphrased())
