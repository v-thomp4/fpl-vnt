import os
from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup
from operator import itemgetter
#import sentry_sdk
#from sentry_sdk.integrations.flask import FlaskIntegration
import redis
import json
#from selenium import webdriver
#from selenium.webdriver.chrome.options import Options
#from selenium.webdriver.common.by import By

#options = Options()
#prefs = {"profile.managed_default_content_settings.images": 2}
#options.add_experimental_option("prefs", prefs)
#options.add_argument('--headless')
#options.add_argument('--no-sandbox')
#options.add_argument('--disable-dev-shm-usage')
#driver = webdriver.Chrome(options=options)
#driver.get("https://www.livefpl.net/leagues/510143")
#e = driver.find_element(By.CLASS_NAME, "btn-not-active")
#e.click()
"""
    Nathan - 5379613
    Hiếu Nguyễn - 7266208
    Melencolia - 5377348
    Linkvn - 7305869
    NhuomDoTroiAu - 3852498

    loki - 128949
    TANZON - 5384523
    CB® BigSam - 1967639
    tuanmua - 6825437
    ALEXTUAN - 2556122
"""
"""
sentry_sdk.init(
    dsn="http://c8c9c892dd844bf0976cd3e6ac78a8a2@10.111.194.10:9002/2",
    integrations=[FlaskIntegration()]
)
"""

def count_point(soup, id, name=''):
    gw = soup.find(id="%s_gw" %id).get_text()
    total = soup.find(id="%s_total" %id).get_text()
    hit = soup.find(id="%s_hit" %id).get_text().split('\n', 1)[0]
    played = soup.find(id="%s_played" %id).get_text()
    transfers_list = soup.find(id="%s" %id).find(class_="table-transfers").get_text().strip().replace("\n", "<br>")
    chip = soup.find(id="%s_chip" %id).get_text()
    n_played = int(played.split("/")[0])
    t_played = int(played.split("/")[1])
    cap = soup.find(id="%s_cap" %id).get_text()
    vice_cap = soup.find(id="%s_vc" %id).get_text()
    event = soup.find(target="_blank")['href'].split('/')[-1]
    i = 0
    p_list = []
    #table_club_shirt_1 = str(soup.find_all(id="%s_1" %id)[0].find(class_="table-club-shirt")).replace("<img", "<img width='12px'").replace("\"", "\'")
    #played_1 = soup.find(id="%s_1" %id).get_text().strip()[1:].strip().replace("\n0%\n", " %s :" % table_club_shirt_1)
    while i < 15:
        p = soup.find_all(id="%s_%s" %(id, i))[0]
        table_club_shirt = str(p.find(class_="table-club-shirt")).replace("<img", "<img width='12px'").replace("\"", "\'").replace("../static/new_logos", "https://res.cloudinary.com/dck9rbq8d/image/upload/v1684140873")
        table_club_shirt_1 = str(soup.find_all(id="%s_1" %id)[0].find(class_="table-club-shirt")).replace("<img", "<img width='12px'").replace("\"", "\'")
        played_ = p.get_text().strip()[1:].strip().replace("\n0%\n", " %s :" % table_club_shirt)
        captain_t = "(C)"
        played_full = played_.split(" ")[0]
        if captain_t in played_:
            played_ = "<div class='inline-captain'><b>%s</b></div>" %played_
        else:
            if i < 11:
                played_ = "<div class='inline-played'>%s</div>" %played_
                #p_name = played_.split(" ")[0]
                #played_ = played_.replace("%s" %p_name, "<div class='inline-played'>%s" % p_name)
                try:
                    soup.find_all(id="%s_%s" %(id, i))[0].find(class_="table-player-ytoplay").get_text()
                except:
                    print("player-played")
                else:
                    played_ = p.get_text().strip()[1:].strip().replace("\n0%\n", " %s :" % table_club_shirt)
                    p_name = played_.split(" ")[0]
                    played_ = "<div class='inline-nplayed'>[#] %s</div>" %played_
            else:
                played_ = "<div class='inline'>[B] %s</div>" %played_
        p_list.append(played_)
        i += 1
    played_list = ''.join(p_list)
    #played_list = "%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s" \
    #% (p_list[0], p_list[1], p_list[2], p_list[3], p_list[4], p_list[5], p_list[6], p_list[7], p_list[8], p_list[9], p_list[10], p_list[11], p_list[12], p_list[13], p_list[14])

    user_list = {'name': name, 'point': int(gw) + int(hit), 'played': played, 'captain': cap, 'vice_cap': vice_cap, 'played': played, 'hit': hit, 'gw': gw, 'chip': chip, 'event': event, 'id': id, 'total': int(total), 'played_list': played_list, "transfers_list": transfers_list}
    return user_list, int(gw) + int(hit), cap, played, n_played, t_played

def hello():
    # Create a User Agent (Optional)

    headers = {"User-Agent": "Mozilla/5.0 (Linux; U; Android 4.2.2; he-il; NEO-X5-116A Build/JDQ39) AppleWebKit/534.30 ("
                              "KHTML, like Gecko) Version/4.0 Safari/534.30"}

    # # Send get() Request and fetch the webpage contents
    response = requests.get("https://www2.livefpl.net/leagues/1223245", headers=headers)
    webpage = response.content
    # Check Status Code (Optional)
    # print(response.status_code)

    # Create a Beautiful Soup Object
    soup = BeautifulSoup(webpage, "html.parser")
    result = soup.find(class_="btn-active").get_text()
    # list array team
    #point_mandan = 0
    point_mandan = count_point(soup, 128949)[1] + count_point(soup, 2556122)[1] + \
    count_point(soup, 6825437)[1] + count_point(soup, 5384523)[1] + count_point(soup, 1967639)[1]
    print(point_mandan)
    point_phandao = count_point(soup, 5379613)[1] + count_point(soup, 7266208)[1] + \
    count_point(soup, 5377348)[1] + count_point(soup, 7305869)[1] + count_point(soup, 3852498)[1]
    
    cap_mandan  = [count_point(soup, 128949)[2] + count_point(soup, 2556122)[2] + \
    count_point(soup, 6825437)[2] + count_point(soup, 5384523)[2] + count_point(soup, 1967639)[2]]
    cap_mandan.sort()
    cap_mandan = ', '.join(cap_mandan)

    cap_phandao  = [count_point(soup, 5379613)[2] + count_point(soup, 7266208)[2] + \
    count_point(soup, 5377348)[2] + count_point(soup, 7305869)[2] + count_point(soup, 3852498)[2]]
    cap_phandao.sort()
    cap_phandao = ', '.join(cap_phandao)

    n_played_mandan  = count_point(soup, 128949)[4] + count_point(soup, 2556122)[4] + \
    count_point(soup, 6825437)[4] + count_point(soup, 5384523)[4] + count_point(soup, 1967639)[4]
    t_played_mandan  = count_point(soup, 128949)[5] + count_point(soup, 2556122)[5] + \
    count_point(soup, 6825437)[5] + count_point(soup, 5384523)[5] + count_point(soup, 1967639)[5]

    n_played_phandao  = count_point(soup, 5379613)[4] + count_point(soup, 7266208)[4] + \
    count_point(soup, 5377348)[4] + count_point(soup, 7305869)[4] + count_point(soup, 3852498)[4]
    t_played_phandao  = count_point(soup, 5379613)[5] + count_point(soup, 7266208)[5] + \
    count_point(soup, 5377348)[5] + count_point(soup, 7305869)[5] + count_point(soup, 3852498)[5]

    vnt_list = [{'name': '5T - Mân Đàn', 'point': point_mandan, 'cap': cap_mandan, 'n_played': n_played_mandan, \
                't_played': t_played_mandan, 'team': 'Thọ Mạnh: %s<br>Tân Hoàng: %s<br>Thái Nguyễn: %s<br>Tuấn Mệt: %s<br>Tuấn Mưa: %s' % (count_point(soup, \
                128949)[1], count_point(soup, 5384523)[1], count_point(soup, 1967639)[1], count_point(soup, 2556122)[1], count_point(soup, 6825437)[1])}, {'name': 'Phấn Đào', 'point': point_phandao, \
                'cap': cap_phandao, 'n_played': n_played_phandao, 't_played': t_played_phandao, 'team': 'Hiếu Nguyễn: %s<br>Nam Trần: %s<br>Chính Nguyễn: \
                %s<br>Hiếu Trần: %s<br>Tùng Linh: %s' % (count_point(soup, 7266208)[1], count_point(soup, 5379613)[1], count_point(soup, 5377348)[1], count_point(soup, 3852498)[1], count_point(soup, 7305869)[1])}]

    vnt_list = sorted(vnt_list, key=itemgetter('point'), reverse=True)
    vnt_list[0].update({'table' : 1})
    vnt_list[1].update({'table' : 2})
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    json_vnt_list = json.dumps(vnt_list)
    r.set('vnt_list', json_vnt_list)
    # list array members
    user_list = [count_point(soup, 7266208, 'Hiếu Nguyễn')[0], count_point(soup, 5379613, 'Nam Trần')[0], count_point(soup, 2556122, 'Tuấn Mệt')[0], \
                 count_point(soup, 5384523, 'Tân Hoàng')[0], count_point(soup, 1967639, 'Thái Nguyễn')[0], \
                 count_point(soup, 6825437, 'Tuấn Mưa')[0], count_point(soup, 5377348, 'Chính Nguyễn')[0], count_point(soup, 128949, 'Thọ Mạnh')[0], \
                 count_point(soup, 7305869, 'Tùng Linh')[0], count_point(soup, 3852498, 'Hiếu Trần')[0],]
    user_list = sorted(user_list, key=itemgetter('total'), reverse=True)
    user_list[0].update({'table' : 1})
    user_list[1].update({'table' : 2})
    user_list[2].update({'table' : 3})
    user_list[3].update({'table' : 4})
    user_list[4].update({'table' : 5})
    user_list[5].update({'table' : 6})
    user_list[6].update({'table' : 7})
    user_list[7].update({'table' : 8})
    user_list[8].update({'table' : 9})
    user_list[9].update({'table' : 10})

    json_user_list = json.dumps(user_list)
    r.set('user_list', json_user_list)
    r.set('result', result.encode('utf-8'))
if __name__ == "__main__":
    hello()
