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


DEST.append(dict(slug="indonezja", flag="🇮🇩", name="Indonezja – Lombok i Flores", place="Gili (bez samochodów), Komodo, opcjonalnie Yogyakarta", gulf=False,
  price="ok. 5 080 zł", price7="", price_note="Lufthansa do Singapuru + Scoot na Lombok",
  summary="Spokojniejsza „Bali sprzed 20 lat”: Gili Air/Meno z żółwiami przy plaży, puste plaże południa Lomboka, opcjonalnie 4–5 dni Komodo. Po drodze noc w Singapurze.",
  weather="🌦 pora deszczowa: krótkie ulewy, 24–31°C, 6–8 h słońca", sea="29°C", entry="e-VOA ok. 120 zł/os. (zapowiedziana podwyżka); karta przyjazdu online",
  chips=[("ok","Bez Zatoki"),("ok","Mało turystów"),("warn","Pora deszczowa"),("warn","Noc w Singapurze, osobne bilety"),("warn","Powrót w poniedziałek")],
  options=[
   dict(title="Lufthansa Kraków ↔ Singapur + Scoot na Lombok", tag="Najlepsza opcja", gulf=False, pp="ok. 5 080 zł",
    why="Lufthansa w obie strony 3 902 zł + Scoot tam 548 zł i z powrotem 629 zł. Wieczór i noc w Singapurze (Gardens by the Bay). Taryfy: Lufthansa Light 8 kg podręcznego, Scoot Fly 10 kg.",
    out_title="Tam: pt 19.02 → nd 21.02", out=[
     dep("19:05","19:05","pt 19.02 · wylot z Krakowa, LH 1369"),
     stop("20:45","20:45","Frankfurt (Niemcy)","Przesiadka <b>55 min</b>"),
     stop("21:40","21:40","wylot, LH 780 (nocny)"), fly("lot 12 h 25 min"),
     arr("17:05","10:05","sob 20.02 · Singapur · Polska + 7 h"),
     night("🛏 Nocleg w Singapurze"),
     dep("06:55","sob 23:55","nd 21.02 · Scoot TR 366"), fly("lot 2 h 55 min"),
     arr("09:50","02:50","nd 21.02 · Lombok (LOP), Indonezja · Polska + 7 h"),
     night("🚐 Na Gili: ok. 2 h autem do portu + 15 min łódką")],
    out_bio="Lot nocny w polską noc, w Singapurze wieczór i normalna noc w hotelu – jetlag rozkłada się na dwa dni.",
    back_title="Powrót: nd 7.03 → pn 8.03", back=[
     dep("10:25","03:25","nd 7.03 · Lombok, Scoot TR 367"),
     stop("13:20","06:20","Singapur","<b>10 h 35 min</b> – lotnisko Jewel (wodospad, place zabaw) albo pół dnia w mieście"),
     stop("23:55","16:55","wylot, LH 781 (nocny)"), fly("lot 13 h 20 min"),
     stop("06:15","06:15","pn 8.03 · Frankfurt","Przesiadka <b>1 h 45 min</b>"),
     arr("09:35","09:35","pn 8.03 · Kraków")],
    back_bio="W domu w poniedziałek rano – dzieci tracą poniedziałek. Spokojniej: Scoot z Lomboka w sobotę 6.03 o 17:30 i niedziela w Singapurze.",
    note="Scoot to osobny bilet – przy spóźnieniu nikt nie przebukuje; dlatego noc w Singapurze w drodze tam i zapas w drodze powrotnej."),
   dict(title="Flores (Komodo) 4–5 dni + Lombok", gulf=False, pp="ok. 5 500 zł",
    why="Lufthansa 3 902 zł + Scoot do Labuan Bajo 570 zł + Wings Air Labuan Bajo → Lombok 402 zł + Scoot z Lomboka 629 zł. Smoki z Komodo, różowa plaża, manty – przy fali rejsy bywają przesuwane, warto mieć dzień zapasu.",
    out_title="Tam: pt 19.02 → nd 21.02", out=[
     dep("19:05","19:05","pt 19.02 · Kraków → Frankfurt → Singapur (jak wyżej)"),
     arr("17:05","10:05","sob 20.02 · Singapur"), night("🛏 Nocleg w Singapurze"),
     dep("14:30","07:30","nd 21.02 · Scoot do Labuan Bajo"), fly("lot 3 h 25 min"),
     arr("17:55","10:55","nd 21.02 · Labuan Bajo (Flores)"),
     night("✈ W połowie pobytu: Wings Air Labuan Bajo 09:20 → Lombok 10:40 (codziennie)")],
    back_title="Powrót: jak w opcji 1 (z Lomboka, Kraków pn 8.03 9:35)", back=[]),
   dict(title="Turkish Kraków ↔ Singapur w sobotę + Scoot", gulf=False, pp="ok. 4 770 zł",
    why="Najtaniej i powrót w niedzielę rano, ale na Lombok dopiero w poniedziałek po południu. Cena Turkish (ok. 3 670 zł) z wyszukiwania dla 1 osoby – dla 7 może być nieco wyższa.",
    out_title="Tam: sob 20.02 → pn 22.02", out=[
     dep("19:25","19:25","sob 20.02 · wylot z Krakowa, TK 1274"),
     stop("23:50","21:50","Stambuł (Turcja)","Przesiadka <b>2 h</b>"),
     stop("01:50","23:50","wylot, TK 54 (nocny)"),
     arr("17:40","10:40","nd 21.02 · Singapur"), night("🛏 Nocleg w Singapurze"),
     dep("14:00","07:00","pn 22.02 · Scoot"), arr("16:55","09:55","pn 22.02 · Lombok")],
    back_title="Powrót: sob 6.03 → nd 7.03", back=[
     dep("17:30","10:30","sob 6.03 · Lombok, Scoot"),
     stop("20:25","13:25","Singapur","Przesiadka <b>2 h 50 min</b> (osobne bilety)"),
     stop("23:15","16:15","wylot, TK 55 (nocny)"),
     stop("05:50","03:50","nd 7.03 · Stambuł","Przesiadka <b>2 h 10 min</b>"),
     arr("08:20","08:20","nd 7.03 · Kraków")]),
   dict(title="Yogyakarta (Borobudur) + Lombok", gulf=False, pp="ok. 5 360 zł",
    why="Kultura na start (Borobudur, Prambanan, wulkan Merapi), potem plaża. Na Jawie szczyt pory deszczowej – zwiedzanie rano.",
    out_title="Tam: pt 19.02 → nd 21.02", out=[
     dep("19:05","19:05","pt 19.02 · Kraków → Frankfurt → Singapur (jak opcja 1)"),
     arr("17:05","10:05","sob 20.02 · Singapur"), night("🛏 Nocleg w Singapurze"),
     dep("08:00","01:00","nd 21.02 · Scoot TR 248 (albo 16:40)"),
     arr("09:30","03:30","nd 21.02 · Yogyakarta (Jawa) · Polska + 6 h"),
     night("✈ W połowie: Yogyakarta 17:45 → Lombok 20:15 (JT 778, 376 zł/os.)")],
    back_title="Powrót: jak w opcji 1 (z Lomboka, Kraków pn 8.03 9:35)", back=[]),
   dict(title="KLM przez Amsterdam i Singapur na Bali (tylko przesiadka) + Wings Air na Lombok", gulf=False, pp="ok. 5 190 zł",
    why="Wylot o 17:35, noc przy lotnisku na Bali (bez zostawania na Bali). Minus: odprawa na Bali, możliwa opłata turystyczna ok. 35 zł/os.",
    out_title="Tam: pt 19.02 → nd 21.02", out=[
     dep("17:35","17:35","pt 19.02 · Kraków, KL 1328"), stop("19:35","19:35","Amsterdam","Przesiadka <b>1 h 10 min</b>"),
     stop("16:15","09:15","sob 20.02 · Singapur","Postój <b>1 h 20 min</b>, ten sam samolot"),
     arr("20:20","13:20","sob 20.02 · Bali (DPS)"), night("🛏 Nocleg przy lotnisku"),
     dep("11:10","04:10","nd 21.02 · Wings Air"), arr("12:00","05:00","nd 21.02 · Lombok")],
    back_title="Powrót: nd 7.03 → pn 8.03", back=[
     dep("16:55","09:55","nd 7.03 · Lombok → Bali"), stop("21:40","14:40","wylot z Bali, KL 836","ok. 4 h na lotnisku na Bali"),
     stop("08:35","08:35","pn 8.03 · Amsterdam","Przesiadka <b>6 h 30 min</b>"),
     arr("17:00","17:00","pn 8.03 · Kraków")]),
  ],
  extra="Na ten termin odradzamy: Yogyakartę jako jedyne miejsce (300–400 mm deszczu w lutym), Manado/Bunaken (wzburzone morze, a jedyny bilet z Krakowa idzie przez Dubaj), Belitung (rejsy często odwoływane), Raja Ampat (2 dni podróży w każdą stronę). Wszędzie w porze deszczowej: repelent z DEET (denga)."))

TZ = {'sri-lanka': '+4 h 30 min', 'malezja-borneo': '+7 h', 'tajwan': '+7 h', 'filipiny': '+7 h', 'tajlandia': '+6 h', 'kambodza': '+6 h', 'chiny-hainan': '+7 h', 'wietnam': '+6 h', 'laos': '+6 h', 'indonezja': '+7 h (Jawa +6 h)', 'kombinacje': '+7 h', 'huby': '+6 h (Bangkok) / +7 h / +8 h (Seul)', 'ekwador': '−6 h (Galápagos −7 h)'}
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
STATS.update({
 "Lufthansa Kraków ↔ Singapur + Scoot na Lombok": (("31 h 45 min","17 h","55 min + noc w Singapurze","+ ok. 2 h 15 min na Gili"),("30 h 10 min","17 h 50 min","12 h 20 min","")),
 "Flores (Komodo) 4–5 dni + Lombok": (("39 h 50 min","17 h 30 min","55 min + noc i przedpołudnie w Singapurze",""),None),
 "Turkish Kraków ↔ Singapur w sobotę + Scoot": (("38 h 30 min","16 h 10 min","2 h + noc i przedpołudnie w Singapurze",""),("21 h 50 min","16 h 50 min","5 h","")),
 "Yogyakarta (Borobudur) + Lombok": (("32 h 25 min","16 h 35 min","55 min + noc w Singapurze",""),None),
 "KLM przez Amsterdam i Singapur na Bali (tylko przesiadka) + Wings Air na Lombok": (("35 h 25 min","18 h 05 min","1 h 10 min + 1 h 20 min + noc na Bali",""),("31 h 05 min","19 h 05 min","12 h","")),
})
STATS_BY_SLUG = {("tajlandia","Turkish Airlines z Krakowa, wylot w sobotę"): (("13 h 40 min do Bangkoku","11 h 50 min","1 h 50 min","+ lot krajowy na Phuket (1 h 30)"),None)}


ROUTE = {
 "Air Arabia z Krakowa, przez Szardżę": "Kraków → Szardża (ZEA) → Kolombo",
 "Air Arabia z Krakowa, wylot w sobotę": "Kraków → Szardża (ZEA) → Kolombo",
 "flydubai z Warszawy, przez Dubaj": "Warszawa → Dubaj (ZEA) → Kolombo",
 "KLM + IndiGo z Krakowa, przez Amsterdam i Indie": "Kraków → Amsterdam → Mumbaj → Kolombo",
 "Lufthansa + Malaysia Airlines przez Frankfurt i Singapur, potem lot na Borneo": "Kraków → Frankfurt → Singapur → Kuala Lumpur → Kota Kinabalu",
 "Austrian + Malaysia Airlines przez Wiedeń i Bangkok": "Kraków → Wiedeń → Bangkok → Kuala Lumpur",
 "Turkish Airlines z Krakowa, przez Stambuł": "Kraków → Stambuł → Tajpej",
 "Lufthansa + China Airlines z Krakowa do Kaohsiung (południe)": "Kraków → Frankfurt → Hongkong → Kaohsiung",
 "Lufthansa + Malaysia Airlines do Kuala Lumpur, potem AirAsia do Siem Reap": "Kraków → Frankfurt → Singapur → Kuala Lumpur → Siem Reap",
 "Turkish Airlines z Krakowa do Kantonu, potem China Southern do Sanyi": "Kraków → Stambuł → Kanton → Sanya",
 "KLM + Vietnam Airlines z Krakowa, przez Amsterdam i Singapur": "Kraków → Amsterdam → Singapur → Sajgon",
 "Turkish do Bangkoku + Bangkok Airways do Luang Prabang": "Kraków → Stambuł → Bangkok → Luang Prabang",
}
ROUTE.update({
 "Lufthansa Kraków ↔ Singapur + Scoot na Lombok": "Kraków → Frankfurt → Singapur (nocleg) → Lombok",
 "Flores (Komodo) 4–5 dni + Lombok": "Kraków → Frankfurt → Singapur (nocleg) → Labuan Bajo → Lombok",
 "Turkish Kraków ↔ Singapur w sobotę + Scoot": "Kraków → Stambuł → Singapur (nocleg) → Lombok",
 "Yogyakarta (Borobudur) + Lombok": "Kraków → Frankfurt → Singapur (nocleg) → Yogyakarta → Lombok",
 "KLM przez Amsterdam i Singapur na Bali (tylko przesiadka) + Wings Air na Lombok": "Kraków → Amsterdam → Singapur → Bali (nocleg) → Lombok",
})
ROUTE_BY_SLUG = {("filipiny","Turkish Airlines z Krakowa, wylot w sobotę"): "Kraków → Stambuł → Manila → Palawan / Boracay",
                 ("tajlandia","Turkish Airlines z Krakowa, wylot w sobotę"): "Kraków → Stambuł → Bangkok → Phuket"}
def route_of(slug, o): return ROUTE_BY_SLUG.get((slug, o["title"])) or ROUTE.get(o["title"], "")

def stats_html(st):
    if not st: return ""
    total, air, tr, extra = st
    cells = f'<div class="st tot"><span>Cała podróż</span><b>{total}</b></div>'
    if air: cells += f'<div class="st"><span>✈ W samolocie</span><b>{air}</b></div>'
    cells += f'<div class="st"><span>⏱ Przesiadki</span><b>{tr}</b></div>'
    ex = f'<div class="stx">{extra}</div>' if extra else ''
    return f'<div class="stats">{cells}</div>{ex}'


# ---------- Malaysia update (deep-dive 24.10 evening) ----------
_m = _d("malezja-borneo")
_lh = _m["options"][0]
_lh.update(pp="ok. 5 000 zł", tag="Najlepsza opcja – piątek",
  why="Lufthansa do Kuala Lumpur 4 311 zł + AirAsia po Borneo ok. 690 zł (KL → Sandakan 281, Sandakan → Kota Kinabalu 98, Kota Kinabalu → KL 311).")
_lh["out"][-3:] = [night("🛏 1–2 noce w Kuala Lumpur"),
  dep("","","AirAsia KL → Sandakan (Sepilok, orangutany) – 3 noce"),
  dep("","","AirAsia Sandakan → Kota Kinabalu – 7–8 nocy (wyspy, plaża, park Kinabalu)")]
_lh["back"][0] = dep("po południu","","nd 7.03 · AirAsia Kota Kinabalu → Kuala Lumpur (2 h 40 min)")
_tk = dict(title="Turkish Airlines przez Stambuł, sobota → sobota", tag="Powrót w niedzielę rano", gulf=False, pp="do ok. 5 410 zł",
  why="Suma dwóch biletów w jedną stronę (2 699 + 2 019 zł) + AirAsia po Borneo ok. 690 zł. Bilet w obie strony powinien wyjść taniej (Google nie pokazał go przez przeciążenie). EcoFly bez walizki (z walizką ok. +290 zł).",
  out_title="Tam: sob 20.02 → nd 21.02", out=[
   dep("19:25","19:25","sob 20.02 · Kraków, TK 1274"),
   stop("23:50","21:50","Stambuł (Turcja)","Przesiadka <b>2 h</b>"),
   stop("01:50","23:50","wylot, TK 60 (nocny)"),
   arr("17:20","10:20","nd 21.02 · Kuala Lumpur · Polska + 7 h"),
   night("🛏 1–2 noce w KL, potem AirAsia na Borneo (jak w opcji 1)")],
  back_title="Powrót: sob 6.03 → nd 7.03", back=[
   dep("23:45","16:45","sob 6.03 · Kuala Lumpur, TK 61 (nocny)"),
   stop("ok. 06:10","ok. 04:10","nd 7.03 · Stambuł","Przesiadka <b>1 h 50 min</b>"),
   stop("08:00","06:00","wylot, TK 1271"),
   arr("08:20","08:20","nd 7.03 · Kraków")],
  back_bio="W domu w niedzielę rano – dzieci nie tracą szkoły.")
_fi = dict(title="Finnair do Singapuru w niedzielę + AirAsia na Borneo, powrót Lufthansą", gulf=False, pp="ok. 4 510 zł",
  why="Najtańszy długi lot (Finnair 1 846 zł) + AirAsia Singapur ↔ Kota Kinabalu (364 + 349 zł) + Lufthansa z Singapuru 1 948 zł. Cztery osobne bilety, wylot dopiero w niedzielę.",
  out_title="Tam: nd 21.02 → pn 22.02", out=[
   dep("18:55","18:55","nd 21.02 · Kraków, AY 1166"), stop("","","Helsinki (Finlandia)","Przesiadka"),
   arr("18:40","11:40","pn 22.02 · Singapur"), night("🛏 Nocleg w Singapurze, potem AirAsia do Kota Kinabalu")],
  back_title="Powrót: nd 7.03 → pn 8.03", back=[
   dep("","","nd 7.03 · AirAsia Kota Kinabalu → Singapur"),
   dep("23:55","16:55","nd 7.03 · Singapur, LH 781 (nocny)"), stop("06:15","06:15","pn 8.03 · Frankfurt","Przesiadka <b>1 h 45 min</b>"),
   arr("09:35","09:35","pn 8.03 · Kraków")])
_au = _m["options"][1]
_au.update(title="Austrian + Malaysia Airlines przez Wiedeń i Bangkok, w niedzielę", pp="ok. 5 030 zł",
  why="Tam 2 318 zł (nd 21.02, 14:45 z Krakowa – w sobotę nie lata), powrót Turkish w sobotę nocą 2 019 zł, plus AirAsia po Borneo. Albo powrót nd 7.03 KL 8:15 → Warszawa 18:15 (1 148 zł) – razem ok. 4 290 zł + pociąg.",
  out_title="Tam: nd 21.02 → pn 22.02")
for it in _au["out"]:
    pass
_au["out"] = [dep("14:45","14:45","nd 21.02 · Kraków, OS 680"), stop("15:45","15:45","Wiedeń","Przesiadka <b>4 h 30 min</b>"),
  stop("12:20","06:20","pn 22.02 · Bangkok (Tajlandia)","Przesiadka <b>1 h 55 min</b>"), arr("17:35","10:35","pn 22.02 · Kuala Lumpur")]
_au["back_title"] = "Powrót: jak Turkish (Kraków nd 7.03 8:20)"
_m["options"] = [_lh, _tk, _fi, _au]
_m.update(price="ok. 5 000 zł", price_note="z lotami po Borneo",
  place="Borneo (Sabah): orangutany w Sepilok, wyspy przy Kota Kinabalu",
  summary="KL 1–2 noce → Sandakan/Sepilok 3 noce (orangutany) → Kota Kinabalu 7–8 nocy (wyspy parku Tunku Abdul Rahman, plaża, park Kinabalu). Pora sucha – najbliżej klimatu Perhentian.",
  chips=[("ok","Bez Zatoki"),("ok","Pora sucha na Borneo"),("ok","Piątek albo sobota z Krakowa"),("warn","Loty krajowe – osobne bilety")],
  extra="Wschodnie wybrzeże (Perhentian, Redang, Tioman, Kapas) w tym terminie odpada: Perhentian Kecil otwiera się ok. 15–20 marca, Redang od ok. 1 marca, łodzie i morze jeszcze niepewne. Kraków–Bangkok bezpośrednio nie ma (bezpośrednio tylko LOT z Warszawy). Bilet prosto do Kota Kinabalu albo Penang – ok. 2× drożej niż KL + AirAsia. Alternatywa bez Borneo: Cameron Highlands + Penang (plaże słabsze).")
STATS["Turkish Airlines przez Stambuł, sobota → sobota"] = (("14 h 55 min do KL","12 h 55 min","2 h","+ noc w KL i loty po Borneo"),("15 h 35 min","13 h 45 min","1 h 50 min","+ wcześniej lot z Kota Kinabalu do KL"))
STATS["Finnair do Singapuru w niedzielę + AirAsia na Borneo, powrót Lufthansą"] = (("16 h 45 min do Singapuru","","1 przesiadka","+ noc w Singapurze i lot na Borneo"),("16 h 40 min z Singapuru","14 h 55 min","1 h 45 min",""))
STATS["Austrian + Malaysia Airlines przez Wiedeń i Bangkok, w niedzielę"] = STATS.pop("Austrian + Malaysia Airlines przez Wiedeń i Bangkok")
ROUTE["Lufthansa + Malaysia Airlines przez Frankfurt i Singapur, potem lot na Borneo"] = "Kraków → Frankfurt → Singapur → Kuala Lumpur → Sandakan → Kota Kinabalu"
ROUTE["Turkish Airlines przez Stambuł, sobota → sobota"] = "Kraków → Stambuł → Kuala Lumpur → Borneo"
ROUTE["Finnair do Singapuru w niedzielę + AirAsia na Borneo, powrót Lufthansą"] = "Kraków → Helsinki → Singapur → Kota Kinabalu"
ROUTE["Austrian + Malaysia Airlines przez Wiedeń i Bangkok, w niedzielę"] = ROUTE.pop("Austrian + Malaysia Airlines przez Wiedeń i Bangkok")


DEST.append(dict(slug="kombinacje", flag="🧭", name="Kombinacje: tam do jednego miasta, z powrotem z innego", place="np. Hongkong → Borneo → Singapur", gulf=False,
  price="od ok. 4 150 zł", price7="", price_note="wszystkie loty, bez hoteli",
  summary="Długi lot do jednego wielkiego miasta, powrót z innego, a w środku tanie loty lokalne. Najczęściej Turkish w sobotę 19:25 z Krakowa i powrót w niedzielę 8:20.",
  weather="zależy od planu – Borneo sucho, Palawan sucho, Tajwan chłodniej, Lombok deszczowo", sea="24–30°C", entry="zależy od krajów – patrz kafelki krajów",
  chips=[("ok","Bez Zatoki"),("ok","Powrót w niedzielę rano"),("ok","2–3 różne miejsca"),("warn","Loty lokalne – osobne bilety")],
  options=[
   dict(title="Hongkong → Borneo (Kota Kinabalu) → Singapur", tag="Najlepszy plan", gulf=False, pp="ok. 4 270 zł",
    why="Turkish Kraków → Hongkong, Singapur → Kraków na jednym bilecie 3 500 zł + HK Express Hongkong → Kota Kinabalu 419 zł + AirAsia Kota Kinabalu → Singapur 348 zł. Trzy światy: miasto, przyroda i plaża, miasto-ogród.",
    out_title="Tam: sob 20.02 → nd 21.02", out=[
     dep("19:25","19:25","sob 20.02 · Kraków, TK 1274"),
     stop("23:50","21:50","Stambuł (Turcja)","Przesiadka <b>1 h 55 min</b>"),
     stop("01:45","23:45","wylot (nocny)"), fly("lot ok. 10 h 20 min"),
     arr("17:05","10:05","nd 21.02 · Hongkong · Polska + 7 h"),
     night("🛏 2 noce w Hongkongu (Victoria Peak, Ocean Park / Disneyland)"),
     dep("21:30","14:30","wt 23.02 · HK Express do Kota Kinabalu (albo AirAsia 13:15)"), arr("00:35","17:35","śr 24.02 · Kota Kinabalu, Borneo"),
     night("🏝 9 nocy na Borneo: wyspy Tunku Abdul Rahman, plaże, orangutany w Sepilok"),
     dep("09:05","02:05","czw 4.03 · AirAsia do Singapuru"), arr("11:30","04:30","Singapur"),
     night("🛏 2 noce w Singapurze (Gardens by the Bay, zoo, Sentosa)")],
    back_title="Powrót: sob 6.03 → nd 7.03", back=[
     dep("23:15","16:15","sob 6.03 · Singapur (Turkish, nocny)"),
     stop("05:50","03:50","nd 7.03 · Stambuł","Przesiadka <b>2 h 10 min</b>"),
     stop("08:00","06:00","wylot, TK 1271"), arr("08:20","08:20","nd 7.03 · Kraków")],
    back_bio="W domu w niedzielę rano."),
   dict(title="Hongkong → Borneo → Kuala Lumpur (dwa osobne bilety)", tag="Najtańszy", gulf=False, pp="ok. 4 150 zł",
    why="Lufthansa Kraków → Hongkong 1 682 zł + Turkish Kuala Lumpur → Kraków 1 742 zł + Hongkong → Kota Kinabalu 419 zł + Kota Kinabalu → KL 311 zł. Ten sam lot Lufthansy w piątek 19.02: +370 zł/os. Powrót nocny (nd rano): +276 zł/os.",
    out_title="Tam: sob 20.02 → nd 21.02", out=[
     dep("19:05","19:05","sob 20.02 (albo pt 19.02) · Kraków, LH 1369"),
     stop("20:45","20:45","Frankfurt","Przesiadka <b>1 h 05 min</b>"),
     stop("21:50","21:50","wylot, LH 796 (nocny)"), fly("lot 11 h 40 min"),
     arr("16:30","09:30","nd 21.02 · Hongkong"),
     night("🛏 2 noce w Hongkongu → 8 nocy w Kota Kinabalu → 2–3 noce w Kuala Lumpur")],
    back_title="Powrót: sob 6.03", back=[
     dep("08:15","01:15","sob 6.03 · Kuala Lumpur, TK 63"),
     stop("14:40","12:40","Stambuł","Przesiadka <b>3 h 35 min</b>"),
     arr("18:30","18:30","sob 6.03 · Kraków")],
    back_bio="W domu w sobotę wieczorem – cała niedziela na odpoczynek."),
   dict(title="Tajwan (Tajpej + Kenting) → Hongkong", gulf=False, pp="ok. 4 190 zł",
    why="Turkish Kraków → Tajpej, Hongkong → Kraków 3 835 zł + HK Express Kaohsiung → Hongkong 353 zł + szybka kolej Tajpej → Kaohsiung (ok. 180 zł, dzieci taniej). Najchłodniej z planów.",
    out_title="Tam: sob 20.02 → nd 21.02", out=[
     dep("19:25","19:25","sob 20.02 · Kraków, TK 1274"),
     stop("23:50","21:50","Stambuł","Przesiadka <b>2 h 05 min</b>"),
     arr("17:40","10:40","nd 21.02 · Tajpej"),
     night("🛏 3 noce Tajpej → kolej do Kaohsiung + 1,5–2 h → 7 nocy Kenting → lot do Hongkongu, 3 noce")],
    back_title="Powrót: sob 6.03 → nd 7.03", back=[
     dep("23:15","16:15","sob 6.03 · Hongkong (Turkish, nocny)"),
     stop("06:10","04:10","nd 7.03 · Stambuł","Przesiadka <b>1 h 50 min</b>"),
     arr("08:20","08:20","nd 7.03 · Kraków")]),
   dict(title="Singapur → Lombok/Gili → Bali (tylko lotnisko)", gulf=False, pp="ok. 4 470 zł",
    why="Turkish Kraków → Singapur, Denpasar → Kraków 3 818 zł + Scoot Singapur → Lombok 547 zł + szybka łódź na Bali (ok. 100 zł). Pora deszczowa w Indonezji.",
    out_title="Tam: sob 20.02 → nd 21.02", out=[
     dep("19:25","19:25","sob 20.02 · Kraków, TK 1274"),
     stop("23:50","21:50","Stambuł","Przesiadka <b>2 h</b>"),
     arr("17:40","10:40","nd 21.02 · Singapur"),
     night("🛏 2 noce Singapur → Scoot na Lombok (wt 14:00 → 16:55) → ok. 10 nocy Lombok + Gili → łódź na Bali, noc przy lotnisku")],
    back_title="Powrót: sob 6.03 → nd 7.03", back=[
     dep("21:10","14:10","sob 6.03 · Bali (Denpasar), Turkish"),
     stop("05:40","03:40","nd 7.03 · Stambuł","Przesiadka <b>2 h 20 min</b>"),
     arr("08:20","08:20","nd 7.03 · Kraków")]),
   dict(title="Hongkong → Palawan (El Nido) → Manila", gulf=False, pp="ok. 4 770 zł",
    why="Turkish Kraków → Hongkong, Manila → Kraków 4 058 zł + Cebu Pacific Hongkong → Puerto Princesa (przez Manilę) 556 zł + Puerto Princesa → Manila 153 zł. Najpiękniejsze plaże, pora sucha; dużo przesiadek i długi dojazd do El Nido.",
    out_title="Tam: sob 20.02 → nd 21.02", out=[
     dep("19:25","19:25","sob 20.02 · Kraków, TK 1274"),
     stop("23:50","21:50","Stambuł","Przesiadka <b>1 h 55 min</b>"),
     arr("17:05","10:05","nd 21.02 · Hongkong"),
     night("🛏 2 noce Hongkong → wt 11:00 Cebu Pacific → Puerto Princesa 17:10 → 10–11 nocy Palawan")],
    back_title="Powrót: sob 6.03 → nd 7.03", back=[
     dep("10:15","03:15","sob 6.03 · Puerto Princesa → Manila (Cebu Pacific)"),
     dep("21:35","14:35","sob 6.03 · Manila, TK 85"),
     stop("05:45","03:45","nd 7.03 · Stambuł","Przesiadka <b>2 h 15 min</b>"),
     arr("08:20","08:20","nd 7.03 · Kraków")]),
  ],
  extra="Ceny biletów „tam do jednego, z powrotem z innego” z KAYAK (Google liczył je błędnie), loty lokalne z Google; dla 7 osób Turkish wychodzi nawet taniej niż dla 1 dorosłego (zniżka dla dzieci). Zasada przy osobnych biletach: pierwszy lot lokalny nie w dniu przylotu, ostatni dzień przed lotem do Europy. W piątek po 16:00 z Krakowa tylko Lufthansa 19:05 (Hongkong/Singapur ok. 4 600 zł/os. na jednym bilecie). Numery części lotów Turkish między Stambułem a Azją do sprawdzenia przy rezerwacji."))
STATS.update({
 "Hongkong → Borneo (Kota Kinabalu) → Singapur": (("14 h 40 min do Hongkongu","12 h 45 min","1 h 55 min",""),("16 h 05 min","13 h 55 min","2 h 10 min","")),
 "Hongkong → Borneo → Kuala Lumpur (dwa osobne bilety)": (("14 h 25 min","13 h 20 min","1 h 05 min",""),("17 h 15 min","13 h 40 min","3 h 35 min","")),
 "Tajwan (Tajpej + Kenting) → Hongkong": (("15 h 15 min","13 h 10 min","2 h 05 min",""),("16 h 05 min","14 h 15 min","1 h 50 min","")),
 "Singapur → Lombok/Gili → Bali (tylko lotnisko)": (("15 h 15 min","13 h 15 min","2 h",""),("18 h 10 min","15 h 50 min","2 h 20 min","")),
 "Hongkong → Palawan (El Nido) → Manila": (("14 h 40 min","12 h 45 min","1 h 55 min",""),("17 h 45 min z Manili","15 h 30 min","2 h 15 min","+ rano lot z Palawanu do Manili")),
})
ROUTE.update({
 "Hongkong → Borneo (Kota Kinabalu) → Singapur": "Kraków → Stambuł → Hongkong · Kota Kinabalu · Singapur → Stambuł → Kraków",
 "Hongkong → Borneo → Kuala Lumpur (dwa osobne bilety)": "Kraków → Frankfurt → Hongkong · Kota Kinabalu · Kuala Lumpur → Stambuł → Kraków",
 "Tajwan (Tajpej + Kenting) → Hongkong": "Kraków → Stambuł → Tajpej · Kenting · Hongkong → Stambuł → Kraków",
 "Singapur → Lombok/Gili → Bali (tylko lotnisko)": "Kraków → Stambuł → Singapur · Lombok · Bali → Stambuł → Kraków",
 "Hongkong → Palawan (El Nido) → Manila": "Kraków → Stambuł → Hongkong · Palawan · Manila → Stambuł → Kraków",
})



DEST.append(dict(slug="huby", flag="🏙", name="Przez wielkie miasto (hub) + tani lot dalej", place="Singapur, Bangkok, Kuala Lumpur, Hongkong, Seul", gulf=False,
  price="od ok. 4 000 zł", price7="", price_note="lot długi + loty lokalne, bez hoteli",
  summary="Tani lot do wielkiego miasta, 2 noce na zwiedzanie, potem tania linia na plażę. Najlepiej: Singapur + Penang.",
  weather="Penang, Krabi, Phuket: sucho, 32–33°C · Cebu/Bohol: sucho, 30°C", sea="28–30°C", entry="zależy od kraju – patrz kafelki krajów",
  chips=[("ok","Bez Zatoki"),("ok","Miasto + plaża"),("warn","Loty lokalne – osobne bilety"),("warn","Ceny z wyszukiwania dla 1 os.")],
  options=[
   dict(title="Singapur + Penang", tag="Najlepszy plan", gulf=False, pp="ok. 4 110 zł",
    why="Turkish Kraków ↔ Singapur + Scoot do Penang 256 zł + AirAsia z powrotem 189 zł. Na Borneo zamiast Penang: ok. 4 540 zł. W piątek po pracy: Lufthansa 19:05 przez Frankfurt, ok. 4 350 zł, powrót pn 9:35.",
    out_title="Tam: sob 20.02 → nd 21.02", out=[
     dep("19:25","19:25","sob 20.02 · Kraków, TK 1274"),
     stop("23:50","21:50","Stambuł (Turcja)","Przesiadka <b>2 h</b>"),
     stop("01:50","23:50","wylot, TK 54 (nocny)"), fly("lot ok. 10 h 50 min"),
     arr("17:40","10:40","nd 21.02 · Singapur · Polska + 7 h"),
     night("🛏 2 noce w Singapurze (Gardens by the Bay, zoo, Sentosa)"),
     dep("08:00","01:00","wt 23.02 · Scoot do Penang (Malezja)"),
     night("🏝 ok. 10 nocy Penang (George Town, Batu Ferringhi)")],
    back_title="Powrót: pt 5.03 → nd 7.03", back=[
     dep("","","pt 5.03 · AirAsia Penang → Singapur, noc w Singapurze"),
     dep("23:15","16:15","sob 6.03 · Singapur, TK 55 (nocny)"),
     stop("05:50","03:50","nd 7.03 · Stambuł","Przesiadka <b>2 h 10 min</b>"),
     arr("08:20","08:20","nd 7.03 · Kraków")], back_bio="W domu w niedzielę rano."),
   dict(title="Kuala Lumpur + Penang albo Borneo", gulf=False, pp="ok. 4 480 zł",
    why="Lufthansa + Singapore Airlines w piątek po pracy + AirAsia do Penang 129 zł w każdą stronę (prawie co godzinę). Z Borneo zamiast Penang: ok. 4 850 zł.",
    out_title="Tam: pt 19.02 → sob 20.02", out=[
     dep("19:05","19:05","pt 19.02 · Kraków, LH 1369"), stop("20:45","20:45","Frankfurt","Przesiadka"),
     stop("","","Singapur","Przesiadka"), arr("19:40","12:40","sob 20.02 · Kuala Lumpur"),
     night("🛏 1–2 noce w KL, potem AirAsia do Penang (1 h)")],
    back_title="Powrót: nd 7.03 → pn 8.03", back=[
     dep("23:55","16:55","nd 7.03 · Kuala Lumpur (nocny)"), stop("06:00","06:00","pn 8.03 · Frankfurt","Przesiadka <b>2 h</b>"),
     arr("09:35","09:35","pn 8.03 · Kraków")]),
   dict(title="Hongkong + Cebu albo Bohol (Filipiny)", gulf=False, pp="ok. 4 350–4 640 zł",
    why="Lufthansa Kraków ↔ Hongkong (ten sam rozkład pt, sob i nd) + Cebu Pacific Hongkong → Cebu 518 zł, z powrotem 439 zł. Palawan przez Manilę: ok. 4 550 zł; Kaohsiung (Tajwan): ok. 4 240 zł.",
    out_title="Tam: sob 20.02 → nd 21.02", out=[
     dep("19:05","19:05","sob 20.02 · Kraków, LH 1369"), stop("20:45","20:45","Frankfurt","Przesiadka <b>1 h 05 min</b>"),
     stop("21:50","21:50","wylot, LH 796 (nocny)"), arr("16:30","09:30","nd 21.02 · Hongkong"),
     night("🛏 2 noce w Hongkongu"), dep("21:35","14:35","wt 23.02 · Cebu Pacific"), arr("00:30","17:30","śr 24.02 · Cebu")],
    back_title="Powrót: pt 5.03 → nd 7.03", back=[
     dep("17:45","10:45","pt 5.03 · Cebu → Hongkong, noc w Hongkongu"),
     dep("23:45","16:45","sob 6.03 · Hongkong (nocny)"), stop("06:10","06:10","nd 7.03 · Frankfurt","Przesiadka"),
     arr("09:35","09:35","nd 7.03 · Kraków")]),
   dict(title="Bangkok + Krabi albo Phuket (LOT z Warszawy bez przesiadki)", gulf=False, pp="ok. 4 770 zł",
    why="LOT Warszawa ↔ Bangkok bez przesiadki + Thai Vietjet do Krabi 194 zł / Phuket 175 zł, z powrotem ok. 264 zł. Plus pociąg do Warszawy. Z Krakowa: SWISS nd 14:40 przez Zurych, ok. 4 490 zł (powrót 7 h 35 min czekania w Wiedniu).",
    out_title="Tam: nd 21.02 → pn 22.02", out=[
     dep("14:45","14:45","nd 21.02 · Warszawa, LO 65 (bez przesiadki)"), fly("lot 10 h 20 min"),
     arr("07:05","01:05","pn 22.02 · Bangkok · Polska + 6 h"),
     night("🛏 2 noce w Bangkoku, potem lot na Krabi / Phuket")],
    back_title="Powrót: nd 7.03", back=[
     dep("09:05","03:05","nd 7.03 · Bangkok, LO 66 (bez przesiadki)"), arr("15:00","15:00","nd 7.03 · Warszawa")]),
   dict(title="Seul + Cebu (LOT z Warszawy)", gulf=False, pp="ok. 3 980 zł",
    why="Najtańszy lot długi: LOT Warszawa ↔ Seul bez przesiadki 2 898 zł + Cebu Pacific Seul ↔ Cebu 425 + 654 zł. Najmniej wygodnie: mroźny Seul, nocny przylot do Cebu, 5-godzinne loty lokalne.",
    out_title="Tam: sob 20.02 → nd 21.02", out=[
     dep("11:50","11:50","sob 20.02 · Warszawa, LOT (bez przesiadki)"), fly("lot ok. 11 h"),
     arr("07:00","23:00","nd 21.02 · Seul (Korea Płd.) · Polska + 8 h"), night("✈ Dalej Cebu Pacific do Cebu (ok. 5 h)")],
    back_title="Powrót: przez Seul do Warszawy", back=[]),
  ],
  extra="Ceny z wyszukiwań dla 1 dorosłego (dla 7 osób Google dziś prawie nic nie pokazywał) – przed zakupem sprawdzić dla 7. Kraków–Bangkok bez przesiadki nie ma; LOT lata z Warszawy codziennie oprócz piątku. Chiny jako hub: 240-godzinny tranzyt bez wizy działa tylko przy locie dalej do innego kraju. Inne tanie loty lokalne: Singapur ↔ Kuala Lumpur 171–256 zł (ponad 30 dziennie), Hongkong → Manila 313 zł, Manila → Boracay 140 zł / Palawan 156 zł / Bohol 168 zł, Kuala Lumpur → Siem Reap 346 zł."))
STATS.update({
 "Singapur + Penang": (("15 h 15 min do Singapuru","13 h 15 min","2 h","+ 2 noce w Singapurze i ok. 1 h 30 min lotu do Penang"),("16 h 05 min z Singapuru","13 h 55 min","2 h 10 min","+ dzień wcześniej lot z Penang")),
 "Kuala Lumpur + Penang albo Borneo": (("17 h 35 min do KL","","2 przesiadki","+ lot do Penang 1 h"),("16 h 40 min","14 h 40 min","2 h","")),
 "Hongkong + Cebu albo Bohol (Filipiny)": (("14 h 25 min do Hongkongu","13 h 20 min","1 h 05 min","+ 2 noce w HK i lot do Cebu"),("16 h 50 min z Hongkongu","","1 przesiadka","")),
 "Bangkok + Krabi albo Phuket (LOT z Warszawy bez przesiadki)": (("10 h 20 min","10 h 20 min","bez przesiadki","+ ok. 2 h 30 min pociągiem do Warszawy"),("11 h 55 min","11 h 55 min","bez przesiadki","+ pociąg do Krakowa")),
 "Seul + Cebu (LOT z Warszawy)": (("11 h 10 min do Seulu","11 h 10 min","bez przesiadki","+ ok. 5 h lotu do Cebu"),None),
})
ROUTE.update({
 "Singapur + Penang": "Kraków → Stambuł → Singapur · Penang · Singapur → Stambuł → Kraków",
 "Kuala Lumpur + Penang albo Borneo": "Kraków → Frankfurt → Singapur → Kuala Lumpur · Penang",
 "Hongkong + Cebu albo Bohol (Filipiny)": "Kraków → Frankfurt → Hongkong · Cebu · Hongkong → Frankfurt → Kraków",
 "Bangkok + Krabi albo Phuket (LOT z Warszawy bez przesiadki)": "Warszawa → Bangkok (bez przesiadki) · Krabi / Phuket",
 "Seul + Cebu (LOT z Warszawy)": "Warszawa → Seul (bez przesiadki) · Cebu",
})


DEST.append(dict(slug="ekwador", region="americas", flag="🇪🇨", name="Ekwador (+ Galápagos)", place="Quito, Andy, Amazonia; opcjonalnie Galápagos", gulf=False,
  price="", price7="", price_note="",
  summary="Galápagos (żółwie, lwy morskie, snorkeling) albo sam kontynent (Andy + Amazonia). W lutym–marcu 2027 silne El Niño – decyzję o Galápagos podjąć w XII–I i rezerwować z darmową zmianą.",
  weather="⚠️ silne El Niño: wybrzeże – deszcze i powodzie; Andy chłodno (Quito 2 850 m); Galápagos ciepło, więcej deszczu", sea="Galápagos 27–29°C (mniej ryb niż zwykle)",
  entry="bez wizy 90 dni; ubezpieczenie, bilet powrotny i rezerwacja hotelu; eTA Kanady (7 CAD) przy przesiadce w Toronto",
  chips=[("bad","Silne El Niño w lutym–marcu"),("warn","Stan wyjątkowy (m.in. Quito), wybrzeże odradzane"),("ok","Galápagos – ciepłe morze"),("warn","Galápagos +4–6 tys. zł/os.")],
  options=[
   dict(title="Lufthansa + Air Canada, Kraków ⇄ Quito", tag="Najtańsza", kind="direct", gulf=False, pp="ok. 3 700 zł",
    why="3 704 zł w KAYAK (4 303 zł w Google), szukane dla 7 osób. Wylot w sobotę o 6:00 rano. Powrót w sobotę 6.03 kosztuje 5 000–5 800 zł – niedziela 7.03 oszczędza ok. 1 300–1 500 zł/os. Galápagos osobno: loty ok. 1 200–1 400 zł/os. w obie strony + opłata parku 200 USD (dziecko 100 USD) + 20 USD karta.",
    out_title="Tam: sob 20.02 → nd 21.02", out=[
     dep("06:00","06:00","sob 20.02 · Kraków, LH 1627"), stop("","","Monachium (Niemcy)","Przesiadka"),
     stop("","","Toronto (Kanada), AC 837 → AC 960","Przesiadka · potrzebne eTA"),
     arr("00:10","06:10","nd 21.02 · Quito · Polska − 6 h")],
    back_title="Powrót: nd 7.03 → pn 8.03", back=[
     dep("09:00","15:00","nd 7.03 · Quito, AC 961"), stop("","","Toronto, AC 840","Przesiadka"),
     stop("","","Frankfurt, LH 1362","Przesiadka"), arr("09:35","09:35","pn 8.03 · Kraków")]),
   dict(title="KLM: tam do Quito, z powrotem z Guayaquil (pod Galápagos)", kind="direct", gulf=False, pp="ok. 5 150 zł",
    why="Najwygodniej: jedna przesiadka w Amsterdamie w każdą stronę, wylot w niedzielę. W sobotę ta sama trasa (Lufthansa + Avianca) kosztuje 5 616 zł. Przesiadka na lotnisku w Guayaquil jest OK (miasto odradzane).",
    out_title="Tam: nd 21.02", out=[
     dep("06:00","06:00","nd 21.02 · Kraków, KL 1322"), stop("","","Amsterdam, KL 755","Przesiadka"),
     arr("16:20","22:20","nd 21.02 · Quito")],
    back_title="Powrót: nd 7.03 → pn 8.03", back=[
     dep("20:20","02:20","nd 7.03 · Guayaquil, KL 755 (bez przesiadki do Amsterdamu)"), stop("","","Amsterdam, KL 1327","Przesiadka"),
     arr("17:00","17:00","pn 8.03 · Kraków")]),
   dict(title="Turkish + Avianca przez Stambuł i Bogotę", kind="direct", gulf=False, pp="ok. 4 610 zł",
    why="Tam do Quito, z powrotem z Guayaquil. Wylot w sobotę 19:25 z Krakowa, ale 28 h w jedną i 26 h w drugą stronę – bardzo męczące dla dzieci; możliwe, że to dwie osobne rezerwacje. Z Warszawy w piątek 19:10: 4 261 zł, 36 h.",
    out_title="Tam: sob 20.02 → nd 21.02", out=[
     dep("19:25","19:25","sob 20.02 · Kraków"), stop("","","Stambuł (Turcja), potem Bogota (Kolumbia)","2 przesiadki"),
     arr("","","nd 21.02 · Quito")],
    back_title="Powrót: z Guayaquil przez Bogotę i Stambuł (ok. 26 h)", back=[]),
  ],
  extra="Trasy: C – Quito 2 → Santa Cruz + Isabela 6 → Baños 2 → Amazonia (Napo) 2: ok. 5 950 zł/os. „twardych” kosztów (loty, opłaty, promy, bez hoteli). A – Quito → Mindo → 9 nocy na Galápagos (San Cristóbal, Santa Cruz, Isabela) → powrót z Guayaquil: ok. 7 500 zł/os. B – sam kontynent (Andy + Amazonia), bez plaży: ok. 3 700 zł/os. Rejs 8-dniowy z 6-latkiem – nie polecamy, lepiej wyspy z bazą na lądzie. Bezpiecznie: Galápagos, Andy (Otavalo, Cotopaxi, Baños), Amazonia Napo; unikać wybrzeża i Cuyabeno. Zdrowie: denga (repelent), żółta febra tylko zalecana w Amazonii. El Niño: NOAA (8.10.2026) – silne do bardzo silnego I–III 2027."))
STATS.update({
 "Lufthansa + Air Canada, Kraków ⇄ Quito": (("24 h 10 min","","2 przesiadki",""),("18 h 35 min","","2 przesiadki","")),
 "KLM: tam do Quito, z powrotem z Guayaquil (pod Galápagos)": (("16 h 20 min","","1 przesiadka",""),("14 h 40 min","","1 przesiadka","")),
 "Turkish + Avianca przez Stambuł i Bogotę": (("ok. 28 h","","2 przesiadki",""),None),
})
ROUTE.update({
 "Lufthansa + Air Canada, Kraków ⇄ Quito": "Kraków → Monachium → Toronto → Quito",
 "KLM: tam do Quito, z powrotem z Guayaquil (pod Galápagos)": "Kraków → Amsterdam → Quito · Guayaquil → Amsterdam → Kraków",
 "Turkish + Avianca przez Stambuł i Bogotę": "Kraków → Stambuł → Bogota → Quito",
})

# ---------- Warsaw comparison (warszawa-dane.md, 24.10 evening) ----------
WAW = {
 "sri-lanka": "Warszawa: 2 988 zł (sob 11:45, przez Szardżę)",
 "malezja-borneo": "Warszawa: ok. 4 600 zł (Lufthansa pt 18:35)",
 "indonezja": "Warszawa: ok. 4 910 zł (Austrian + Singapore Airlines pt 19:25)",
 "tajwan": "Warszawa: 4 528 zł (LOT + KLM, nd 16:45)",
 "filipiny": "Warszawa: ok. 5 260 zł (Turkish pt 18:40) – o 1 000 zł taniej",
 "tajlandia": "Warszawa: ok. 4 240 zł (LOT bez przesiadki do Bangkoku, nd 14:45)",
 "kambodza": "Warszawa: ok. 4 700 zł",
 "chiny-hainan": "Warszawa: ok. 5 600 zł",
}
for _x in DEST:
    if _x["slug"] in WAW: _x["alt"] = WAW[_x["slug"]]

# ---------- booking links: (slug, option index) -> (Google Flights query, airline name, airline URL) ----------
P = "4 adults 3 children"
AL = {
 "Air Arabia": "https://www.airarabia.com/pl", "flydubai": "https://www.flydubai.com/pl/",
 "KLM": "https://www.klm.pl/", "Lufthansa": "https://www.lufthansa.com/pl/pl/homepage",
 "Austrian": "https://www.austrian.com/pl/pl/homepage", "Turkish Airlines": "https://www.turkishairlines.com/pl-pl/",
 "Korean Air": "https://www.koreanair.com/", "Condor": "https://www.condor.com/pl/",
 "AirAsia": "https://www.airasia.com/", "Air Canada": "https://www.aircanada.com/pl/pl/aco/home.html", "LOT": "https://www.lot.com/pl/pl", "Finnair": "https://www.finnair.com/pl-pl", "Scoot": "https://www.flyscoot.com/pl", "China Airlines": "https://www.china-airlines.com/pl/pl",
}
BOOK = {
 ("sri-lanka",1): (f"Flights from KRK to CMB on 2027-02-19 return 2027-03-07 {P} Air Arabia", "Air Arabia"),
 ("sri-lanka",2): (f"Flights from KRK to CMB on 2027-02-20 return 2027-03-07 {P} Air Arabia", "Air Arabia"),
 ("sri-lanka",3): (f"Flights from WAW to CMB on 2027-02-19 return 2027-03-07 {P} flydubai", "flydubai"),
 ("sri-lanka",4): (f"Flights from KRK to CMB on 2027-02-20 return 2027-03-07 {P} KLM", "KLM"),
 ("malezja-borneo",1): (f"Flights from KRK to KUL on 2027-02-19 return 2027-03-07 {P} Lufthansa", "Lufthansa"),
 ("malezja-borneo",2): (f"Flights from KRK to KUL on 2027-02-20 return 2027-03-06 {P} Turkish Airlines", "Turkish Airlines"),
 ("malezja-borneo",3): (f"One way flights from KRK to SIN on 2027-02-21 {P} Finnair", "Finnair"),
 ("malezja-borneo",4): (f"One way flights from KRK to KUL on 2027-02-21 {P} Austrian", "Austrian"),
 ("tajwan",1): (f"Flights from KRK to TPE on 2027-02-20 return 2027-03-06 {P} Turkish Airlines", "Turkish Airlines"),
 ("tajwan",2): (f"Flights from KRK to KHH on 2027-02-19 return 2027-03-07 {P} Lufthansa", "Lufthansa"),
 ("filipiny",1): (f"Flights from KRK to MNL on 2027-02-20 return 2027-03-06 {P} Turkish Airlines", "Turkish Airlines"),
 ("tajlandia",1): (f"Flights from KRK to BKK on 2027-02-20 return 2027-03-06 {P} Turkish Airlines", "Turkish Airlines"),
 ("kambodza",1): (f"Flights from KRK to KUL on 2027-02-19 return 2027-03-07 {P} Lufthansa", "Lufthansa"),
 ("chiny-hainan",1): (f"Flights from KRK to CAN on 2027-02-20 return 2027-03-06 {P} Turkish Airlines", "Turkish Airlines"),
 ("wietnam",1): (f"Flights from KRK to SGN on 2027-02-19 return 2027-03-07 {P} KLM", "KLM"),
 ("indonezja",1): (f"Flights from KRK to SIN on 2027-02-19 return 2027-03-07 {P} Lufthansa", "Lufthansa"),
 ("indonezja",2): (f"Flights from KRK to SIN on 2027-02-19 return 2027-03-07 {P} Lufthansa", "Scoot"),
 ("indonezja",3): (f"Flights from KRK to SIN on 2027-02-20 return 2027-03-06 {P} Turkish Airlines", "Turkish Airlines"),
 ("indonezja",4): (f"Flights from KRK to SIN on 2027-02-19 return 2027-03-07 {P} Lufthansa", "Scoot"),
 ("indonezja",5): (f"Flights from KRK to DPS on 2027-02-19 return 2027-03-07 {P} KLM", "KLM"),
 ("kombinacje",1): (f"Flights from KRK to HKG on 2027-02-20 return 2027-03-06 {P} Turkish Airlines", "Turkish Airlines"),
 ("kombinacje",2): (f"One way flights from KRK to HKG on 2027-02-20 {P} Lufthansa", "Lufthansa"),
 ("kombinacje",3): (f"Flights from KRK to TPE on 2027-02-20 return 2027-03-06 {P} Turkish Airlines", "Turkish Airlines"),
 ("kombinacje",4): (f"Flights from KRK to SIN on 2027-02-20 return 2027-03-06 {P} Turkish Airlines", "Turkish Airlines"),
 ("kombinacje",5): (f"Flights from KRK to HKG on 2027-02-20 return 2027-03-06 {P} Turkish Airlines", "Turkish Airlines"),
 ("huby",1): (f"Flights from KRK to SIN on 2027-02-20 return 2027-03-06 {P} Turkish Airlines", "Turkish Airlines"),
 ("huby",2): (f"Flights from KRK to KUL on 2027-02-19 return 2027-03-07 {P} Lufthansa", "Lufthansa"),
 ("huby",3): (f"Flights from KRK to HKG on 2027-02-20 return 2027-03-06 {P} Lufthansa", "Lufthansa"),
 ("huby",4): (f"Flights from WAW to BKK on 2027-02-21 return 2027-03-07 {P} LOT", "LOT"),
 ("huby",5): (f"Flights from WAW to ICN on 2027-02-20 return 2027-03-06 {P} LOT", "LOT"),
 ("ekwador",1): (f"Flights from KRK to UIO on 2027-02-20 return 2027-03-07 {P} Air Canada", "Air Canada"),
 ("ekwador",3): (f"Flights from KRK to UIO on 2027-02-20 return 2027-03-07 {P} Turkish Airlines", "Turkish Airlines"),
 ("laos",1): (f"Flights from KRK to BKK on 2027-02-20 return 2027-03-06 {P} Turkish Airlines", "Turkish Airlines"),
}
from urllib.parse import quote
KAYAK = {
 ("ekwador",2): "KRK-UIO/2027-02-21/GYE-KRK/2027-03-07",
 ("kombinacje",1): "KRK-HKG/2027-02-20/SIN-KRK/2027-03-06",
 ("kombinacje",2): "KRK-HKG/2027-02-20/KUL-KRK/2027-03-06",
 ("kombinacje",3): "KRK-TPE/2027-02-20/HKG-KRK/2027-03-06",
 ("kombinacje",4): "KRK-SIN/2027-02-20/DPS-KRK/2027-03-06",
 ("kombinacje",5): "KRK-HKG/2027-02-20/MNL-KRK/2027-03-06",
}
def book_html(o):
    if o.get("_kayak"):
        k = "https://www.kayak.pl/flights/" + o["_kayak"] + "/4adults/children-8-8-6?sort=price_a"
        al = (o["_book"] or (None, "KLM"))[1]
        return (f'<div class="book"><a class="gf" href="{k}" target="_blank" rel="noopener">Sprawdź i zarezerwuj (KAYAK, wiele miast) →</a>'
                f'<a class="al" href="{AL[al]}" target="_blank" rel="noopener">Strona {al}</a></div>'
                '<p class="note">Bilet długi; loty lokalne kupuje się osobno.</p>')
    b = o.get("_book")
    if not b: return ""
    q, al = b
    gf = "https://www.google.com/travel/flights?hl=pl&curr=PLN&q=" + quote(q)
    return (f'<div class="book"><a class="gf" href="{gf}" target="_blank" rel="noopener">Sprawdź i zarezerwuj (Google Flights) →</a>'
            f'<a class="al" href="{AL[al]}" target="_blank" rel="noopener">Strona {al}</a></div>')

import re as _re
def _num(pp):
    m = _re.search(r"(\d[\d ]{2,})", pp.replace("\u00a0"," "))
    return int(m.group(1).replace(" ","")) if m else 10**9
KIND_LABEL = {"direct": '<span class="badge kind">Jednym biletem</span>', "hub": '<span class="badge kind hub">Przez hub · osobne bilety</span>'}

# ---------- rendering ----------
CSS = open(OUT / "style.css").read() if (OUT / "style.css").exists() else ""

def page(title, body, back=False):
    nav = '<a class="back" href="index.html">← Wszystkie kierunki</a>' if back else ''
    return f'''<!doctype html><html lang="pl"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex, nofollow">
<meta http-equiv="Cache-Control" content="no-cache"><title>{html.escape(title)}</title>
<link rel="stylesheet" href="style.css?v=e"></head><body>
<header><div class="wrap">{nav}<h1>{title}</h1>
<div class="chips"><span class="chip">19.02 – 7.03.2027</span><span class="chip">ceny z {UPDATED}, za osobę</span></div>
</div></header><div class="wrap">{body}
<footer><p>Google Flights, {UPDATED}: w obie strony, najtańsza taryfa (bagaż podręczny), dziecko = dorosły.</p>
<p><a href="info.html">Zatoka Perska · rezygnacja i ubezpieczenie · bagaż</a> · Ostatnia aktualizacja: {UPDATED}</p></footer>
</div></body></html>'''

def chip_html(chips):
    return ''.join(f'<span class="flag {k}">{"✓" if k=="ok" else "!" if k=="warn" else "✕"} {html.escape(t)}</span>' for k, t in chips)

def teaser(d):
    rows = []
    for kind, label in (("direct","✈ Jednym biletem"),("hub","🏙 Przez hub z noclegiem")):
        ops = [o for o in d["options"] if o.get("kind") == kind]
        if not ops: continue
        best = min(ops, key=lambda o: _num(o["pp"]))
        rows.append(f'<div class="trow"><span>{label}</span><b>od {_num(best["pp"]):,} zł</b></div>'.replace(",", " "))
    alt = f'<span class="alt">{d["alt"]}</span>' if d.get("alt") else ''
    return f'<div class="tprice">{"".join(rows)}<span class="pnote">za osobę, w obie strony, z lotami lokalnymi</span>{alt}</div>'

def tile(d):
    if d.get("pending"):
        return f'''<div class="tile pending"><div class="tflag">{d["flag"]}</div><h2>{d["name"]}</h2><p class="place">{d["place"]}</p>
<p>{d["summary"]}</p><span class="btn disabled">W przygotowaniu</span></div>'''
    cls = "tile notrec" if d.get("notrec") else "tile"
    return f'''<a class="{cls}" href="{d["slug"]}.html"><div class="tflag">{d["flag"]}</div>
<h2>{d["name"]}</h2><p class="place">{d["place"]}</p>
<p class="route">✈ {d["options"][0]["_route"]}</p>
{teaser(d)}
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
    parts = [f'<div class="card {"best" if i==1 else ""}">{badge}{KIND_LABEL.get(o.get("kind"),"")}{g}<h3 class="otitle">{o["title"]}</h3><p class="route">✈ {o["_route"]}</p>',
             f'<div class="price"><div><b>{o["pp"]}</b><span>za osobę, w obie strony{" · " + o["p7"] if str(o.get("p7","")).startswith("+") else ""}</span>{('<span class="alt">' + o["alt"] + '</span>') if o.get("alt") else ''}</div></div>',
             f'<p class="why">{o["why"]}</p>']
    if o.get("out"):
        st = o.get("_stats")
        parts.append(f'<div class="leg-title"><h4>{o["out_title"]}</h4></div>{stats_html(st[0] if st else None)}{tl(o["out"])}')
        if o.get("out_bio"): parts.append(f'<div class="bio">🌙 <b>Dla organizmu:</b> {o["out_bio"]}</div>')
    st = o.get("_stats")
    parts.append(f'<div class="leg-title"><h4>{o["back_title"]}</h4></div>{stats_html(st[1] if st and o.get("back") else None)}')
    if o.get("back"): parts.append(tl(o["back"]))
    if o.get("back_bio"): parts.append(f'<div class="bio">🌙 <b>Dla organizmu:</b> {o["back_bio"]}</div>')
    if o.get("note"): parts.append(f'<p class="note">{o["note"]}</p>')
    parts.append(book_html(o))
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
    asia = ''.join(tile(d) for d in dests if d.get("region", "asia") == "asia")
    amer = ''.join(tile(d) for d in dests if d.get("region") == "americas")
    amer_html = f'<h2 class="region">Ameryka</h2><div class="tiles">{amer}</div>' if amer else ''
    body = f'''<h2 class="region">Azja</h2><div class="tiles">{asia}</div>{amer_html}
<div class="callout warn"><a href="info.html">Zatoka Perska, rezygnacja i ubezpieczenie, bagaż →</a></div>
<h2>Kierunki, których nie bierzemy pod uwagę</h2>
<div class="card rejected">
<h3>Odrzucone przez nas</h3>
<ul>
<li><b>🇮🇳 Indie</b> – niedawno byliśmy.</li>
<li><b>🇻🇳 Wietnam</b> – niedawno byliśmy.</li>
<li><b>🇮🇩 Bali</b> – obie rodziny już były; tłok i bardzo dużo turystów.</li>
<li><b>🇲🇾 Langkawi</b> – niedawno byliśmy (Malezja zostaje: Borneo albo Penang).</li>
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
<li><b>Indonezja: Manado/Bunaken, Belitung, Raja Ampat</b> – wzburzone morze i odwoływane rejsy w lutym; Raja Ampat 2 dni podróży.</li>
</ul>
</div>'''
    return page("Ferie 2027: dokąd w Azji?", body)

INFO = open(OUT / "info_body.html").read() if (OUT / "info_body.html").exists() else ""

if __name__ == "__main__":
    # precompute per-option data while options still sit at their original (slug, index)
    for d in DEST:
        for i, o in enumerate(d["options"], 1):
            o["_book"] = BOOK.get((d["slug"], i)); o["_kayak"] = KAYAK.get((d["slug"], i))
            o["_route"] = route_of(d["slug"], o)
            o["_stats"] = STATS_BY_SLUG.get((d["slug"], o["title"])) or STATS.get(o["title"])
    byslug = {d["slug"]: d for d in DEST}
    pool = {o["title"]: o for sl in ("kombinacje", "huby") for o in byslug[sl]["options"]}
    for o in pool.values(): o.pop("tag", None)
    def opt(slug, title): return next(o for o in byslug[slug]["options"] if o["title"] == title)
    HUB = "hub"; DIR = "direct"
    def setk(o, k): o["kind"] = k; return o
    m = byslug["malezja-borneo"]
    m["options"] = [setk(pool["Hongkong → Borneo (Kota Kinabalu) → Singapur"], HUB),
                    setk(opt("malezja-borneo","Lufthansa + Malaysia Airlines przez Frankfurt i Singapur, potem lot na Borneo"), DIR),
                    setk(pool["Singapur + Penang"], HUB),
                    setk(opt("malezja-borneo","Turkish Airlines przez Stambuł, sobota → sobota"), DIR),
                    setk(pool["Hongkong → Borneo → Kuala Lumpur (dwa osobne bilety)"], HUB),
                    setk(pool["Kuala Lumpur + Penang albo Borneo"], DIR),
                    setk(opt("malezja-borneo","Finnair do Singapuru w niedzielę + AirAsia na Borneo, powrót Lufthansą"), HUB)]
    m["options"][0]["tag"] = "Najlepszy plan"
    m.update(name="Malezja", place="Borneo (orangutany, wyspy) albo Penang",
      summary="Borneo: Sepilok i wyspy przy Kota Kinabalu, pora sucha. Albo Penang (George Town, plaże). Jednym biletem do Kuala Lumpur albo przez Hongkong / Singapur z noclegiem.")
    i_ = byslug["indonezja"]
    io = i_["options"]
    for o in io: o["kind"] = HUB
    io[-1]["kind"] = DIR   # KLM to Bali (one ticket to Indonesia)
    i_["options"] = [io[0], setk(pool["Singapur → Lombok/Gili → Bali (tylko lotnisko)"], HUB)] + io[1:]
    t = byslug["tajwan"]
    for o in t["options"]: o["kind"] = DIR
    t["options"].insert(1, setk(pool["Tajwan (Tajpej + Kenting) → Hongkong"], HUB))
    f = byslug["filipiny"]
    tk = setk(f["options"][0], DIR); tk.pop("tag", None); tk["pp"] = "ok. 6 260 zł"
    f["options"] = [setk(pool["Hongkong → Palawan (El Nido) → Manila"], HUB), setk(pool["Hongkong + Cebu albo Bohol (Filipiny)"], HUB), tk,
                    setk(pool["Seul + Cebu (LOT z Warszawy)"], HUB)]
    f["options"][0]["tag"] = "Najlepszy plan"
    f.update(summary="Najpiękniejsze plaże, pora sucha. Jednym biletem tylko Turkish w sobotę (drogo); taniej przez Hongkong z 2 nocami i tanim lotem dalej.",
      chips=[("ok","Bez Zatoki"),("ok","Najlepsze plaże"),("warn","Dużo przesiadek"),("warn","Loty lokalne – osobne bilety")])
    th = byslug["tajlandia"]
    for o in th["options"]: o["kind"] = DIR
    th["options"][0]["pp"] = "ok. 4 790 zł"
    th["options"].append(setk(pool["Bangkok + Krabi albo Phuket (LOT z Warszawy bez przesiadki)"], DIR))
    for sl in ("sri-lanka", "chiny-hainan"):
        for o in byslug[sl]["options"]: o.setdefault("kind", DIR)
    for sl in ("kambodza", "laos"):
        for o in byslug[sl]["options"]: o.setdefault("kind", HUB)
    for o in byslug["ekwador"]["options"]: o.setdefault("kind", DIR)
    order = [byslug[x] for x in ("sri-lanka","malezja-borneo","indonezja","filipiny","tajwan","tajlandia","kambodza","chiny-hainan","laos","ekwador")]
    DEST[:] = order
    (OUT / "index.html").write_text(index(order))
    for d in DEST: (OUT / f'{d["slug"]}.html').write_text(detail(d))
    (OUT / "info.html").write_text(page("Bezpieczeństwo, rezygnacja, bagaż", INFO, back=True))
    print("built", len(DEST) + 2, "pages")
