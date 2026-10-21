"""Todos los textos propios del complemento, en un solo sitio.

Se muestran en el idioma de la interfaz de Anki. El inglés es la base
universal (Anki siempre lo tiene) y sirve de reserva para cualquier idioma
o clave que no esté traducida aquí; encima se añaden los demás idiomas de
Anki. Así el usuario ve los avisos en su propio idioma, y quien tenga un
idioma no incluido ve un inglés claro en vez de un texto en otro idioma.

Nota: aquí solo van los textos que ve el usuario y que Anki no tiene ya
traducidos. Los botones del panel (Aceptar / Cancelar) son botones estándar
de Qt que Anki traduce solo, y el título es el nombre del complemento (que no
se traduce), así que ninguno de esos aparece en esta tabla.
"""

from __future__ import annotations

# Idioma de reserva: siempre presente y con todas las claves.
BASE_LANGUAGE: str = "en"

STRINGS: dict[str, dict[str, str]] = {
    "en": {
        "save_failed": "Couldn't save the change: {error}",
        "field_missing": "The field “{field}” no longer exists. The change was not saved.",
        "note_missing": "The note no longer exists. The change was not saved.",
        "bad_message": "The editor sent a command that wasn't understood. The change was not saved.",
        "render_failed": "The change was saved, but the card couldn't be redrawn.",
        "opt_require_modifier": "Require Ctrl + click to start editing (⌘ on Mac)",
    },
    "es": {
        "save_failed": "No se pudo guardar el cambio: {error}",
        "field_missing": "El campo «{field}» ya no existe. El cambio no se ha guardado.",
        "note_missing": "La nota ya no existe. El cambio no se ha guardado.",
        "bad_message": "El editor envió una orden que no se entiende. El cambio no se ha guardado.",
        "render_failed": "El cambio se ha guardado, pero no se pudo redibujar la tarjeta.",
        "opt_require_modifier": "Exigir Ctrl + clic para empezar a editar (⌘ en Mac)",
    },
    "fr": {
        "save_failed": "Impossible d'enregistrer la modification : {error}",
        "field_missing": "Le champ « {field} » n'existe plus. La modification n'a pas été enregistrée.",
        "note_missing": "La note n'existe plus. La modification n'a pas été enregistrée.",
        "bad_message": "L'éditeur a envoyé une commande incompréhensible. La modification n'a pas été enregistrée.",
        "render_failed": "La modification a été enregistrée, mais la carte n'a pas pu être réaffichée.",
        "opt_require_modifier": "Exiger Ctrl + clic pour commencer à modifier (⌘ sur Mac)",
    },
    "de": {
        "save_failed": "Die Änderung konnte nicht gespeichert werden: {error}",
        "field_missing": "Das Feld „{field}“ existiert nicht mehr. Die Änderung wurde nicht gespeichert.",
        "note_missing": "Die Notiz existiert nicht mehr. Die Änderung wurde nicht gespeichert.",
        "bad_message": "Der Editor hat einen unverständlichen Befehl gesendet. Die Änderung wurde nicht gespeichert.",
        "render_failed": "Die Änderung wurde gespeichert, aber die Karte konnte nicht neu dargestellt werden.",
        "opt_require_modifier": "Strg + Klick zum Bearbeiten erforderlich (⌘ auf dem Mac)",
    },
    "it": {
        "save_failed": "Impossibile salvare la modifica: {error}",
        "field_missing": "Il campo «{field}» non esiste più. La modifica non è stata salvata.",
        "note_missing": "La nota non esiste più. La modifica non è stata salvata.",
        "bad_message": "L'editor ha inviato un comando incomprensibile. La modifica non è stata salvata.",
        "render_failed": "La modifica è stata salvata, ma non è stato possibile ridisegnare la carta.",
        "opt_require_modifier": "Richiedi Ctrl + clic per iniziare a modificare (⌘ su Mac)",
    },
    "pt": {
        "save_failed": "Não foi possível salvar a alteração: {error}",
        "field_missing": "O campo «{field}» não existe mais. A alteração não foi salva.",
        "note_missing": "A nota não existe mais. A alteração não foi salva.",
        "bad_message": "O editor enviou um comando que não foi compreendido. A alteração não foi salva.",
        "render_failed": "A alteração foi salva, mas não foi possível redesenhar o cartão.",
        "opt_require_modifier": "Exigir Ctrl + clique para começar a editar (⌘ no Mac)",
    },
    "nl": {
        "save_failed": "Kan de wijziging niet opslaan: {error}",
        "field_missing": "Het veld “{field}” bestaat niet meer. De wijziging is niet opgeslagen.",
        "note_missing": "De notitie bestaat niet meer. De wijziging is niet opgeslagen.",
        "bad_message": "De editor stuurde een onbegrijpelijk commando. De wijziging is niet opgeslagen.",
        "render_failed": "De wijziging is opgeslagen, maar de kaart kon niet opnieuw worden getekend.",
        "opt_require_modifier": "Ctrl + klik vereisen om te beginnen met bewerken (⌘ op Mac)",
    },
    "sv": {
        "save_failed": "Det gick inte att spara ändringen: {error}",
        "field_missing": "Fältet ”{field}” finns inte längre. Ändringen sparades inte.",
        "note_missing": "Anteckningen finns inte längre. Ändringen sparades inte.",
        "bad_message": "Redigeraren skickade ett kommando som inte kunde tolkas. Ändringen sparades inte.",
        "render_failed": "Ändringen sparades, men kortet kunde inte ritas om.",
        "opt_require_modifier": "Kräv Ctrl + klick för att börja redigera (⌘ på Mac)",
    },
    "da": {
        "save_failed": "Ændringen kunne ikke gemmes: {error}",
        "field_missing": "Feltet “{field}” findes ikke længere. Ændringen blev ikke gemt.",
        "note_missing": "Noten findes ikke længere. Ændringen blev ikke gemt.",
        "bad_message": "Editoren sendte en kommando, der ikke kunne forstås. Ændringen blev ikke gemt.",
        "render_failed": "Ændringen blev gemt, men kortet kunne ikke gentegnes.",
        "opt_require_modifier": "Kræv Ctrl + klik for at begynde at redigere (⌘ på Mac)",
    },
    "nb": {
        "save_failed": "Kunne ikke lagre endringen: {error}",
        "field_missing": "Feltet «{field}» finnes ikke lenger. Endringen ble ikke lagret.",
        "note_missing": "Notatet finnes ikke lenger. Endringen ble ikke lagret.",
        "bad_message": "Editoren sendte en kommando som ikke kunne forstås. Endringen ble ikke lagret.",
        "render_failed": "Endringen ble lagret, men kortet kunne ikke tegnes på nytt.",
        "opt_require_modifier": "Krev Ctrl + klikk for å begynne å redigere (⌘ på Mac)",
    },
    "fi": {
        "save_failed": "Muutosta ei voitu tallentaa: {error}",
        "field_missing": "Kenttää ”{field}” ei ole enää olemassa. Muutosta ei tallennettu.",
        "note_missing": "Muistiinpanoa ei ole enää olemassa. Muutosta ei tallennettu.",
        "bad_message": "Editori lähetti komennon, jota ei ymmärretty. Muutosta ei tallennettu.",
        "render_failed": "Muutos tallennettiin, mutta korttia ei voitu piirtää uudelleen.",
        "opt_require_modifier": "Vaadi Ctrl + napsautus muokkauksen aloittamiseen (⌘ Macissa)",
    },
    "pl": {
        "save_failed": "Nie udało się zapisać zmiany: {error}",
        "field_missing": "Pole „{field}” już nie istnieje. Zmiana nie została zapisana.",
        "note_missing": "Notatka już nie istnieje. Zmiana nie została zapisana.",
        "bad_message": "Edytor wysłał niezrozumiałe polecenie. Zmiana nie została zapisana.",
        "render_failed": "Zmiana została zapisana, ale nie udało się ponownie narysować karty.",
        "opt_require_modifier": "Wymagaj Ctrl + kliknięcie, aby rozpocząć edycję (⌘ na Macu)",
    },
    "cs": {
        "save_failed": "Změnu se nepodařilo uložit: {error}",
        "field_missing": "Pole „{field}“ již neexistuje. Změna nebyla uložena.",
        "note_missing": "Poznámka již neexistuje. Změna nebyla uložena.",
        "bad_message": "Editor odeslal příkaz, kterému nebylo možné porozumět. Změna nebyla uložena.",
        "render_failed": "Změna byla uložena, ale kartu se nepodařilo znovu vykreslit.",
        "opt_require_modifier": "Vyžadovat Ctrl + kliknutí pro zahájení úprav (⌘ na Macu)",
    },
    "sk": {
        "save_failed": "Zmenu sa nepodarilo uložiť: {error}",
        "field_missing": "Pole „{field}“ už neexistuje. Zmena nebola uložená.",
        "note_missing": "Poznámka už neexistuje. Zmena nebola uložená.",
        "bad_message": "Editor odoslal príkaz, ktorému nebolo možné porozumieť. Zmena nebola uložená.",
        "render_failed": "Zmena bola uložená, ale kartu sa nepodarilo znova vykresliť.",
        "opt_require_modifier": "Vyžadovať Ctrl + kliknutie na začatie úprav (⌘ na Macu)",
    },
    "sl": {
        "save_failed": "Spremembe ni bilo mogoče shraniti: {error}",
        "field_missing": "Polje »{field}« ne obstaja več. Sprememba ni bila shranjena.",
        "note_missing": "Zapisek ne obstaja več. Sprememba ni bila shranjena.",
        "bad_message": "Urejevalnik je poslal ukaz, ki ga ni bilo mogoče razumeti. Sprememba ni bila shranjena.",
        "render_failed": "Sprememba je bila shranjena, vendar kartice ni bilo mogoče znova izrisati.",
        "opt_require_modifier": "Zahtevaj Ctrl + klik za začetek urejanja (⌘ na Macu)",
    },
    "hr": {
        "save_failed": "Promjenu nije moguće spremiti: {error}",
        "field_missing": "Polje „{field}” više ne postoji. Promjena nije spremljena.",
        "note_missing": "Bilješka više ne postoji. Promjena nije spremljena.",
        "bad_message": "Uređivač je poslao naredbu koju nije moguće razumjeti. Promjena nije spremljena.",
        "render_failed": "Promjena je spremljena, ali karticu nije moguće ponovno iscrtati.",
        "opt_require_modifier": "Zahtijevaj Ctrl + klik za početak uređivanja (⌘ na Macu)",
    },
    "sr": {
        "save_failed": "Није могуће сачувати измену: {error}",
        "field_missing": "Поље „{field}” више не постоји. Измена није сачувана.",
        "note_missing": "Белешка више не постоји. Измена није сачувана.",
        "bad_message": "Уређивач је послао команду која није разумљива. Измена није сачувана.",
        "render_failed": "Измена је сачувана, али картицу није могуће поново исцртати.",
        "opt_require_modifier": "Захтевај Ctrl + клик за почетак уређивања (⌘ на Мек-у)",
    },
    "ro": {
        "save_failed": "Modificarea nu a putut fi salvată: {error}",
        "field_missing": "Câmpul „{field}” nu mai există. Modificarea nu a fost salvată.",
        "note_missing": "Nota nu mai există. Modificarea nu a fost salvată.",
        "bad_message": "Editorul a trimis o comandă care nu a putut fi înțeleasă. Modificarea nu a fost salvată.",
        "render_failed": "Modificarea a fost salvată, dar cardul nu a putut fi redesenat.",
        "opt_require_modifier": "Necesită Ctrl + clic pentru a începe editarea (⌘ pe Mac)",
    },
    "hu": {
        "save_failed": "A módosítást nem sikerült menteni: {error}",
        "field_missing": "A(z) „{field}” mező már nem létezik. A módosítás nem lett elmentve.",
        "note_missing": "A jegyzet már nem létezik. A módosítás nem lett elmentve.",
        "bad_message": "A szerkesztő értelmezhetetlen parancsot küldött. A módosítás nem lett elmentve.",
        "render_failed": "A módosítás elmentve, de a kártyát nem sikerült újrarajzolni.",
        "opt_require_modifier": "Ctrl + kattintás szükséges a szerkesztés megkezdéséhez (⌘ Macen)",
    },
    "el": {
        "save_failed": "Δεν ήταν δυνατή η αποθήκευση της αλλαγής: {error}",
        "field_missing": "Το πεδίο «{field}» δεν υπάρχει πλέον. Η αλλαγή δεν αποθηκεύτηκε.",
        "note_missing": "Η σημείωση δεν υπάρχει πλέον. Η αλλαγή δεν αποθηκεύτηκε.",
        "bad_message": "Ο επεξεργαστής έστειλε μια εντολή που δεν ήταν κατανοητή. Η αλλαγή δεν αποθηκεύτηκε.",
        "render_failed": "Η αλλαγή αποθηκεύτηκε, αλλά δεν ήταν δυνατή η επανασχεδίαση της κάρτας.",
        "opt_require_modifier": "Απαίτηση Ctrl + κλικ για έναρξη επεξεργασίας (⌘ σε Mac)",
    },
    "bg": {
        "save_failed": "Промяната не можа да бъде запазена: {error}",
        "field_missing": "Полето „{field}“ вече не съществува. Промяната не е запазена.",
        "note_missing": "Бележката вече не съществува. Промяната не е запазена.",
        "bad_message": "Редакторът изпрати команда, която не беше разбрана. Промяната не е запазена.",
        "render_failed": "Промяната е запазена, но картата не можа да бъде преначертана.",
        "opt_require_modifier": "Изисквай Ctrl + щракване за започване на редактиране (⌘ на Mac)",
    },
    "ru": {
        "save_failed": "Не удалось сохранить изменение: {error}",
        "field_missing": "Поле «{field}» больше не существует. Изменение не сохранено.",
        "note_missing": "Заметка больше не существует. Изменение не сохранено.",
        "bad_message": "Редактор отправил непонятную команду. Изменение не сохранено.",
        "render_failed": "Изменение сохранено, но не удалось перерисовать карточку.",
        "opt_require_modifier": "Требовать Ctrl + щелчок для начала редактирования (⌘ на Mac)",
    },
    "uk": {
        "save_failed": "Не вдалося зберегти зміну: {error}",
        "field_missing": "Поле «{field}» більше не існує. Зміну не збережено.",
        "note_missing": "Нотатка більше не існує. Зміну не збережено.",
        "bad_message": "Редактор надіслав незрозумілу команду. Зміну не збережено.",
        "render_failed": "Зміну збережено, але не вдалося перемалювати картку.",
        "opt_require_modifier": "Вимагати Ctrl + клік для початку редагування (⌘ на Mac)",
    },
    "be": {
        "save_failed": "Не ўдалося захаваць змену: {error}",
        "field_missing": "Поле «{field}» больш не існуе. Змена не захавана.",
        "note_missing": "Нататка больш не існуе. Змена не захавана.",
        "bad_message": "Рэдактар даслаў незразумелую каманду. Змена не захавана.",
        "render_failed": "Змена захавана, але не ўдалося перамаляваць картку.",
        "opt_require_modifier": "Патрабаваць Ctrl + клік для пачатку рэдагавання (⌘ на Mac)",
    },
    "tr": {
        "save_failed": "Değişiklik kaydedilemedi: {error}",
        "field_missing": "“{field}” alanı artık mevcut değil. Değişiklik kaydedilmedi.",
        "note_missing": "Not artık mevcut değil. Değişiklik kaydedilmedi.",
        "bad_message": "Düzenleyici anlaşılamayan bir komut gönderdi. Değişiklik kaydedilmedi.",
        "render_failed": "Değişiklik kaydedildi ancak kart yeniden çizilemedi.",
        "opt_require_modifier": "Düzenlemeye başlamak için Ctrl + tıklama gerektir (Mac'te ⌘)",
    },
    "ca": {
        "save_failed": "No s'ha pogut desar el canvi: {error}",
        "field_missing": "El camp «{field}» ja no existeix. El canvi no s'ha desat.",
        "note_missing": "La nota ja no existeix. El canvi no s'ha desat.",
        "bad_message": "L'editor ha enviat una ordre que no s'entén. El canvi no s'ha desat.",
        "render_failed": "El canvi s'ha desat, però no s'ha pogut redibuixar la targeta.",
        "opt_require_modifier": "Requereix Ctrl + clic per començar a editar (⌘ al Mac)",
    },
    "gl": {
        "save_failed": "Non se puido gardar o cambio: {error}",
        "field_missing": "O campo «{field}» xa non existe. O cambio non se gardou.",
        "note_missing": "A nota xa non existe. O cambio non se gardou.",
        "bad_message": "O editor enviou unha orde que non se entende. O cambio non se gardou.",
        "render_failed": "O cambio gardouse, pero non se puido redebuxar a tarxeta.",
        "opt_require_modifier": "Requirir Ctrl + clic para comezar a editar (⌘ en Mac)",
    },
    "eu": {
        "save_failed": "Ezin izan da aldaketa gorde: {error}",
        "field_missing": "«{field}» eremua ez da existitzen jada. Aldaketa ez da gorde.",
        "note_missing": "Oharra ez da existitzen jada. Aldaketa ez da gorde.",
        "bad_message": "Editoreak ulertu ezin den komando bat bidali du. Aldaketa ez da gorde.",
        "render_failed": "Aldaketa gorde da, baina ezin izan da txartela berriro marraztu.",
        "opt_require_modifier": "Editatzen hasteko Ctrl + klik eskatu (⌘ Mac-en)",
    },
    "et": {
        "save_failed": "Muudatust ei õnnestunud salvestada: {error}",
        "field_missing": "Välja „{field}” enam ei eksisteeri. Muudatust ei salvestatud.",
        "note_missing": "Märkmet enam ei eksisteeri. Muudatust ei salvestatud.",
        "bad_message": "Redaktor saatis käsu, millest ei saadud aru. Muudatust ei salvestatud.",
        "render_failed": "Muudatus salvestati, kuid kaarti ei õnnestunud uuesti joonistada.",
        "opt_require_modifier": "Nõua redigeerimise alustamiseks Ctrl + klõps (⌘ Macis)",
    },
    "vi": {
        "save_failed": "Không thể lưu thay đổi: {error}",
        "field_missing": "Trường “{field}” không còn tồn tại. Thay đổi chưa được lưu.",
        "note_missing": "Ghi chú không còn tồn tại. Thay đổi chưa được lưu.",
        "bad_message": "Trình chỉnh sửa đã gửi một lệnh không hiểu được. Thay đổi chưa được lưu.",
        "render_failed": "Thay đổi đã được lưu, nhưng không thể vẽ lại thẻ.",
        "opt_require_modifier": "Yêu cầu Ctrl + nhấp để bắt đầu chỉnh sửa (⌘ trên Mac)",
    },
    "th": {
        "save_failed": "ไม่สามารถบันทึกการเปลี่ยนแปลง: {error}",
        "field_missing": "ไม่มีช่อง “{field}” อีกต่อไป การเปลี่ยนแปลงไม่ได้ถูกบันทึก",
        "note_missing": "ไม่มีโน้ตนี้อีกต่อไป การเปลี่ยนแปลงไม่ได้ถูกบันทึก",
        "bad_message": "ตัวแก้ไขส่งคำสั่งที่ไม่เข้าใจ การเปลี่ยนแปลงไม่ได้ถูกบันทึก",
        "render_failed": "บันทึกการเปลี่ยนแปลงแล้ว แต่ไม่สามารถวาดการ์ดใหม่ได้",
        "opt_require_modifier": "ต้องกด Ctrl + คลิกเพื่อเริ่มแก้ไข (⌘ บน Mac)",
    },
    "ms": {
        "save_failed": "Tidak dapat menyimpan perubahan: {error}",
        "field_missing": "Medan “{field}” tidak wujud lagi. Perubahan tidak disimpan.",
        "note_missing": "Nota tidak wujud lagi. Perubahan tidak disimpan.",
        "bad_message": "Penyunting menghantar arahan yang tidak difahami. Perubahan tidak disimpan.",
        "render_failed": "Perubahan disimpan, tetapi kad tidak dapat dilukis semula.",
        "opt_require_modifier": "Perlukan Ctrl + klik untuk mula menyunting (⌘ pada Mac)",
    },
    "ar": {
        "save_failed": "تعذّر حفظ التغيير: {error}",
        "field_missing": "الحقل «{field}» لم يعد موجودًا. لم يتم حفظ التغيير.",
        "note_missing": "الملاحظة لم تعد موجودة. لم يتم حفظ التغيير.",
        "bad_message": "أرسل المحرِّر أمرًا غير مفهوم. لم يتم حفظ التغيير.",
        "render_failed": "تم حفظ التغيير، لكن تعذّر إعادة رسم البطاقة.",
        "opt_require_modifier": "اطلب Ctrl + نقرة لبدء التحرير (⌘ على Mac)",
    },
    "he": {
        "save_failed": "לא ניתן היה לשמור את השינוי: {error}",
        "field_missing": "השדה «{field}» כבר לא קיים. השינוי לא נשמר.",
        "note_missing": "הפתק כבר לא קיים. השינוי לא נשמר.",
        "bad_message": "העורך שלח פקודה שלא הובנה. השינוי לא נשמר.",
        "render_failed": "השינוי נשמר, אך לא ניתן היה לצייר מחדש את הכרטיס.",
        "opt_require_modifier": "דרוש Ctrl + לחיצה כדי להתחיל לערוך (⌘ ב-Mac)",
    },
    "fa": {
        "save_failed": "ذخیرهٔ تغییر ممکن نشد: {error}",
        "field_missing": "فیلد «{field}» دیگر وجود ندارد. تغییر ذخیره نشد.",
        "note_missing": "یادداشت دیگر وجود ندارد. تغییر ذخیره نشد.",
        "bad_message": "ویرایشگر فرمانی نامفهوم ارسال کرد. تغییر ذخیره نشد.",
        "render_failed": "تغییر ذخیره شد، اما ترسیم دوبارهٔ کارت ممکن نشد.",
        "opt_require_modifier": "برای شروع ویرایش، Ctrl + کلیک لازم است (⌘ در Mac)",
    },
    "ja": {
        "save_failed": "変更を保存できませんでした：{error}",
        "field_missing": "フィールド「{field}」は存在しません。変更は保存されませんでした。",
        "note_missing": "ノートが存在しません。変更は保存されませんでした。",
        "bad_message": "エディタが認識できないコマンドを送信しました。変更は保存されませんでした。",
        "render_failed": "変更は保存されましたが、カードを再描画できませんでした。",
        "opt_require_modifier": "編集を始めるには Ctrl + クリックを必須にする（Mac では ⌘）",
    },
    "zh": {
        "save_failed": "无法保存更改：{error}",
        "field_missing": "字段“{field}”已不存在。更改未保存。",
        "note_missing": "笔记已不存在。更改未保存。",
        "bad_message": "编辑器发送了无法识别的命令。更改未保存。",
        "render_failed": "更改已保存，但无法重新绘制卡片。",
        "opt_require_modifier": "需要按住 Ctrl 并点击才能开始编辑（Mac 上为 ⌘）",
    },
    "ko": {
        "save_failed": "변경 사항을 저장할 수 없습니다: {error}",
        "field_missing": "«{field}» 필드가 더 이상 존재하지 않습니다. 변경 사항이 저장되지 않았습니다.",
        "note_missing": "노트가 더 이상 존재하지 않습니다. 변경 사항이 저장되지 않았습니다.",
        "bad_message": "편집기가 이해할 수 없는 명령을 보냈습니다. 변경 사항이 저장되지 않았습니다.",
        "render_failed": "변경 사항은 저장되었지만 카드를 다시 그릴 수 없습니다.",
        "opt_require_modifier": "편집을 시작하려면 Ctrl + 클릭 필요 (Mac에서는 ⌘)",
    },
    "eo": {
        "save_failed": "Ne eblis konservi la ŝanĝon: {error}",
        "field_missing": "La kampo «{field}» ne plu ekzistas. La ŝanĝo ne estis konservita.",
        "note_missing": "La noto ne plu ekzistas. La ŝanĝo ne estis konservita.",
        "bad_message": "La redaktilo sendis nekompreneblan komandon. La ŝanĝo ne estis konservita.",
        "render_failed": "La ŝanĝo estis konservita, sed la karto ne povis esti redesegnita.",
        "opt_require_modifier": "Postuli Ctrl + klako por komenci redakti (⌘ en Mac)",
    },
    "la": {
        "save_failed": "Mutatio servari non potuit: {error}",
        "field_missing": "Campus «{field}» iam non exstat. Mutatio non servata est.",
        "note_missing": "Nota iam non exstat. Mutatio non servata est.",
        "bad_message": "Editor mandatum non intellectum misit. Mutatio non servata est.",
        "render_failed": "Mutatio servata est, sed charta iterum depingi non potuit.",
        "opt_require_modifier": "Ad editionem incipiendam Ctrl + clic requirere (⌘ in Mac)",
    },
    "af": {
        "save_failed": "Kon nie die verandering stoor nie: {error}",
        "field_missing": "Die veld “{field}” bestaan nie meer nie. Die verandering is nie gestoor nie.",
        "note_missing": "Die notas bestaan nie meer nie. Die verandering is nie gestoor nie.",
        "bad_message": "Die redigeerder het 'n onverstaanbare opdrag gestuur. Die verandering is nie gestoor nie.",
        "render_failed": "Die verandering is gestoor, maar die kaart kon nie herteken word nie.",
        "opt_require_modifier": "Vereis Ctrl + klik om te begin redigeer (⌘ op Mac)",
    },
    "ga": {
        "save_failed": "Níorbh fhéidir an t-athrú a shábháil: {error}",
        "field_missing": "Níl an réimse “{field}” ann a thuilleadh. Níor sábháladh an t-athrú.",
        "note_missing": "Níl an nóta ann a thuilleadh. Níor sábháladh an t-athrú.",
        "bad_message": "Sheol an t-eagarthóir ordú nár tuigeadh. Níor sábháladh an t-athrú.",
        "render_failed": "Sábháladh an t-athrú, ach níorbh fhéidir an cárta a atarraingt.",
        "opt_require_modifier": "Éiligh Ctrl + cliceáil chun tosú ag cur in eagar (⌘ ar Mac)",
    },
    "oc": {
        "save_failed": "Impossible d'enregistrar la modificacion : {error}",
        "field_missing": "Lo camp « {field} » existís pas mai. La modificacion es pas estada enregistrada.",
        "note_missing": "La nòta existís pas mai. La modificacion es pas estada enregistrada.",
        "bad_message": "L'editor a mandat una comanda incompresibla. La modificacion es pas estada enregistrada.",
        "render_failed": "La modificacion es estada enregistrada, mas la carta a pas pogut èsser tornada afichar.",
        "opt_require_modifier": "Requerir Ctrl + clic per començar d'editar (⌘ sus Mac)",
    },
    "kk": {
        "save_failed": "Өзгерісті сақтау мүмкін болмады: {error}",
        "field_missing": "«{field}» өрісі енді жоқ. Өзгеріс сақталмады.",
        "note_missing": "Жазба енді жоқ. Өзгеріс сақталмады.",
        "bad_message": "Редактор түсініксіз пәрмен жіберді. Өзгеріс сақталмады.",
        "render_failed": "Өзгеріс сақталды, бірақ картаны қайта салу мүмкін болмады.",
        "opt_require_modifier": "Өңдеуді бастау үшін Ctrl + шерту қажет (Mac-те ⌘)",
    },
    "mn": {
        "save_failed": "Өөрчлөлтийг хадгалж чадсангүй: {error}",
        "field_missing": "«{field}» талбар байхгүй болсон. Өөрчлөлт хадгалагдсангүй.",
        "note_missing": "Тэмдэглэл байхгүй болсон. Өөрчлөлт хадгалагдсангүй.",
        "bad_message": "Засварлагч ойлгомжгүй тушаал илгээв. Өөрчлөлт хадгалагдсангүй.",
        "render_failed": "Өөрчлөлт хадгалагдсан ч картыг дахин зурж чадсангүй.",
        "opt_require_modifier": "Засварлаж эхлэхийн тулд Ctrl + товшилт шаардах (Mac дээр ⌘)",
    },
    "hy": {
        "save_failed": "Չհաջողվեց պահպանել փոփոխությունը՝ {error}",
        "field_missing": "«{field}» դաշտն այլևս գոյություն չունի։ Փոփոխությունը չպահպանվեց։",
        "note_missing": "Նշումն այլևս գոյություն չունի։ Փոփոխությունը չպահպանվեց։",
        "bad_message": "Խմբագրիչն ուղարկեց անհասկանալի հրաման։ Փոփոխությունը չպահպանվեց։",
        "render_failed": "Փոփոխությունը պահպանվեց, բայց քարտը չհաջողվեց վերագծել։",
        "opt_require_modifier": "Խմբագրումը սկսելու համար պահանջել Ctrl + սեղմում (Mac-ում՝ ⌘)",
    },
    "uz": {
        "save_failed": "O'zgarishni saqlab bo'lmadi: {error}",
        "field_missing": "«{field}» maydoni endi mavjud emas. O'zgarish saqlanmadi.",
        "note_missing": "Eslatma endi mavjud emas. O'zgarish saqlanmadi.",
        "bad_message": "Tahrirlagich tushunarsiz buyruq yubordi. O'zgarish saqlanmadi.",
        "render_failed": "O'zgarish saqlandi, lekin kartani qayta chizib bo'lmadi.",
        "opt_require_modifier": "Tahrirlashni boshlash uchun Ctrl + bosish talab qilinsin (Mac'da ⌘)",
    },
    "tl": {
        "save_failed": "Hindi ma-save ang pagbabago: {error}",
        "field_missing": "Wala na ang field na “{field}”. Hindi na-save ang pagbabago.",
        "note_missing": "Wala na ang note. Hindi na-save ang pagbabago.",
        "bad_message": "Nagpadala ang editor ng utos na hindi naunawaan. Hindi na-save ang pagbabago.",
        "render_failed": "Na-save ang pagbabago, ngunit hindi ma-redraw ang kard.",
        "opt_require_modifier": "Mangailangan ng Ctrl + click para magsimulang mag-edit (⌘ sa Mac)",
    },
    "yi": {
        "save_failed": "מען האָט נישט געקענט אָפּהיטן די ענדערונג: {error}",
        "field_missing": "דאָס פֿעלד «{field}» עקזיסטירט מער נישט. די ענדערונג איז נישט אָפּגעהיט געוואָרן.",
        "note_missing": "די נאָטיץ עקזיסטירט מער נישט. די ענדערונג איז נישט אָפּגעהיט געוואָרן.",
        "bad_message": "דער רעדאַקטאָר האָט געשיקט אַ נישט-פֿאַרשטענדלעכן באַפֿעל. די ענדערונג איז נישט אָפּגעהיט געוואָרן.",
        "render_failed": "די ענדערונג איז אָפּגעהיט געוואָרן, אָבער מען האָט נישט געקענט איבערצייכענען די קאָרטל.",
        "opt_require_modifier": "פֿאָדער Ctrl + קליק צו אָנהייבן רעדאַקטירן (⌘ אויף Mac)",
    },
}


def _current_base_language() -> str:
    """Idioma base de la interfaz de Anki ("es", "en", "pt", "zh"...).

    Se lee en cada llamada, no al importar, para respetar un cambio de idioma
    sin depender de cuándo se cargó el módulo. Si por lo que sea no se puede
    leer, se cae al idioma base (inglés), que siempre está disponible.
    """
    try:
        import anki.lang

        raw = (anki.lang.current_lang or "").replace("_", "-")
        base = raw.split("-", 1)[0].strip().lower()
        return base or BASE_LANGUAGE
    except Exception:
        return BASE_LANGUAGE


def tr(key: str, **values: str) -> str:
    base = STRINGS[BASE_LANGUAGE]
    table = STRINGS.get(_current_base_language(), base)
    # Si al idioma le falta una clave concreta, se completa con la base inglesa.
    text = table.get(key) or base.get(key, key)
    if not values:
        return text
    try:
        return text.format(**values)
    except (KeyError, IndexError):
        return text
