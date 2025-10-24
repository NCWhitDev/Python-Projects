import json
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
# https://eldenring.wiki.fextralife.com/Builds


def spell_stats(driver, href):
    driver.get(href)
    time.sleep(3)
    Type = '/html/body/div[4]/div[2]/div[2]/div[2]/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[1]/div[1]/div/table/tbody/tr[3]/td[2]/a'
    FPCost = '/html/body/div[4]/div[2]/div[2]/div[2]/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[1]/div[1]/div/table/tbody/tr[4]/td[1]'
    ReqS = '/html/body/div[4]/div[2]/div[2]/div[2]/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[1]/div[1]/div/table/tbody/tr[4]/td[2]'
    Effect = '/html/body/div[4]/div[2]/div[2]/div[2]/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[1]/div[1]/div/table/tbody/tr[5]/td/div[1]'
    # ReqI = '/html/body/div[4]/div[2]/div[2]/div[2]/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[1]/div[1]/div/table/tbody/tr[5]/td/div[2]/a[1]/following-sibling::text()'
    # ReqF = '/html/body/div[4]/div[2]/div[2]/div[2]/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[1]/div[1]/div/table/tbody/tr[5]/td/div[2]/a[2]/following-sibling::text()'
    # ReqA = '/html/body/div[4]/div[2]/div[2]/div[2]/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[1]/div[1]/div/table/tbody/tr[5]/td/div[2]/a[3]/following-sibling::text()'


    info = {
        "URL": driver.find_element(By.CSS_SELECTOR,'a[id="page-title"]').get_attribute('href'),
        "Name": driver.find_element(By.TAG_NAME, 'h2').text,
        "Type": driver.find_element(By.XPATH, Type).text,
        "FP Cost": driver.find_element(By.XPATH, FPCost).text,
        'Required Slots': driver.find_element(By.XPATH, ReqS).text,
        'Effect': driver.find_element(By.XPATH, Effect).text,
        # 'Required Intelligence': driver.find_element(By.XPATH, ReqI),
        # 'Required Faith': driver.find_element(By.XPATH, ReqF),
        # 'Required Arcane': driver.find_element(By.XPATH, ReqA),
    }

    # Write to JSON File
    file_path = "spells.json"
    json_line = json.dumps(info)
    with open(file_path, 'a') as fp:
        fp.write(json_line + '\n')


def to_get_A(driver, URL):
    # We will scroll to top (until we find target element) print the text and then click on it.
    driver.execute_script("window.scrollTo(0, 0);")
    top_element = driver.find_element(By.XPATH, '//*[@id="wiki-content-block"]/p[1]/text()[4]').text
    print(top_element)

    #Get info on Socrcies and Incantations
    sorceries = driver.find_element(By.LINK_TEXT, 'Sorceries')
    sorceries.click()
    info = driver.find_element(By.XPATH, '//*[@id="wiki-content-block"]/p[1]').text
    print(info)

    # Sorceries - Open in new browser tab (optional)
    vid_link = driver.find_element(By.XPATH, '//*[@id="gqSzUthyrsU"]')
    vid_link.click()
    

    time.sleep(3)
    incantations = driver.find_element(By.LINK_TEXT, 'Incantations')
    incantations.click()
    info = driver.find_element(By.XPATH, '//*[@id="wiki-content-block"]/p[1]').text
    print(info)

    # Incantations - Open in new browser tab (optional)
    vid_link = driver.find_element(By.XPATH, '//*[@id="wiki-content-block"]/div[1]/div[2]/div[1]/div/iframe')
    vid_link.click()

def main(URL):
    driver = webdriver.Firefox()
    driver.get(URL)
    spells = []

    # We only want the first 1-207 elements
    # Gives all the <a>
    time.sleep(3)     
    spells = driver.find_elements(By.XPATH, "/html/body/div[4]/div[2]/div[2]/div[2]/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[1]/div[5]//a[@class='wiki_link wiki_tooltip']")
    print(spells)
    print(len(spells))
    spells = [x.get_attribute('href') for x in spells]
    print(spells)

    for spell_link in spells:
        spell_stats(driver, spell_link)

    # to_get_A(driver, URL)

    # Closes the browser window
    driver.quit()

if __name__ == "__main__":
    main("https://eldenring.wiki.fextralife.com/Magic+Spells") 
