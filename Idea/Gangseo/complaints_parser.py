import os
import time
import warnings
import pandas as pd
import chromedriver_autoinstaller
import tqdm
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

warnings.filterwarnings('ignore')


def main():
    output_dir = "../output/complaints/"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    path = chromedriver_autoinstaller.install()
    driver = webdriver.Chrome(path)

    driver.get("https://www.gangseo.seoul.kr/gs0202022?curPage=1")
    driver.set_window_size(200, 800)

    time.sleep(2)

    title_list = []
    view_list = []

    for i in tqdm.tqdm(range(1, 99)):
        try:
            for row in range(1, 10):
                title_xpath = f'//*[@id="container"]/div[1]/div/div/div[3]/div/table/tbody/tr[{row}]/td[2]'
                title_row = driver.find_element("xpath", title_xpath)
                title = title_row.text
                title_list.append(title)

                view_xpath = f'//*[@id="container"]/div[1]/div/div/div[3]/div/table/tbody/tr[{row}]/td[6]'
                view_row = driver.find_element("xpath", view_xpath)
                view = view_row.text
                view_list.append(view)

            next = "#container > div.content-body > div > div > div.paginate > a.m-next"
            next_button = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, next)))

            next_button.click()

        except:
            break

    print(len(title_list), len(view_list))

    df = pd.DataFrame({'title': title_list, 'view': view_list})
    df.to_csv(os.path.join(output_dir, "강서구_민원.csv"), encoding='utf-8-sig')

if __name__ == '__main__':
    main()