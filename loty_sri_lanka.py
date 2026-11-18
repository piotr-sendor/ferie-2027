#!/usr/bin/env python3
"""Sri Lanka flights board: loty-sri-lanka.html, built from loty-sri-lanka.json (since 14.11.2026).

The routine loty-sri-lanka (Center, Tue/Fri) keeps the JSON up to date after every run, then:
    python3 loty_sri_lanka.py && git add loty-sri-lanka.* && git commit -m "Loty Sri Lanka DD.MM" && git push
Looks and building blocks (cards, timeline, Gulf badges, stats, booking links) come from build.py,
so this page reads exactly like the destination pages of the ferie-2027 site.

JSON: {"updated": "DD.MM.YYYY", "show": 8 (how many best options stay visible; the rest is folded), "intro": html, "comfort": html, "options": [...]} - options in ranking order
(best first). One option:
  title, status ("ok" = priced and bookable | "lead" = a lead, not confirmed | "no" = rejected), tag (optional),
  gulf (bool), pp ("4 175 zł"), p7 (optional), price_date ("14.11"), why (html), comfort (html: aircraft per leg),
  chips [[ok|warn|bad, text]], route, stats [[total, in the air, transfers, extra] | null, same for back] (optional),
  out_title, out [[kind, ...]], back_title, back, out_bio, back_bio, note, book [Google Flights query, airline] (optional).
  kayak (optional): KAYAK path for the booking button. "others" (optional): same cards for other destinations,
  shown after the Sri Lanka ranking under "Inne kierunki"; "others_note": one line above them.
  others may carry "group"; DATA["groups"][group] = {title, lead, points, summary_name, summary, summary_pp} gives
  the destination header (shared facts) and one row in "W skrócie" for the whole group.
  summary + summary_name (optional): the option gets a row in the "W skrócie" table at the top.
  points [[label, html]] and variants {"head": [...], "rows": [[...]]} (optional): short facts / comparison table.
  Timeline items: ["dep", time, polish time, text], ["arr", ...], ["stop", time, pl, text, box], ["fly", text], ["night", text].
"""
import html, json, pathlib
import build as B

OUT = pathlib.Path(__file__).parent
DATA = json.loads((OUT / "loty-sri-lanka.json").read_text())
B.UPDATED = DATA["updated"]
B.AL.update({"SAS": "https://www.flysas.com/pl-pl/", "Edelweiss": "https://www.flyedelweiss.com/pl", "SWISS": "https://www.swiss.com/pl/pl/homepage",
             "Qatar Airways": "https://www.qatarairways.com/pl-pl/homepage.html", "Emirates": "https://www.emirates.com/pl/polish/",
             "SriLankan": "https://www.srilankan.com/pl_pl/", "French Bee": "https://www.frenchbee.com/pl",
             "Etihad": "https://www.etihad.com/pl-pl/", "Air China": "https://www.airchina.com.cn/en/", "IndiGo": "https://www.goindigo.in/", "Air India": "https://www.airindia.com/"})
STATUS = {"ok": ('ok', 'Sprawdzona cena'), "lead": ('warn', 'Trop – do potwierdzenia'), "no": ('bad', 'Odrzucona')}


MORE_CSS = ('<style>details.more{margin:18px 0}details.more>summary{cursor:pointer;font-weight:700;color:#0b7a75;'
            'background:#fff;border:1px solid #e3e8ec;border-radius:12px;padding:14px 16px;list-style:none}'
            'details.more>summary::-webkit-details-marker{display:none}details.more>summary:before{content:"▸ "}'
            'details.more[open]>summary:before{content:"▾ "}'
            'ul.pts{margin:10px 0 4px;padding-left:0;list-style:none}ul.pts li{padding:5px 0;border-bottom:1px dashed #e3e8ec;font-size:15px}'
            'ul.pts li:last-child{border-bottom:0}table.var,table.sum{width:100%;border-collapse:collapse;font-size:14px;margin:10px 0}'
            'table.var th,table.var td,table.sum th,table.sum td{text-align:left;padding:7px 6px;border-bottom:1px solid #e3e8ec;vertical-align:top}'
            'table.var th,table.sum th{color:#62707c;font-weight:600;font-size:12.5px}table.sum td.p{white-space:nowrap;font-weight:700;color:#0b7a75}'
            '.sumwrap{overflow-x:auto}.slist{display:flex;flex-direction:column;gap:8px}'
            '.srow{display:grid;grid-template-columns:1fr auto;gap:4px 10px;background:#fff;border:1px solid #e3e8ec;border-radius:12px;'
            'padding:12px 14px;text-decoration:none;color:#1f2a33}.srow .sn{font-weight:700;color:#0e5f8a}'
            '.srow .sp{font-weight:800;color:#0b7a75;white-space:nowrap;text-align:right}.srow .sl{grid-column:1/-1;font-size:14px;color:#62707c}'
            '.srow .flag{margin-right:4px}</style>')


def anchor(prefix, i):
    return f"{prefix}-{i}"


def item(it):
    k = it[0]
    if k == "fly": return B.fly(it[1])
    if k == "night": return B.night(it[1])
    if k == "stop": return B.stop(it[1], it[2], it[3], it[4] if len(it) > 4 else None)
    return (B.dep if k == "dep" else B.arr)(it[1], it[2], it[3])


def card(o, i, aid=None):
    o = dict(o)
    o["out"] = [item(x) for x in o.get("out", [])]
    o["back"] = [item(x) for x in o.get("back", [])]
    o.setdefault("back_title", "Powrót")
    o["_route"] = o.get("route", "")
    o["_stats"] = tuple(tuple(s) if s else None for s in o["stats"]) if o.get("stats") else None
    o["_book"] = tuple(o["book"]) if o.get("book") else None
    o["_kayak"] = o.get("kayak")  # KAYAK path, e.g. "KRK-COK/2027-02-19/2027-03-06" (button "Sprawdź i zarezerwuj (KAYAK)")
    if o.get("price_date"):
        src = o["price_date"] if any(c.isalpha() for c in o["price_date"]) else f'Google Flights {o["price_date"]}'
        o["why"] = f'{o["why"]} <span class="m">(cena: {src})</span>'
    k, label = STATUS[o.get("status", "ok")]
    chips = B.chip_html([(k, label)] + [tuple(c) for c in o.get("chips", [])])
    comfort = f'<div class="bio">💺 <b>Komfort:</b> {o["comfort"]}</div>' if o.get("comfort") else ''
    if o.get("points"):  # [[label, html], ...] – short facts instead of a long paragraph
        comfort += '<ul class="pts">' + ''.join(f'<li><b>{a}:</b> {b}</li>' for a, b in o["points"]) + '</ul>'
    if o.get("variants"):  # {"head": [...], "rows": [[...], ...]} – compact comparison table
        v = o["variants"]
        comfort += ('<div class="sumwrap"><table class="var"><tr>' + ''.join(f'<th>{x}</th>' for x in v["head"]) + '</tr>'
                    + ''.join('<tr>' + ''.join(f'<td>{x}</td>' for x in r) + '</tr>' for r in v["rows"]) + '</table></div>')
    h = B.option(o, i)
    # status + chips right under the title line, comfort box right after the "why" paragraph
    h = h.replace('<p class="route">', f'<div class="flags">{chips}</div><p class="route">', 1)
    h = h.replace(f'<p class="why">{o["why"]}</p>', f'<p class="why">{o["why"]}</p>{comfort}', 1)
    if o.get("kayak"):  # build.py's KAYAK button is worded for multi-city trips with local flights
        h = h.replace("(KAYAK, wiele miast)", "(KAYAK)")
        if not o.get("local_flights"):
            h = h.replace('<p class="note">Bilet długi; loty lokalne kupuje się osobno.</p>', '')
    if aid:
        h = h.replace('<div class="card', f'<div id="{aid}" class="card', 1)
    return h.replace('class="card best"', 'class="card"', 1) if i != 1 else h


def summary_table(ops, others):
    """'W skrócie': every option or other destination with a "summary" line, prices taken from the cards (no drift).
    Phone-first: one compact block per row instead of a wide table."""
    rows = []
    groups, seen = DATA.get("groups", {}), set()
    for prefix, lst in (("sl", ops), ("inne", others)):
        for i, o in enumerate(lst, 1):
            g = o.get("group")
            if g in groups and g not in seen and groups[g].get("summary"):  # one row for a whole destination group
                seen.add(g); gr = groups[g]
                rows.append(f'<a class="srow" href="#g-{g}"><span class="sn">{gr["summary_name"]}</span>'
                            f'<span class="sp">{gr["summary_pp"]}</span><span class="sl"><span class="flag ok">✓ bez Zatoki</span> {gr["summary"]}</span></a>')
            if o.get("summary"):
                g = '<span class="flag warn">! przez Zatokę</span>' if o.get("gulf") else '<span class="flag ok">✓ bez Zatoki</span>'
                rows.append(f'<a class="srow" href="#{anchor(prefix, i)}"><span class="sn">{o["summary_name"]}</span>'
                            f'<span class="sp">{o.get("summary_pp", o["pp"])}</span><span class="sl">{g} {o["summary"]}</span></a>')
    if not rows:
        return ''
    return ('<h2>W skrócie</h2><div class="slist">' + ''.join(rows) + '</div>'
            '<p class="note">Kliknij wiersz, żeby przejść do szczegółów. Ceny za osobę w obie strony, przy 7 osobach.</p>')


def main():
    ops = DATA["options"]
    show = DATA.get("show", 8)  # Piotr 14.11: only the best real options in view, the rest folded under "Pozostałe opcje"
    ranked = ''.join(card(o, i, anchor("sl", i)) for i, o in enumerate(ops[:show], 1))
    rest = ops[show:]
    if rest:
        ranked += (f'<details class="more"><summary>Pozostałe opcje na Sri Lankę ({len(rest)}) – słabsze, droższe albo odrzucone. '
                   f'Kliknij, żeby rozwinąć</summary>' + ''.join(card(o, i, anchor("sl", i)) for i, o in enumerate(rest, show + 1)) + '</details>')
    others = DATA.get("others", [])
    groups = DATA.get("groups", {})
    other_html, cur = '', None
    for i, o in enumerate(others, 1):
        g = o.get("group")
        if g != cur and g in groups:  # destination header: shared facts once, then one card per flight variant
            gr = groups[g]
            pts = ''.join(f'<li><b>{a}:</b> {b}</li>' for a, b in gr.get("points", []))
            other_html += (f'<h3 id="g-{g}" style="font-size:20px;margin:28px 0 8px">{gr["title"]}</h3>'
                           f'<div class="card intro"><p>{gr.get("lead", "")}</p><ul class="pts">{pts}</ul></div>')
        cur = g
        other_html += card(o, i, anchor("inne", i))
    if others:
        other_html = (f'<h2 id="inne">Inne kierunki – też warte rozważenia</h2><p class="note">{DATA.get("others_note", "")}</p>'
                      + other_html)

    body = (f'<div class="card intro">{DATA["intro"]}</div>' + summary_table(ops, others) +
            f'<div class="callout info">{DATA["comfort"]}</div>'
            f'<h2 id="sri-lanka">Najlepsze opcje na Sri Lankę</h2>'
            f'<p class="note">Ceny za osobę w obie strony, przy rezerwacji dla 7 osób (4 dorosłych + 3 dzieci). '
            f'Godziny lokalne; na szaro czas polski. Aktualizacja we wtorki i piątki rano.</p>{ranked}{other_html}'
            f'<div class="callout"><a href="sri-lanka.html">Sri Lanka – opis kierunku</a> · '
            f'<a href="info.html">Zatoka, ubezpieczenie, bagaż →</a></div>')
    body = MORE_CSS + body
    html_out = B.page(f"Sri Lanka i inne kierunki: loty – stan na {DATA['updated']}", body, back=True)
    # build.py's footer says "dziecko = dorosły"; our prices are searched for 4 adults + 3 children (Codex 14.11)
    html_out = html_out.replace("dziecko = dorosły", "ceny dla 4 dorosłych + 3 dzieci (8, 8, 6 lat), za osobę")
    (OUT / "loty-sri-lanka.html").write_text(html_out)
    print("built loty-sri-lanka.html,", len(ops), "options")


if __name__ == "__main__":
    main()
