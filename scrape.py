from bs4 import BeautifulSoup
import requests
# install: pip install --upgrade arabic-reshaper
import arabic_reshaper
import json
# install: pip install python-bidi
from bidi.algorithm import get_display
# correct its direction

dict = {1: 7,
        2: 286,
        3: 200,
        4: 176,
        5: 120,
        6: 165,
        7: 206,
        8: 75,
        9: 129,
        10: 109,
        11: 123,
        12: 111,
        13: 43,
        14: 52,
        15: 99,
        16: 128,
        17: 111,
        18: 110,
        19: 98,
        20: 135,
        21: 112,
        22: 78,
        23: 118,
        24: 64,
        25: 77,
        26: 227,
        27: 93,
        28: 88,
        29: 69,
        30: 60,
        31: 34,
        32: 30,
        33: 73,
        34: 54,
        35: 45,
        36: 83,
        37: 182,
        38: 88,
        39: 75,
        40: 85,
        41: 54,
        42: 53,
        43: 89,
        44: 59,
        45: 37,
        46: 35,
        47: 38,
        48: 29,
        49: 18,
        50: 45,
        51: 60,
        52: 49,
        53: 62,
        54: 55,
        55: 78,
        56: 96,
        57: 29,
        58: 22,
        59: 24,
        60: 13,
        61: 14,
        62: 11,
        63: 11,
        64: 18,
        65: 12,
        66: 12,
        67: 30,
        68: 52,
        69: 52,
        70: 44,
        71: 28,
        72: 28,
        73: 20,
        74: 56,
        75: 40,
        76: 31,
        77: 50,
        78: 40,
        79: 46,
        80: 42,
        81: 29,
        82: 19,
        83: 36,
        84: 25,
        85: 22,
        86: 17,
        87: 19,
        88: 26,
        89: 30,
        90: 20,
        91: 15,
        92: 21,
        93: 11,
        94: 8,
        95: 8,
        96: 19,
        97: 5,
        98: 8,
        99: 8,
        100: 11,
        101: 11,
        102: 8,
        103: 3,
        104: 9,
        105: 5,
        106: 4,
        107: 7,
        108: 3,
        109: 6,
        110: 3,
        111: 5,
        112: 4,
        113: 5,
        114: 6}

final = {}


def ayas(surah_num):

    num_ayahs = dict[surah_num]
    l = []
    for i in range(1, num_ayahs+1):
        page = requests.get("https://al-quran.info/" +
                            str(surah_num) + "/" + str(i) + "/Ca")
        soup = BeautifulSoup(page.text, "html.parser")

        price = soup.findAll("div", attrs={"class": "quran-content"})

        text = []

        for i in range(num_ayahs):
            try:
                text.append(price[i].text)
            except:
                pass

        text = ' '.join(text)

        reshaped_text = arabic_reshaper.reshape(text)
        bidi_text = get_display(reshaped_text)

        l.append(bidi_text)
    return l


def make():
    for i in range(1, 115):
        try:
            final[i] = {
                'number': i,
                'ayas': ayas(i)
            }
            print(f'Surah {i} done')

        except:
            final[i] = {
                'number': i,
                'ayas': []
            }
    a_file = open("quran.json", "w")
    json.dump(final, a_file)
    a_file.close()


a_file = open("quran.json", "r")
json_object = json.load(a_file)
a_file.close()


def fix():
    x5 = ['أَلَم تَرَ كَيفَ فَعَلَ رَبُّكَ بِأَصحابِ الفيلِ',
          'أَلَم يَجعَل كَيدَهُم في تَضليلٍ', 'وَأَرسَلَ عَلَيهِم طَيرًا أَبابيلَ', 'تَرميهِم بِحِجارَةٍ مِن سِجّيلٍ', 'فَجَعَلَهُم كَعَصفٍ مَأكولٍ']

    l = []
    for i in range(len(x5)):
        reshaped_text = arabic_reshaper.reshape(x5[i])
        bidi_text = get_display(reshaped_text)
        l.append(bidi_text)
    a_file = open("quran.json", "r")
    json_object = json.load(a_file)
    a_file.close()
    json_object['105']['ayas'] = l
    a_file = open("quran.json", "w")
    json.dump(json_object, a_file)
    a_file.close()


def getaya(sura, number):
    a_file = open("quran.json", "r")
    json_object = json.load(a_file)
    a_file.close()
    return json_object[str(sura)]['ayas'][number-1]


for i in range(1, 6):
    print(getaya(105, i))
