#!/usr/bin/env python3
"""Generates the ferie-2027 site: index.html (tiles), one page per destination, info.html."""
import html, pathlib

OUT = pathlib.Path(__file__).parent
UPDATED = "24.10.2026"

# ---------- timeline helpers ----------
# ("dep"|"arr", local time, Polish time, description)  ("fly", text)  ("stop", local, pl, desc, box)  ("night", text)
def dep(t, pl, d): return ("dep", t, pl, d)
def arr(t, pl, d): return ("arr", t, pl, d)
def fly(d): return ("fly", d)
def stop(t, pl, d, box=None): return ("stop", t, pl, d, box)
def night(d): return ("night", d)

GULF = '<span class="badge gulf">przez Zatokę Perską</span>'
NOGULF = '<span class="badge nogulf">bez Zatoki</span>'

DEST = [
 dict(slug="sri-lanka", flag="🇱🇰", name="Sri Lanka", place="Kolombo → plaże i dżungla", gulf=True,
  price="3 005 zł", price7="21 035 zł", price_note="Air Arabia, wylot pt 19.02 22:10",
  summary="Najtaniej i najszybciej (11 h, 1 przesiadka), wylot w piątek po pracy prosto z Krakowa. Powrót nd 7.03 przed południem.",
  weather="☀️ 30–31°C, pora sucha na zachodzie i południu", sea="27–28°C",
  entry="ETA online przed wylotem (sprawdzić, czy dla Polaków bezpłatna)",
  chips=[("warn","Przesiadka w ZEA (Szardża) – Zatoka Perska"),("ok","Najtańsza opcja"),("ok","Powrót w niedzielę")],
  options=[
   dict(title="Air Arabia z Krakowa, przez Szardżę", tag="Najlepsza opcja", gulf=True,
    pp="3 005 zł", p7="21 035 zł", total_out="11 h 05 min", total_back="13 h 10 min",
    why="Jedyny lot z Krakowa w piątek po pracy. Najtaniej i jedna z najszybszych opcji. Taryfa Basic: 10 kg bagażu podręcznego.",
    out_title="Tam: pt 19.02 → sob 20.02", out=[
     dep("22:10","22:10","pt 19.02 · wylot z Krakowa (KRK)"), fly("lot ok. 5 h 40 min"),
     stop("ok. 06:50","ok. 03:50","sob 20.02 · Szardża (SHJ), Zjednoczone Emiraty Arabskie","Przesiadka <b>1 h</b> · czas lokalny = Polska + 3 h"),
     stop("ok. 07:50","ok. 04:50","wylot z Szardży"), fly("lot ok. 4 h 25 min"),
     arr("13:45","09:15","sob 20.02 · Kolombo (CMB), Sri Lanka · czas lokalny = Polska + 4 h 30 min")],
    out_bio="Wylot o porze snu dzieci, przesiadka w środku polskiej nocy, lądowanie o 9:15 polskiego czasu – na miejscu wczesne popołudnie.",
    back_title="Powrót: nd 7.03", back=[
     dep("02:40","sob 22:10","nd 7.03 (noc z soboty na niedzielę) · wylot z Kolombo – na lotnisku ok. 23:40 w sobotę"), fly("lot ok. 4 h 20 min"),
     stop("ok. 05:30","ok. 02:30","Szardża (SHJ), ZEA","Przesiadka <b>ok. 2 h</b>"),
     stop("ok. 07:35","ok. 04:35","wylot z Szardży"), fly("lot ok. 6 h 45 min"),
     arr("11:20","11:20","nd 7.03 · Kraków")],
    back_bio="Ostatni pełny dzień na wyspie: sobota 6.03. Podróż w polską noc, w domu w niedzielę przed obiadem.",
    note="Godziny w Szardży wyliczone z rozkładu Air Arabia (± ok. 15 min); reszta z Google Flights."),
   dict(title="Air Arabia z Krakowa, wylot w sobotę", gulf=True, pp="3 005 zł", p7="21 035 zł", total_out="11 h 50 min",
    why="Ta sama cena i ten sam powrót, ale wylot w sobotę w południe i przylot w środku nocy.",
    out_title="Tam: sob 20.02 → nd 21.02", out=[
     dep("12:10","12:10","sob 20.02 · wylot z Krakowa"), stop("","","Szardża (ZEA)","Przesiadka <b>1 h 45 min</b>"),
     arr("04:30","00:00","nd 21.02 · Kolombo")], back_title="Powrót: jak w opcji wyżej (nd 7.03, Kraków 11:20)", back=[]),
   dict(title="flydubai z Warszawy, przez Dubaj", gulf=True, pp="3 974 zł", p7="27 820 zł + pociąg", total_out="15 h 20 min", total_back="14 h 25 min",
    why="Wieczorny wylot z Warszawy – z Krakowa pociągiem po pracy.",
    out_title="Tam: pt 19.02 → sob 20.02", out=[
     dep("20:30","20:30","pt 19.02 · wylot z Warszawy (WAW)"), stop("","","Dubaj (DXB), ZEA","Przesiadka <b>4 h 40 min</b>"),
     arr("16:20","11:50","sob 20.02 · Kolombo")],
    back_title="Powrót: nd 7.03", back=[
     dep("09:15","04:45","nd 7.03 · wylot z Kolombo"), stop("","","Dubaj (DXB), ZEA","Przesiadka <b>2 h 25 min</b>"),
     arr("19:10","19:10","nd 7.03 · Warszawa")]),
   dict(title="KLM + IndiGo z Krakowa, przez Amsterdam i Indie", gulf=False, pp="4 677 zł", p7="32 739 zł", total_out="22 h",
    why="Jedyna sensowna trasa na Sri Lankę bez Zatoki – ale wylot w sobotę o 6:00 i powrót w poniedziałek.",
    out_title="Tam: sob 20.02 → nd 21.02", out=[
     dep("06:00","06:00","sob 20.02 · wylot z Krakowa"), stop("","","Amsterdam (Holandia), potem Mumbaj (Indie)","2 przesiadki"),
     arr("08:10","03:40","nd 21.02 · Kolombo")],
    back_title="Powrót: nd 7.03 → pn 8.03", back=[
     dep("21:50","17:20","nd 7.03 · wylot z Kolombo"), stop("","","Bangalore (Indie), potem Amsterdam","2 przesiadki"),
     arr("11:15","11:15","pn 8.03 · Kraków")]),
  ],
  extra="Sprawdzone też: Lufthansa + Qatar przez Monachium i Dohę (sob 6:00, 3 918 zł/os.), flydubai/Emirates z Krakowa w sobotę 23:10 (4 059 zł/os.), Wiedeń (Air Arabia ok. 3 330 zł/os.), Wrocław (tylko rano, od ok. 4 000 zł/os.). Katowice: Air Arabia ma latać do Szardży od 17.12.2026."),

 dict(slug="malezja-borneo", flag="🇲🇾", name="Malezja – Borneo", place="Kota Kinabalu (Sabah): wyspy, orangutany", gulf=False,
  price="ok. 4 920 zł", price7="ok. 34 400 zł", price_note="z lotem krajowym na Borneo",
  summary="Wylot w piątek po pracy z Krakowa (19:05) przez Frankfurt i Singapur, nocleg w Kuala Lumpur, potem 2 h 40 min na Borneo. Bez wizy.",
  weather="🌤 31°C / noc 23°C, przelotne deszcze", sea="28–29°C", entry="bez wizy 90 dni; karta MDAC online",
  chips=[("ok","Bez Zatoki"),("ok","Piątek po pracy z Krakowa"),("warn","Powrót w poniedziałek rano"),("warn","Osobny bilet na lot krajowy")],
  options=[
   dict(title="Lufthansa + Malaysia Airlines przez Frankfurt i Singapur, potem lot na Borneo", tag="Najlepsza opcja", gulf=False,
    pp="4 311 zł", p7="30 175 zł", total_out="18 h 40 min do Kuala Lumpur", total_back="16 h 40 min",
    why="Wieczorny wylot z Krakowa, jedna rezerwacja aż do Kuala Lumpur. Na Borneo AirAsia / Firefly – ok. 300 zł/os. w jedną stronę (razem ok. 4 920 zł/os.).",
    out_title="Tam: pt 19.02 → sob 20.02", out=[
     dep("19:05","19:05","pt 19.02 · wylot z Krakowa, LH 1369"),
     stop("20:45","20:45","Frankfurt (Niemcy)","Przesiadka <b>55 min</b> – krótka, ale na jednym bilecie"),
     stop("21:40","21:40","wylot z Frankfurtu, LH 780 (nocny)"), fly("lot ok. 12 h 25 min"),
     stop("17:05","10:05","sob 20.02 · Singapur","Przesiadka <b>ok. 2 h</b> · czas lokalny = Polska + 7 h"),
     stop("ok. 19:05","ok. 12:05","wylot Malaysia Airlines"),
     arr("20:45","13:45","sob 20.02 · Kuala Lumpur (Malezja)"),
     night("🛏 Nocleg w Kuala Lumpur (albo 1–2 dni miasta: wieże Petronas, akwarium)"),
     dep("rano","","nd 21.02 · AirAsia / Firefly do Kota Kinabalu"), fly("lot 2 h 40 min"),
     arr("","","Kota Kinabalu, Borneo")],
    out_bio="Lot nocny w polską noc, w Kuala Lumpur wieczór (13:45 polskiego czasu) – nocleg pomaga złapać nowy rytm.",
    back_title="Powrót: nd 7.03 → pn 8.03", back=[
     dep("po południu","","nd 7.03 · lot z Kota Kinabalu do Kuala Lumpur (2 h 40 min)"),
     dep("23:55","16:55","nd 7.03 · wylot z Kuala Lumpur, LH 705 (nocny)"), fly("lot ok. 13 h"),
     stop("06:00","06:00","pn 8.03 · Frankfurt","Przesiadka <b>2 h</b>"),
     stop("08:00","08:00","wylot z Frankfurtu, LH 1362"),
     arr("09:35","09:35","pn 8.03 · Kraków")],
    back_bio="Cała niedziela jeszcze w Malezji, w Krakowie w poniedziałek rano – dzieci tracą poniedziałek w szkole.",
    note="Lot krajowy to osobny bilet – przy spóźnieniu nikt nie przebukuje, dlatego nocleg w KL po drodze."),
   dict(title="Austrian + Malaysia Airlines przez Wiedeń i Bangkok", gulf=False, pp="3 632 zł", p7="25 426 zł", total_out="19 h 50 min do Kuala Lumpur",
    why="Taniej o ok. 680 zł/os., ale wylot z Krakowa o 14:45 – trzeba wziąć wolne w piątek.",
    out_title="Tam: pt 19.02 → sob 20.02", out=[
     dep("14:45","14:45","pt 19.02 · wylot z Krakowa, OS 680"),
     stop("15:45","15:45","Wiedeń (Austria)","Przesiadka <b>4 h 30 min</b>"),
     stop("20:15","20:15","wylot z Wiednia, OS 5 (nocny)"),
     stop("12:20","06:20","sob 20.02 · Bangkok (Tajlandia)","Przesiadka <b>1 h 55 min</b>"),
     stop("14:15","08:15","wylot MH 789"), arr("17:35","10:35","sob 20.02 · Kuala Lumpur")],
    back_title="Powrót: jak w opcji wyżej (pn 8.03, Kraków 9:35)", back=[]),
  ],
  extra="Langkawi pominięte – już tam byliśmy. Wschodnie wybrzeże Malezji (Perhentian, Tioman) w tym terminie odpada – monsun."),

 dict(slug="tajwan", flag="🇹🇼", name="Tajwan", place="Tajpej + Kenting na południu", gulf=False,
  price="4 164 zł", price7="29 151 zł", price_note="Turkish, wylot sob 20.02",
  summary="Jedna krótka przesiadka w Stambule, bezpieczny i świetny dla dzieci kraj. Powrót w niedzielę rano.",
  weather="🌧 Tajpej 17–20°C i deszcz · 🌤 Kenting 24–26°C", sea="24–25°C (tylko południe)", entry="bez wizy 90 dni; karta TWAC online",
  chips=[("ok","Bez Zatoki"),("ok","1 przesiadka"),("warn","Północ chłodna i deszczowa"),("warn","Morze tylko 24–25°C")],
  options=[
   dict(title="Turkish Airlines z Krakowa, przez Stambuł", tag="Najlepsza opcja", gulf=False,
    pp="4 164 zł", p7="29 151 zł", total_out="15 h 15 min", total_back="17 h 20 min",
    why="Najkrótsza podróż z jedną przesiadką; wylot w sobotę wieczorem, powrót w niedzielę rano. EcoFly: 8 kg kabinowa + torba.",
    out_title="Tam: sob 20.02 → nd 21.02", out=[
     dep("19:25","19:25","sob 20.02 · wylot z Krakowa, TK 1274"),
     stop("23:50","21:50","Stambuł (Turcja)","Przesiadka <b>2 h 05 min</b> · czas lokalny = Polska + 2 h"),
     stop("01:55","23:55","wylot ze Stambułu (nocny)"),
     arr("17:40","10:40","nd 21.02 · Tajpej (TPE) · czas lokalny = Polska + 7 h"),
     night("🚄 Na południe: szybka kolej do Kaohsiung (1,5 h) + 1,5–2 h autem do Kentingu")],
    out_bio="Lot nocny w polską noc, przylot do Tajpej w polskie przedpołudnie (17:40 na miejscu).",
    back_title="Powrót: sob 6.03 → nd 7.03", back=[
     dep("22:00","15:00","sob 6.03 · wylot z Tajpej, TK 25 (nocny)"),
     stop("05:50","03:50","nd 7.03 · Stambuł","Przesiadka <b>2 h 10 min</b>"),
     stop("08:00","06:00","wylot ze Stambułu, TK 1271"),
     arr("08:20","08:20","nd 7.03 · Kraków")],
    back_bio="W domu w niedzielę rano – cały dzień na odpoczynek przed szkołą."),
   dict(title="Lufthansa + China Airlines z Krakowa do Kaohsiung (południe)", gulf=False, pp="5 221 zł", p7="36 547 zł", total_out="20 h 10 min", total_back="22 h 35 min",
    why="Wylot w piątek po pracy i lądowanie od razu na południu wyspy, ale drożej i powrót w poniedziałek.",
    out_title="Tam: pt 19.02 → sob 20.02", out=[
     dep("19:05","19:05","pt 19.02 · wylot z Krakowa, LH 1369"),
     stop("20:45","20:45","Frankfurt","Przesiadka <b>1 h 05 min</b>"),
     stop("21:50","21:50","wylot, LH 796 (nocny)"),
     stop("16:30","09:30","sob 20.02 · Hongkong","Przesiadka <b>4 h 15 min</b>"),
     stop("20:45","13:45","wylot, CI 936"), arr("22:15","15:15","sob 20.02 · Kaohsiung")],
    back_title="Powrót: nd 7.03 → pn 8.03", back=[
     dep("18:00","11:00","nd 7.03 · wylot z Kaohsiung, CI 935"),
     stop("19:45","12:45","Hongkong","Przesiadka <b>4 h</b>"),
     stop("23:45","16:45","wylot, LH 797 (nocny)"),
     stop("06:10","06:10","pn 8.03 · Frankfurt","Przesiadka <b>1 h 50 min</b>"),
     arr("09:35","09:35","pn 8.03 · Kraków")]),
  ],
  extra="Tajpej w tym terminie: dobre na 2–3 dni miasta (Taipei 101, nocne targi, zoo), nie na plażę."),

 dict(slug="filipiny", flag="🇵🇭", name="Filipiny", place="Palawan / Boracay / Bohol", gulf=False,
  price="ok. 4 150 zł", price7="ok. 29 000 zł", price_note="z Wiednia, z lotem krajowym",
  summary="Najpiękniejsze plaże i najpewniejsza pogoda (pora sucha). Ale tani lot jest z Wiednia – w piątek po pracy z Krakowa się nie zdąży.",
  weather="☀️ 30–31°C / noc 24°C, pora sucha", sea="27–28°C", entry="bez wizy 30 dni; rejestracja eTravel online",
  chips=[("ok","Bez Zatoki"),("ok","Najlepsze plaże"),("warn","Wylot z Wiednia o 19:30"),("warn","Nocleg w Manili po drodze")],
  options=[
   dict(title="Korean Air z Wiednia, przez Seul", tag="Najtańsza bez Zatoki", gulf=False,
    pp="3 817 zł", p7="26 720 zł + dojazd do Wiednia", total_out="19 h 40 min do Manili", total_back="24 h 35 min",
    why="Najtaniej, walizka 23 kg zwykle w cenie. Dalej Cebu Pacific na Palawan / Boracay / Bohol – ok. 150–170 zł/os. w jedną stronę.",
    out_title="Tam: pt 19.02 → sob 20.02", out=[
     dep("19:30","19:30","pt 19.02 · wylot z Wiednia, KE 938 (nocny)"),
     stop("14:30","06:30","sob 20.02 · Seul (Korea Płd.)","Przesiadka <b>4 h 25 min</b> · czas lokalny = Polska + 8 h"),
     stop("18:55","10:55","wylot, KE 623"),
     arr("22:10","15:10","sob 20.02 · Manila · czas lokalny = Polska + 7 h"),
     night("🛏 Nocleg w Manili, w niedzielę lot krajowy (np. Puerto Princesa 1 h 30, Caticlan/Boracay 1 h 10)")],
    back_title="Powrót: nd 7.03 → pn 8.03", back=[
     dep("23:35","16:35","nd 7.03 · wylot z Manili, KE 624 (nocny)"),
     stop("04:20","nd 20:20","pn 8.03 · Seul","Przesiadka <b>7 h 45 min</b>"),
     stop("12:05","04:05","wylot, KE 937"), arr("17:10","17:10","pn 8.03 · Wiedeń")]),
   dict(title="Turkish Airlines z Krakowa, wylot w sobotę", gulf=False, pp="5 964 zł", p7="41 745 zł", total_out="15 h 45 min", total_back="17 h 45 min",
    why="Prosto z Krakowa i powrót w niedzielę rano, ale wyraźnie drożej (z lotem krajowym ok. 6 300 zł/os.).",
    out_title="Tam: sob 20.02 → nd 21.02", out=[
     dep("19:25","19:25","sob 20.02 · wylot z Krakowa, TK 1274"),
     stop("23:50","21:50","Stambuł","Przesiadka <b>1 h 55 min</b>"),
     stop("01:45","23:45","wylot, TK 84 (nocny)"), arr("18:10","11:10","nd 21.02 · Manila")],
    back_title="Powrót: sob 6.03 → nd 7.03", back=[
     dep("21:35","14:35","sob 6.03 · wylot z Manili, TK 85"),
     stop("05:45","03:45","nd 7.03 · Stambuł","Przesiadka <b>2 h 15 min</b>"),
     arr("08:20","08:20","nd 7.03 · Kraków")]),
  ],
  extra="Na Boracay w lutym czasem wieje i są fale po wschodniej stronie wyspy. Do El Nido z Puerto Princesa 5–6 h busem."),

 dict(slug="tajlandia", flag="🇹🇭", name="Tajlandia", place="Phuket / Krabi (dla porównania)", gulf=False,
  price="ok. 3 700 zł", price7="ok. 25 900 zł", price_note="Condor z Wiednia + lot na Phuket",
  summary="Najtaniej bez Zatoki i sprawdzone. Lot z Wiednia (Condor przez Frankfurt) albo Turkish z Krakowa w sobotę.",
  weather="☀️ 32–33°C, sucho – najlepsza pora", sea="29°C", entry="bez wizy; karta TDAC online",
  chips=[("ok","Bez Zatoki"),("ok","Najtaniej bez Zatoki"),("warn","Wylot z Wiednia"),("warn","Sprawdzić, czy lot Condora nie ląduje w Abu Zabi")],
  options=[
   dict(title="Condor z Wiednia, przez Frankfurt", tag="Najtańsza bez Zatoki", gulf=False,
    pp="3 258 zł", p7="22 808 zł + dojazd do Wiednia", total_out="15 h 10 min", total_back="15 h 55 min",
    why="Najtańszy lot bez Zatoki w całym zestawieniu. Dalej na Phuket ok. 220 zł/os. w jedną stronę. Economy Light – tylko bagaż podręczny.",
    out_title="Tam: pt 19.02 → sob 20.02", out=[
     dep("17:10","17:10","pt 19.02 · wylot z Wiednia, DE 4365"),
     stop("18:30","18:30","Frankfurt","Przesiadka <b>2 h 45 min</b>"),
     stop("21:15","21:15","wylot, DE 2574 (nocny)"),
     arr("14:20","08:20","sob 20.02 · Bangkok · czas lokalny = Polska + 6 h")],
    back_title="Powrót: nd 7.03", back=[
     dep("11:35","05:35","nd 7.03 · wylot z Bangkoku, DE 2575"),
     stop("18:25","18:25","Frankfurt","Przesiadka <b>1 h 45 min</b>"),
     arr("21:30","21:30","nd 7.03 · Wiedeń")],
    note="Część lotów Condora Bangkok–Frankfurt w inne dni ma międzylądowanie w Abu Zabi – przy rezerwacji sprawdzić."),
   dict(title="Turkish Airlines z Krakowa, wylot w sobotę", gulf=False, pp="4 346 zł", p7="30 425 zł",
    why="Prosto z Krakowa, powrót w niedzielę rano.",
    out_title="Tam: sob 20.02 → nd 21.02", out=[
     dep("19:25","19:25","sob 20.02 · wylot z Krakowa"), stop("23:50","21:50","Stambuł","Przesiadka <b>1 h 50 min</b>"),
     stop("01:40","23:40","wylot, TK 68"), arr("15:05","09:05","nd 21.02 · Bangkok")],
    back_title="Powrót: sob 6.03 → nd 7.03, Kraków 8:20", back=[]),
  ]),

 dict(slug="kambodza", flag="🇰🇭", name="Kambodża", place="Siem Reap (Angkor), przez Kuala Lumpur", gulf=False,
  price="4 320–5 000 zł", price7="ok. 30 300–35 000 zł", price_note="bilet do KL + AirAsia",
  summary="Przygoda: świątynie Angkoru rano, basen po południu. Bilet do Kuala Lumpur + AirAsia 2 h do Siem Reap.",
  weather="🔥 33–35°C, bez deszczu", sea="28–29°C (Koh Rong – daleko od Angkoru)", entry="e-wiza 30 USD/os.",
  chips=[("ok","Bez Zatoki"),("warn","Upał 33–35°C"),("warn","Osobne bilety, nocleg w KL"),("warn","Plaża daleko od Angkoru")],
  options=[
   dict(title="Lufthansa + Malaysia Airlines do Kuala Lumpur, potem AirAsia do Siem Reap", tag="Najlepsza opcja", gulf=False,
    pp="ok. 5 000 zł", p7="ok. 35 000 zł",
    why="Wylot w piątek po pracy. Taniej (ok. 4 320 zł/os.) przez Wiedeń z wylotem o 14:45.",
    out_title="Tam: pt 19.02 → nd 21.02", out=[
     dep("19:05","19:05","pt 19.02 · wylot z Krakowa (jak Malezja: Frankfurt, Singapur)"),
     arr("20:45","13:45","sob 20.02 · Kuala Lumpur"), night("🛏 Nocleg w Kuala Lumpur"),
     dep("13:45","06:45","nd 21.02 · AirAsia z Kuala Lumpur"), fly("lot 2 h 05 min"),
     arr("14:50","08:50","nd 21.02 · Siem Reap (SAI) · czas lokalny = Polska + 6 h")],
    back_title="Powrót: nd 7.03 → pn 8.03", back=[
     dep("po południu","","nd 7.03 · Siem Reap → Kuala Lumpur"),
     dep("23:55","16:55","wylot z Kuala Lumpur, LH 705"), stop("06:00","06:00","pn 8.03 · Frankfurt","Przesiadka <b>2 h</b>"),
     arr("09:35","09:35","pn 8.03 · Kraków")]),
  ]),

 dict(slug="chiny-hainan", flag="🇨🇳", name="Chiny – Hainan", place="Sanya (plaże), przez Kanton", gulf=False,
  price="ok. 5 500 zł", price7="ok. 38 500 zł", price_note="Turkish do Kantonu + lot na Hainan",
  summary="Jedyne naprawdę ciepłe miejsce w Chinach w lutym. Turkish w sobotę do Kantonu i drogi lot krajowy do Sanyi.",
  weather="☀️ Sanya 26–28°C, sucho · 🌧 Guilin 7–14°C i deszcz · 🌥 Kanton 17–22°C, mżawki", sea="23–24°C (chłodniej niż w Tajlandii)",
  entry="bez wizy – na razie tylko do 31.12.2026",
  chips=[("ok","Bez Zatoki"),("warn","Wiza w 2027 niepewna"),("warn","Guilin/Yangshuo: zimno i deszcz"),("warn","Drogi lot krajowy")],
  options=[
   dict(title="Turkish Airlines z Krakowa do Kantonu, potem China Southern do Sanyi", tag="Najlepsza opcja", gulf=False,
    pp="ok. 5 500 zł", p7="ok. 38 500 zł", total_out="14 h 10 min do Kantonu", total_back="16 h 05 min",
    why="Sam lot do Kantonu: 3 765 zł/os. Lot Kanton–Sanya to aż ok. 866 zł/os. w jedną stronę.",
    out_title="Tam: sob 20.02 → nd 21.02", out=[
     dep("19:25","19:25","sob 20.02 · wylot z Krakowa, TK 1274"),
     stop("23:50","21:50","Stambuł","Przesiadka <b>1 h 45 min</b>"),
     stop("01:35","23:35","wylot, TK 72 (nocny)"),
     arr("16:35","09:35","nd 21.02 · Kanton (Guangzhou) · czas lokalny = Polska + 7 h"),
     dep("22:10","15:10","nd 21.02 · China Southern do Sanyi"), arr("23:55","16:55","nd 21.02 · Sanya, Hainan")],
    back_title="Powrót: sob 6.03 → nd 7.03", back=[
     dep("","","sob 6.03 · lot z Sanyi do Kantonu"),
     dep("23:15","16:15","sob 6.03 · wylot z Kantonu (Turkish, nocny)"),
     stop("ok. 05:55","ok. 03:55","nd 7.03 · Stambuł","Przesiadka <b>2 h 05 min</b>"),
     arr("08:20","08:20","nd 7.03 · Kraków")]),
  ],
  extra="Ruch bezwizowy dla Polaków ogłoszony na razie do 31.12.2026 – przedłużenie zwykle w listopadzie. Bez niego trzeba złożyć wizy (7 osób, centrum wizowe w Warszawie). Xishuangbanna (Yunnan): sucho i 26–30°C, ale bez morza. Guilin/Yangshuo w lutym odradzamy."),

 dict(slug="wietnam", flag="🇻🇳", name="Wietnam", place="Phu Quoc (dla porównania)", gulf=False,
  price="ok. 5 430 zł", price7="ok. 38 000 zł", price_note="KLM do Sajgonu + lot na Phu Quoc",
  summary="Wylot w piątek o 17:35 z Krakowa (KLM przez Amsterdam i Singapur), plaże i parki rozrywki na Phu Quoc.",
  weather="☀️ 31–32°C, sucho – najlepsza pora", sea="27–28°C", entry="bez wizy 45 dni",
  chips=[("ok","Bez Zatoki"),("ok","Piątek po pracy z Krakowa"),("warn","Droższe"),("warn","Powrót w poniedziałek")],
  options=[
   dict(title="KLM + Vietnam Airlines z Krakowa, przez Amsterdam i Singapur", tag="Najlepsza opcja", gulf=False,
    pp="5 129 zł", p7="35 902 zł", total_out="20 h 05 min", total_back="22 h 15 min",
    why="Wylot po pracy prosto z Krakowa. Dalej Vietjet na Phu Quoc – ok. 150 zł/os. w jedną stronę.",
    out_title="Tam: pt 19.02 → sob 20.02", out=[
     dep("17:35","17:35","pt 19.02 · wylot z Krakowa, KL 1328"),
     stop("19:35","19:35","Amsterdam","Przesiadka <b>1 h 10 min</b>"),
     stop("20:45","20:45","wylot, KL 835 (nocny)"),
     stop("16:15","09:15","sob 20.02 · Singapur","Przesiadka <b>2 h 10 min</b>"),
     stop("18:25","11:25","wylot, VN 654"), arr("19:40","13:40","sob 20.02 · Sajgon · czas lokalny = Polska + 6 h")],
    back_title="Powrót: nd 7.03 → pn 8.03", back=[
     dep("19:00","13:00","nd 7.03 · wylot z Sajgonu, MH 767"),
     stop("22:00","15:00","Kuala Lumpur","Przesiadka <b>1 h 50 min</b>"),
     stop("23:50","16:50","wylot, KL 810 (nocny)"),
     stop("06:20","06:20","pn 8.03 · Amsterdam","Przesiadka <b>3 h</b>"),
     arr("11:15","11:15","pn 8.03 · Kraków")]),
  ]),

 dict(slug="laos", flag="🇱🇦", name="Laos", place="Luang Prabang", gulf=False, notrec=True,
  price="ok. 5 600 zł", price7="ok. 39 250 zł", price_note="przez Bangkok",
  summary="W tym terminie nie polecamy: od początku marca smog z wypalania pól, brak morza, drogie loty.",
  weather="☀️ 30–32°C / noc 14–17°C · 🌫 od marca smog", sea="brak morza", entry="e-wiza ok. 50 USD/os.",
  chips=[("bad","Smog od początku marca"),("warn","Drogo"),("warn","Bez morza")],
  options=[
   dict(title="Condor z Wiednia do Bangkoku + Bangkok Airways do Luang Prabang", gulf=False, pp="ok. 5 600 zł", p7="ok. 39 250 zł",
    why="Lot Bangkok–Luang Prabang to ok. 1 175 zł/os. w jedną stronę.",
    out_title="Tam: pt 19.02 → nd 21.02", out=[
     dep("17:10","17:10","pt 19.02 · wylot z Wiednia (jak Tajlandia)"), arr("14:20","08:20","sob 20.02 · Bangkok"),
     night("🛏 Nocleg w Bangkoku"), dep("10:55","04:55","Bangkok Airways"), arr("13:05","07:05","Luang Prabang")],
    back_title="Powrót: przez Bangkok, Wiedeń nd 7.03 21:30", back=[]),
  ]),
]

TZ = {'sri-lanka': '+4 h 30 min', 'malezja-borneo': '+7 h', 'tajwan': '+7 h', 'filipiny': '+7 h', 'tajlandia': '+6 h', 'kambodza': '+6 h', 'chiny-hainan': '+7 h', 'wietnam': '+6 h', 'laos': '+6 h'}
INDO_PENDING = dict(slug="indonezja", flag="🇮🇩", name="Indonezja (bez Bali)", place="np. Lombok, Flores (Komodo), Jawa", pending=True,
  summary="Research w toku – Bali odpada (tłok). Pojawi się tutaj pod tym samym linkiem.")



# ---------- post-processing: Friday from Vienna is not realistic (can't get there after work) ----------
def _d(slug): return next(d for d in DEST if d["slug"] == slug)
_f = _d("filipiny"); _f["options"] = [o for o in _f["options"] if not o["title"].startswith("Korean Air")]
_f["options"][0]["tag"] = "Najlepsza opcja"
_f["options"][0]["why"] = "Prosto z Krakowa, jedna przesiadka w Stambule, powrót w niedzielę rano. Dalej Cebu Pacific na Palawan / Boracay / Bohol – ok. 150–170 zł/os. w jedną stronę (razem ok. 6 260 zł/os.)."
_f["options"][0]["out"].append(night("🛏 Nocleg w Manili, w poniedziałek lot krajowy (np. Puerto Princesa 1 h 30, Caticlan/Boracay 1 h 10)"))
_f.update(price="ok. 6 260 zł", price_note="Turkish z Krakowa w sobotę + lot krajowy",
  summary="Najpiękniejsze plaże i najpewniejsza pogoda (pora sucha). Z Krakowa tylko Turkish w sobotę – wyraźnie drożej. Tańszy Korean Air lata z Wiednia w piątek wieczorem – nie do zdążenia po pracy.",
  chips=[("ok","Bez Zatoki"),("ok","Najlepsze plaże"),("warn","Drogo"),("warn","Nocleg w Manili po drodze")],
  extra="Tańsza opcja (Korean Air z Wiednia przez Seul, ok. 4 150 zł/os. z lotem krajowym) startuje w piątek o 19:30 z Wiednia – po pracy w Krakowie nierealne. Na Boracay w lutym czasem wieje i są fale po wschodniej stronie wyspy. Do El Nido z Puerto Princesa 5–6 h busem.")

_t = _d("tajlandia"); _t["options"] = [o for o in _t["options"] if not o["title"].startswith("Condor")]
_t["options"][0].update(tag="Najlepsza opcja", why="Prosto z Krakowa, jedna przesiadka w Stambule, powrót w niedzielę rano. Dalej na Phuket ok. 220 zł/os. w jedną stronę (razem ok. 4 790 zł/os.). EcoFly: 8 kg kabinowa + torba.")
_t["options"][0]["out"].append(night("✈ Dalej lot krajowy Bangkok → Phuket (1 h 30) albo Krabi, najlepiej z zapasem"))
_t.update(price="ok. 4 790 zł", price_note="Turkish z Krakowa w sobotę + lot na Phuket",
  summary="Sprawdzony kierunek, najlepsza pora roku. Z Krakowa Turkish w sobotę przez Stambuł, powrót w niedzielę rano.",
  chips=[("ok","Bez Zatoki"),("ok","Powrót w niedzielę"),("warn","Wylot w sobotę"),("warn","Osobny bilet na lot krajowy")],
  extra="Najtańszy lot bez Zatoki (Condor z Wiednia, ok. 3 700 zł/os. z Phuketem) startuje w piątek o 17:10 z Wiednia – po pracy w Krakowie nierealne.")

_l = _d("laos")
_l["options"] = [dict(title="Turkish do Bangkoku + Bangkok Airways do Luang Prabang", gulf=False, pp="ok. 6 700 zł",
    why="Lot Bangkok–Luang Prabang to ok. 1 175 zł/os. w jedną stronę.",
    out_title="Tam: sob 20.02 → pn 22.02", out=[
     dep("19:25","19:25","sob 20.02 · wylot z Krakowa (jak Tajlandia, przez Stambuł)"), arr("15:05","09:05","nd 21.02 · Bangkok"),
     night("🛏 Nocleg w Bangkoku"), dep("10:55","04:55","pn 22.02 · Bangkok Airways"), arr("13:05","07:05","pn 22.02 · Luang Prabang")],
    back_title="Powrót: przez Bangkok, Kraków nd 7.03 8:20", back=[])]
_l.update(price="ok. 6 700 zł", price_note="przez Bangkok")
_d("sri-lanka")["options"][2]["p7"] = "+ pociąg Kraków–Warszawa"

# ---------- travel-time stats per option title: (total, in the air, transfers, extra note) ----------
STATS = {
 "Air Arabia z Krakowa, przez Szardżę": (("11 h 05 min","10 h 05 min","1 h",""),("13 h 10 min","11 h 05 min","2 h 05 min","")),
 "Air Arabia z Krakowa, wylot w sobotę": (("11 h 50 min","10 h 05 min","1 h 45 min",""),("13 h 10 min","11 h 05 min","2 h 05 min","")),
 "flydubai z Warszawy, przez Dubaj": (("15 h 20 min","10 h 40 min","4 h 40 min","+ ok. 2 h 30 min pociągiem Kraków–Warszawa"),("14 h 25 min","12 h","2 h 25 min","+ pociąg do Krakowa")),
 "KLM + IndiGo z Krakowa, przez Amsterdam i Indie": (("22 h","","2 przesiadki",""),("17 h 55 min","","2 przesiadki","")),
 "Lufthansa + Malaysia Airlines przez Frankfurt i Singapur, potem lot na Borneo": (("18 h 40 min do Kuala Lumpur","15 h 45 min","2 h 55 min","+ nocleg w KL i 2 h 40 min lotu na Borneo"),("16 h 40 min z Kuala Lumpur","14 h 40 min","2 h","+ wcześniej 2 h 40 min lotu z Borneo i czekanie w KL")),
 "Austrian + Malaysia Airlines przez Wiedeń i Bangkok": (("19 h 50 min do Kuala Lumpur","13 h 25 min","6 h 25 min","+ nocleg w KL i lot na Borneo"),("16 h 40 min z Kuala Lumpur","14 h 40 min","2 h","")),
 "Turkish Airlines z Krakowa, przez Stambuł": (("15 h 15 min","13 h 10 min","2 h 05 min","+ ok. 3–4 h koleją i autem na południe"),("17 h 20 min","15 h 10 min","2 h 10 min","")),
 "Lufthansa + China Airlines z Krakowa do Kaohsiung (południe)": (("20 h 10 min","14 h 50 min","5 h 20 min",""),("22 h 35 min","16 h 45 min","5 h 50 min","")),
 "Turkish Airlines z Krakowa, wylot w sobotę": (("15 h 45 min","13 h 50 min","1 h 55 min","+ nocleg w Manili i lot krajowy"),("17 h 45 min","15 h 30 min","2 h 15 min","")),
 "Lufthansa + Malaysia Airlines do Kuala Lumpur, potem AirAsia do Siem Reap": (("18 h 40 min do Kuala Lumpur","15 h 45 min","2 h 55 min","+ nocleg w KL i 2 h 05 min lotu do Siem Reap"),("16 h 40 min z Kuala Lumpur","14 h 40 min","2 h","+ wcześniej lot z Siem Reap do KL")),
 "Turkish Airlines z Krakowa do Kantonu, potem China Southern do Sanyi": (("14 h 10 min do Kantonu","12 h 25 min","1 h 45 min","+ 5 h 35 min czekania w Kantonie i 1 h 45 min lotu do Sanyi"),("16 h 05 min z Kantonu","14 h","2 h 05 min","+ wcześniej lot z Sanyi do Kantonu")),
 "KLM + Vietnam Airlines z Krakowa, przez Amsterdam i Singapur": (("20 h 05 min","16 h 45 min","3 h 20 min","+ lot na Phu Quoc (1 h)"),("22 h 15 min","17 h 25 min","4 h 50 min","")),
 "Turkish do Bangkoku + Bangkok Airways do Luang Prabang": (("13 h 40 min do Bangkoku","11 h 50 min","1 h 50 min","+ nocleg w Bangkoku i 2 h 10 min lotu"),None),
}
# Thailand Turkish has the same title as the Philippines one; stats keyed by (slug,title) override:
STATS_BY_SLUG = {("tajlandia","Turkish Airlines z Krakowa, wylot w sobotę"): (("13 h 40 min do Bangkoku","11 h 50 min","1 h 50 min","+ lot krajowy na Phuket (1 h 30)"),None)}

def stats_html(st):
    if not st: return ""
    total, air, tr, extra = st
    cells = f'<div class="st tot"><span>Cała podróż</span><b>{total}</b></div>'
    if air: cells += f'<div class="st"><span>✈ W samolocie</span><b>{air}</b></div>'
    cells += f'<div class="st"><span>⏱ Przesiadki</span><b>{tr}</b></div>'
    ex = f'<div class="stx">{extra}</div>' if extra else ''
    return f'<div class="stats">{cells}</div>{ex}'

# ---------- booking links: (slug, option index) -> (Google Flights query, airline name, airline URL) ----------
P = "4 adults 3 children"
AL = {
 "Air Arabia": "https://www.airarabia.com/pl", "flydubai": "https://www.flydubai.com/pl/",
 "KLM": "https://www.klm.pl/", "Lufthansa": "https://www.lufthansa.com/pl/pl/homepage",
 "Austrian": "https://www.austrian.com/pl/pl/homepage", "Turkish Airlines": "https://www.turkishairlines.com/pl-pl/",
 "Korean Air": "https://www.koreanair.com/", "Condor": "https://www.condor.com/pl/",
 "AirAsia": "https://www.airasia.com/", "China Airlines": "https://www.china-airlines.com/pl/pl",
}
BOOK = {
 ("sri-lanka",1): (f"Flights from KRK to CMB on 2027-02-19 return 2027-03-07 {P} Air Arabia", "Air Arabia"),
 ("sri-lanka",2): (f"Flights from KRK to CMB on 2027-02-20 return 2027-03-07 {P} Air Arabia", "Air Arabia"),
 ("sri-lanka",3): (f"Flights from WAW to CMB on 2027-02-19 return 2027-03-07 {P} flydubai", "flydubai"),
 ("sri-lanka",4): (f"Flights from KRK to CMB on 2027-02-20 return 2027-03-07 {P} KLM", "KLM"),
 ("malezja-borneo",1): (f"Flights from KRK to KUL on 2027-02-19 return 2027-03-07 {P} Lufthansa", "Lufthansa"),
 ("malezja-borneo",2): (f"Flights from KRK to KUL on 2027-02-19 return 2027-03-07 {P} Austrian", "Austrian"),
 ("tajwan",1): (f"Flights from KRK to TPE on 2027-02-20 return 2027-03-06 {P} Turkish Airlines", "Turkish Airlines"),
 ("tajwan",2): (f"Flights from KRK to KHH on 2027-02-19 return 2027-03-07 {P} Lufthansa", "Lufthansa"),
 ("filipiny",1): (f"Flights from KRK to MNL on 2027-02-20 return 2027-03-06 {P} Turkish Airlines", "Turkish Airlines"),
 ("tajlandia",1): (f"Flights from KRK to BKK on 2027-02-20 return 2027-03-06 {P} Turkish Airlines", "Turkish Airlines"),
 ("kambodza",1): (f"Flights from KRK to KUL on 2027-02-19 return 2027-03-07 {P} Lufthansa", "Lufthansa"),
 ("chiny-hainan",1): (f"Flights from KRK to CAN on 2027-02-20 return 2027-03-06 {P} Turkish Airlines", "Turkish Airlines"),
 ("wietnam",1): (f"Flights from KRK to SGN on 2027-02-19 return 2027-03-07 {P} KLM", "KLM"),
 ("laos",1): (f"Flights from KRK to BKK on 2027-02-20 return 2027-03-06 {P} Turkish Airlines", "Turkish Airlines"),
}
from urllib.parse import quote
def book_html(slug, i):
    b = BOOK.get((slug, i))
    if not b: return ""
    q, al = b
    gf = "https://www.google.com/travel/flights?hl=pl&curr=PLN&q=" + quote(q)
    return (f'<div class="book"><a class="gf" href="{gf}" target="_blank" rel="noopener">Sprawdź i zarezerwuj (Google Flights) →</a>'
            f'<a class="al" href="{AL[al]}" target="_blank" rel="noopener">Strona {al}</a></div>'
            '<p class="note">Link otwiera wyszukiwanie z naszymi lotniskami, datami i 7 pasażerami (wpisz potem wiek dzieci). Przewoźnicy nie pozwalają linkować prosto do wybranego lotu.</p>')

# ---------- rendering ----------
CSS = open(OUT / "style.css").read() if (OUT / "style.css").exists() else ""

def page(title, body, back=False):
    nav = '<a class="back" href="index.html">← Wszystkie kierunki</a>' if back else ''
    return f'''<!doctype html><html lang="pl"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex, nofollow">
<meta http-equiv="Cache-Control" content="no-cache"><title>{html.escape(title)}</title>
<link rel="stylesheet" href="style.css?v=d"></head><body>
<header><div class="wrap">{nav}<h1>{title}</h1>
<div class="chips"><span class="chip">19.02 – 7.03.2027</span><span class="chip">ceny z {UPDATED}, za osobę</span></div>
</div></header><div class="wrap">{body}
<footer><p>Google Flights, {UPDATED}: w obie strony, najtańsza taryfa (bagaż podręczny), dziecko = dorosły.</p>
<p><a href="info.html">Zatoka Perska · rezygnacja i ubezpieczenie · bagaż</a> · Ostatnia aktualizacja: {UPDATED}</p></footer>
</div></body></html>'''

def chip_html(chips):
    return ''.join(f'<span class="flag {k}">{"✓" if k=="ok" else "!" if k=="warn" else "✕"} {html.escape(t)}</span>' for k, t in chips)

def tile(d):
    if d.get("pending"):
        return f'''<div class="tile pending"><div class="tflag">{d["flag"]}</div><h2>{d["name"]}</h2><p class="place">{d["place"]}</p>
<p>{d["summary"]}</p><span class="btn disabled">W przygotowaniu</span></div>'''
    cls = "tile notrec" if d.get("notrec") else "tile"
    return f'''<a class="{cls}" href="{d["slug"]}.html"><div class="tflag">{d["flag"]}</div>
<h2>{d["name"]}</h2><p class="place">{d["place"]}</p>
<div class="tprice"><b>{d["price"]}</b><span>za osobę, w obie strony · {d["price_note"]}</span></div>
<p>{d["summary"]}</p>
<div class="facts"><div>🕐 Różnica czasu: <b>{TZ[d["slug"]]}</b></div><div>🌡 {d["weather"]}</div><div>🌊 Morze: {d["sea"]}</div><div>🛂 {d["entry"]}</div></div>
<div class="flags">{chip_html(d["chips"])}</div>
<span class="btn">Zobacz loty i szczegóły →</span></a>'''

def tl(items):
    out = ['<ul class="tl">']
    for it in items:
        k = it[0]
        if k == "fly": out.append(f'<li class="fly"><div class="d">✈ {it[1]}</div></li>')
        elif k == "night": out.append(f'<li class="night"><div class="nbox">{it[1]}</div></li>')
        else:
            t, pl, d = it[1], it[2], it[3]
            tt = f'<span class="t">{t}</span>' if t else ''
            pp = f'<span class="pl">PL {pl}</span>' if pl else ''
            box = f'<div class="box">⏱ {it[4]}</div>' if k == "stop" and len(it) > 4 and it[4] else ''
            out.append(f'<li class="{k}">{tt}{pp}<div class="d">{d}</div>{box}</li>')
    out.append('</ul>')
    return ''.join(out)

def option(o, i, slug=''):
    badge = f'<span class="badge">{o["tag"]}</span> ' if o.get("tag") else f'<span class="badge num">Opcja {i}</span> '
    g = GULF if o["gulf"] else NOGULF
    parts = [f'<div class="card {"best" if i==1 else ""}">{badge}{g}<h3 class="otitle">{o["title"]}</h3>',
             f'<div class="price"><div><b>{o["pp"]}</b><span>za osobę, w obie strony{" · " + o["p7"] if str(o.get("p7","")).startswith("+") else ""}</span></div></div>',
             f'<p class="why">{o["why"]}</p>']
    if o.get("out"):
        st = STATS_BY_SLUG.get((slug, o["title"])) or STATS.get(o["title"])
        parts.append(f'<div class="leg-title"><h4>{o["out_title"]}</h4></div>{stats_html(st[0] if st else None)}{tl(o["out"])}')
        if o.get("out_bio"): parts.append(f'<div class="bio">🌙 <b>Dla organizmu:</b> {o["out_bio"]}</div>')
    st = STATS_BY_SLUG.get((slug, o["title"])) or STATS.get(o["title"])
    parts.append(f'<div class="leg-title"><h4>{o["back_title"]}</h4></div>{stats_html(st[1] if st and o.get("back") else None)}')
    if o.get("back"): parts.append(tl(o["back"]))
    if o.get("back_bio"): parts.append(f'<div class="bio">🌙 <b>Dla organizmu:</b> {o["back_bio"]}</div>')
    if o.get("note"): parts.append(f'<p class="note">{o["note"]}</p>')
    parts.append(book_html(slug, i))
    parts.append('</div>')
    return ''.join(parts)

def detail(d):
    body = [f'<div class="card intro"><div class="flags">{chip_html(d["chips"])}</div>',
            f'<p class="place big">{d["place"]}</p><p>{d["summary"]}</p>',
            f'<div class="facts row3"><div><b>Różnica czasu</b><br>{TZ[d["slug"]]} względem Polski</div><div><b>Pogoda 20.02–7.03</b><br>{d["weather"]}</div><div><b>Morze</b><br>{d["sea"]}</div><div><b>Wjazd dla Polaków</b><br>{d["entry"]}</div></div></div>',
            '<h2>Loty – od najlepszego</h2><p class="note">Godziny lokalne; na szaro czas polski.</p>']
    for i, o in enumerate(d["options"], 1): body.append(option(o, i, d['slug']))
    if d.get("extra"): body.append(f'<div class="callout info">{d["extra"]}</div>')
    body.append('<div class="callout"><a href="info.html">Zatoka, ubezpieczenie, bagaż →</a></div>')
    return page(f'{d["flag"]} {d["name"]}', ''.join(body), back=True)

def index(dests):
    tiles = ''.join(tile(d) for d in dests)
    body = f'''<div class="tiles">{tiles}</div>
<div class="callout warn"><a href="info.html">Zatoka Perska, rezygnacja i ubezpieczenie, bagaż →</a></div>
<h2>Kierunki, których nie bierzemy pod uwagę</h2>
<div class="card rejected">
<h3>Odrzucone przez nas</h3>
<ul>
<li><b>🇮🇳 Indie</b> – niedawno byliśmy.</li>
<li><b>🇻🇳 Wietnam</b> – niedawno byliśmy.</li>
<li><b>🇮🇩 Bali</b> – obie rodziny już były; tłok i bardzo dużo turystów.</li>
<li><b>🇲🇾 Langkawi</b> – niedawno byliśmy (Malezja zostaje, ale Borneo).</li>
<li><b>🇲🇲 Birma (Mjanma)</b> – trwa wojna.</li>
<li><b>Przesiadki w Zatoce Perskiej</b> (Dubaj, Szardża, Abu Zabi, Doha) – tylko tam, gdzie nie ma sensownej alternatywy (Sri Lanka), zawsze z oznaczeniem.</li>
<li><b>Wyloty z Wiednia w piątek</b> – po pracy w Krakowie nie da się zdążyć.</li>
</ul>
<h3>Odpadają w tym terminie (pogoda, bezpieczeństwo)</h3>
<ul>
<li><b>Chiny – Guilin / Yangshuo, Kanton</b> – w lutym 7–14°C (Kanton 17–22°C) i mżawki.</li>
<li><b>Tajwan – północ (Tajpej)</b> – 17–20°C i deszcz; tylko na 2–3 dni miasta, na plażę południe.</li>
<li><b>Malezja – wschodnie wybrzeże (Perhentian, Tioman)</b> – monsun do połowy marca, wyspy często zamknięte.</li>
<li><b>🇱🇦 Laos</b> – od początku marca smog z wypalania pól, drogie loty (zostawiony na końcu kafelków dla porównania).</li>
<li><b>Seul / Japonia</b> – w lutym mróz; Seul tylko jako przesiadka.</li>
</ul>
</div>'''
    return page("Ferie 2027: dokąd w Azji?", body)

INFO = open(OUT / "info_body.html").read() if (OUT / "info_body.html").exists() else ""

if __name__ == "__main__":
    order = [DEST[0], DEST[1], DEST[2], DEST[3], INDO_PENDING, DEST[4], DEST[5], DEST[6], DEST[8]]  # Vietnam (DEST[7]) rejected: been there recently
    (OUT / "index.html").write_text(index(order))
    for d in DEST: (OUT / f'{d["slug"]}.html').write_text(detail(d))
    (OUT / "info.html").write_text(page("Bezpieczeństwo, rezygnacja, bagaż", INFO, back=True))
    print("built", len(DEST) + 2, "pages")
