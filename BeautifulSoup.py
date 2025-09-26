import json
import time
import requests
from protego import Protego
from bs4 import BeautifulSoup

# one line for constant global headers (fix its value)
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ' \
             '(KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 OPR/120.0.0.0'
HEADERS = {'user-agent': user_agent}

def robot_parser(domain_name):
    robots = requests.get(domain_name + '/robots.txt', headers=HEADERS)
    rp = Protego.parse(robots.text)
    return rp

def helper_scrape(url, crawl_delay):
    # Will download a page, scrape it for data and return.
    response = requests.get(url, headers=HEADERS)
    time.sleep(crawl_delay)
    soup = BeautifulSoup(response.text, 'html.parser')
    boost = soup.find('span', string='Boost').next_sibling.strip()
    attk = soup.find('a', title="Elden Ring Physical Damage").next_sibling.strip()
    crit = soup.find('a', string='Crit').parent.next_sibling.strip()
    holy = soup.find('a', title="Elden Ring Holy Damage").parent.next_sibling.strip()
    magic = soup.find('a', string='Mag').next_sibling.strip()
    fp = soup.find('a', string='FP').next_sibling.strip()
    weight = soup.find('a', title='Elden Ring Weight').find_next('span').text
    dictionary = {
        'URL': url,
        'Title': soup.find('title').text.strip(),
        'Description': soup.find('em').text.strip(),
        'Boost': boost,
        'AttDMG': attk,
        'Crit': crit,
        'Holy_DMG': holy,
        'Magic_DMG': magic,
        'FP': fp,
        'Weight': weight
    }

    json_line = json.dumps(dictionary)
    with open('ERW.jl', 'a') as fp:
        fp.write(json_line + '\n')


# =========================================================
def main(domain_link):
    # download url and get all links that we want to request + scrape from.
    links = []
    index_link = domain_link + '/Weapons'
    robot = robot_parser(domain_link)
    crawl_delay = robot.crawl_delay('*') or 0
    response = requests.get(index_link, headers=HEADERS)
    time.sleep(crawl_delay)
    if robot.can_fetch(index_link, '*'):
        soup = BeautifulSoup(response.text, 'html.parser')

        i = soup.find_all('a', class_ = 'wiki_link wiki_tooltip')
        for each in i:
            links.append(each['href'])

        # No dups
        links = set(links)
        print(links)
        print(len(links))

        counts = 0
        for each in links:
            # DONT GET https://eldenring.wiki.fextralife.com/Upgrades <1-409>
            if each == '/Upgrades': continue

            item = domain_link + each
            if robot.can_fetch(item, '*'):
                try:
                    if "'" in each: pass
                    helper_scrape(item,crawl_delay)
                    print(item)
                    counts += 1
                except:
                    print("\n This item did not work " + item + "\n")
                    continue
        print(counts)

if __name__ == '__main__':
    main('https://eldenring.wiki.fextralife.com')
    # Sources:
    # https://github.com/scrapy/protego
    # https://www.crummy.com/software/BeautifulSoup/bs4/doc/#Tag