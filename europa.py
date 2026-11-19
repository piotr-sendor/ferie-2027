#!/usr/bin/env python3
"""Europe alternative report: europa.html (19.11.2026) - Madeira, Canary Islands, Azores for 7-10 days in the same window.

Prices: KAYAK 19.11.2026, one-way searches without stops (+-3 days) for 4 adults + 3 children, so every option
is two one-way tickets (Ryanair / Wizz Air) unless noted. Weather: long-term February averages from travel climate
sites (weather2travel, holiday-weather, guidetocanaryislands), rounded. Run: python3 europa.py
"""
import pathlib
import build as B

OUT = pathlib.Path(__file__).parent
B.UPDATED = "19.11.2026"

# one row per proposal: (label, out, back, nights, total for 7, per person, note)
DEST = [
 dict(id="teneryfa", flag="🇪🇸", name="Teneryfa (południe)", tz="Polska − 1 h",
  lead="Najpewniejsze słońce i ciepło z całej listy. Południe wyspy (Costa Adeje, Los Cristianos, El Médano) jest wyraźnie cieplejsze i suchsze od północy.",
  weather=[("W dzień", "21–23°C na południu, 19–20°C na północy (Puerto de la Cruz)"), ("W nocy", "15–16°C"),
           ("Morze", "ok. 19°C – da się kąpać, dla dzieci rześko"), ("Słońce", "ok. 7 h dziennie, deszcz 1–3 dni w miesiącu (głównie północ)"),
           ("Uwaga", "pasat: na plaży wiatr, odczuwalnie chłodniej; na Teide (3 715 m) śnieg i ok. 0–5°C – ciepłe kurtki na wycieczkę")],
  todo="Kolejka na Teide i księżycowy krajobraz, rejs do grindwali i delfinów (żyją między Teneryfą a La Gomerą przez cały rok), Loro Parque, Siam Park, wąwóz Masca, czarne plaże, targi w La Laguna.",
  flights=[
   ("<b>Kraków, Ryanair, tydzień</b>", "sob 20.02 06:50 → 11:35", "sob 27.02 12:10 → 18:35", "7", "9 812 zł", "ok. 1 400 zł", "4 124 + 5 688 zł; w domu w sobotę wieczorem"),
   ("Kraków, Ryanair, 8 nocy", "sob 20.02 06:50 → 11:35", "nd 28.02 18:20 → pn 00:45", "8", "9 839 zł", "ok. 1 405 zł", "powrót w nocy z niedzieli na poniedziałek"),
   ("Katowice, Wizz Air, 9 nocy", "pt 19.02 13:20 → 18:05", "nd 28.02 18:50 → pn 01:10", "9", "9 087 zł", "ok. 1 300 zł", "3 749 + 5 338 zł; powrót w nocy"),
   ("Warszawa, Ryanair, 9 nocy", "pt 19.02 12:50 → 17:55", "nd 28.02 18:20 → pn 00:55", "9", "8 604 zł", "ok. 1 230 zł", "3 230 + 5 374 zł; dojazd do Warszawy"),
  ]),
 dict(id="gran-canaria", flag="🇪🇸", name="Gran Canaria (południe)", tz="Polska − 1 h",
  lead="Pogoda jak na południu Teneryfy, najwięcej plaż z łagodnym wejściem do wody. Południe (Maspalomas, Puerto de Mogán) słoneczne, stolica Las Palmas chłodniejsza.",
  weather=[("W dzień", "21–23°C na południu, ok. 20°C w Las Palmas"), ("W nocy", "ok. 15°C"), ("Morze", "ok. 19°C"),
           ("Słońce", "ok. 7 h dziennie, deszczu prawie nie ma na południu (ok. 2 dni)"), ("Uwaga", "wiatr na plażach, w górach (Roque Nublo) chłodno")],
  todo="Wydmy Maspalomas (mini-Sahara nad oceanem), Puerto de Mogán („mała Wenecja”), góry Roque Nublo, Palmitos Park, rejsy łodzią ze szklanym dnem, wioski w głębi wyspy.",
  flights=[
   ("<b>Kraków, Ryanair, 9 nocy</b>", "pt 19.02 13:10 → 17:45", "nd 28.02 16:30 → 22:55", "9", "10 122 zł", "ok. 1 445 zł", "3 833 + 6 289 zł; w domu w niedzielę wieczorem"),
   ("Kraków, Ryanair, tydzień", "nd 21.02 11:20 → 15:55", "nd 28.02 16:30 → 22:55", "7", "9 992 zł", "ok. 1 425 zł", "3 703 + 6 289 zł"),
   ("Kraków, Ryanair, taniej z powrotem w środę", "pt 19.02 13:10 → 17:45", "śr 3.03 17:15 → 23:40", "12", "8 355 zł", "ok. 1 195 zł", "za długo (12 nocy) – dla porównania"),
  ]),
 dict(id="fuerteventura", flag="🇪🇸", name="Fuerteventura", tz="Polska − 1 h",
  lead="Najdłuższe i najszersze plaże Kanarów, pustynny krajobraz, najsuchsza wyspa. Najtańsze bilety z całej listy (Wizz Air z Katowic). Minus: wiatr.",
  weather=[("W dzień", "21–22°C"), ("W nocy", "14–15°C"), ("Morze", "ok. 18,5°C – najchłodniejsze z Kanarów"),
           ("Słońce", "ok. 7 h dziennie, deszcz rzadko (1–2 dni)"),
           ("Uwaga", "<b>wietrznie</b> (raj dla kitesurferów) – na plaży odczuwalnie 17–18°C; najbardziej osłonięte południe (Morro Jable)")],
  todo="Wydmy Corralejo, wysepka Lobos (rejs, snorkeling), plaże Sotavento i Cofete, Oasis Park (zoo), lekcje surfingu dla dzieci, kozie farmy z serem majorero.",
  flights=[
   ("<b>Katowice, Wizz Air, 10 nocy</b>", "pt 19.02 07:10 → 11:45", "pn 1.03 12:30 → 18:35", "10", "5 593 zł", "ok. 800 zł", "2 520 + 3 073 zł – najtaniej z całej listy"),
   ("Katowice, Wizz Air, tydzień", "pn 22.02 07:10 → 11:45", "pn 1.03 12:30 → 18:35", "7", "5 157 zł", "ok. 735 zł", "2 084 + 3 073 zł; wylot w poniedziałek"),
   ("Kraków, Ryanair, tydzień", "nd 21.02 06:50 → 11:10", "nd 28.02 11:45 → 17:55", "7", "10 277 zł", "ok. 1 470 zł", "5 260 + 5 017 zł"),
  ]),
 dict(id="lanzarote", flag="🇪🇸", name="Lanzarote", tz="Polska − 1 h",
  lead="Wulkaniczna wyspa (park Timanfaya, czarne pola lawy, sztuka Césara Manrique). Z Polski w tym terminie <b>tylko czartery</b> – same bilety drogie, opłaca się raczej wycieczka z biurem (lot + hotel).",
  weather=[("W dzień", "ok. 21°C"), ("W nocy", "ok. 14°C"), ("Morze", "ok. 19°C"), ("Słońce", "ok. 7 h, prawie bez deszczu"), ("Uwaga", "wietrznie, jak na Fuerteventurze")],
  todo="Park Narodowy Timanfaya (gejzery i grill na cieple wulkanu), Jameos del Agua, winnice La Geria na lawie, plaże Papagayo, rejs na wysepkę La Graciosa.",
  flights=[
   ("Katowice, czarter Enter Air", "sob 20.02 08:10 → 13:05", "do sprawdzenia w biurze", "7", "ok. 20 400 zł w jedną stronę", "ok. 2 900 zł w jedną stronę", "same miejsca w czarterze – drogo; szukać pakietu w biurze"),
   ("Warszawa, czarter Enter Air / Smartwings", "sob 20.02 09:10 → 14:10", "do sprawdzenia w biurze", "7", "ok. 17 100 zł w jedną stronę", "ok. 2 450 zł w jedną stronę", "jw."),
  ]),
 dict(id="madera", flag="🇵🇹", name="Madera", tz="Polska − 1 h",
  lead="Zielona, górzysta wyspa wiecznej wiosny – raczej na wędrówki, ogrody i miasteczka niż na plażę. Najwięcej „prawdziwego życia” z europejskich opcji. Z Krakowa bez przesiadki nie ma; Wizz Air z Katowic i z Warszawy.",
  weather=[("W dzień", "18–19°C w Funchal"), ("W nocy", "13–14°C"), ("Morze", "ok. 18°C – chłodne, kąpiel raczej w podgrzewanych basenach"),
           ("Słońce", "ok. 5–6 h dziennie; przelotne deszcze 5–10 dni w miesiącu, zwykle krótkie, rano sucho"),
           ("Uwaga", "w górach (Pico do Arieiro, 1 818 m) ok. 5°C, mgła i wiatr; północ wyspy wilgotniejsza niż Funchal")],
  todo="Lewady – łatwe szlaki wzdłuż kanałów przez las wawrzynowy (także dla dzieci), targ Mercado dos Lavradores, kolejka linowa i zjazd koszami wiklinowymi z Monte, rejs do delfinów, naturalne baseny Porto Moniz, plantacje bananów.",
  flights=[
   ("<b>Katowice, Wizz Air, 8 nocy</b>", "sob 20.02 07:10 → 11:25", "nd 28.02 11:35 → 17:30", "8", "7 676 zł", "ok. 1 095 zł", "2 860 + 4 816 zł; w domu w niedzielę po południu"),
   ("Warszawa, Wizz Air, 9 nocy", "pt 19.02 11:25 → 15:55", "nd 28.02 16:40 → 22:50", "9", "5 845 zł", "ok. 835 zł", "3 182 + 2 663 zł; dojazd do Warszawy"),
   ("Warszawa, Wizz Air, tydzień", "nd 21.02 11:25 → 15:55", "nd 28.02 16:40 → 22:50", "7", "5 474 zł", "ok. 780 zł", "2 811 + 2 663 zł"),
  ]),
 dict(id="azory", flag="🇵🇹", name="Azory (São Miguel)", tz="Polska − 2 h",
  lead="Najbardziej dzika i przyrodnicza opcja: kratery z jeziorami, gorące źródła, jedyne w Europie plantacje herbaty, ananasy pod szkłem. Ale w lutym <b>chłodno, deszczowo i wietrznie</b> – to nie wyjazd na plażę. Bez przesiadki z Polski nie ma; najlepiej TAP z Warszawy przez Lizbonę (jeden bilet).",
  weather=[("W dzień", "16–17°C"), ("W nocy", "11–12°C"), ("Morze", "ok. 16°C – za zimno na kąpiel"),
           ("Słońce", "4–6 h dziennie; deszcz w 13–19 dniach miesiąca, pogoda zmienia się kilka razy dziennie"),
           ("Uwaga", "wiatr i mgła na kraterach (widoki na Sete Cidades bywają zasłonięte); <b>ciepła kąpiel w gorących źródłach Furnas i Terra Nostra (35–40°C) przy każdej pogodzie</b>")],
  todo="Gorące źródła i obiad cozido gotowany w wulkanicznej ziemi w Furnas, plantacje herbaty Gorreana, szklarnie z ananasami, jeziora Sete Cidades i Lagoa do Fogo, rejs do kaszalotów (żyją tu cały rok, ale zimą rejsy zależą od pogody).",
  flights=[
   ("<b>Warszawa, TAP przez Lizbonę, 8 nocy</b>", "pt 19.02 17:55 → 23:45 (50 min w Lizbonie)", "sob 27.02 19:25 → nd 12:10 (8 h 20 min nocą w Lizbonie)", "8", "8 614 zł", "ok. 1 230 zł", "jeden bilet; minus: noc na lotnisku w Lizbonie w drodze powrotnej"),
   ("Warszawa, TAP + LOT, wygodny powrót", "pt 19.02 17:55 → 23:45", "sob 27.02 09:30 → 20:00 (1 h 55 min w Lizbonie)", "8", "12 679 zł", "ok. 1 810 zł", "powrót za dnia, w domu w sobotę wieczorem"),
   ("Kraków, Ryanair + Azores Airlines przez Porto", "sob 20.02 16:40 → 23:25", "nd 28.02 17:45 → pn 11:20 (noc w Porto)", "8", "11 607 zł", "ok. 1 660 zł", "osobne bilety, przesiadki na własne ryzyko – odradzamy"),
  ]),
]

SUMMARY = [  # (anchor, name, best option, total, per person, weather in one line, verdict)
 ("teneryfa", "🇪🇸 Teneryfa", "Kraków, sob 20.02 → sob 27.02", "9 812 zł", "ok. 1 400 zł", "22°C, morze 19°C, słońce", "<b>najpewniejsze ciepło</b>, plaża + wulkan + walenie"),
 ("gran-canaria", "🇪🇸 Gran Canaria", "Kraków, pt 19.02 → nd 28.02", "10 122 zł", "ok. 1 445 zł", "22°C, morze 19°C, słońce", "plaże i wydmy, pogoda jak Teneryfa"),
 ("fuerteventura", "🇪🇸 Fuerteventura", "Katowice, pt 19.02 → pn 1.03", "5 593 zł", "ok. 800 zł", "21°C, morze 18,5°C, wiatr", "<b>najtaniej</b>, najlepsze plaże, ale wietrznie"),
 ("lanzarote", "🇪🇸 Lanzarote", "tylko czarter / pakiet", "–", "–", "21°C, morze 19°C, wiatr", "wulkany; same bilety drogie"),
 ("madera", "🇵🇹 Madera", "Katowice, sob 20.02 → nd 28.02", "7 676 zł", "ok. 1 095 zł", "18–19°C, morze 18°C, przelotne deszcze", "<b>najwięcej przyrody i życia</b>, mniej plaży"),
 ("azory", "🇵🇹 Azory", "Warszawa (TAP), pt 19.02 → sob 27.02", "8 614 zł", "ok. 1 230 zł", "16–17°C, deszcz i wiatr", "przygoda i gorące źródła, nie plaża"),
]


def dest_html(d):
    w = ''.join(f'<li><b>{a}:</b> {b}</li>' for a, b in d["weather"])
    rows = ''.join(f'<tr><td>{f[0]}</td><td>{f[1]}</td><td>{f[2]}</td><td>{f[3]}</td><td class="p">{f[4]}</td><td>{f[5]}</td><td class="m">{f[6]}</td></tr>'
                   for f in d["flights"])
    return (f'<h2 id="{d["id"]}">{d["flag"]} {d["name"]}</h2>'
            f'<div class="card"><p>{d["lead"]}</p>'
            f'<h3 style="margin:14px 0 4px">☀️ Pogoda w drugiej połowie lutego</h3><ul class="pts">{w}<li><b>Czas:</b> {d["tz"]}</li></ul>'
            f'<h3 style="margin:14px 0 4px">✈ Konkretne loty (7 osób)</h3>'
            f'<div class="sumwrap"><table class="sum"><tr><th>Wariant</th><th>Tam</th><th>Z powrotem</th><th>Noce</th><th>Za 7 osób</th><th>Na osobę</th><th>Uwagi</th></tr>{rows}</table></div>'
            f'<p class="bio">🧭 <b>Na miejscu:</b> {d["todo"]}</p></div>')


def main():
    summ = ''.join(f'<tr><td><a href="#{a}"><b>{n}</b></a></td><td>{o}</td><td class="p">{t}</td><td>{pp}</td><td>{w}</td><td>{v}</td></tr>'
                   for a, n, o, t, pp, w, v in SUMMARY)
    body = (
        '<div class="card intro"><p><b>Pomysł:</b> zamiast dalekiej Azji – 7 do 10 dni bliżej, w tym samym terminie (wylot pt 19.02 – nd 21.02). '
        'Sprawdziliśmy Maderę, Wyspy Kanaryjskie i Azory: konkretne loty bez przesiadki z Krakowa, Katowic i Warszawy dla 4 dorosłych + 3 dzieci, '
        'ceny z KAYAK z 19.11.2026.</p>'
        '<p><b>Ważne:</b> to tanie linie (Ryanair, Wizz Air) – w cenie tylko mały bagaż pod fotel. Walizka rejestrowana to zwykle ok. 150–250 zł '
        'za sztukę w jedną stronę (przy 3–4 walizkach na grupę ok. 1 000–2 000 zł w obie strony). Lot trwa 4,5–6 h – bez zmiany strefy czasowej, '
        'dzieci nie odczuwają różnicy czasu.</p></div>'
        '<h2>W skrócie</h2><div class="sumwrap"><table class="sum"><tr><th>Kierunek</th><th>Najlepszy wariant</th><th>Za 7 osób</th><th>Na osobę</th>'
        f'<th>Pogoda</th><th>Dla kogo</th></tr>{summ}</table></div>'
        '<p class="note">Ceny za bilety w obie strony bez walizek. Dla porównania Azja (Hainan, Borneo, Filipiny, Sri Lanka): ok. 28 500–33 000 zł za 7 osób – '
        '<a href="loty-sri-lanka.html#porownanie">porównanie lotów do Azji</a>.</p>'
        '<div class="callout info">☀️ <b>Pogoda w jednym zdaniu:</b> najcieplej i najpewniej na południu <b>Teneryfy i Gran Canarii</b> (22°C, morze 19°C); '
        '<b>Fuerteventura</b> tak samo ciepła, ale wietrzna; <b>Madera</b> o 3–4°C chłodniejsza, z przelotnymi deszczami – bardziej na wędrówki niż plażę; '
        '<b>Azory</b> to 16°C, deszcz i wiatr – na przyrodę i gorące źródła, nie na kąpiel w morzu.</div>'
        + ''.join(dest_html(d) for d in DEST) +
        '<div class="callout">Źródła pogody: średnie wieloletnie dla lutego (weather2travel, holiday-weather, guidetocanaryislands, '
        'dane Regionu Madery) – zaokrąglone; konkretna pogoda w danym roku może się różnić o kilka stopni. '
        'Ceny lotów: KAYAK 19.11.2026, wyszukiwanie w jedną stronę bez przesiadek, 4 dorosłych + 3 dzieci; ceny tanich linii szybko rosną.</div>'
    )
    out = B.page("Ferie 2027 bliżej: Madera, Kanary, Azory", body, back=True)
    out = out.replace("Google Flights, 19.11.2026: w obie strony, najtańsza taryfa (bagaż podręczny), dziecko = dorosły.",
                      "KAYAK, 19.11.2026: bilety w jedną stronę bez przesiadek, 4 dorosłych + 3 dzieci, bez walizek.")
    (OUT / "europa.html").write_text(out)
    print("built europa.html")


if __name__ == "__main__":
    main()
