#!/usr/bin/env python3
"""Sri Lanka flights board: loty-sri-lanka.html, built from loty-sri-lanka.json (since 14.11.2026).

The routine loty-sri-lanka (Center, Tue/Fri) keeps the JSON up to date after every run, then:
    python3 loty_sri_lanka.py && git add loty-sri-lanka.* && git commit -m "Loty Sri Lanka DD.MM" && git push
Looks and building blocks (cards, timeline, Gulf badges, stats, booking links) come from build.py,
so this page reads exactly like the destination pages of the ferie-2027 site.

JSON: {"updated": "DD.MM.YYYY", "intro": html, "comfort": html, "options": [...]} - options in ranking order
(best first). One option:
  title, status ("ok" = priced and bookable | "lead" = a lead, not confirmed | "no" = rejected), tag (optional),
  gulf (bool), pp ("4 175 zł"), p7 (optional), price_date ("14.11"), why (html), comfort (html: aircraft per leg),
  chips [[ok|warn|bad, text]], route, stats [[total, in the air, transfers, extra] | null, same for back] (optional),
  out_title, out [[kind, ...]], back_title, back, out_bio, back_bio, note, book [Google Flights query, airline] (optional).
  Timeline items: ["dep", time, polish time, text], ["arr", ...], ["stop", time, pl, text, box], ["fly", text], ["night", text].
"""
import html, json, pathlib
import build as B

OUT = pathlib.Path(__file__).parent
DATA = json.loads((OUT / "loty-sri-lanka.json").read_text())
B.UPDATED = DATA["updated"]
B.AL.update({"Edelweiss": "https://www.flyedelweiss.com/pl", "SWISS": "https://www.swiss.com/pl/pl/homepage",
             "Qatar Airways": "https://www.qatarairways.com/pl-pl/homepage.html", "Emirates": "https://www.emirates.com/pl/polish/",
             "SriLankan": "https://www.srilankan.com/pl_pl/", "French Bee": "https://www.frenchbee.com/pl",
             "Etihad": "https://www.etihad.com/pl-pl/", "IndiGo": "https://www.goindigo.in/", "Air India": "https://www.airindia.com/"})
STATUS = {"ok": ('ok', 'Sprawdzona cena'), "lead": ('warn', 'Trop – do potwierdzenia'), "no": ('bad', 'Odrzucona')}


def item(it):
    k = it[0]
    if k == "fly": return B.fly(it[1])
    if k == "night": return B.night(it[1])
    if k == "stop": return B.stop(it[1], it[2], it[3], it[4] if len(it) > 4 else None)
    return (B.dep if k == "dep" else B.arr)(it[1], it[2], it[3])


def card(o, i):
    o = dict(o)
    o["out"] = [item(x) for x in o.get("out", [])]
    o["back"] = [item(x) for x in o.get("back", [])]
    o.setdefault("back_title", "Powrót")
    o["_route"] = o.get("route", "")
    o["_stats"] = tuple(tuple(s) if s else None for s in o["stats"]) if o.get("stats") else None
    o["_book"] = tuple(o["book"]) if o.get("book") else None
    o["_kayak"] = None
    if o.get("price_date"):
        o["why"] = f'{o["why"]} <span class="m">(cena: Google Flights {o["price_date"]})</span>'
    k, label = STATUS[o.get("status", "ok")]
    chips = B.chip_html([(k, label)] + [tuple(c) for c in o.get("chips", [])])
    comfort = f'<div class="bio">💺 <b>Komfort:</b> {o["comfort"]}</div>' if o.get("comfort") else ''
    h = B.option(o, i)
    # status + chips right under the title line, comfort box right after the "why" paragraph
    h = h.replace('<p class="route">', f'<div class="flags">{chips}</div><p class="route">', 1)
    h = h.replace(f'<p class="why">{o["why"]}</p>', f'<p class="why">{o["why"]}</p>{comfort}', 1)
    return h.replace('class="card best"', 'class="card"', 1) if i != 1 else h


def main():
    ops = DATA["options"]
    ranked = ''.join(card(o, i) for i, o in enumerate(ops, 1))
    body = (f'<div class="card intro">{DATA["intro"]}</div>'
            f'<div class="callout info">{DATA["comfort"]}</div>'
            f'<h2>Wszystkie opcje – od najlepszej do najsłabszej</h2>'
            f'<p class="note">Ceny za osobę w obie strony, przy rezerwacji dla 7 osób (4 dorosłych + 3 dzieci). '
            f'Godziny lokalne; na szaro czas polski. Aktualizacja we wtorki i piątki rano.</p>{ranked}'
            f'<div class="callout"><a href="sri-lanka.html">Sri Lanka – opis kierunku</a> · '
            f'<a href="info.html">Zatoka, ubezpieczenie, bagaż →</a></div>')
    (OUT / "loty-sri-lanka.html").write_text(B.page(f"Sri Lanka: loty – stan na {DATA['updated']}", body, back=True))
    print("built loty-sri-lanka.html,", len(ops), "options")


if __name__ == "__main__":
    main()
