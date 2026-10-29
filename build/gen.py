"""Bygger Craft Kids-utkastet. Kör från repo-roten:  python3 build/gen.py"""
import json, html, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from content import P
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = ROOT
cat = json.load(open(os.path.join(ROOT, "catalogue.json")))
CAT = {"STEM-light":"Teknik & experiment","recycled":"Återbruk","paper":"Papper","nature":"Natur","weaving":"Vävning","yarn":"Garn","costume":"Utklädnad","seasonal-winter":"Vinter","seasonal-christmas":"Jul","seasonal-autumn":"Höst & Halloween","seasonal-any":"Alla högtider","halloween":"Halloween"}
MESS = {"low":"Lite stök","medium":"Lagom stök","high":"Mycket stök"}
SET = {"indoor":"Inomhus","outdoor":"Utomhus","indoor build / outdoor use":"Byggs inne, används ute","indoor / on the go":"Inomhus eller på resan"}
TIME = {"30–45 min":"30–45 minuter","45–60 min (can expand)":"45–60 minuter (kan byggas ut)","15–20 min":"15–20 minuter","45 min + paint drying":"45 minuter + torktid för färgen","20–40 min per card":"20–40 minuter per kort","45 min":"45 minuter","20–30 min":"20–30 minuter","45 min + 1–2 days drying":"45 minuter + 1–2 dygns torktid","30–40 min + paint drying":"30–40 minuter + torktid för färgen","45–60 min":"45–60 minuter","30 min + glue drying":"30 minuter + torktid för limmet","30–45 min (+ 20 min if making the dough)":"30–45 minuter"}
e = html.escape
NAV = [("hem","index.html","Hem"),("pyssel","pyssel.html","Alla pyssel"),("om","om.html","Om")]

def page(title, desc, body, current, pre=""):
    nav = "".join(f'<li><a href="{pre}{href}"' + (' aria-current="page"' if key==current else '') + f'>{lbl}</a></li>' for key,href,lbl in NAV)
    return f"""<!doctype html>
<html lang="sv">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<meta name="description" content="{e(desc)}">
<title>{e(title)} – Craft Kids (utkast)</title>
<link rel="stylesheet" href="{pre}assets/style.css">
</head>
<body>
<a class="skip-link" href="#innehall">Hoppa till innehållet</a>
<div class="draft-banner" role="note">Utkast – inte publicerat</div>
<header class="site">
<a class="brand" href="{pre}index.html">Craft Kids<span class="visually-hidden"> – till startsidan</span></a>
<nav class="main" aria-label="Huvudmeny"><ul>{nav}</ul></nav>
</header>
<main id="innehall" tabindex="-1">
{body}
</main>
<footer class="site"><div class="wrap">
<nav aria-label="Sidfot"><ul>{nav}</ul></nav>
<p>Craft Kids – pyssel för barn 9–12 år. Det här är ett <strong>utkast</strong> och är inte publicerat.</p>
<p>Instruktionerna är omskrivna med egna ord. Originalkällorna anges på varje pysselsida.</p>
</div></footer>
</body></html>
"""

def w(rel, s):
    open(os.path.join(SITE, rel), "w").write(s)

items = [i for i in cat["items"] if i["id"] in P]  # bara projekt med svensk text byggs
N = len(items)
NUM = {10:"Tio",11:"Elva",12:"Tolv",17:"Sjutton"}.get(N, str(N))
allcats = []
for it in items:
    for x in it["category"]:
        if x not in allcats: allcats.append(x)

# ---------- Projektsidor ----------
for n, it in enumerate(items):
    c = P[it["id"]]
    tags = "".join(f'<li><a href="../pyssel.html?kategori={x}">{e(CAT[x])}</a></li>' for x in it["category"])
    b  = f'<nav class="breadcrumb" aria-label="Du är här"><ol><li><a href="../index.html">Hem</a></li><li><a href="../pyssel.html">Alla pyssel</a></li><li><span aria-current="page">{e(it["title_sv"])}</span></li></ol></nav>\n'
    b += f'<article aria-labelledby="titel">\n<h1 id="titel">{e(it["title_sv"])}</h1>\n<p class="lead">{c["lead"]}</p>\n'
    b += '<h2 id="fakta">Snabbfakta</h2>\n<dl class="facts" aria-labelledby="fakta">\n'
    b += f'<dt>Ålder</dt><dd>9–12 år</dd>\n<dt>Tid</dt><dd>{TIME[it["time"]]}</dd>\n<dt>Stök</dt><dd>{MESS[it["mess"]]}</dd>\n<dt>Plats</dt><dd>{SET[it["setting"]]}</dd>\n</dl>\n'
    b += f'<h3 id="taggar">Kategorier</h3>\n<ul class="tags" aria-labelledby="taggar">{tags}</ul>\n'
    b += '<section class="safety" aria-labelledby="sakerhet">\n<h2 id="sakerhet"><span aria-hidden="true">⚠️ </span>Säkerhet – läs först</h2>\n<ul>' + "".join(f"<li>{s}</li>" for s in c["safety"]) + "</ul>\n</section>\n"
    b += '<section aria-labelledby="material">\n<h2 id="material">Det här behöver du</h2>\n<ul>' + "".join(f"<li>{m}</li>" for m in c["materials"]) + "</ul>\n</section>\n"
    b += '<section aria-labelledby="steg">\n<h2 id="steg">Så här gör du</h2>\n<ol class="steps">' + "".join(f"<li>{s}</li>" for s in c["steps"]) + "</ol>\n</section>\n"
    b += f'<section aria-labelledby="tips">\n<h2 id="tips">Tips och fundera vidare</h2>\n<p class="tip">{c["tip"]}</p>\n</section>\n'
    b += '<section class="a11y" aria-labelledby="tillganglighet">\n<h2 id="tillganglighet">Tillgänglighet</h2>\n'
    b += '<p>Texten är skriven med enkla ord och korta steg, ett steg i taget. Läs gärna stegen högt tillsammans, eller låt barnet bocka av dem ett efter ett. Den som har svårt med finmotorik kan låta en vuxen eller kompis hålla i, medan barnet bestämmer och designar.</p>\n'
    b += '<h3>Förslag på alt-texter till bilder</h3>\n<ul>' + "".join(f"<li>{e(a)}</li>" for a in c["alts"]) + "</ul>\n</section>\n"
    b += f'<section aria-labelledby="kalla">\n<h2 id="kalla">Källa och inspiration</h2>\n<p class="source">Idén kommer från <strong>{e(it["source"])}</strong> (på engelska): <a href="{e(it["url"])}" hreflang="en">{e(it["title_en"])}</a>. Instruktionerna här är omskrivna med egna ord på svenska.</p>\n' + (f'<p class="source">Halloweenversionen beskrivs också på <a href="{e(it["source_extra"])}" hreflang="en">Science Buddies blogg</a> (på engelska).</p>\n' if it.get("source_extra") else '') + '</section>\n</article>\n'
    prev, nxt = items[n-1], items[(n+1) % len(items)]
    b += f'<nav class="pagenav" aria-label="Fler pyssel"><a href="{prev["id"]}.html"><span aria-hidden="true">← </span>Föregående: {e(prev["title_sv"])}</a><a href="{nxt["id"]}.html">Nästa: {e(nxt["title_sv"])}<span aria-hidden="true"> →</span></a></nav>\n'
    w(f"projects/{it['id']}.html", page(it["title_sv"], c["lead"], b, "pyssel", "../"))
    it["html_path"] = f"projects/{it['id']}.html"; it["status"] = "written"; it["full_page_written"] = True; it.setdefault("written_date", "2026-10-29")

# ---------- Alla pyssel ----------
b  = ('<h1>Alla pyssel</h1>\n<p class="lead">{NUM} pyssel och byggprojekt för 9–12 år, med billigt material – papper, kartong, återbruk, garn och saker från naturen. Välj filter för att hitta rätt pyssel.</p>\n').replace('{NUM}', NUM)
b += '<form id="filters" aria-labelledby="filterrubrik" onsubmit="return false">\n<h2 id="filterrubrik">Filtrera</h2>\n'
b += '<fieldset><legend>Ålder</legend><div class="filter-group"><label><input type="checkbox" name="age" value="9-12" checked disabled> 9–12 år (alla pyssel)</label></div></fieldset>\n'
b += '<fieldset><legend>Kategori – visar pyssel som har minst en av de valda</legend><div class="filter-group">' + "".join(f'<label><input type="checkbox" name="cat" value="{x}"> {e(CAT[x])}</label>' for x in allcats) + '</div></fieldset>\n'
b += '<fieldset><legend>Stök</legend><div class="filter-group">' + "".join(f'<label><input type="checkbox" name="mess" value="{k}"> {v}</label>' for k,v in MESS.items()) + '</div></fieldset>\n'
b += '<fieldset><legend>Plats</legend><div class="filter-group"><label><input type="checkbox" name="place" value="inne"> Kan göras inomhus</label><label><input type="checkbox" name="place" value="ute"> Utomhus</label></div></fieldset>\n'
b += '<button type="button" id="rensa">Rensa filter</button>\n</form>\n'
b += f'<p id="antal" role="status" aria-live="polite">Visar alla {N} pyssel.</p>\n<ul class="cards" id="lista">\n'
for it in items:
    place = "ute" if it["setting"]=="outdoor" else ("inne ute" if "outdoor" in it["setting"] else "inne")
    tags = ", ".join(CAT[x] for x in it["category"])
    b += f'<li data-cat="{" ".join(it["category"])}" data-mess="{it["mess"]}" data-place="{place}"><h2><a href="projects/{it["id"]}.html">{e(it["title_sv"])}</a></h2><p class="meta">9–12 år · {TIME[it["time"]]} · {MESS[it["mess"]]} · {SET[it["setting"]]}</p><p class="meta">Kategorier: {e(tags)}</p></li>\n'
b += '</ul>\n<p id="tomt" hidden>Inga pyssel matchar alla filter. Prova att ta bort ett filter.</p>\n'
b += """<script>
(function(){
 var f=document.getElementById('filters'),items=[].slice.call(document.querySelectorAll('#lista>li')),out=document.getElementById('antal'),tomt=document.getElementById('tomt');
 function vals(n){return [].slice.call(f.querySelectorAll('input[name='+n+']:checked')).map(function(i){return i.value})}
 function has(list,v){return v.split(' ').some(function(x){return list.indexOf(x)>-1})}
 function run(){var c=vals('cat'),m=vals('mess'),p=vals('place'),n=0;
  items.forEach(function(li){var ok=(!c.length||has(c,li.dataset.cat))&&(!m.length||m.indexOf(li.dataset.mess)>-1)&&(!p.length||has(p,li.dataset.place));li.hidden=!ok;if(ok)n++});
  out.textContent=n===items.length?'Visar alla '+n+' pyssel.':'Visar '+n+' av '+items.length+' pyssel.';tomt.hidden=n>0;}
 var k=new URLSearchParams(location.search).get('kategori');
 if(k){var box=f.querySelector('input[name=cat][value="'+k+'"]');if(box)box.checked=true;}
 f.addEventListener('change',run);
 document.getElementById('rensa').addEventListener('click',function(){f.querySelectorAll('input[type=checkbox]:not([disabled])').forEach(function(i){i.checked=false});run()});
 run();
})();
</script>
<noscript><p>Filtren kräver JavaScript. Alla pyssel visas ändå i listan.</p></noscript>
"""
w("pyssel.html", page("Alla pyssel", "Alla pyssel för barn 9–12 år, med filter för kategori, stök och plats.", b, "pyssel"))

# ---------- Hem ----------
counts = {x: sum(x in it["category"] for it in items) for x in allcats}
chips = "".join(f'<li><a href="pyssel.html?kategori={x}">{e(CAT[x])} <span class="visually-hidden">–</span>({counts[x]})</a></li>' for x in allcats)
picks = [items[i] for i in (0, 4, 8)]
b  = '<section class="hero" aria-labelledby="valkommen">\n<h1 id="valkommen">Välkommen till Craft Kids!</h1>\n'
b += '<p class="lead">Här finns pyssel och byggprojekt för dig som är 9–12 år. Du bygger, klipper, flätar och testar – med saker som oftast redan finns hemma: papper, kartong, garn, tomma förpackningar och pinnar från skogen.</p>\n'
b += '<p><a class="cta" href="pyssel.html">Se alla pyssel</a></p>\n</section>\n'
b += '<section aria-labelledby="forvem">\n<h2 id="forvem">Vem är Craft Kids för?</h2>\n<ul class="feature-list">'
b += '<li><h3>Barn 9–12 år</h3><p>Instruktionerna är skrivna så att du kan följa dem själv, ett steg i taget.</p></li>'
b += '<li><h3>Vuxna som pysslar med barn</h3><p>Föräldrar, fritidspersonal och lärare hittar snabbt tid, material och hur mycket det stökar.</p></li>'
b += '<li><h3>Alla som vill läsa lätt</h3><p>Stor text, tydlig kontrast, enkla ord och sidor som fungerar med tangentbord och skärmläsare.</p></li>'
b += '</ul>\n</section>\n'
b += f'<section aria-labelledby="kategorier">\n<h2 id="kategorier">Hitta pyssel efter kategori</h2>\n<ul class="chips">{chips}</ul>\n</section>\n'
b += '<section aria-labelledby="tips3">\n<h2 id="tips3">Tre pyssel att börja med</h2>\n<ul class="cards">'
for it in picks:
    b += f'<li><h3><a href="projects/{it["id"]}.html">{e(it["title_sv"])}</a></h3><p class="meta">{TIME[it["time"]]} · {MESS[it["mess"]]} · {SET[it["setting"]]}</p><p>{P[it["id"]]["lead"]}</p></li>'
b += f'</ul>\n<p><a class="cta cta-secondary" href="pyssel.html">Visa alla {N} pyssel</a></p>\n</section>\n'
hw = [it for it in items if "halloween" in it["category"]]
b += f'<section aria-labelledby="halloween">\n<h2 id="halloween"><span aria-hidden="true">🎃 </span>Halloween-pyssel</h2>\n<p>Det är höst och snart halloween! Vi har {len(hw)} pyssel med fladdermöss, spöken, pumpor och häxor – utan levande ljus.</p>\n<ul class="chips">' + "".join(f'<li><a href="projects/{it["id"]}.html">{e(it["title_sv"])}</a></li>' for it in hw) + '</ul>\n<p><a class="cta cta-secondary" href="pyssel.html?kategori=halloween">Visa alla halloween-pyssel</a></p>\n</section>\n'
b += '<section class="safety" aria-labelledby="sakert">\n<h2 id="sakert"><span aria-hidden="true">⚠️ </span>Pyssla säkert</h2>\n<p>Varje pyssel har en gul säkerhetsruta högst upp. Där står det när en <strong>vuxen behöver hjälpa till</strong>, till exempel med vassa verktyg. Vi använder aldrig levande ljus – bara LED-ljus. <a href="om.html#sakerhet">Läs mer om säkerhet</a>.</p>\n</section>\n'
w("index.html", page("Hem", "Craft Kids – pyssel och byggprojekt för barn 9–12 år, på lätt svenska.", b, "hem"))

# ---------- Om ----------
srcs = sorted({(it["source"]) for it in items})
b  = '<h1>Om Craft Kids</h1>\n<p class="lead">Craft Kids samlar roliga och prisvärda pyssel för barn 9–12 år, skrivna på enkel svenska.</p>\n'
b += '<section aria-labelledby="syfte">\n<h2 id="syfte">Varför finns Craft Kids?</h2>\n<ul><li>Vi vill att alla barn ska kunna skapa – oavsett ekonomi, läsförmåga eller funktionsvariation.</li><li>Materialet ska vara billigt och gärna återbrukat: papper, kartong, garn, förpackningar och saker från naturen.</li><li>Pysslen ska vara lagom utmanande för 9–12 år: lite teknik, lite konst, lite tålamod.</li></ul>\n</section>\n'
b += '<section class="safety" aria-labelledby="sakerhet">\n<h2 id="sakerhet"><span aria-hidden="true">⚠️ </span>Säkerhet</h2>\n<ul>'
b += '<li>Varje pyssel har en säkerhetsruta som ska läsas <strong>innan</strong> du börjar.</li>'
b += '<li>Vassa verktyg, till exempel hobbykniv, ska bara användas av en vuxen. Står det ”vuxen hjälper till” betyder det att en vuxen ska vara med i just det steget.</li>'
b += '<li>Vi använder <strong>aldrig levande ljus</strong> i pysslen – bara batteridrivna LED-ljus.</li>'
b += '<li>Vi föreslår hellre hobbylim eller tejp än limpistol. Om en limpistol ändå används ska en vuxen sköta den.</li>'
b += '<li>Ballonger innehåller latex och smådelar som kulor kan orsaka kvävning hos små barn. Det står på de pyssel där det gäller.</li>'
b += '<li>Ute i naturen använder vi bara sådant som redan ligger på marken.</li>'
b += '</ul>\n</section>\n'
b += '<section aria-labelledby="kallor">\n<h2 id="kallor">Källor och hur vi skriver</h2>\n<p>Idéerna kommer från fria, offentliga pysselsidor. Vi kopierar inte deras texter. I stället skriver vi om instruktionerna med egna ord på enkel svenska, och anpassar säkerhetsråden. Varje pysselsida länkar till originalet.</p>\n'
b += '<p>Källor vi har hämtat idéer från:</p>\n<ul>' + "".join(f"<li>{e(s)}</li>" for s in srcs) + '</ul>\n</section>\n'
b += '<section aria-labelledby="tillg">\n<h2 id="tillg">Tillgänglighet</h2>\n<ul><li>Stor text som går att förstora, och tydlig kontrast mellan text och bakgrund.</li><li>Allt går att använda med tangentbord. En tydlig ram visar var du är på sidan.</li><li>Länken ”Hoppa till innehållet” finns först på varje sida.</li><li>Varje pysselsida har förslag på alt-texter till bilder.</li><li>Hittar du något som inte fungerar? Berätta för oss, så rättar vi det.</li></ul>\n</section>\n'
b += '<section aria-labelledby="status">\n<h2 id="status">Status</h2>\n<p>Webbplatsen är ett <strong>utkast</strong>. Den är inte publicerad och ska inte visas i sökmotorer.</p>\n</section>\n'
w("om.html", page("Om", "Om Craft Kids: syfte, säkerhet, källor och tillgänglighet.", b, "om"))

open(os.path.join(SITE, "robots.txt"), "w").write("# Utkast – inte publicerat\nUser-agent: *\nDisallow: /\n")
cat["updated"] = "2026-10-29"
cat["site"] = "Craft Kids"
cat["site_pages"] = {"home":"index.html","listing":"pyssel.html","about":"om.html"}
cat["site_index"] = "pyssel.html"
cat["shared_css"] = "assets/style.css"
cat["notes"] = "Drafts only, not published (noindex + robots.txt Disallow). Swedish pages rewritten in own words; sources credited. Rebuild: python3 build/gen.py"
json.dump(cat, open(os.path.join(ROOT, "catalogue.json"), "w"), ensure_ascii=False, indent=2)
print("built")
