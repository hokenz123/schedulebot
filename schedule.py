import js2py
import requests
from sys import argv
import datetime
from datetime import timedelta

command = argv

currdate = datetime.date.today()


headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "Connection": "keep-alive",
    #"Cookie": "CurrentSchedule=lesson; StudPrepAudit=1; divisionStuds=7; kurs=1; group=8878; _ym_uid=1697203841552738301; _ym_d=1697203841; tmr_lvid=cac6924b5c66bad53e10004aa6e60e25; tmr_lvidTS=1697203841122; PHPSESSID=dbfght6g6qvstafhav3ja4ldo2; session-cookie=178e99a96c39e8b4eb9c3d6dbeb261f5bf45131b29cb777dee266c0345556cd5bf76468455c2383a7303c326782b0be5; blind-font-size=fontsize-normal; blind-colors=color1; blind-font=sans-serif; blind-spacing=spacing-small; blind-images=imagesoff; _ym_isad=2; csrf-token-name=csrftoken; _ym_visorc=w; tmr_detect=0%7C1697463179369; csrf-token-value=178e99c8f66c40642d7f7c0493c299d36f61043539bf10751ef82661738e8fb5e331cecc699cc61b",
    "Host": "oreluniver.ru",
    "Referer": "https://oreluniver.ru/schedule",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
    "sec-ch-ua": '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "Windows"
}

group = '8878'
numberLessons = ["8:30 - 10:00", "10:10 - 11:40", "12:00 - 13:30", "13:40 - 15: 10", "15:20 - 16:50", "17:00 - 18:30"]
def get_schedule(date):
    code = 'function lol(x) {ds = new Date(); CurrentWeekStart = ds.getTime()+86400000-86400000*ds.getDay(); CurrentWeekStart = (CurrentWeekStart-(ds.getTimezoneOffset()*60000))-(3600*ds.getHours()+60*ds.getMinutes()+(1*ds.getSeconds()))*1000; return "https://oreluniver.ru/schedule//"+x+"///"+CurrentWeekStart+"/printschedule";}'
    res = js2py.eval_js(code)
    url = res(group)
    session = requests.session()
    response = session.get(url, headers=headers).json()
    inp = currdate
    if date == "next": inp = currdate + timedelta(1)
    schedule = ""
    cntr = 0
    for i in range(len(response)-2):
        responseJson = response[str(i)]
        if responseJson['DateLesson'] == str(inp):
            if cntr < 1: 
                schedule += f'В этот день к {responseJson["NumberLesson"]} паре\n'
                cntr += 1
            l = ""
            if responseJson['NumberSubGruop'] != 0: l = "Подгруппа: "+str(responseJson['NumberSubGruop'])+"\n"
#            print(f'{numberLessons[responseJson["NumberLesson"]-1]}')
            schedule += f'{responseJson["TitleSubject"]} ({responseJson["TypeLesson"]})\n{numberLessons[responseJson["NumberLesson"]-1]}\n{responseJson["Family"]} {responseJson["Name"][0]}.{responseJson["SecondName"][0]}. \n{responseJson["Korpus"]+ "-" +responseJson["NumberRoom"]}\n{l}\n'
    if cntr == 0:
        schedule = "Завтра нет пар!" if date == "next" else "Сегодня нет пар!"
    return schedule
# print (get_schedule("next"))
