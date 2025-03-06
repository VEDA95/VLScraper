from os import getenv
from dotenv import load_dotenv
from selenium.webdriver import Chrome, ChromeOptions, ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

def main() -> None:
    load_dotenv()

    bar_code = getenv("VALUE_LINE_BARCODE")
    login_url = getenv("LOGIN_URL")
    url_root = getenv("VALUE_LINE_URL_ROOT")

    if bar_code is None or len(bar_code) == 0:
        raise Exception("VALUE_LINE_BARCODE environment variable is not set.")

    if login_url is None or len(login_url) == 0:
        raise Exception("VALUE_LINE_LOGIN_URL environment variable is not set")

    if url_root is None or len(url_root) == 0:
        raise Exception("VALUE_LINE_URL_ROOT environment variable is not set")

    browser_options = ChromeOptions()
    browser_options.add_argument("--headless")
    browser = Chrome(options=browser_options)

    browser.get(login_url)

    barcode_input = browser.find_element(By.ID, "user-barcode")
    submit_button = browser.find_element(By.XPATH, "div.log-on-buttons > button[type=submit]")
    dashboard_link = browser.find_element(By.XPATH, "a[title=DASHBOARD]")
    current_issue_link = browser.find_element(By.XPATH, "div.span6:first-of-type > ul > li > a")

    ActionChains(browser).click(barcode_input).send_keys(bar_code).perform()
    ActionChains(browser).click(submit_button).perform()

    wait = WebDriverWait(browser, 10)

    wait.until(lambda _: dashboard_link.is_displayed())
    dashboard_link.click()

    wait = WebDriverWait(browser, 10)

    wait.until(lambda _: current_issue_link.is_displayed())
    current_issue_link.click()

if __name__ == "__main__":
    try:
        main()

    except Exception as error:
        print(error)
        exit(1)

    except KeyboardInterrupt:
        print("\nGoodbye!")
