"""Textos visibles del complemento, en todos los idiomas de Anki.

Los rotulos que Anki ya traduce (Aceptar, Cancelar, Restaurar los valores
predeterminados, el aviso al restaurar) no viven aqui: se piden a Anki o a Qt
en dialogs.py, para que coincidan siempre con el resto del programa.
"""

from __future__ import annotations

from functools import lru_cache

# Idioma de reserva cuando Anki corre en una lengua que no esta en la tabla.
FALLBACK: str = "en"

TRANSLATIONS: dict[str, dict[str, str]] = {
    "en": {"shortcut_prefix": "Shortcut:", "placeholder": "Press the keyboard shortcut", "on": "Always on top: enabled", "off": "Always on top: disabled", "shortcut_updated": "Keyboard shortcut updated", "conflict": "«{shortcut}» cannot be used. Choose a combination that includes Ctrl or Alt and that Anki does not already use.", "error": "Something went wrong"},
    "es": {"shortcut_prefix": "Atajo:", "placeholder": "Presione el atajo de teclado", "on": "Siempre visible: activado", "off": "Siempre visible: desactivado", "shortcut_updated": "Atajo de teclado actualizado", "conflict": "No se puede usar «{shortcut}». Elige una combinación que incluya Ctrl o Alt y que Anki no use ya.", "error": "Se produjo un problema"},
    "fr": {"shortcut_prefix": "Raccourci :", "placeholder": "Appuyez sur le raccourci clavier", "on": "Toujours au premier plan : activé", "off": "Toujours au premier plan : désactivé", "shortcut_updated": "Raccourci clavier mis à jour", "conflict": "« {shortcut} » ne peut pas être utilisé. Choisissez une combinaison qui contient Ctrl ou Alt et qu'Anki n'utilise pas déjà.", "error": "Un problème est survenu"},
    "de": {"shortcut_prefix": "Tastenkürzel:", "placeholder": "Drücken Sie die Tastenkombination", "on": "Immer im Vordergrund: aktiviert", "off": "Immer im Vordergrund: deaktiviert", "shortcut_updated": "Tastenkombination aktualisiert", "conflict": "„{shortcut}“ kann nicht verwendet werden. Wählen Sie eine Kombination mit Strg oder Alt, die Anki noch nicht verwendet.", "error": "Ein Problem ist aufgetreten"},
    "it": {"shortcut_prefix": "Scorciatoia:", "placeholder": "Premi la scorciatoia da tastiera", "on": "Sempre in primo piano: attivato", "off": "Sempre in primo piano: disattivato", "shortcut_updated": "Scorciatoia da tastiera aggiornata", "conflict": "«{shortcut}» non si può usare. Scegli una combinazione che includa Ctrl o Alt e che Anki non usi già.", "error": "Si è verificato un problema"},
    "pt_BR": {"shortcut_prefix": "Atalho:", "placeholder": "Pressione o atalho de teclado", "on": "Sempre visível: ativado", "off": "Sempre visível: desativado", "shortcut_updated": "Atalho de teclado atualizado", "conflict": "Não é possível usar «{shortcut}». Escolha uma combinação que inclua Ctrl ou Alt e que o Anki ainda não use.", "error": "Ocorreu um problema"},
    "pt_PT": {"shortcut_prefix": "Atalho:", "placeholder": "Prima o atalho de teclado", "on": "Sempre visível: ativado", "off": "Sempre visível: desativado", "shortcut_updated": "Atalho de teclado atualizado", "conflict": "Não é possível usar «{shortcut}». Escolha uma combinação que inclua Ctrl ou Alt e que o Anki ainda não use.", "error": "Ocorreu um problema"},
    "nl": {"shortcut_prefix": "Sneltoets:", "placeholder": "Druk op de sneltoets", "on": "Altijd op de voorgrond: ingeschakeld", "off": "Altijd op de voorgrond: uitgeschakeld", "shortcut_updated": "Sneltoets bijgewerkt", "conflict": "«{shortcut}» kan niet worden gebruikt. Kies een combinatie met Ctrl of Alt die Anki nog niet gebruikt.", "error": "Er is een probleem opgetreden"},
    "ca": {"shortcut_prefix": "Drecera:", "placeholder": "Premeu la drecera de teclat", "on": "Sempre visible: activat", "off": "Sempre visible: desactivat", "shortcut_updated": "Drecera de teclat actualitzada", "conflict": "No es pot fer servir «{shortcut}». Trieu una combinació que inclogui Ctrl o Alt i que l'Anki no faci servir ja.", "error": "S'ha produït un problema"},
    "gl": {"shortcut_prefix": "Atallo:", "placeholder": "Prema o atallo de teclado", "on": "Sempre visible: activado", "off": "Sempre visible: desactivado", "shortcut_updated": "Atallo de teclado actualizado", "conflict": "Non se pode usar «{shortcut}». Escolla unha combinación que inclúa Ctrl ou Alt e que Anki non use xa.", "error": "Produciuse un problema"},
    "ro": {"shortcut_prefix": "Comandă rapidă:", "placeholder": "Apăsați comanda rapidă de la tastatură", "on": "Mereu deasupra: activat", "off": "Mereu deasupra: dezactivat", "shortcut_updated": "Comanda rapidă a fost actualizată", "conflict": "«{shortcut}» nu poate fi folosită. Alegeți o combinație care include Ctrl sau Alt și pe care Anki nu o folosește deja.", "error": "A apărut o problemă"},
    "ru": {"shortcut_prefix": "Сочетание клавиш:", "placeholder": "Нажмите сочетание клавиш", "on": "Поверх окон: включено", "off": "Поверх окон: выключено", "shortcut_updated": "Сочетание клавиш обновлено", "conflict": "«{shortcut}» использовать нельзя. Выберите сочетание с Ctrl или Alt, которое Anki ещё не использует.", "error": "Произошла ошибка"},
    "uk": {"shortcut_prefix": "Комбінація клавіш:", "placeholder": "Натисніть комбінацію клавіш", "on": "Завжди зверху: увімкнено", "off": "Завжди зверху: вимкнено", "shortcut_updated": "Комбінацію клавіш оновлено", "conflict": "«{shortcut}» використати не можна. Виберіть комбінацію з Ctrl або Alt, яку Anki ще не використовує.", "error": "Сталася помилка"},
    "pl": {"shortcut_prefix": "Skrót:", "placeholder": "Naciśnij skrót klawiszowy", "on": "Zawsze na wierzchu: włączone", "off": "Zawsze na wierzchu: wyłączone", "shortcut_updated": "Skrót klawiszowy zaktualizowany", "conflict": "Nie można użyć «{shortcut}». Wybierz kombinację zawierającą Ctrl lub Alt, której Anki jeszcze nie używa.", "error": "Wystąpił problem"},
    "cs": {"shortcut_prefix": "Zkratka:", "placeholder": "Stiskněte klávesovou zkratku", "on": "Vždy navrchu: zapnuto", "off": "Vždy navrchu: vypnuto", "shortcut_updated": "Klávesová zkratka aktualizována", "conflict": "«{shortcut}» nelze použít. Zvolte kombinaci s Ctrl nebo Alt, kterou Anki zatím nepoužívá.", "error": "Došlo k chybě"},
    "sk": {"shortcut_prefix": "Skratka:", "placeholder": "Stlačte klávesovú skratku", "on": "Vždy navrchu: zapnuté", "off": "Vždy navrchu: vypnuté", "shortcut_updated": "Klávesová skratka aktualizovaná", "conflict": "«{shortcut}» sa nedá použiť. Zvoľte kombináciu s Ctrl alebo Alt, ktorú Anki zatiaľ nepoužíva.", "error": "Vyskytla sa chyba"},
    "sl": {"shortcut_prefix": "Bližnjica:", "placeholder": "Pritisnite bližnjico na tipkovnici", "on": "Vedno na vrhu: vklopljeno", "off": "Vedno na vrhu: izklopljeno", "shortcut_updated": "Bližnjica na tipkovnici posodobljena", "conflict": "«{shortcut}» ni mogoče uporabiti. Izberite kombinacijo s Ctrl ali Alt, ki je Anki še ne uporablja.", "error": "Prišlo je do napake"},
    "hr": {"shortcut_prefix": "Prečac:", "placeholder": "Pritisnite tipkovnički prečac", "on": "Uvijek na vrhu: uključeno", "off": "Uvijek na vrhu: isključeno", "shortcut_updated": "Tipkovnički prečac ažuriran", "conflict": "«{shortcut}» se ne može koristiti. Odaberite kombinaciju s Ctrl ili Alt koju Anki još ne koristi.", "error": "Došlo je do pogreške"},
    "sr": {"shortcut_prefix": "Пречица:", "placeholder": "Притисните пречицу на тастатури", "on": "Увек на врху: укључено", "off": "Увек на врху: искључено", "shortcut_updated": "Пречица на тастатури ажурирана", "conflict": "«{shortcut}» не може да се користи. Изаберите комбинацију са Ctrl или Alt коју Anki још не користи.", "error": "Дошло је до грешке"},
    "bg": {"shortcut_prefix": "Клавишна комбинация:", "placeholder": "Натиснете клавишната комбинация", "on": "Винаги отгоре: включено", "off": "Винаги отгоре: изключено", "shortcut_updated": "Клавишната комбинация е обновена", "conflict": "«{shortcut}» не може да се използва. Изберете комбинация с Ctrl или Alt, която Anki още не използва.", "error": "Възникна проблем"},
    "sv": {"shortcut_prefix": "Kortkommando:", "placeholder": "Tryck på kortkommandot", "on": "Alltid överst: på", "off": "Alltid överst: av", "shortcut_updated": "Kortkommando uppdaterat", "conflict": "«{shortcut}» kan inte användas. Välj en kombination med Ctrl eller Alt som Anki inte redan använder.", "error": "Ett problem uppstod"},
    "da": {"shortcut_prefix": "Genvej:", "placeholder": "Tryk på genvejstasten", "on": "Altid øverst: til", "off": "Altid øverst: fra", "shortcut_updated": "Genvejstast opdateret", "conflict": "«{shortcut}» kan ikke bruges. Vælg en kombination med Ctrl eller Alt, som Anki ikke allerede bruger.", "error": "Der opstod et problem"},
    "nb": {"shortcut_prefix": "Hurtigtast:", "placeholder": "Trykk på hurtigtasten", "on": "Alltid øverst: på", "off": "Alltid øverst: av", "shortcut_updated": "Hurtigtast oppdatert", "conflict": "«{shortcut}» kan ikke brukes. Velg en kombinasjon med Ctrl eller Alt som Anki ikke allerede bruker.", "error": "Det oppstod et problem"},
    "fi": {"shortcut_prefix": "Pikanäppäin:", "placeholder": "Paina pikanäppäintä", "on": "Aina päällimmäisenä: käytössä", "off": "Aina päällimmäisenä: pois käytöstä", "shortcut_updated": "Pikanäppäin päivitetty", "conflict": "«{shortcut}» ei voi käyttää. Valitse yhdistelmä, jossa on Ctrl tai Alt ja jota Anki ei jo käytä.", "error": "Tapahtui virhe"},
    "et": {"shortcut_prefix": "Kiirklahv:", "placeholder": "Vajutage kiirklahvi", "on": "Alati pealmine: sees", "off": "Alati pealmine: väljas", "shortcut_updated": "Kiirklahv uuendatud", "conflict": "«{shortcut}» ei saa kasutada. Valige kombinatsioon, milles on Ctrl või Alt ja mida Anki juba ei kasuta.", "error": "Ilmnes probleem"},
    "lt": {"shortcut_prefix": "Spartusis klavišas:", "placeholder": "Paspauskite spartųjį klavišą", "on": "Visada viršuje: įjungta", "off": "Visada viršuje: išjungta", "shortcut_updated": "Spartusis klavišas atnaujintas", "conflict": "«{shortcut}» naudoti negalima. Pasirinkite derinį su Ctrl arba Alt, kurio Anki dar nenaudoja.", "error": "Įvyko klaida"},
    "lv": {"shortcut_prefix": "Īsinājumtaustiņš:", "placeholder": "Nospiediet īsinājumtaustiņu", "on": "Vienmēr virspusē: ieslēgts", "off": "Vienmēr virspusē: izslēgts", "shortcut_updated": "Īsinājumtaustiņš atjaunināts", "conflict": "«{shortcut}» nevar izmantot. Izvēlieties kombināciju ar Ctrl vai Alt, kuru Anki vēl neizmanto.", "error": "Radās kļūda"},
    "hu": {"shortcut_prefix": "Billentyűparancs:", "placeholder": "Nyomja meg a billentyűparancsot", "on": "Mindig felül: bekapcsolva", "off": "Mindig felül: kikapcsolva", "shortcut_updated": "Billentyűparancs frissítve", "conflict": "A(z) «{shortcut}» nem használható. Válasszon Ctrl vagy Alt billentyűt tartalmazó kombinációt, amelyet az Anki még nem használ.", "error": "Hiba történt"},
    "el": {"shortcut_prefix": "Συντόμευση:", "placeholder": "Πατήστε τη συντόμευση πληκτρολογίου", "on": "Πάντα σε πρώτο πλάνο: ενεργό", "off": "Πάντα σε πρώτο πλάνο: ανενεργό", "shortcut_updated": "Η συντόμευση πληκτρολογίου ενημερώθηκε", "conflict": "Το «{shortcut}» δεν μπορεί να χρησιμοποιηθεί. Επιλέξτε συνδυασμό με Ctrl ή Alt που δεν χρησιμοποιεί ήδη το Anki.", "error": "Παρουσιάστηκε πρόβλημα"},
    "tr": {"shortcut_prefix": "Kısayol:", "placeholder": "Klavye kısayoluna basın", "on": "Her zaman üstte: açık", "off": "Her zaman üstte: kapalı", "shortcut_updated": "Klavye kısayolu güncellendi", "conflict": "«{shortcut}» kullanılamaz. Ctrl veya Alt içeren ve Anki'nin henüz kullanmadığı bir kombinasyon seçin.", "error": "Bir sorun oluştu"},
    "ar": {"shortcut_prefix": "الاختصار:", "placeholder": "اضغط اختصار لوحة المفاتيح", "on": "البقاء في المقدمة: مفعّل", "off": "البقاء في المقدمة: معطّل", "shortcut_updated": "تم تحديث اختصار لوحة المفاتيح", "conflict": "لا يمكن استخدام «{shortcut}». اختر تركيبة تتضمن Ctrl أو Alt ولا يستخدمها Anki بالفعل.", "error": "حدثت مشكلة"},
    "he": {"shortcut_prefix": "קיצור דרך:", "placeholder": "הקש על קיצור המקלדת", "on": "תמיד למעלה: פעיל", "off": "תמיד למעלה: כבוי", "shortcut_updated": "קיצור המקלדת עודכן", "conflict": "לא ניתן להשתמש ב-«{shortcut}». בחר צירוף הכולל Ctrl או Alt שאנקי אינו משתמש בו כבר.", "error": "אירעה תקלה"},
    "fa": {"shortcut_prefix": "میانبر:", "placeholder": "میانبر صفحه‌کلید را فشار دهید", "on": "همیشه در بالا: فعال", "off": "همیشه در بالا: غیرفعال", "shortcut_updated": "میانبر صفحه‌کلید به‌روزرسانی شد", "conflict": "«{shortcut}» قابل استفاده نیست. ترکیبی شامل Ctrl یا Alt انتخاب کنید که Anki از آن استفاده نکند.", "error": "مشکلی پیش آمد"},
    "hi": {"shortcut_prefix": "शॉर्टकट:", "placeholder": "कीबोर्ड शॉर्टकट दबाएँ", "on": "हमेशा ऊपर: चालू", "off": "हमेशा ऊपर: बंद", "shortcut_updated": "कीबोर्ड शॉर्टकट अपडेट किया गया", "conflict": "«{shortcut}» का उपयोग नहीं किया जा सकता। ऐसा संयोजन चुनें जिसमें Ctrl या Alt हो और जिसे Anki पहले से उपयोग न करता हो।", "error": "कोई समस्या हुई"},
    "th": {"shortcut_prefix": "ปุ่มลัด:", "placeholder": "กดปุ่มลัดบนแป้นพิมพ์", "on": "ปักหมุดอยู่บนสุด: เปิด", "off": "ปักหมุดอยู่บนสุด: ปิด", "shortcut_updated": "อัปเดตปุ่มลัดแล้ว", "conflict": "ใช้ «{shortcut}» ไม่ได้ เลือกชุดปุ่มที่มี Ctrl หรือ Alt และที่ Anki ยังไม่ได้ใช้", "error": "เกิดข้อผิดพลาด"},
    "vi": {"shortcut_prefix": "Phím tắt:", "placeholder": "Nhấn phím tắt", "on": "Luôn ở trên cùng: bật", "off": "Luôn ở trên cùng: tắt", "shortcut_updated": "Đã cập nhật phím tắt", "conflict": "Không thể dùng «{shortcut}». Hãy chọn tổ hợp có Ctrl hoặc Alt và Anki chưa dùng.", "error": "Đã xảy ra sự cố"},
    "id": {"shortcut_prefix": "Pintasan:", "placeholder": "Tekan pintasan papan ketik", "on": "Selalu di atas: aktif", "off": "Selalu di atas: nonaktif", "shortcut_updated": "Pintasan papan ketik diperbarui", "conflict": "«{shortcut}» tidak dapat digunakan. Pilih kombinasi yang memuat Ctrl atau Alt dan yang belum dipakai Anki.", "error": "Terjadi masalah"},
    "ms": {"shortcut_prefix": "Pintasan:", "placeholder": "Tekan pintasan papan kekunci", "on": "Sentiasa di atas: dihidupkan", "off": "Sentiasa di atas: dimatikan", "shortcut_updated": "Pintasan papan kekunci dikemas kini", "conflict": "«{shortcut}» tidak boleh digunakan. Pilih gabungan yang mengandungi Ctrl atau Alt dan yang belum digunakan Anki.", "error": "Berlaku masalah"},
    "ja": {"shortcut_prefix": "ショートカット:", "placeholder": "キーボードショートカットを押してください", "on": "常に最前面: 有効", "off": "常に最前面: 無効", "shortcut_updated": "キーボードショートカットを更新しました", "conflict": "「{shortcut}」は使用できません。Ctrl または Alt を含み、Anki がまだ使っていない組み合わせを選んでください。", "error": "問題が発生しました"},
    "ko": {"shortcut_prefix": "단축키:", "placeholder": "단축키를 누르세요", "on": "항상 위에 표시: 켜짐", "off": "항상 위에 표시: 꺼짐", "shortcut_updated": "단축키가 업데이트되었습니다", "conflict": "「{shortcut}」은(는) 사용할 수 없습니다. Ctrl 또는 Alt를 포함하고 Anki가 아직 쓰지 않는 조합을 선택하세요.", "error": "문제가 발생했습니다"},
    "zh_CN": {"shortcut_prefix": "快捷键：", "placeholder": "请按下快捷键", "on": "始终置顶：已开启", "off": "始终置顶：已关闭", "shortcut_updated": "快捷键已更新", "conflict": "无法使用「{shortcut}」。请选择包含 Ctrl 或 Alt 且 Anki 尚未使用的组合。", "error": "发生了问题"},
    "zh_TW": {"shortcut_prefix": "快捷鍵：", "placeholder": "請按下快捷鍵", "on": "永遠置頂：已開啟", "off": "永遠置頂：已關閉", "shortcut_updated": "快捷鍵已更新", "conflict": "無法使用「{shortcut}」。請選擇包含 Ctrl 或 Alt 且 Anki 尚未使用的組合。", "error": "發生了問題"},
    "eo": {"shortcut_prefix": "Klavkombino:", "placeholder": "Premu la klavkombinon", "on": "Ĉiam supre: ŝaltita", "off": "Ĉiam supre: malŝaltita", "shortcut_updated": "Klavkombino ĝisdatigita", "conflict": "«{shortcut}» ne uzeblas. Elektu kombinon kun Ctrl aŭ Alt, kiun Anki ankoraŭ ne uzas.", "error": "Okazis problemo"},
    "af": {"shortcut_prefix": "Kortpad:", "placeholder": "Druk die sleutelbordkortpad", "on": "Altyd bo-op: aan", "off": "Altyd bo-op: af", "shortcut_updated": "Sleutelbordkortpad opgedateer", "conflict": "«{shortcut}» kan nie gebruik word nie. Kies 'n kombinasie met Ctrl of Alt wat Anki nog nie gebruik nie.", "error": "Iets het verkeerd geloop"},
    "be": {"shortcut_prefix": "Спалучэнне клавіш:", "placeholder": "Націсніце спалучэнне клавіш", "on": "Заўсёды зверху: уключана", "off": "Заўсёды зверху: выключана", "shortcut_updated": "Спалучэнне клавіш абноўлена", "conflict": "«{shortcut}» выкарыстаць нельга. Абярыце спалучэнне з Ctrl або Alt, якое Anki яшчэ не выкарыстоўвае.", "error": "Узнікла памылка"},
    "eu": {"shortcut_prefix": "Lasterbidea:", "placeholder": "Sakatu teklatu-lasterbidea", "on": "Beti gainean: aktibatuta", "off": "Beti gainean: desaktibatuta", "shortcut_updated": "Teklatu-lasterbidea eguneratuta", "conflict": "«{shortcut}» ezin da erabili. Aukeratu Ctrl edo Alt duen konbinazio bat, Ankik erabiltzen ez duena.", "error": "Arazo bat gertatu da"},
    "ga": {"shortcut_prefix": "Aicearra:", "placeholder": "Brúigh an t-aicearra méarchláir", "on": "I gcónaí ar bharr: ar siúl", "off": "I gcónaí ar bharr: as", "shortcut_updated": "Aicearra méarchláir nuashonraithe", "conflict": "Ní féidir «{shortcut}» a úsáid. Roghnaigh teaglaim ina bhfuil Ctrl nó Alt agus nach n-úsáideann Anki cheana.", "error": "Tharla fadhb"},
    "hy": {"shortcut_prefix": "Դյուրանցում.", "placeholder": "Սեղմեք ստեղնաշարի դյուրանցումը", "on": "Միշտ վերևում. միացված", "off": "Միշտ վերևում. անջատված", "shortcut_updated": "Ստեղնաշարի դյուրանցումը թարմացվել է", "conflict": "«{shortcut}»-ը հնարավոր չէ օգտագործել։ Ընտրեք Ctrl կամ Alt պարունակող համակցություն, որը Anki-ն դեռ չի օգտագործում։", "error": "Խնդիր առաջացավ"},
    "jbo": {"shortcut_prefix": "lerpinsle:", "placeholder": "ko danre lo lerpinsle", "on": "ca'o gapru: cnino", "off": "ca'o gapru: nalcnino", "shortcut_updated": "lerpinsle basti", "conflict": "lo «{shortcut}» na se pilno. ko cuxna lo lerpinsle poi vasru la ctrl. ja la alt. gi'e na se pilno la .ankis.", "error": "da na snada"},
    "kk": {"shortcut_prefix": "Тіркесім:", "placeholder": "Пернетақта тіркесімін басыңыз", "on": "Әрқашан үстінде: қосулы", "off": "Әрқашан үстінде: өшірулі", "shortcut_updated": "Пернетақта тіркесімі жаңартылды", "conflict": "«{shortcut}» пайдалану мүмкін емес. Құрамында Ctrl немесе Alt бар және Anki әлі қолданбайтын тіркесімді таңдаңыз.", "error": "Қате орын алды"},
    "la": {"shortcut_prefix": "Compendium:", "placeholder": "Preme compendium claviaturae", "on": "Semper supra: activum", "off": "Semper supra: inactivum", "shortcut_updated": "Compendium claviaturae renovatum", "conflict": "«{shortcut}» adhiberi non potest. Elige coniunctionem quae Ctrl vel Alt contineat quaque Anki iam non utitur.", "error": "Problema accidit"},
    "mn": {"shortcut_prefix": "Товчлол:", "placeholder": "Товчлолыг дарна уу", "on": "Үргэлж дээр: асаалттай", "off": "Үргэлж дээр: унтраалттай", "shortcut_updated": "Товчлол шинэчлэгдлээ", "conflict": "«{shortcut}»-ыг ашиглах боломжгүй. Ctrl эсвэл Alt агуулсан, Anki хараахан ашиглаагүй хослолыг сонгоно уу.", "error": "Алдаа гарлаа"},
    "my": {"shortcut_prefix": "ဖြတ်လမ်း:", "placeholder": "ကီးဘုတ်ဖြတ်လမ်းကို နှိပ်ပါ", "on": "အမြဲအပေါ်တွင်: ဖွင့်ထားသည်", "off": "အမြဲအပေါ်တွင်: ပိတ်ထားသည်", "shortcut_updated": "ကီးဘုတ်ဖြတ်လမ်း အပ်ဒိတ်လုပ်ပြီးပါပြီ", "conflict": "«{shortcut}» ကို အသုံးမပြုနိုင်ပါ။ Ctrl သို့မဟုတ် Alt ပါဝင်ပြီး Anki မသုံးသေးသော ပေါင်းစပ်မှုကို ရွေးပါ။", "error": "ပြဿနာတစ်ခု ဖြစ်ပွားခဲ့သည်"},
    "oc": {"shortcut_prefix": "Acorchi :", "placeholder": "Quichatz l'acorchi de clavièr", "on": "Totjorn amont : activat", "off": "Totjorn amont : desactivat", "shortcut_updated": "Acorchi de clavièr actualizat", "conflict": "Se pòt pas utilizar «{shortcut}». Causissètz una combinason que conten Ctrl o Alt e qu'Anki utiliza pas ja.", "error": "Un problèma s'es produch"},
    "or": {"shortcut_prefix": "ସର୍ଟକଟ୍:", "placeholder": "କୀବୋର୍ଡ ସର୍ଟକଟ୍ ଦବାନ୍ତୁ", "on": "ସର୍ବଦା ଉପରେ: ଚାଲୁ", "off": "ସର୍ବଦା ଉପରେ: ବନ୍ଦ", "shortcut_updated": "କୀବୋର୍ଡ ସର୍ଟକଟ୍ ଅପଡେଟ୍ ହୋଇଛି", "conflict": "«{shortcut}» ବ୍ୟବହାର କରାଯାଇପାରିବ ନାହିଁ। Ctrl କିମ୍ବା Alt ଥିବା ଏବଂ Anki ପୂର୍ବରୁ ବ୍ୟବହାର କରୁନଥିବା ଏକ ସଂଯୋଗ ବାଛନ୍ତୁ।", "error": "ଏକ ସମସ୍ୟା ଘଟିଛି"},
    "sq": {"shortcut_prefix": "Shkurtore:", "placeholder": "Shtypni shkurtoren e tastierës", "on": "Gjithmonë sipër: aktivizuar", "off": "Gjithmonë sipër: çaktivizuar", "shortcut_updated": "Shkurtorja e tastierës u përditësua", "conflict": "«{shortcut}» nuk mund të përdoret. Zgjidhni një kombinim që përmban Ctrl ose Alt dhe që Anki nuk e përdor tashmë.", "error": "Ndodhi një problem"},
    "ug": {"shortcut_prefix": "تېزلەتمە:", "placeholder": "كۇنۇپكا تېزلەتمىسىنى بېسىڭ", "on": "ھەمىشە ئۈستىدە: ئوچۇق", "off": "ھەمىشە ئۈستىدە: تاقاق", "shortcut_updated": "كۇنۇپكا تېزلەتمىسى يېڭىلاندى", "conflict": "«{shortcut}» نى ئىشلەتكىلى بولمايدۇ. Ctrl ياكى Alt بار، Anki تېخى ئىشلەتمىگەن بىرىكمىنى تاللاڭ.", "error": "مەسىلە كۆرۈلدى"},
    "uz": {"shortcut_prefix": "Yorliq:", "placeholder": "Klaviatura yorlig'ini bosing", "on": "Doim tepada: yoqilgan", "off": "Doim tepada: o'chirilgan", "shortcut_updated": "Klaviatura yorlig'i yangilandi", "conflict": "«{shortcut}» dan foydalanib bo'lmaydi. Tarkibida Ctrl yoki Alt bo'lgan va Anki hali ishlatmayotgan birikmani tanlang.", "error": "Muammo yuz berdi"},
    "yi": {"shortcut_prefix": "אָפּקירצונג:", "placeholder": "דריקט די קלאַוויאַטור־אָפּקירצונג", "on": "שטענדיק אויבן: אָנגעצונדן", "off": "שטענדיק אויבן: אויסגעלאָשן", "shortcut_updated": "די קלאַוויאַטור־אָפּקירצונג איז דערהיינטיקט", "conflict": "מען קען נישט נוצן «{shortcut}». קלייבט אויס אַ קאָמבינאַציע מיט Ctrl אָדער Alt וואָס Anki נוצט נאָך נישט.", "error": "עס איז געשען אַ פּראָבלעם"},
    "fil": {"shortcut_prefix": "Shortcut:", "placeholder": "Pindutin ang keyboard shortcut", "on": "Laging nasa ibabaw: naka-on", "off": "Laging nasa ibabaw: naka-off", "shortcut_updated": "Na-update ang shortcut sa keyboard", "conflict": "Hindi magagamit ang «{shortcut}». Pumili ng kombinasyong may Ctrl o Alt at hindi pa ginagamit ng Anki.", "error": "May naganap na problema"},
}


@lru_cache(maxsize=16)
def _resolve(code: str) -> str:
    code = code.replace("-", "_")
    parts = code.split("_")
    primary = parts[0].lower()
    region = parts[1].upper() if len(parts) > 1 else ""
    if primary == "zh":
        return "zh_TW" if region in ("TW", "HK", "MO") or "HANT" in code.upper() else "zh_CN"
    if primary == "pt":
        return "pt_PT" if region == "PT" else "pt_BR"
    if primary in ("fil", "tl"):
        return "fil"
    return primary if primary in TRANSLATIONS else FALLBACK


def current_lang() -> str:
    """Idioma activo de Anki, leido en cada consulta.

    No se guarda en cache: quien cambia el idioma en las preferencias de Anki
    debe ver los textos del complemento en el idioma nuevo sin reiniciar.
    """
    try:
        import anki.lang

        raw = getattr(anki.lang, "current_lang", "")
        return _resolve(raw if isinstance(raw, str) else "")
    except Exception:
        return FALLBACK


def tr(key: str, **values: str) -> str:
    table = TRANSLATIONS.get(current_lang(), TRANSLATIONS[FALLBACK])
    value = table.get(key)
    if value is None:
        value = TRANSLATIONS[FALLBACK].get(key, key)
    if not values:
        return value
    try:
        return value.format(**values)
    except (KeyError, IndexError):
        return value
