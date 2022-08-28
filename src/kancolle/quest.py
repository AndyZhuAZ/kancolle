import requests


class Quest:
    code: str
    name: str
    desc: str
    bonus: str
    requirement: str
    pre: list

    def __init__(self,
                 code: str,
                 name: str,
                 desc: str | None,
                 bonus: str | None,
                 req: str | None,
                 pre: list[str] | None) -> None:
        super().__init__()
        self.code = code
        self.name = name
        self.desc = desc
        self.bonus = bonus
        self.requirement = req
        self.pre = pre

    def json(self):
        pass

    def pre_quest(self):
        return [query_id(i) for i in self.pre]


def query_id(_id):
    quest = {
        "code": "B185",
        "desc": "编成包含「Fletcher级」以及「John C.Butler级」2只以上的舰队，反复出击南西诸岛东部奥廖尔海，中部北海域孔雀岛近海，南西海域槟榔屿海域深部，昭南本土航线！消灭敌军！",
        "memo": "奖励:以下奖励三选一：特制家具职人 ×2间宫 ×2改修资材 ×7以下奖励二选一：5inch単装砲 Mk.30 ×4GFCS Mk.37 ×1",
        "memo2": "以Fletcher、Johnston、Samuel B.Roberts其中两艘+任意舰四艘出击2-3、6-4、7-3P2、7-4各2次S胜",
        "name": "美驱逐舰部队的激战",
        "pre": [
            "B184",
            "F110"
        ]
    }
    quest = Quest(quest['code'], quest['name'], quest['desc'], quest["memo"], quest["memo2"], quest["pre"])
    return quest


kcwiki_urls = ['https://zh.kcwiki.cn/index.php?title=%E4%BB%BB%E5%8A%A1&action=raw',
               'https://zh.kcwiki.cn/index.php?title=%E4%BB%BB%E5%8A%A1/%E6%9C%9F%E9%97%B4%E9%99%90%E5%AE%9A%E4%BB%BB'
               '%E5%8A%A1&action=raw',
               'https://zh.kcwiki.cn/index.php?title=%E4%BB%BB%E5%8A%A1/%E6%9C%80%E6%96%B0%E4%BB%BB%E5%8A%A1&action=raw',
               ]  # 三个需要抓取的网站
kcwiki_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/88.0.4324.104 Safari/537.36',
    'cookie': "_ga=GA1.2.1881705690.1629543107; VEE=wikitext; vector-nav-p-.E5.B8.B8.E7.94.A8.E9.80.9F.E6.9F.A5=true; "
              "vector-nav-p-.E5.87.BA.E5.87.BB.E6.B5.B7.E5.9F.9F=true; vector-nav-p-tb=true; "
              "vector-nav-p-.E5.8F.82.E4.B8.8E.E7.BC.96.E5.86.99kcwiki=true; vector-nav-p-.E6.B2.99.E7.9B.92=true; "
              "vector-nav-p-.E6.B8.B8.E6.88.8F.E6.96.87.E5.8C.96=true; "
              "vector-nav-p-kcwiki.E6.97.97.E4.B8.8B.E9.A1.B9.E7.9B.AE=true; vector-nav-p-.E9.81.93.E5.85.B7=true; "
              "vector-nav-p-.E5.85.A5.E6.B8.A0.E3.83.BB.E8.A1.A5.E7.BB.99=true; "
              "vector-nav-p-.E6.94.B9.E8.A3.85.E3.83.BB.E5.B7.A5.E5.8E.82=true; kcwiki_UserName=Callofblood; "
              "kcwiki_UserID=5277; kcwiki_Token=a696414057db9b77a8a4472b77eeaf90; _gid=GA1.2.1109110936.1631275946; "
              "kcwiki__session=1tin18vua2u0c4nmk9i511h50fbbsqm7; vector-nav-p-.E4.BB.BB.E5.8A.A1=true "
}


def quest_data_init(path, website):
    session = requests.Session()
    if website == 'kcwiki':
        session.headers = kcwiki_headers
        for index, url in enumerate(kcwiki_urls):
            result = session.get(url)
            pages = result.text.split('页首}}\n')
            for page_index, page in enumerate(pages[1:]):
                with open('{}/{}_{}'.format(path, index, page_index), 'w', encoding='utf-8') as f:
                    f.write(page.split('{{页尾')[0])
    elif website == 'wiki':
        pass
