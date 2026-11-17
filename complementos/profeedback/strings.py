"""Todos los textos que ve la persona, en los idiomas que ofrece Anki.

Si Anki está en un idioma que no figura aquí, se usa el inglés; y si a un idioma le falta
un texto concreto, ese texto sale en inglés. Para corregir o añadir un texto solo hay que
tocar este archivo. Los identificadores del código van en inglés; lo que se lee en pantalla,
aquí.
"""

from __future__ import annotations

from typing import Final, Literal

FlagKey = Literal["new_card", "hard_exercise", "previous_mistake"]

UIKey = Literal[
    "group_sound",
    "group_appearance",
    "test",
    "btn_accept",
    "label_volume",
    "sound_random",
    "sound_off",
    "open_folder",
    "label_on_correct",
    "label_on_again",
    "label_deck_finish",
    "label_day_finish",
    "test_correct",
    "test_again",
    "test_deck_finish",
    "test_day_finish",
    "preview",
    "preview_confetti",
    "play_failed",
    "styled_buttons",
    "flags_option",
    "confetti_option",
    "voice_madera",
    "voice_campanilla",
    "voice_suave",
    "error_generic",
    "error_badge",
    "error_buttons",
    "error_sound",
    "error_celebration",
]

DEFAULT_LANG: Final[str] = "en"

# Anki guarda el idioma como "es_ES", "pt_BR", "zh_TW", "jbo_EN"...  Estas
# equivalencias traducen esos códigos a las claves de las tablas de abajo.
_ALIASES: Final[dict[str, str]] = {
    "no": "nb",
    "nn": "nb",
    "in": "id",
    "iw": "he",
    "fil": "tl",
}

_FLAG_STRINGS: Final[dict[str, dict[str, str]]] = {
    "en": {
        "new_card": "NEW CARD",
        "hard_exercise": "HOLDING OUT",
        "previous_mistake": "ANOTHER CHANCE",
    },
    "es": {
        "new_card": "TARJETA NUEVA",
        "hard_exercise": "SE RESISTE",
        "previous_mistake": "OTRA OPORTUNIDAD",
    },
    "pt_BR": {
        "new_card": "CARTÃO NOVO",
        "hard_exercise": "ESTÁ RESISTINDO",
        "previous_mistake": "OUTRA CHANCE",
    },
    "pt_PT": {
        "new_card": "CARTÃO NOVO",
        "hard_exercise": "ESTÁ A RESISTIR",
        "previous_mistake": "OUTRA OPORTUNIDADE",
    },
    "ca": {
        "new_card": "TARGETA NOVA",
        "hard_exercise": "SE RESISTEIX",
        "previous_mistake": "UNA ALTRA OPORTUNITAT",
    },
    "gl": {
        "new_card": "TARXETA NOVA",
        "hard_exercise": "RESÍSTESE",
        "previous_mistake": "OUTRA OPORTUNIDADE",
    },
    "eu": {
        "new_card": "TXARTEL BERRIA",
        "hard_exercise": "GOGORRA DA",
        "previous_mistake": "BESTE AUKERA BAT",
    },
    "fr": {
        "new_card": "NOUVELLE CARTE",
        "hard_exercise": "ELLE RÉSISTE",
        "previous_mistake": "UNE AUTRE CHANCE",
    },
    "oc": {
        "new_card": "CARTA NOVÈLA",
        "hard_exercise": "RESISTÍS",
        "previous_mistake": "UNA AUTRA ESCASENÇA",
    },
    "it": {
        "new_card": "NUOVA CARTA",
        "hard_exercise": "RESISTE",
        "previous_mistake": "UN'ALTRA OCCASIONE",
    },
    "la": {
        "new_card": "CHARTA NOVA",
        "hard_exercise": "RESISTIT",
        "previous_mistake": "ALTERA OCCASIO",
    },
    "de": {
        "new_card": "NEUE KARTE",
        "hard_exercise": "HARTNÄCKIG",
        "previous_mistake": "NEUE CHANCE",
    },
    "nl": {
        "new_card": "NIEUWE KAART",
        "hard_exercise": "HARDNEKKIG",
        "previous_mistake": "NIEUWE KANS",
    },
    "af": {
        "new_card": "NUWE KAART",
        "hard_exercise": "HARDNEKKIG",
        "previous_mistake": "NOG 'N KANS",
    },
    "da": {
        "new_card": "NYT KORT",
        "hard_exercise": "GENSTRIDIG",
        "previous_mistake": "NY CHANCE",
    },
    "nb": {
        "new_card": "NYTT KORT",
        "hard_exercise": "GJENSTRIDIG",
        "previous_mistake": "NY SJANSE",
    },
    "sv": {
        "new_card": "NYTT KORT",
        "hard_exercise": "SEGLIVAD",
        "previous_mistake": "NY CHANS",
    },
    "fi": {
        "new_card": "UUSI KORTTI",
        "hard_exercise": "SINNIKÄS",
        "previous_mistake": "UUSI MAHDOLLISUUS",
    },
    "et": {
        "new_card": "UUS KAART",
        "hard_exercise": "VISA",
        "previous_mistake": "UUS VÕIMALUS",
    },
    "pl": {
        "new_card": "NOWA KARTA",
        "hard_exercise": "OPIERA SIĘ",
        "previous_mistake": "KOLEJNA SZANSA",
    },
    "cs": {
        "new_card": "NOVÁ KARTA",
        "hard_exercise": "ODOLÁVÁ",
        "previous_mistake": "DALŠÍ ŠANCE",
    },
    "sk": {
        "new_card": "NOVÁ KARTA",
        "hard_exercise": "ODOLÁVA",
        "previous_mistake": "ĎALŠIA ŠANCA",
    },
    "sl": {
        "new_card": "NOVA KARTICA",
        "hard_exercise": "SE UPIRA",
        "previous_mistake": "NOVA PRILOŽNOST",
    },
    "hr": {
        "new_card": "NOVA KARTICA",
        "hard_exercise": "ODOLIJEVA",
        "previous_mistake": "NOVA PRILIKA",
    },
    "sr": {
        "new_card": "НОВА КАРТИЦА",
        "hard_exercise": "ОДОЛЕВА",
        "previous_mistake": "НОВА ПРИЛИКА",
    },
    "hu": {
        "new_card": "ÚJ KÁRTYA",
        "hard_exercise": "MAKACS",
        "previous_mistake": "ÚJABB ESÉLY",
    },
    "ro": {
        "new_card": "CARTONAȘ NOU",
        "hard_exercise": "REZISTĂ",
        "previous_mistake": "ÎNCĂ O ȘANSĂ",
    },
    "bg": {
        "new_card": "НОВА КАРТА",
        "hard_exercise": "УПОРИТА",
        "previous_mistake": "НОВ ШАНС",
    },
    "el": {
        "new_card": "ΝΕΑ ΚΑΡΤΑ",
        "hard_exercise": "ΑΝΤΙΣΤΕΚΕΤΑΙ",
        "previous_mistake": "ΑΛΛΗ ΜΙΑ ΕΥΚΑΙΡΙΑ",
    },
    "ru": {
        "new_card": "НОВАЯ КАРТОЧКА",
        "hard_exercise": "НЕ ПОДДАЁТСЯ",
        "previous_mistake": "ЕЩЁ ОДИН ШАНС",
    },
    "uk": {
        "new_card": "НОВА КАРТКА",
        "hard_exercise": "НЕ ПІДДАЄТЬСЯ",
        "previous_mistake": "ЩЕ ОДИН ШАНС",
    },
    "be": {
        "new_card": "НОВАЯ КАРТКА",
        "hard_exercise": "НЕ ПАДДАЕЦЦА",
        "previous_mistake": "ЯШЧЭ АДЗІН ШАНЕЦ",
    },
    "kk": {
        "new_card": "ЖАҢА КАРТА",
        "hard_exercise": "БЕРІЛМЕЙДІ",
        "previous_mistake": "ТАҒЫ БІР МҮМКІНДІК",
    },
    "mn": {
        "new_card": "ШИНЭ КАРТ",
        "hard_exercise": "ДАВАГДАХГҮЙ БАЙНА",
        "previous_mistake": "ДАХИН БОЛОМЖ",
    },
    "tr": {
        "new_card": "YENİ KART",
        "hard_exercise": "DİRENİYOR",
        "previous_mistake": "BİR ŞANS DAHA",
    },
    "uz": {
        "new_card": "YANGI KARTA",
        "hard_exercise": "BO'YSUNMAYAPTI",
        "previous_mistake": "YANA BIR IMKONIYAT",
    },
    "hy": {
        "new_card": "ՆՈՐ ՔԱՐՏ",
        "hard_exercise": "ԴԻՄԱԴՐՈՒՄ Է",
        "previous_mistake": "ԵՎՍ ՄԵԿ ՀՆԱՐԱՎՈՐՈՒԹՅՈՒՆ",
    },
    "he": {
        "new_card": "כרטיס חדש",
        "hard_exercise": "מתעקש",
        "previous_mistake": "הזדמנות נוספת",
    },
    "yi": {
        "new_card": "נײַע קאַרטל",
        "hard_exercise": "שטעלט זיך אַנטקעגן",
        "previous_mistake": "נאָך אַ געלעגנהייט",
    },
    "ar": {
        "new_card": "بطاقة جديدة",
        "hard_exercise": "صامدة",
        "previous_mistake": "فرصة أخرى",
    },
    "fa": {
        "new_card": "کارت جدید",
        "hard_exercise": "مقاومت می‌کند",
        "previous_mistake": "فرصتی دیگر",
    },
    "ug": {
        "new_card": "يېڭى كارتا",
        "hard_exercise": "بوي سۇنمايدۇ",
        "previous_mistake": "يەنە بىر پۇرسەت",
    },
    "or": {
        "new_card": "ନୂଆ କାର୍ଡ",
        "hard_exercise": "ଟିକି ରହିଛି",
        "previous_mistake": "ଆଉ ଏକ ସୁଯୋଗ",
    },
    "th": {
        "new_card": "การ์ดใหม่",
        "hard_exercise": "ยังดื้ออยู่",
        "previous_mistake": "อีกโอกาสหนึ่ง",
    },
    "vi": {
        "new_card": "THẺ MỚI",
        "hard_exercise": "CÒN KHÓ NHỚ",
        "previous_mistake": "THÊM MỘT CƠ HỘI",
    },
    "ms": {
        "new_card": "KAD BAHARU",
        "hard_exercise": "MASIH DEGIL",
        "previous_mistake": "PELUANG LAGI",
    },
    "tl": {
        "new_card": "BAGONG KARD",
        "hard_exercise": "MATIGAS PA",
        "previous_mistake": "ISA PANG PAGKAKATAON",
    },
    "ja": {
        "new_card": "新規カード",
        "hard_exercise": "手ごわいカード",
        "previous_mistake": "もう一度チャンス",
    },
    "zh_CN": {
        "new_card": "新卡片",
        "hard_exercise": "顽固卡片",
        "previous_mistake": "再来一次机会",
    },
    "zh_TW": {
        "new_card": "新卡片",
        "hard_exercise": "頑固卡片",
        "previous_mistake": "再來一次機會",
    },
    "ko": {
        "new_card": "새 카드",
        "hard_exercise": "버티는 카드",
        "previous_mistake": "또 한 번의 기회",
    },
    "ga": {
        "new_card": "CÁRTA NUA",
        "hard_exercise": "AG CUR I GCOINNE",
        "previous_mistake": "DEIS EILE",
    },
    "eo": {
        "new_card": "NOVA KARTO",
        "hard_exercise": "REZISTAS",
        "previous_mistake": "ALIA ŜANCO",
    },
    "jbo": {
        "new_card": "CNINO KARDA",
        "hard_exercise": "XRANI FANTA",
        "previous_mistake": "DRATA LO NU KAKNE",
    },
}

_UI_STRINGS: Final[dict[str, dict[str, str]]] = {
    "en": {
        "group_appearance": "Appearance",
        "test": "Test",
        "btn_accept": "OK",
        "label_volume": "Volume",
        "sound_random": "Random",
        "label_deck_finish": "When a deck is finished",
    },
    "es": {
        "group_appearance": "Aspecto",
        "test": "Probar",
        "btn_accept": "Aceptar",
        "label_volume": "Volumen",
        "sound_random": "Aleatorio",
        "label_deck_finish": "Al terminar un mazo",
    },
    "pt_BR": {
        "group_appearance": "Aparência",
        "test": "Testar",
        "btn_accept": "Aceitar",
        "label_volume": "Volume",
        "sound_random": "Aleatório",
        "label_deck_finish": "Ao terminar um baralho",
    },
    "pt_PT": {
        "group_appearance": "Aparência",
        "test": "Testar",
        "btn_accept": "Aceitar",
        "label_volume": "Volume",
        "sound_random": "Aleatório",
        "label_deck_finish": "Ao terminar um baralho",
    },
    "ca": {
        "group_appearance": "Aspecte",
        "test": "Provar",
        "btn_accept": "Accepta",
        "label_volume": "Volum",
        "sound_random": "Aleatori",
        "label_deck_finish": "En acabar una baralla",
    },
    "gl": {
        "group_appearance": "Aspecto",
        "test": "Probar",
        "btn_accept": "Aceptar",
        "label_volume": "Volume",
        "sound_random": "Aleatorio",
        "label_deck_finish": "Ao rematar un mazo",
    },
    "eu": {
        "group_appearance": "Itxura",
        "test": "Probatu",
        "btn_accept": "Onartu",
        "label_deck_finish": "Sorta bat amaitzean",
    },
    "fr": {
        "group_appearance": "Apparence",
        "test": "Tester",
        "btn_accept": "Accepter",
        "label_volume": "Volume",
        "sound_random": "Aléatoire",
        "label_deck_finish": "À la fin d’un paquet",
    },
    "oc": {
        "group_appearance": "Aparéncia",
        "test": "Ensajar",
        "btn_accept": "Acceptar",
        "label_deck_finish": "Quand un paquet es acabat",
    },
    "it": {
        "group_appearance": "Aspetto",
        "test": "Testa",
        "btn_accept": "Accetta",
        "label_volume": "Volume",
        "sound_random": "Casuale",
        "label_deck_finish": "Al termine di un mazzo",
    },
    "la": {
        "group_appearance": "Species",
        "test": "Probare",
        "btn_accept": "Accipe",
        "label_deck_finish": "Fasce finito",
    },
    "de": {
        "group_appearance": "Erscheinungsbild",
        "test": "Testen",
        "btn_accept": "OK",
        "label_volume": "Lautstärke",
        "sound_random": "Zufällig",
        "label_deck_finish": "Wenn ein Stapel fertig ist",
    },
    "nl": {
        "group_appearance": "Uiterlijk",
        "test": "Testen",
        "btn_accept": "Accepteren",
        "label_deck_finish": "Als een stapel klaar is",
    },
    "af": {
        "group_appearance": "Voorkoms",
        "test": "Toets",
        "btn_accept": "Aanvaar",
        "label_deck_finish": "Wanneer 'n pak klaar is",
    },
    "da": {
        "group_appearance": "Udseende",
        "test": "Test",
        "btn_accept": "Accepter",
        "label_deck_finish": "Når en bunke er færdig",
    },
    "nb": {
        "group_appearance": "Utseende",
        "test": "Test",
        "btn_accept": "Godta",
        "label_deck_finish": "Når en kortstokk er ferdig",
    },
    "sv": {
        "group_appearance": "Utseende",
        "test": "Testa",
        "btn_accept": "Acceptera",
        "label_deck_finish": "När en kortlek är klar",
    },
    "fi": {
        "group_appearance": "Ulkoasu",
        "test": "Testaa",
        "btn_accept": "Hyväksy",
        "label_deck_finish": "Kun pakka on valmis",
    },
    "et": {
        "group_appearance": "Välimus",
        "test": "Testi",
        "btn_accept": "Nõustu",
        "label_deck_finish": "Kui pakk on läbi",
    },
    "pl": {
        "group_appearance": "Wygląd",
        "test": "Testuj",
        "btn_accept": "Akceptuj",
        "label_deck_finish": "Po ukończeniu talii",
    },
    "cs": {
        "group_appearance": "Vzhled",
        "test": "Otestovat",
        "btn_accept": "Přijmout",
        "label_deck_finish": "Po dokončení balíčku",
    },
    "sk": {
        "group_appearance": "Vzhľad",
        "test": "Otestovať",
        "btn_accept": "Prijať",
        "label_deck_finish": "Po dokončení balíčka",
    },
    "sl": {
        "group_appearance": "Videz",
        "test": "Testiraj",
        "btn_accept": "Sprejmi",
        "label_deck_finish": "Ko je komplet končan",
    },
    "hr": {
        "group_appearance": "Izgled",
        "test": "Testiraj",
        "btn_accept": "Prihvati",
        "label_deck_finish": "Kad je špil gotov",
    },
    "sr": {
        "group_appearance": "Изглед",
        "test": "Тест",
        "btn_accept": "Прихвати",
        "label_deck_finish": "Када је шпил завршен",
    },
    "hu": {
        "group_appearance": "Megjelenés",
        "test": "Teszt",
        "btn_accept": "Elfogadás",
        "label_deck_finish": "Egy pakli befejezésekor",
    },
    "ro": {
        "group_appearance": "Aspect",
        "test": "Testează",
        "btn_accept": "Acceptă",
        "label_deck_finish": "La terminarea unui pachet",
    },
    "bg": {
        "group_appearance": "Облик",
        "test": "Тест",
        "btn_accept": "Приеми",
        "label_deck_finish": "При завършване на тесте",
    },
    "el": {
        "group_appearance": "Εμφάνιση",
        "test": "Δοκιμή",
        "btn_accept": "Αποδοχή",
        "label_deck_finish": "Όταν ολοκληρωθεί μια τράπουλα",
    },
    "ru": {
        "group_appearance": "Оформление",
        "test": "Проверить",
        "btn_accept": "Принять",
        "label_deck_finish": "При завершении колоды",
    },
    "uk": {
        "group_appearance": "Зовнішній вигляд",
        "test": "Перевірити",
        "btn_accept": "Прийняти",
        "label_deck_finish": "Коли колоду завершено",
    },
    "be": {
        "group_appearance": "Знешні выгляд",
        "test": "Праверыць",
        "btn_accept": "Прыняць",
        "label_deck_finish": "Калі калода скончана",
    },
    "kk": {
        "group_appearance": "Сыртқы түрі",
        "test": "Сынау",
        "btn_accept": "Қабылдау",
        "label_deck_finish": "Топтама аяқталғанда",
    },
    "mn": {
        "group_appearance": "Харагдац",
        "test": "Турших",
        "btn_accept": "Зөвшөөрөх",
        "label_deck_finish": "Багц дуусахад",
    },
    "tr": {
        "group_appearance": "Görünüm",
        "test": "Test Et",
        "btn_accept": "Kabul Et",
        "label_deck_finish": "Bir deste bitince",
    },
    "uz": {
        "group_appearance": "Koʻrinish",
        "test": "Sinash",
        "btn_accept": "Qabul qilish",
        "label_deck_finish": "Toʻplam tugaganda",
    },
    "hy": {
        "group_appearance": "Տեսք",
        "test": "Փորձել",
        "btn_accept": "Ընդունել",
        "label_deck_finish": "Երբ խումբն ավարտվում է",
    },
    "he": {
        "group_appearance": "מראה",
        "test": "בדוק",
        "btn_accept": "אישור",
        "label_deck_finish": "בסיום חפיסה",
    },
    "yi": {
        "group_appearance": "אויסזען",
        "test": "פּרוּוו",
        "btn_accept": "אָנעמען",
        "label_deck_finish": "װען אַ פּעקל איז פֿאַרטיק",
    },
    "ar": {
        "group_appearance": "المظهر",
        "test": "اختبار",
        "btn_accept": "قبول",
        "label_deck_finish": "عند إنهاء مجموعة",
    },
    "fa": {
        "group_appearance": "ظاهر",
        "test": "آزمایش",
        "btn_accept": "تأیید",
        "label_deck_finish": "هنگام پایان یک دسته",
    },
    "ug": {
        "group_appearance": "كۆرۈنۈش",
        "test": "سىناش",
        "btn_accept": "قوبۇل قىلىش",
        "label_deck_finish": "بىر توپلام تاماملانغاندا",
    },
    "or": {
        "group_appearance": "ରୂପ",
        "test": "ପରୀକ୍ଷା",
        "btn_accept": "ଗ୍ରହଣ କରନ୍ତୁ",
        "label_deck_finish": "ଏକ ଡେକ୍ ଶେଷ ହେଲେ",
    },
    "th": {
        "group_appearance": "รูปลักษณ์",
        "test": "ทดสอบ",
        "btn_accept": "ยอมรับ",
        "label_deck_finish": "เมื่อจบสำรับ",
    },
    "vi": {
        "group_appearance": "Giao diện",
        "test": "Thử",
        "btn_accept": "Chấp nhận",
        "label_deck_finish": "Khi hoàn thành một bộ thẻ",
    },
    "ms": {
        "group_appearance": "Rupa",
        "test": "Uji",
        "btn_accept": "Terima",
        "label_deck_finish": "Apabila satu dek tamat",
    },
    "tl": {
        "group_appearance": "Hitsura",
        "test": "Subukan",
        "btn_accept": "Tanggapin",
        "label_deck_finish": "Kapag tapos na ang isang deck",
    },
    "ja": {
        "group_appearance": "外観",
        "test": "テスト",
        "btn_accept": "OK",
        "label_deck_finish": "デッキを終えたとき",
    },
    "zh_CN": {
        "group_appearance": "外观",
        "test": "测试",
        "btn_accept": "确定",
        "label_deck_finish": "完成一个牌组时",
    },
    "zh_TW": {
        "group_appearance": "外觀",
        "test": "測試",
        "btn_accept": "確定",
        "label_deck_finish": "完成一個牌組時",
    },
    "ko": {
        "group_appearance": "외관",
        "test": "테스트",
        "btn_accept": "확인",
        "label_deck_finish": "덱을 끝냈을 때",
    },
    "ga": {
        "group_appearance": "Cuma",
        "test": "Tástáil",
        "btn_accept": "Glac leis",
        "label_deck_finish": "Nuair a chríochnaítear deic",
    },
    "eo": {
        "group_appearance": "Aspekto",
        "test": "Testi",
        "btn_accept": "Akcepti",
        "label_deck_finish": "Kiam kartaro finiĝas",
    },
    "jbo": {
        "group_appearance": "tarmi",
        "test": "cipra",
        "btn_accept": "je'e",
        "label_deck_finish": "ca lo nu mo'u pa karda girzu",
    },
}


# Textos de la 2.5.0 (informe 2.4.0, aprobado entero el 2026-11-16): ventana de opciones en dos
# recuadros, «Sin sonido» en cada lista, nombres de los sonidos de serie y avisos de fallo que
# dicen qué dejó de funcionar. En los nueve idiomas completos; en los demás salen en inglés.
_UI_2_5: Final[dict[str, dict[str, str]]] = {
    "en": {
        "group_sound": "Sound",
        "sound_off": "No sound",
        "open_folder": "Open the folder for these sounds…",
        "label_on_correct": "When correct",
        "label_on_again": "When pressing «Again»",
        "label_deck_finish": "When a deck is finished",
        "label_day_finish": "When the day is finished",
        "test_correct": "Test the correct-answer sound",
        "test_again": "Test the «Again» sound",
        "test_deck_finish": "Test the deck-finished sound",
        "test_day_finish": "Test the day-finished sound",
        "preview": "Preview",
        "preview_confetti": "Preview the confetti",
        "play_failed": "The sound could not be played. Check the computer's audio output.",
        "styled_buttons": "Colorful buttons with relief",
        "flags_option": "Badges above the card",
        "confetti_option": "Confetti when finished",
        "voice_madera": "Wood",
        "voice_campanilla": "Bell",
        "voice_suave": "Soft",
        "error_generic": "ProFeedback ran into a problem. Anki keeps working. The details are in the add-on's log.",
        "error_badge": "ProFeedback could not show the badge. Anki keeps working. The details are in the add-on's log.",
        "error_buttons": "ProFeedback could not paint the buttons. Anki keeps working. The details are in the add-on's log.",
        "error_sound": "ProFeedback could not play the sound. Anki keeps working. The details are in the add-on's log.",
        "error_celebration": "ProFeedback could not celebrate the end. Anki keeps working. The details are in the add-on's log.",
    },
    "es": {
        "group_sound": "Sonido",
        "sound_off": "Sin sonido",
        "open_folder": "Abrir la carpeta de estos sonidos…",
        "label_on_correct": "Al acertar",
        "label_on_again": "Al pulsar «Otra vez»",
        "label_deck_finish": "Al terminar un mazo",
        "label_day_finish": "Al terminar el día",
        "test_correct": "Probar el sonido de acierto",
        "test_again": "Probar el sonido de «Otra vez»",
        "test_deck_finish": "Probar el sonido de fin de mazo",
        "test_day_finish": "Probar el sonido de fin del día",
        "preview": "Ver",
        "preview_confetti": "Ver el confeti",
        "play_failed": "No se pudo reproducir. Compruebe la salida de audio del equipo.",
        "styled_buttons": "Botones de colores con relieve",
        "flags_option": "Insignias sobre la tarjeta",
        "confetti_option": "Confeti al terminar",
        "voice_madera": "Madera",
        "voice_campanilla": "Campanilla",
        "voice_suave": "Suave",
        "error_generic": "ProFeedback tuvo un problema. Anki sigue funcionando. El detalle está en el registro del complemento.",
        "error_badge": "ProFeedback no pudo mostrar la insignia. Anki sigue funcionando. El detalle está en el registro del complemento.",
        "error_buttons": "ProFeedback no pudo pintar los botones. Anki sigue funcionando. El detalle está en el registro del complemento.",
        "error_sound": "ProFeedback no pudo reproducir el sonido. Anki sigue funcionando. El detalle está en el registro del complemento.",
        "error_celebration": "ProFeedback no pudo celebrar el final. Anki sigue funcionando. El detalle está en el registro del complemento.",
    },
    "pt_BR": {
        "group_sound": "Som",
        "sound_off": "Sem som",
        "open_folder": "Abrir a pasta destes sons…",
        "label_on_correct": "Ao acertar",
        "label_on_again": "Ao tocar em «De novo»",
        "label_deck_finish": "Ao terminar um baralho",
        "label_day_finish": "Ao terminar o dia",
        "test_correct": "Testar o som de acerto",
        "test_again": "Testar o som de «De novo»",
        "test_deck_finish": "Testar o som de fim de baralho",
        "test_day_finish": "Testar o som de fim do dia",
        "preview": "Ver",
        "preview_confetti": "Ver os confetes",
        "play_failed": "Não foi possível reproduzir. Verifique a saída de áudio do computador.",
        "styled_buttons": "Botões coloridos com relevo",
        "flags_option": "Emblemas sobre o cartão",
        "confetti_option": "Confete ao terminar",
        "voice_madera": "Madeira",
        "voice_campanilla": "Sininho",
        "voice_suave": "Suave",
        "error_generic": "O ProFeedback teve um problema. O Anki continua funcionando. Os detalhes estão no registro do complemento.",
        "error_badge": "O ProFeedback não conseguiu mostrar o emblema. O Anki continua funcionando. Os detalhes estão no registro do complemento.",
        "error_buttons": "O ProFeedback não conseguiu pintar os botões. O Anki continua funcionando. Os detalhes estão no registro do complemento.",
        "error_sound": "O ProFeedback não conseguiu reproduzir o som. O Anki continua funcionando. Os detalhes estão no registro do complemento.",
        "error_celebration": "O ProFeedback não conseguiu comemorar o final. O Anki continua funcionando. Os detalhes estão no registro do complemento.",
    },
    "pt_PT": {
        "group_sound": "Som",
        "sound_off": "Sem som",
        "open_folder": "Abrir a pasta destes sons…",
        "label_on_correct": "Ao acertar",
        "label_on_again": "Ao premir «Errei»",
        "label_deck_finish": "Ao terminar um baralho",
        "label_day_finish": "Ao terminar o dia",
        "test_correct": "Testar o som de acerto",
        "test_again": "Testar o som de «Errei»",
        "test_deck_finish": "Testar o som de fim de baralho",
        "test_day_finish": "Testar o som de fim do dia",
        "preview": "Ver",
        "preview_confetti": "Ver os confetes",
        "play_failed": "Não foi possível reproduzir. Verifique a saída de áudio do computador.",
        "styled_buttons": "Botões coloridos com relevo",
        "flags_option": "Emblemas sobre o cartão",
        "confetti_option": "Confetes ao terminar",
        "voice_madera": "Madeira",
        "voice_campanilla": "Campainha",
        "voice_suave": "Suave",
        "error_generic": "O ProFeedback teve um problema. O Anki continua a funcionar. Os detalhes estão no registo do complemento.",
        "error_badge": "O ProFeedback não conseguiu mostrar o emblema. O Anki continua a funcionar. Os detalhes estão no registo do complemento.",
        "error_buttons": "O ProFeedback não conseguiu pintar os botões. O Anki continua a funcionar. Os detalhes estão no registo do complemento.",
        "error_sound": "O ProFeedback não conseguiu reproduzir o som. O Anki continua a funcionar. Os detalhes estão no registo do complemento.",
        "error_celebration": "O ProFeedback não conseguiu celebrar o final. O Anki continua a funcionar. Os detalhes estão no registo do complemento.",
    },
    "ca": {
        "group_sound": "So",
        "sound_off": "Sense so",
        "open_folder": "Obre la carpeta d'aquests sons…",
        "label_on_correct": "En encertar",
        "label_on_again": "En prémer «Una altra vegada»",
        "label_deck_finish": "En acabar un mall",
        "label_day_finish": "En acabar el dia",
        "test_correct": "Prova el so d'encert",
        "test_again": "Prova el so d'«Una altra vegada»",
        "test_deck_finish": "Prova el so de final de mall",
        "test_day_finish": "Prova el so de final del dia",
        "preview": "Veure",
        "preview_confetti": "Veure el confeti",
        "play_failed": "No s'ha pogut reproduir. Comproveu la sortida d'àudio de l'equip.",
        "styled_buttons": "Botons de colors amb relleu",
        "flags_option": "Insígnies sobre la targeta",
        "confetti_option": "Confeti en acabar",
        "voice_madera": "Fusta",
        "voice_campanilla": "Campaneta",
        "voice_suave": "Suau",
        "error_generic": "ProFeedback ha tingut un problema. L'Anki continua funcionant. El detall és al registre del complement.",
        "error_badge": "ProFeedback no ha pogut mostrar la insígnia. L'Anki continua funcionant. El detall és al registre del complement.",
        "error_buttons": "ProFeedback no ha pogut pintar els botons. L'Anki continua funcionant. El detall és al registre del complement.",
        "error_sound": "ProFeedback no ha pogut reproduir el so. L'Anki continua funcionant. El detall és al registre del complement.",
        "error_celebration": "ProFeedback no ha pogut celebrar el final. L'Anki continua funcionant. El detall és al registre del complement.",
    },
    "gl": {
        "group_sound": "Son",
        "sound_off": "Sen son",
        "open_folder": "Abrir o cartafol destes sons…",
        "label_on_correct": "Ao acertar",
        "label_on_again": "Ao premer «Outra vez»",
        "label_deck_finish": "Ao rematar unha baralla",
        "label_day_finish": "Ao rematar o día",
        "test_correct": "Probar o son de acerto",
        "test_again": "Probar o son de «Outra vez»",
        "test_deck_finish": "Probar o son de fin de baralla",
        "test_day_finish": "Probar o son de fin do día",
        "preview": "Ver",
        "preview_confetti": "Ver o confeti",
        "play_failed": "Non se puido reproducir. Comprobe a saída de audio do equipo.",
        "styled_buttons": "Botóns de cores con relevo",
        "flags_option": "Insignias sobre a tarxeta",
        "confetti_option": "Confeti ao rematar",
        "voice_madera": "Madeira",
        "voice_campanilla": "Campaíña",
        "voice_suave": "Suave",
        "error_generic": "ProFeedback tivo un problema. Anki segue funcionando. O detalle está no rexistro do complemento.",
        "error_badge": "ProFeedback non puido amosar a insignia. Anki segue funcionando. O detalle está no rexistro do complemento.",
        "error_buttons": "ProFeedback non puido pintar os botóns. Anki segue funcionando. O detalle está no rexistro do complemento.",
        "error_sound": "ProFeedback non puido reproducir o son. Anki segue funcionando. O detalle está no rexistro do complemento.",
        "error_celebration": "ProFeedback non puido celebrar o final. Anki segue funcionando. O detalle está no rexistro do complemento.",
    },
    "fr": {
        "group_sound": "Son",
        "sound_off": "Aucun son",
        "open_folder": "Ouvrir le dossier de ces sons…",
        "label_on_correct": "Bonne réponse",
        "label_on_again": "En appuyant sur « À revoir »",
        "label_deck_finish": "À la fin d'un paquet",
        "label_day_finish": "À la fin de la journée",
        "test_correct": "Tester le son de bonne réponse",
        "test_again": "Tester le son de « À revoir »",
        "test_deck_finish": "Tester le son de fin de paquet",
        "test_day_finish": "Tester le son de fin de journée",
        "preview": "Voir",
        "preview_confetti": "Voir les confettis",
        "play_failed": "Lecture impossible. Vérifiez la sortie audio de l'ordinateur.",
        "styled_buttons": "Boutons colorés en relief",
        "flags_option": "Badges au-dessus de la carte",
        "confetti_option": "Confettis à la fin",
        "voice_madera": "Bois",
        "voice_campanilla": "Clochette",
        "voice_suave": "Doux",
        "error_generic": "ProFeedback a rencontré un problème. Anki continue de fonctionner. Le détail se trouve dans le journal du module.",
        "error_badge": "ProFeedback n'a pas pu afficher le badge. Anki continue de fonctionner. Le détail se trouve dans le journal du module.",
        "error_buttons": "ProFeedback n'a pas pu colorer les boutons. Anki continue de fonctionner. Le détail se trouve dans le journal du module.",
        "error_sound": "ProFeedback n'a pas pu jouer le son. Anki continue de fonctionner. Le détail se trouve dans le journal du module.",
        "error_celebration": "ProFeedback n'a pas pu célébrer la fin. Anki continue de fonctionner. Le détail se trouve dans le journal du module.",
    },
    "it": {
        "group_sound": "Suono",
        "sound_off": "Nessun suono",
        "open_folder": "Apri la cartella di questi suoni…",
        "label_on_correct": "Risposta giusta",
        "label_on_again": "Premendo «Ripeti»",
        "label_deck_finish": "Alla fine di un mazzo",
        "label_day_finish": "Alla fine della giornata",
        "test_correct": "Prova il suono di risposta giusta",
        "test_again": "Prova il suono di «Ripeti»",
        "test_deck_finish": "Prova il suono di fine mazzo",
        "test_day_finish": "Prova il suono di fine giornata",
        "preview": "Vedi",
        "preview_confetti": "Vedi i coriandoli",
        "play_failed": "Impossibile riprodurre. Controlla l'uscita audio del computer.",
        "styled_buttons": "Pulsanti colorati in rilievo",
        "flags_option": "Badge sopra la carta",
        "confetti_option": "Coriandoli alla fine",
        "voice_madera": "Legno",
        "voice_campanilla": "Campanella",
        "voice_suave": "Morbido",
        "error_generic": "ProFeedback ha avuto un problema. Anki continua a funzionare. Il dettaglio è nel registro del componente aggiuntivo.",
        "error_badge": "ProFeedback non è riuscito a mostrare il badge. Anki continua a funzionare. Il dettaglio è nel registro del componente aggiuntivo.",
        "error_buttons": "ProFeedback non è riuscito a colorare i pulsanti. Anki continua a funzionare. Il dettaglio è nel registro del componente aggiuntivo.",
        "error_sound": "ProFeedback non è riuscito a riprodurre il suono. Anki continua a funzionare. Il dettaglio è nel registro del componente aggiuntivo.",
        "error_celebration": "ProFeedback non è riuscito a festeggiare la fine. Anki continua a funzionare. Il dettaglio è nel registro del componente aggiuntivo.",
    },
    "de": {
        "group_sound": "Ton",
        "sound_off": "Kein Ton",
        "open_folder": "Ordner dieser Töne öffnen…",
        "label_on_correct": "Bei richtiger Antwort",
        "label_on_again": "Bei „Nochmal“",
        "label_deck_finish": "Am Ende eines Stapels",
        "label_day_finish": "Am Ende des Tages",
        "test_correct": "Ton für richtige Antwort testen",
        "test_again": "Ton für „Nochmal“ testen",
        "test_deck_finish": "Ton für Stapelende testen",
        "test_day_finish": "Ton für Tagesende testen",
        "preview": "Ansehen",
        "preview_confetti": "Konfetti ansehen",
        "play_failed": "Wiedergabe nicht möglich. Prüfen Sie die Audioausgabe des Computers.",
        "styled_buttons": "Farbige Schaltflächen mit Relief",
        "flags_option": "Abzeichen über der Karte",
        "confetti_option": "Konfetti am Ende",
        "voice_madera": "Holz",
        "voice_campanilla": "Glöckchen",
        "voice_suave": "Sanft",
        "error_generic": "ProFeedback hatte ein Problem. Anki läuft weiter. Die Details stehen im Protokoll des Add-ons.",
        "error_badge": "ProFeedback konnte das Abzeichen nicht anzeigen. Anki läuft weiter. Die Details stehen im Protokoll des Add-ons.",
        "error_buttons": "ProFeedback konnte die Schaltflächen nicht einfärben. Anki läuft weiter. Die Details stehen im Protokoll des Add-ons.",
        "error_sound": "ProFeedback konnte den Ton nicht abspielen. Anki läuft weiter. Die Details stehen im Protokoll des Add-ons.",
        "error_celebration": "ProFeedback konnte das Ende nicht feiern. Anki läuft weiter. Die Details stehen im Protokoll des Add-ons.",
    },
}
for _lang, _texts in _UI_2_5.items():
    _UI_STRINGS.setdefault(_lang, {}).update(_texts)


def _normalize(code: str) -> str:
    """Reduce el código de idioma de Anki a la clave usada en las tablas."""
    code = code.replace("-", "_").strip()
    if not code:
        return DEFAULT_LANG
    lower = code.lower()
    if lower.startswith("zh"):
        upper = code.upper()
        return "zh_TW" if any(t in upper for t in ("TW", "HK", "MO")) else "zh_CN"
    if lower.startswith("pt"):
        return "pt_BR" if "BR" in code.upper() else "pt_PT"
    if lower.startswith("jbo"):
        return "jbo"
    base = lower.split("_")[0]
    return _ALIASES.get(base, base)


_cache: dict[str, str] = {}


def current_lang() -> str:
    """Idioma en el que está la interfaz de Anki ahora mismo."""
    try:
        import anki.lang

        code = getattr(anki.lang, "current_lang", "") or ""
    except Exception:
        return DEFAULT_LANG
    cached = _cache.get(code)
    if cached is not None:
        return cached
    key = _normalize(code)
    if key not in _FLAG_STRINGS:
        key = DEFAULT_LANG
    _cache[code] = key
    return key


def flag_label(flag: FlagKey) -> str:
    entries = _FLAG_STRINGS.get(current_lang()) or _FLAG_STRINGS[DEFAULT_LANG]
    return entries.get(flag) or _FLAG_STRINGS[DEFAULT_LANG][flag]


def ui(key: UIKey) -> str:
    entries = _UI_STRINGS.get(current_lang()) or _UI_STRINGS[DEFAULT_LANG]
    return entries.get(key) or _UI_STRINGS[DEFAULT_LANG][key]


def voice_label(voice: str) -> str:
    """Nombre de una voz de los sonidos de serie («madera» → «Madera»)."""
    key = f"voice_{voice}"
    if key in _UI_STRINGS[DEFAULT_LANG]:
        return ui(key)  # type: ignore[arg-type]
    return voice.capitalize()
