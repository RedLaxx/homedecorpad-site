# -*- coding: utf-8 -*-
"""HomeDecorPad — site builder.

Run:  python3 _build/build.py
Writes a complete static site into the repo root: HTML pages, sitemap,
robots.txt, ads.txt, .nojekyll, assets and README.
No third-party build tools required to deploy.
"""
import os, re, sys, json, shutil, datetime, html as _html

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import theme
from theme import (CSS, head, footer, consent, art, art_raw, ICON, header, TONES)
import md as md_engine

ROOT = os.path.abspath(os.path.join(HERE, ".."))
CONTENT = os.path.join(ROOT, "content")
BUILD_DATE = datetime.date.today().isoformat()
TODAY = datetime.date.today().strftime("%d %B %Y")


def fmt_date(iso, fallback):
    """2026-09-23 -> 23 September 2026 (or a safe fallback if malformed)."""
    try:
        y, m, dd = (int(x) for x in str(iso)[:10].split("-"))
        return datetime.date(y, m, dd).strftime("%d %B %Y")
    except Exception:
        return fallback


LAUNCH_DATE = "23 September 2026"


def load_settings():
    """Site-wide settings come from content/site.yml so Pages CMS can edit them."""
    path = os.path.join(CONTENT, "site.yml")
    data = {}
    if os.path.exists(path):
        data, _ = md_engine.parse_frontmatter("---\n" + open(path, encoding="utf-8").read() + "\n---")
    return data


SETTINGS = load_settings()
LEGAL_EFFECTIVE = fmt_date(SETTINGS.get("legal_effective_date"), LAUNCH_DATE)
LEGAL_UPDATED = fmt_date(SETTINGS.get("legal_updated_date"), LAUNCH_DATE)
theme.BRAND = BRAND = SETTINGS.get("brand") or "HomeDecorPad"
DOMAIN = (os.environ.get("SITE_DOMAIN") or SETTINGS.get("domain") or "https://homedecorpad.com").rstrip("/")
theme.DOMAIN = DOMAIN
theme.EMAIL = EMAIL = SETTINGS.get("email") or "hello@homedecorpad.com"
TAG = theme.AMAZON_TAG = SETTINGS.get("amazon_tag") or "YOUR-AMAZON-TAG-20"
theme.FORMSPREE_ID = SETTINGS.get("formspree_id") or "YOUR_FORM_ID"
theme.ADSENSE_CLIENT = str(SETTINGS.get("adsense_client") or "").strip()
theme.GA4_ID = str(SETTINGS.get("ga4_id") or "").strip()
theme.PINTEREST_VERIFY = str(SETTINGS.get("pinterest_verify") or "").strip()
_social = SETTINGS.get("social")
theme.SOCIAL = {k: str(v or "").strip() for k, v in _social.items()} if isinstance(_social, dict) else {}

POSTS, POST_BY_SLUG, REL = [], {}, {}

CATS = [
    {"slug": "living-room",   "name": "Living Room",             "motif": "sofa",     "tone": 0,
     "blurb": "Layouts, budget updates and the pieces that make a living room feel finished."},
    {"slug": "bedroom",       "name": "Bedroom",                 "motif": "portrait", "tone": 1,
     "blurb": "Cozy bedrooms you can put together in a weekend — textiles, light and layering."},
    {"slug": "small-space",   "name": "Small Space & Renters",   "motif": "flat",     "tone": 2,
     "blurb": "Studio and apartment ideas that respect a security deposit."},
    {"slug": "get-the-look",  "name": "Get the Look for Less",   "motif": "arch",     "tone": 4,
     "blurb": "A designer look, broken into a shopping list and a budget."},
    {"slug": "finds",         "name": "Home Finds & Deals",      "motif": "finds",    "tone": 0,
     "blurb": "Amazon, Target and Walmart pieces worth the money — and what to skip."},
    {"slug": "diy",           "name": "IKEA Hacks & DIY",        "motif": "hack",     "tone": 3,
     "blurb": "Flat-pack upgrades and no-power-tool projects for renters."},
    {"slug": "color",         "name": "Color & Paint",           "motif": "swatches", "tone": 5,
     "blurb": "Palettes, undertones and how to test paint in your own light."},
    {"slug": "wall-decor",    "name": "Wall Decor & Gallery Walls", "motif": "shelf", "tone": 5,
     "blurb": "Damage-free hanging, gallery layouts and wall styling that stays up."},
    {"slug": "kitchen-dining","name": "Kitchen & Dining",        "motif": "basket",   "tone": 3,
     "blurb": "Kitchen and dining styling for real, lived-in kitchens."},
    {"slug": "organization",  "name": "Organization & Storage",  "motif": "basket",   "tone": 2,
     "blurb": "Storage that looks like decor, not plastic tubs."},
]
CAT = {c["slug"]: c for c in CATS}
SLUG_CAT = {}          # slug -> category, filled while loading so links resolve mid-render
ALIASES = {"room-guides": "categories"}


def resolve_link(href, depth):
    """Turn the content syntax into a URL for a page at the given depth."""
    href = href.strip()
    if href.startswith(("http://", "https://", "mailto:", "#", "tel:")):
        return href
    if href.startswith("post:"):
        return post_url(href[5:].strip(), depth)
    if href.startswith("/"):
        base, _, frag = href[1:].partition("#")
        frag = ALIASES.get(frag, frag)
        return "../" * depth + base + (("#" + frag) if frag else "")
    return href


def load_posts():
    """Read content/posts/*.md and render each one into site HTML."""
    folder = os.path.join(CONTENT, "posts")
    staged = []
    for fn in sorted(os.listdir(folder)):
        if not fn.endswith(".md") or fn.startswith("_") or fn.lower() == "readme.md":
            continue
        raw = open(os.path.join(folder, fn), encoding="utf-8").read()
        fm, body_md = md_engine.parse_frontmatter(raw)
        if fm.get("draft") is True:
            continue
        if not fm.get("title") or not fm.get("date"):
            print(f"  ! skipping content/posts/{fn} — it has no title/date frontmatter")
            continue
        slug = str(fm.get("slug") or fn[:-3])
        cat = str(fm.get("category") or "living-room")
        if cat not in CAT:
            raise SystemExit(f"{fn}: unknown category '{cat}'. "
                             f"Valid values: {', '.join(sorted(CAT))}")
        SLUG_CAT[slug] = cat
        staged.append((slug, cat, fm, body_md))

    out = []
    for slug, cat, fm, body_md in staged:
        html, faq = md_engine.render(body_md, lambda h, d=2: resolve_link(h, d))
        out.append({
            "slug": slug, "cat": cat,
            "title": str(fm.get("title") or slug),
            "h1": str(fm.get("h1") or fm.get("title") or slug),
            "date": str(fm.get("date") or BUILD_DATE)[:10],
            "dek": str(fm.get("dek") or ""),
            "intro": str(fm.get("intro") or ""),
            "tags": list(fm.get("tags") or []),
            "motif": str(fm.get("motif") or CAT[cat]["motif"]),
            "hero_image": str(fm.get("hero_image") or "").strip(),
            "related": list(fm.get("related") or []),
            "body": html, "faq": faq,
        })
    out.sort(key=lambda p: p["date"], reverse=True)
    return out

CAT_NOTES = {
 "kitchen-dining": "Full kitchen and dining guides are in progress. In the meantime, three rules do most of the work: clear the counters down to three objects, warm the bulbs to 2700K, and put one wood board or basket on display so the room has an organic element.",
 "organization": "Full storage guides are coming. Start with the 80/20 version: one basket per surface for things that have no home, vertical storage above the toilet and kitchen cabinets, and a labelled box for the seasonal rotation.",
 "living-room": "Start with layout before decor. Pulling the sofa off the wall, sizing the rug properly and adding a second light source fixes more than any new purchase.",
 "bedroom": "Bedroom guides are expanding into guest rooms and kids' rooms this winter.",
}

REL = {p["slug"]: p.get("related", []) for p in POSTS}


# --------------------------------------------------------------------- helpers
def d(iso, fmt="%d %B %Y"):
    y, m, dd = (int(x) for x in iso.split("-"))
    return datetime.date(y, m, dd).strftime(fmt).lstrip("0")


def read_label(p):
    """Reading time computed from the real word count (~210 wpm)."""
    words = len(re.sub(r"<[^>]+>", " ", p["intro"] + p["body"]).split())
    return f"{max(3, round(words / 210))} min read"


def short(text, n=132):
    t = re.sub(r"\s+", " ", text).strip()
    if len(t) <= n:
        return t
    return t[:n].rsplit(" ", 1)[0] + "…"


def post_url(slug, depth=0):
    cat = SLUG_CAT.get(slug) or (POST_BY_SLUG.get(slug) or {}).get("cat")
    if not cat:
        raise SystemExit(f'Content links to "post:{slug}" but no published post has that slug.')
    return f'{"../"*depth}blog/{cat}/{slug}.html'


def amz(q):
    return "https://www.amazon.com/s?k=" + q.replace(" ", "+") + "&tag=" + TAG


REWRITE_RE = re.compile(r'href="(?:\.\./)+([a-z0-9\-]+(?:\.html)?)(#[a-z0-9\-]+)?"')

def rewrite_links(block, depth):
    """Turn the ../..-style links inside article HTML into depth-correct links."""
    def rep(m):
        base, frag = m.group(1), m.group(2) or ""
        name = base[:-5] if base.endswith(".html") else base
        if name in POST_BY_SLUG:
            href = post_url(name, depth)
        else:
            href = "../" * depth + (base if base.endswith(".html") else base + ".html")
        return f'href="{href}{frag}"'
    block = REWRITE_RE.sub(rep, block)
    return block.replace("#room-guides", "#categories")


def card(p, depth=0, cls_art="c4x3", searchable=True):
    c = CAT[p["cat"]]
    data = f' data-cat="{p["cat"]}" data-text="{_html.escape((p["title"]+" "+p["dek"]+" "+" ".join(p["tags"])).lower(), quote=True)}"' if searchable else ""
    if p.get("hero_image"):
        cover = (f'<div class="cover {cls_art}"><img src="{"../" * depth}{p["hero_image"].lstrip("/")}" alt="" '
                 f'style="width:100%;height:100%;object-fit:cover" loading="lazy"></div>')
    else:
        cover = art(p["motif"], c["tone"], cls_art)
    return f"""<article class="card"{data}>
 {cover}
 <div class="body">
  <span class="chip">{c["name"]}</span>
  <h3><a href="{post_url(p['slug'], depth)}">{p['title']}</a></h3>
  <p>{short(p['dek'])}</p>
  <div class="meta"><span>{d(p['date'])}</span><i></i><span>{read_label(p)}</span></div>
 </div></article>"""


def newsletter(depth=0, dark=True):
    form = ('<form class="field" onsubmit="alert(\'Newsletter is not connected yet — see the README to plug in Kit or MailerLite.\');return false;">'
            '<input type="email" placeholder="you@email.com" aria-label="Email address" required>'
            '<button class="btn" type="submit">Send it over</button></form>')
    if not dark:
        return f"""<section class="section"><div class="container"><div class="panel"><div class="pad center">
 <p class="eyebrow">Free weekly email</p>
 <h2 style="max-width:26ch;margin:0 auto .4em">One good decor idea, every Sunday morning</h2>
 <p class="muted" style="max-width:52ch;margin:0 auto 22px">A single room idea, one budget swap and one thing worth buying this week. No spam, unsubscribe any time.</p>
 <div style="max-width:460px;margin:0 auto">{form}</div>
</div></div></div></section>"""
    return f"""<section class="section"><div class="container"><div class="cta">
 <div>
  <p class="eyebrow" style="color:#E9B8A6">Free weekly email</p>
  <h2>One good decor idea, every Sunday morning</h2>
  <p>A single room idea, one budget swap and one thing worth buying this week. No spam, ever — and no more than one email a week.</p>
 </div>
 <div>{form}<p class="muted" style="color:#A79C8F;margin:12px 0 0;font-size:13px">By subscribing you agree to our <a href="{('../'*depth)}privacy-policy.html" style="color:#C9BFB2;text-decoration:underline">Privacy Policy</a>.</p></div>
</div></div></section>"""


def page(path, title, desc, body, depth=0, canonical="", schema="", current="", og="assets/og-default.jpg"):
    canon = canonical or path
    if canon == "index.html":
        canon = ""            # the homepage canonical is the site root, never /index.html
    out = (head(title, desc, rel="../" * depth, canonical=canon, schema=schema, current=current, og=og)
           + "\n<main id=\"main\">\n" + body + "\n</main>\n"
           + footer("../" * depth) + consent("../" * depth) + "</body></html>\n")
    return path, out


# ----------------------------------------------------------------------- pages
def page_home():
    feat = POSTS[0]
    rest = POSTS[1:7]
    hero_art = f'<div class="art">{art_raw("hero", 4)}</div>'
    chips = "".join(f'<a href="blog.html#{c["slug"]}">{c["name"]}</a>' for c in CATS[:8])
    body = f"""
<section class="container hero">
 <div>
  <p class="eyebrow">Home decor ideas &middot; looks for less</p>
  <h1>Designer-looking rooms without the designer budget.</h1>
  <p class="lede">Practical room ideas, shoppable budget swaps and paint palettes you can recreate this weekend — for real homes with real budgets.</p>
  <div class="btnrow">
   <a class="btn" href="start-here.html">Start here</a>
   <a class="btn ghost" href="blog.html">Browse all decor ideas</a>
  </div>
  <div class="trust">
   <span>{ICON['check']}Budget-first picks</span>
   <span>{ICON['check']}Renter friendly</span>
   <span>{ICON['check']}New ideas weekly</span>
  </div>
 </div>
 {hero_art}
</section>

<section class="section tight"><div class="container">
 <div class="sec-head"><h2 style="font-size:22px">Browse by room</h2><a href="blog.html">All 10 room guides →</a></div>
 <div class="cats">{chips}</div>
</div></section>

<section class="section" id="categories"><div class="container">
 <div class="sec-head"><div><p class="eyebrow">Featured</p><h2>This week's idea</h2></div></div>
 <article class="feature">
  {art(CAT[feat['cat']]['motif'], CAT[feat['cat']]['tone'], 'c3x2')}
  <div class="body">
   <span class="chip">{CAT[feat['cat']]['name']}</span>
   <h2><a href="{post_url(feat['slug'])}">{feat['title']}</a></h2>
   <p>{feat['dek']}</p>
   <div class="meta"><span>{d(feat['date'])}</span><i></i><span>{read_label(feat)}</span></div>
   <div class="btnrow"><a class="btn sm" href="{post_url(feat['slug'])}">Read the guide</a></div>
  </div>
 </article>
</div></section>

<section class="section"><div class="container">
 <div class="sec-head"><div><p class="eyebrow">Latest</p><h2>Fresh decor ideas</h2></div><a href="blog.html">See everything →</a></div>
 <div class="grid">{''.join(card(p) for p in rest)}</div>
</div></section>

<section class="section"><div class="container">
 <div class="panel split">
  <div class="cover">{art_raw('arch', 5)}</div>
  <div class="pad">
   <p class="eyebrow">Signature series</p>
   <h2>One room, three budgets</h2>
   <p class="muted">Every room, styled three ways — a $150 refresh, a $500 upgrade and a full makeover. You get the exact shopping list and the order to buy things in, so you never waste money on the wrong piece first.</p>
   <ul>
    <li><a href="{post_url('one-room-three-budgets-cozy-bedroom')}">Cozy bedroom: $150 / $500 / $1,500</a></li>
    <li><a href="{post_url('warm-minimalist-living-room-under-250')}">Warm minimalist living room under $250</a></li>
    <li><a href="blog.html#get-the-look">All Get the Look for Less guides</a></li>
   </ul>
  </div>
 </div>
</div></section>

<section class="section"><div class="container">
 <div class="sec-head"><div><p class="eyebrow">Start here</p><h2>New to the site? Read these first</h2></div><a href="start-here.html">How it works →</a></div>
 <div class="grid two">
  <div class="prosebox"><h3 style="margin-top:0">Fix the room before you shop it</h3>
   <p class="muted">Twelve layout mistakes that make a room feel small — every fix is free.</p>
   <p><a href="{post_url('living-room-layout-mistakes')}">Read the layout guide →</a></p></div>
  <div class="prosebox"><h3 style="margin-top:0">Choose the palette</h3>
   <p class="muted">Eight neutral-anchored colour palettes with proportions that actually work at home.</p>
   <p><a href="{post_url('home-decor-color-palettes-2027')}">See the palettes →</a></p></div>
 </div>
</div></section>

{newsletter()}
"""
    desc = "Home decor ideas, budget room makeovers, paint palettes and shoppable looks for less. Practical decorating for real homes — new guides every week."
    schema = json.dumps({"@context": "https://schema.org", "@type": "WebSite", "name": BRAND,
                         "url": DOMAIN + "/", "description": desc,
                         "publisher": {"@type": "Organization", "name": BRAND}})
    return page("index.html", f"{BRAND} — Home Decor Ideas, Room Makeovers & Looks for Less",
                desc, body, 0, canonical="index.html", schema=schema)


def page_blog():
    sections = ""
    for c in CATS:
        posts = [p for p in POSTS if p["cat"] == c["slug"]]
        if len(posts) == 1:
            p = posts[0]
            inner = (f'<article class="feature catwide">{art(c["motif"], c["tone"], "c3x2")}'
                     f'<div class="body"><span class="chip">{c["name"]}</span>'
                     f'<h3><a href="{post_url(p["slug"])}">{p["title"]}</a></h3>'
                     f'<p>{p["dek"]}</p><div class="meta"><span>{d(p["date"])}</span><i></i>'
                     f'<span>{read_label(p)}</span></div>'
                     f'<div class="btnrow"><a class="btn sm" href="{post_url(p["slug"])}">Read the guide</a></div></div></article>')
        elif posts:
            inner = f'<div class="grid">{"".join(card(p) for p in posts)}</div>'
        else:
            inner = f'<div class="prosebox"><p class="eyebrow">Guides in progress</p><p style="margin:0">{CAT_NOTES.get(c["slug"], "New guides for this category are being written now.")}</p></div>'
        note = CAT_NOTES.get(c["slug"], "") if posts else ""
        sections += f"""<section class="section catsec" id="{c['slug']}"><div class="container">
 <div class="sec-head"><div><p class="eyebrow">Room guide</p><h2>{c['name']}</h2><p class="muted" style="margin:6px 0 0;max-width:60ch">{c['blurb']}</p></div></div>
 {inner}
 {f'<p class="muted" style="max-width:70ch">{note}</p>' if note else ''}
</div></section>"""
    chips = "".join(f'<button type="button" data-f="{c["slug"]}">{c["name"]}</button>' for c in CATS)
    body = f"""
<section class="section tight"><div class="container" id="categories">
 <p class="eyebrow">All decor ideas</p>
 <h1>Room guides, budget makeovers &amp; home finds</h1>
 <p class="lede" style="max-width:62ch">Every guide is written to be used, not just saved: what to do first, what it costs, and what to skip. Filter by room or search below.</p>
 <div class="field" style="margin:24px 0 18px;max-width:520px">
  <input type="search" id="q" placeholder="Search: small apartment, rug, paint…" aria-label="Search guides">
 </div>
 <div class="cats" id="filters"><button type="button" class="on" data-f="all">All guides</button>{chips}</div>
 <p class="muted" id="empty" style="display:none">No guides match that search yet — try a room name like “bedroom” or a topic like “rug”.</p>
</div></section>
{sections}
{newsletter(0, dark=False)}
<script>
(function(){{
 var q=document.getElementById('q'), btns=document.querySelectorAll('#filters button'), secs=document.querySelectorAll('.catsec'), empty=document.getElementById('empty'), active='all';
 function run(){{
  var term=(q.value||'').toLowerCase().trim(), shown=0;
  secs.forEach(function(s){{
   var vis = (active==='all'||s.id===active); s.hidden=!vis; if(!vis) return;
   var cards=s.querySelectorAll('.card'), any=0;
   cards.forEach(function(cd){{
    var ok=!term||cd.getAttribute('data-text').indexOf(term)>-1;
    cd.style.display=ok?'':'none'; if(ok)any++;
   }});
   shown+=any;
  }});
  empty.style.display=shown?'none':'block';
 }}
 q.addEventListener('input',run);
 btns.forEach(function(b){{b.addEventListener('click',function(){{
  active=b.getAttribute('data-f');
  btns.forEach(function(x){{x.classList.toggle('on',x===b);}});
  run();
  if(active!=='all'){{var t=document.getElementById(active);if(t)window.scrollTo({{top:t.offsetTop-90,behavior:'smooth'}});}}
 }});}});
}})();
</script>
"""
    desc = "Browse all HomeDecorPad guides: living room and bedroom ideas, small apartment decor, budget swaps, Amazon home finds, IKEA hacks, wall decor and paint palettes."
    schema = json.dumps({"@context": "https://schema.org", "@type": "CollectionPage", "name": "All decor ideas",
                         "url": DOMAIN + "/blog.html", "publisher": {"@type": "Organization", "name": BRAND}})
    return page("blog.html", f"All Decor Ideas — Room Guides & Budget Makeovers | {BRAND}", desc, body, 0, schema=schema)


def faq_schema(items):
    """FAQPage markup built from the markdown FAQ section."""
    if not items:
        return ""
    qs = []
    for q, a in items:
        clean = re.sub(r"&[a-z]+;|&#\d+;", " ", re.sub(r"<[^>]+>", " ", a))
        qs.append({"@type": "Question",
                   "name": re.sub(r"<[^>]+>", "", q).strip(),
                   "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"\s+", " ", clean).strip()}})
    return json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": qs})


def page_post(p):
    depth = 2  # /blog/<cat>/<slug>.html
    c = CAT[p["cat"]]
    body_html = p["body"]
    hero = (f'<img src="{"../" * depth}{p["hero_image"].lstrip("/")}" '
            f'alt="{_html.escape(p["title"], quote=True)}" style="width:100%;height:100%;object-fit:cover">') \
        if p.get("hero_image") else art_raw(p["motif"], c["tone"])
    pin_title = p["title"][:100]
    pin_desc = (p["dek"] + " " + " ".join("#" + t.replace(" ", "") for t in p["tags"][:3]))[:480]
    rel = REL.get(p["slug"], [])[:3]
    rel_cards = "".join(card(POST_BY_SLUG[s], depth) for s in rel if s in POST_BY_SLUG)
    body = f"""
<article>
 <div class="container narrow post-head">
  <p class="crumb"><a href="{'../'*depth}index.html">Home</a> / <a href="{'../'*depth}blog.html#{c['slug']}">{c['name']}</a></p>
  <span class="chip">{c['name']}</span>
  <h1>{p['h1']}</h1>
  <p class="lede">{p['intro']}</p>
  <div class="meta"><span>By the {BRAND} team</span><i></i><span>{d(p['date'])}</span><i></i><span>{read_label(p)}</span></div>
 </div>
 <div class="container narrow">
  <div class="post-hero">{hero}<div class="tag"><span>{c['name']} &middot; {BRAND}</span></div></div>
 </div>
 <div class="container narrow article">
  {body_html}
  <div class="pincta">{ICON['pin']}<p><b>Save this idea for later</b>Pin the graphic below to your {c['name'].lower()} board so you can find it when you are ready to shop.</p></div>
  <details class="prosebox" style="margin:0 0 30px">
   <summary style="cursor:pointer;font-family:var(--serif);font-size:19px">Copy-and-paste pin title &amp; description</summary>
   <p class="muted" style="margin-top:12px"><b>Pin title:</b> {pin_title}</p>
   <p class="muted"><b>Pin description:</b> {pin_desc}</p>
  </details>
  <div class="author">{art(c['motif'], (c['tone']+2) % 6, 'c1x1')}
   <div><b>Written by the {BRAND} team</b>
   <p>We test budget decor ideas in real homes, photograph what works, and tell you what to skip. Based in Lagos, writing for readers in the US, UK, Canada and Australia.</p></div>
  </div>
  <div class="share">Found this useful? <a href="{'../'*depth}blog.html#{c['slug']}">More {c['name'].lower()} guides →</a> &nbsp;&middot;&nbsp; <a href="{'../'*depth}affiliate-disclosure.html">How we make money</a></div>
 </div>
</article>

<section class="section"><div class="container">
 <div class="sec-head"><div><p class="eyebrow">Keep reading</p><h2>Related ideas</h2></div><a href="{'../'*depth}blog.html">All guides →</a></div>
 <div class="grid">{rel_cards}</div>
</div></section>

{newsletter(depth)}
"""
    schemas = [{"@context": "https://schema.org", "@type": "Article", "headline": p["h1"],
                "description": p["dek"], "datePublished": p["date"], "dateModified": p["date"],
                "articleSection": c["name"], "keywords": ", ".join(p["tags"]),
                "author": {"@type": "Organization", "name": BRAND},
                "publisher": {"@type": "Organization", "name": BRAND,
                              "logo": {"@type": "ImageObject", "url": DOMAIN + "/assets/og-default.jpg"}},
                "image": f"{DOMAIN}/assets/og-{p['cat']}.jpg",
                "mainEntityOfPage": {"@type": "WebPage", "@id": f"{DOMAIN}/blog/{p['cat']}/{p['slug']}.html"}}]
    fs = faq_schema(p["faq"])
    if fs:
        schemas.append(json.loads(fs))
    schema = json.dumps(schemas[0]) if len(schemas) == 1 else json.dumps({"@context": "https://schema.org", "@graph": schemas})
    return page(f"blog/{p['cat']}/{p['slug']}.html",
                f"{p['title']} | {BRAND}", p["dek"], body, depth,
                canonical=f"blog/{p['cat']}/{p['slug']}.html", schema=schema, og=f"assets/og-{p['cat']}.jpg")


def page_start_here():
    picks = [
        ("living-room-layout-mistakes", "Fix the room before you shop it", "Living room",
         "Twelve free layout fixes that make a room feel bigger and more finished."),
        ("home-decor-color-palettes-2027", "Pick your palette", "Color & paint",
         "Eight 60/30/10 palettes with proportions that actually work at home."),
        ("small-apartment-decor-ideas", "Make a small space feel bigger", "Small space",
         "Ten moves that add up in a 500 sq ft rental."),
        ("warm-minimalist-living-room-under-250", "Get a designer look for less", "Get the look",
         "A complete warm minimalist living room for under $250."),
        ("renter-friendly-wall-decor-ideas", "Decorate without losing your deposit", "Wall decor",
         "Seven damage-free ideas that genuinely stay on the wall."),
        ("amazon-home-finds-look-expensive", "Buy the right pieces", "Home finds",
         "Eleven finds under $60 that read far more expensive than they are."),
    ]
    cards = ""
    for slug, title, kicker, sub in picks:
        p_ = POST_BY_SLUG[slug]; c_ = CAT[p_["cat"]]
        cards += (f'<article class="card">{art(c_["motif"], c_["tone"], "c3x2")}'
                  f'<div class="body"><span class="chip">{kicker}</span>'
                  f'<h3><a href="{post_url(slug)}">{title}</a></h3><p>{sub}</p>'
                  f'<div class="meta"><span>{read_label(p_)}</span><i></i>'
                  f'<a href="{post_url(slug)}">Read →</a></div></div></article>')
    body = f"""
<section class="section tight"><div class="container narrow">
 <p class="eyebrow">Start here</p>
 <h1>Make your home look designed — without a designer budget</h1>
 <p class="lede">{BRAND} is a small library of decor ideas that are actually finishable. Every guide answers three questions: what do I do first, what does it cost, and what can I skip?</p>
 <div class="btnrow"><a class="btn" href="blog.html">Browse all guides</a><a class="btn ghost" href="shop-my-home.html">Shop the looks</a></div>
</div></section>

<section class="section"><div class="container narrow">
 <h2>How this site works</h2>
 <p>Most decor content is aimed at people with a renovation budget. This site is built for the opposite: renters, first apartments, and anyone furnishing a room with a number in mind.</p>
 <ul>
  <li><b>Free fixes before purchases.</b> Layout, light and editing come first because they change a room the most and cost the least.</li>
  <li><b>Prices and order of operations.</b> We tell you what to buy first, so you never spend your budget on the wrong piece.</li>
  <li><b>Honest about the cheap stuff.</b> We will tell you when a budget item is not worth it — and what we would return.</li>
 </ul>

 <h2>The four-step method we use in every room</h2>
 <ol class="steps">
  <li><b>Edit.</b> Clear every surface, then put back only what earns its place. Free, and it does more than any purchase.</li>
  <li><b>Light it.</b> Warm bulbs (2700K), three sources at three heights, and a dimmer wherever it is possible. Under $40 for most rooms.</li>
  <li><b>Anchor it.</b> One large-size rug, and a colour palette of a dominant neutral plus one accent. This is where a room stops feeling like a rental.</li>
  <li><b>Layer it.</b> Texture where colour would be busy: bouclé, linen, wood, brass, a basket, one plant. Never more than three objects per surface.</li>
 </ol>

 <div class="callout"><h4>The rule behind all of it</h4><p>Spend on the things your eye lands on — the rug, the lighting, the bedding — and save on the things it does not. A $25 throw in the right texture beats a $200 lamp you cannot see.</p></div>

 <h2>What we are known for</h2>
 <ul>
  <li><b>Get the Look for Less</b> — a designer look broken into a shopping list and a total. <a href="{post_url('warm-minimalist-living-room-under-250')}">Start with the warm minimalist living room</a>.</li>
  <li><b>One Room, Three Budgets</b> — the same room at $150, $500 and $1,500. <a href="{post_url('one-room-three-budgets-cozy-bedroom')}">See the bedroom</a>.</li>
  <li><b>Room guides</b> — layout, light and styling rules by room. <a href="blog.html#living-room">Living room</a>, <a href="blog.html#small-space">small space</a>, <a href="blog.html#color">colour</a>.</li>
 </ul>
</div></section>

<section class="section"><div class="container">
 <div class="sec-head"><div><p class="eyebrow">Start somewhere</p><h2>Pick your first project</h2></div></div>
 <div class="grid">{cards}</div>
</div></section>

<section class="section"><div class="container narrow prosebox">
 <h2 style="margin-top:0">What is coming next</h2>
 <p class="muted">Kitchen and dining styling, storage that looks like decor, a fall and holiday decorating series, and more One Room Three Budgets makeovers — including a home office and an entryway.</p>
 <p class="muted">The best way to see them first is the weekly email: one room idea, one budget swap and one thing worth buying, every Sunday.</p>
</div></section>

{newsletter()}
"""
    desc = "New here? These are the guides to read first: free layout fixes, colour palettes, small-space ideas and budget looks for less. Start decorating in an afternoon."
    return page("start-here.html", f"Start Here — How to Decorate on a Budget | {BRAND}", desc, body, 0,
                schema=json.dumps({"@context": "https://schema.org", "@type": "AboutPage", "name": "Start Here",
                                   "url": DOMAIN + "/start-here.html",
                                   "publisher": {"@type": "Organization", "name": BRAND}}))


def page_about():
    body = f"""
<section class="section tight"><div class="container narrow">
 <p class="eyebrow">About</p>
 <h1>About {BRAND}</h1>
 <p class="lede">{BRAND} is a home decor site for people who want a room that looks considered — on a normal budget, in a normal apartment, without a renovation.</p>
</div></section>

<section class="section"><div class="container narrow article">
 <h2>Why this site exists</h2>
 <p>Interior design content usually shows you the after photo and hides the invoice. We do the opposite. Every guide includes the price ranges, the order to buy things in, and the things we would not spend money on.</p>
 <p>The site started in 2026 as a way to organise our own decorating notes: which purchases changed a room, which ones photographed well but annoyed us within a month, and which "designer" looks could be recreated with a shopping list instead of a contractor.</p>

 <h2>Who it is for</h2>
 <ul>
  <li>Renters who cannot drill, paint or replace anything.</li>
  <li>First-apartment and small-space dwellers who need every purchase to earn its footprint.</li>
  <li>Anyone who wants a warm, calm, lived-in home rather than a showroom.</li>
 </ul>

 <h2>How we choose what to recommend</h2>
 <ol class="steps">
  <li><b>Texture and warmth first.</b> Matte finishes, natural materials and warm tones. We avoid glossy, printed and cold-toned decor even when it is popular.</li>
  <li><b>Scale matters as much as style.</b> An undersized rug or a tiny lamp is the most common expensive mistake, so we recommend sizes before products.</li>
  <li><b>Real prices.</b> We list typical street prices, and we say when something is only worth buying on sale.</li>
  <li><b>No paid placements.</b> Brands cannot buy a mention, a ranking or a positive review. If we ever publish a sponsored post, it is labelled at the top of the page.</li>
 </ol>

 <div class="callout"><h4>How {BRAND} makes money</h4><p>Two ways only: display advertising, and affiliate commission when you buy through one of our links — at no extra cost to you. Both are explained in our <a href="affiliate-disclosure.html">Affiliate &amp; Advertising Disclosure</a>. Affiliate income never changes what we recommend.</p></div>

 <h2>Our editorial standards</h2>
 <ul>
  <li><b>We test or own the products we feature</b> wherever possible. When we have not used something ourselves, we say so.</li>
  <li><b>Illustrations on this site are original artwork</b> created for {BRAND}. We do not publish other people's photographs as our own.</li>
  <li><b>We correct mistakes.</b> If a price, size or recommendation changes, the guide is updated and the date on the page changes with it.</li>
  <li><b>Some images are AI-assisted.</b> Where a graphic is generated rather than photographed by us, it is decorative only — it is never used to misrepresent a product you could buy.</li>
 </ul>

 <h2>Where we are</h2>
 <p>{BRAND} is written and run by a small team based in Lagos, Nigeria, for readers in the United States, United Kingdom, Canada and Australia. We link to retailers that ship to those countries and we price our recommendations in dollars.</p>

 <h2>Work with us</h2>
 <p>We partner with brands on sponsored placements, product features and affiliate campaigns — always labelled, always relevant to a budget-conscious reader. Email <a href="mailto:{EMAIL}">{EMAIL}</a> or use the <a href="contact.html">contact page</a> and tell us what you have in mind.</p>
</div></section>

{newsletter()}
"""
    desc = f"About {BRAND}: a budget-first home decor site for renters and small-space dwellers. Our editorial standards, how we make money, and how to work with us."
    return page("about.html", f"About {BRAND} — Budget-First Home Decor", desc, body, 0,
                schema=json.dumps({"@context": "https://schema.org", "@type": "AboutPage", "name": f"About {BRAND}",
                                   "url": DOMAIN + "/about.html", "publisher": {"@type": "Organization", "name": BRAND}}))


def page_contact():
    body = f"""
<section class="section tight"><div class="container narrow">
 <p class="eyebrow">Contact</p>
 <h1>Get in touch</h1>
 <p class="lede">Questions about a guide, a product recommendation, or working together? Send a message — we read everything and reply to most emails within two business days.</p>
</div></section>

<section class="section"><div class="container">
 <div class="panel split">
  <div class="pad">
   <h2 style="margin-top:0">Send a message</h2>
   <form action="https://formspree.io/f/{theme.FORMSPREE_ID}" method="POST">
    <div class="form-row"><label for="name">Your name</label><input id="name" name="name" type="text" required></div>
    <div class="form-row"><label for="email">Email</label><input id="email" name="email" type="email" required></div>
    <div class="form-row"><label for="topic">What is this about?</label>
     <select id="topic" name="topic" style="width:100%;padding:13px 16px;border-radius:10px;border:1px solid var(--line);font:inherit">
      <option>Reader question</option><option>Brand partnership or sponsorship</option>
      <option>Press or interview</option><option>Something else</option>
     </select></div>
    <div class="form-row"><label for="msg">Message</label><textarea id="msg" name="message" required></textarea></div>
    <button class="btn" type="submit">Send message</button>
    <p class="muted" style="margin-top:14px">This form is not connected yet — replace <code>{theme.FORMSPREE_ID}</code> with your free <a href="https://formspree.io" rel="noopener" target="_blank">Formspree</a> form ID, or swap in any form service. Until then, email works.</p>
   </form>
  </div>
  <div class="pad" style="background:#FBF6EF">
   <h2 style="margin-top:0">Other ways to reach us</h2>
   <p><b>Email:</b> <a href="mailto:{EMAIL}">{EMAIL}</a></p>
   <p><b>Pinterest:</b> <a href="https://www.pinterest.com/" rel="noopener" target="_blank">Follow {BRAND}</a> — the fastest place to see new guides.</p>
   <p><b>Response time:</b> 1–2 business days, Lagos time (WAT).</p>
   <hr>
   <h3>Work with {BRAND}</h3>
   <p class="muted">Our readers are decorating on a budget: renters, small-space dwellers and first-home buyers in the US, UK, Canada and Australia. We work with brands on:</p>
   <ul class="muted">
    <li>Sponsored placements and editorially-labelled features</li>
    <li>Product photography and styling for brand accounts</li>
    <li>Pinterest and affiliate campaigns built on our guides</li>
   </ul>
   <p class="muted"><b>What we do not do:</b> guest posts, link insertions, paid do-follow links, or unlabelled advertorial. Requests for these are declined.</p>
   <div class="btnrow"><a class="btn sm ghost" href="affiliate-disclosure.html">See our disclosure</a></div>
  </div>
 </div>
</div></section>

<section class="section"><div class="container narrow">
 <h2>Common questions</h2>
 <div class="faq">
  <details><summary>Can I ask you to recommend a product for my room?</summary><p>Yes — send the room, the rough budget and one photo if you have it. We answer as many as we can, and the best ones become guides.</p></details>
  <details><summary>Do you accept guest posts?</summary><p>No. All guides are written in-house. We do consider original, unpublished photography collaborations.</p></details>
  <details><summary>I found a broken link or a wrong price. Where do I report it?</summary><p>Email us with the page name. Prices move constantly, so corrections are genuinely helpful and we fix them quickly.</p></details>
  <details><summary>How do I get my product considered?</summary><p>Email a one-paragraph pitch with a link and a price. We buy most of what we feature. If a product is sent for review it is disclosed in the post.</p></details>
 </div>
</div></section>
"""
    desc = f"Contact {BRAND}: reader questions, corrections, press and brand partnerships. Email {EMAIL} — replies within two business days."
    schema = json.dumps({"@context": "https://schema.org", "@type": "ContactPage", "name": f"Contact {BRAND}",
                         "url": DOMAIN + "/contact.html", "publisher": {"@type": "Organization", "name": BRAND}})
    return page("contact.html", f"Contact & Work With Us | {BRAND}", desc, body, 0, schema=schema)


def page_shop():
    def room(title, slug, tone, motif, items):
        lis = "".join(
            f'<li><span><b><a href="{amz(n)}" target="_blank" rel="nofollow sponsored noopener">{n}</a></b>'
            f'<span class="d">{note}</span></span><span class="p">{price}</span></li>'
            for n, note, price in items)
        return f"""<div class="post-hero narrow" style="aspect-ratio:16/9;margin-bottom:0">{art_raw(motif, tone)}<div class="tag"><span>{title} &middot; shoppable</span></div></div>
<div class="shop"><h3>{title}</h3>
<p class="muted">Typical prices at the time of writing. Links go to Amazon search results — see our <a href="affiliate-disclosure.html">disclosure</a>.</p>
<ul>{lis}</ul></div>"""
    living = room("Warm minimalist living room", "living-room", 4, "arch", [
        ("Chunky knit throw, oat", "50×60 in, visible stitch — the single best value item in the room", "$25–40"),
        ("2 bouclé cushion covers, 18×18 in", "Reuse your existing inserts; covers only", "$24"),
        ("Ribbed ceramic vase", "Matte, unglazed look — with two faux stems", "$18–26"),
        ("Acacia wood serving tray", "16–18 in; groups three objects so surfaces look styled", "$20–28"),
        ("Warm 2700K LED bulbs, 4-pack", "Cheapest design upgrade that exists", "$12"),
        ("Washable rug, 8×10 low pile", "Warm neutral; front legs of every seat must sit on it", "$90–150"),
    ])
    bedroom = room("Cozy layered bedroom", "bedroom", 1, "portrait", [
        ("Washed cotton duvet cover", "Oat or warm white — pre-washed, not sateen", "$45–70"),
        ("Ribbed ceramic table lamps, pair", "Linen shade, 20–24 in tall, warm bulb", "$70–95"),
        ("Oatmeal linen curtains, 96 in", "Two panels per window, hung at ceiling height", "$35–60 each"),
        ("Bouclé lumbar pillow", "14×24 in in cream or camel", "$18–28"),
        ("Storage bench, upholstered", "Hinged lid earns its footprint at the end of the bed", "$90–130"),
    ])
    small = room("Small apartment essentials", "small-space", 2, "flat", [
        ("8×10 washable rug", "Unifies small rooms instead of chopping them into zones", "$90–150"),
        ("Wall mirror, 24×36 in", "Hang opposite the biggest window, not opposite a blank wall", "$45–70"),
        ("Plug-in wall sconce", "Second light height with no wiring and no landlord", "$30–45"),
        ("Over-the-door storage rack, slim", "Cleaning supplies, shoes or pantry overflow", "$25–35"),
        ("Woven basket, 16 in", "Plants, throws or magazines — texture that hides clutter", "$20–28"),
    ])
    body = f"""
<section class="section tight"><div class="container narrow">
 <p class="eyebrow">Shop my home</p>
 <h1>Shop the looks (and how our links work)</h1>
 <p class="lede">These are the pieces we actually use in our own rooms, at the price we would pay. If you buy through a link here, {BRAND} may earn a small commission — at no extra cost to you. It never changes what makes the list.</p>
 <div class="btnrow"><a class="btn" href="blog.html#get-the-look">See the budget looks</a><a class="btn ghost" href="affiliate-disclosure.html">Read the disclosure</a></div>
</div></section>

<section class="section"><div class="container narrow">{living}{bedroom}{small}</div></section>

<section class="section"><div class="container narrow">
 <h2>How to shop a room without wasting money</h2>
 <ol class="steps">
  <li><b>Buy the anchor first.</b> The rug sets the palette and the warmth of everything above it. Buy it before cushions, art or accessories.</li>
  <li><b>Buy textiles before objects.</b> Throws, covers and curtains change how a room feels more than any ornament, and they are usually the cheapest items on the list.</li>
  <li><b>Buy lighting third.</b> Two warm bulbs and one extra lamp will do more than a new side table.</li>
  <li><b>Buy decor last</b> — and only after you have edited the surfaces. Shop with 30% empty space in mind.</li>
 </ol>
 <div class="callout"><h4>Sizing before shopping</h4><p>Measure your room, your sofa and your window before you open a single product page. Most disappointing budget purchases are a sizing mistake, not a quality one: rugs that are too small, curtains that are too short, lamps that are too short for the table they sit on.</p></div>

 <h2>What we do not link to</h2>
 <p class="muted">We do not recommend dropshipped decor with no review history, printed wood-grain finishes, mirrored furniture with bevelled edges, or decorative sets of four. If it only looks good in a product render, it does not make the list.</p>
</div></section>

{newsletter()}
"""
    desc = "Shoppable budget decor: the pieces we actually use in living rooms, bedrooms and small apartments, with typical prices and how our affiliate links work."
    return page("shop-my-home.html", f"Shop My Home — Budget Decor We Actually Use | {BRAND}", desc, body, 0,
                schema=json.dumps({"@context": "https://schema.org", "@type": "CollectionPage", "name": "Shop My Home",
                                   "url": DOMAIN + "/shop-my-home.html",
                                   "publisher": {"@type": "Organization", "name": BRAND}}))


def page_404():
    body = f"""
<section class="section"><div class="container narrow center">
 <p class="eyebrow">404</p>
 <h1>That page has moved out</h1>
 <p class="lede">The link is broken or the guide has been renamed. Try one of these instead:</p>
 <div class="btnrow" style="justify-content:center">
  <a class="btn" href="index.html">Home</a>
  <a class="btn ghost" href="blog.html">All decor ideas</a>
  <a class="btn ghost" href="start-here.html">Start here</a>
 </div>
</div></section>
<section class="section"><div class="container">
 <div class="grid">
  {''.join(card(p) for p in POSTS[:3])}
 </div>
</div></section>
"""
    return page("404.html", f"Page not found | {BRAND}", "That page does not exist. Browse the room guides instead.", body, 0)


# --------------------------------------------------------------- legal markdown
PLACEHOLDER = {
    "[BRAND NAME]": BRAND,
    "[DOMAIN]": "homedecorpad.com",
    "[CONTACT EMAIL]": EMAIL,
    "[LAST UPDATED DATE]": LEGAL_UPDATED,
    "**Effective date:** [EFFECTIVE DATE]": f"**Effective date:** {LEGAL_EFFECTIVE}",
    "**Last updated:** [EFFECTIVE DATE]": f"**Last updated:** {LEGAL_UPDATED}",
    "[EFFECTIVE DATE]": LEGAL_EFFECTIVE,
    "[YOUR LEGAL NAME OR REGISTERED BUSINESS NAME]": "the operator of " + BRAND,
    "[OR YOUR PROVIDER]": "",
    "[Mediavine / Raptive and their vendors — ADD WHEN APPLICABLE]":
        "additional ad networks and their vendors, added when applicable",
}
PATHMAP = {
    "/disclosure/": "affiliate-disclosure.html", "/affiliate-disclosure/": "affiliate-disclosure.html",
    "/cookie-policy/": "cookie-policy.html", "/privacy-policy/": "privacy-policy.html",
    "/terms-of-use/": "terms-of-use.html", "/disclaimer/": "disclaimer.html", "/contact/": "contact.html",
}


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def fix_href(u):
    u = u.strip()
    if u.startswith("#") or u.startswith("mailto:"):
        return u
    if u.startswith("http"):
        return u
    if u.startswith("/"):
        return PATHMAP.get(u + ("/" if not u.endswith("/") else ""), u.lstrip("/"))
    m = re.match(r"^(?:https?://)?homedecorpad\.com(/.*)?$", u)
    if m:
        p = m.group(1) or "/"
        key = p if p.endswith("/") else p + "/"
        if key in PATHMAP:
            return PATHMAP[key]
        return "https://homedecorpad.com" + p
    return u


def inline(s):
    s = esc(s)
    def linkrep(m):
        return f'<a href="{fix_href(_unesc(m.group(2)))}">{m.group(1)}</a>'
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", linkrep, s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"<em>\1</em>", s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    return s


def _unesc(s):
    return s.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")


def md_to_html(md):
    lines = md.replace("\r\n", "\n").split("\n")
    out, i = [], 0
    while i < len(lines):
        ln = lines[i]
        if not ln.strip():
            i += 1
            continue
        if ln.strip() == "---":
            out.append("<hr>"); i += 1; continue
        m = re.match(r"^(#{1,4})\s+(.*)$", ln)
        if m:
            lvl = len(m.group(1))
            out.append(f"<h{lvl}>{inline(m.group(2))}</h{lvl}>"); i += 1; continue
        if ln.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                rows.append(cells); i += 1
            if len(rows) >= 2 and set("".join(rows[1])) <= set("-: "):
                head_row, body_rows = rows[0], rows[2:]
            else:
                head_row, body_rows = rows[0], rows[1:]
            t = "<table><thead><tr>" + "".join(f"<th>{inline(c)}</th>" for c in head_row) + "</tr></thead><tbody>"
            for r in body_rows:
                t += "<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>"
            out.append(t + "</tbody></table>")
            continue
        if ln.startswith(">"):
            block = []
            while i < len(lines) and lines[i].startswith(">"):
                block.append(lines[i].lstrip(">").strip()); i += 1
            out.append("<blockquote>" + inline(" ".join(block)) + "</blockquote>")
            continue
        if re.match(r"^\s*[-*]\s+", ln):
            items = []
            while i < len(lines) and re.match(r"^\s*[-*]\s+", lines[i]):
                items.append(inline(re.sub(r"^\s*[-*]\s+", "", lines[i]))); i += 1
            out.append("<ul>" + "".join(f"<li>{x}</li>" for x in items) + "</ul>")
            continue
        if re.match(r"^\s*\d+\.\s+", ln):
            items = []
            while i < len(lines) and re.match(r"^\s*\d+\.\s+", lines[i]):
                items.append(inline(re.sub(r"^\s*\d+\.\s+", "", lines[i]))); i += 1
            out.append("<ol>" + "".join(f"<li>{x}</li>" for x in items) + "</ol>")
            continue
        para = [ln.strip()]
        i += 1
        while i < len(lines) and lines[i].strip() and not re.match(r"^(#{1,4}\s|\||>|\s*[-*]\s|\s*\d+\.\s|---)", lines[i]):
            para.append(lines[i].strip()); i += 1
        out.append("<p>" + "<br>".join(inline(x) for x in para) + "</p>")
    return "\n".join(out)


LEGAL_FILES = [
    ("privacy-policy.html", "privacy-policy.md", "Privacy Policy"),
    ("cookie-policy.html", "cookie-policy.md", "Cookie Policy"),
    ("terms-of-use.html", "terms-of-use.md", "Terms of Use"),
    ("disclaimer.html", "disclaimer.md", "Disclaimer"),
    ("affiliate-disclosure.html", "affiliate-disclosure.md", "Affiliate & Advertising Disclosure"),
]
LEGAL_DIR = os.path.join(ROOT, "..", "home-decor-blog", "legal")
if not os.path.isdir(LEGAL_DIR):
    LEGAL_DIR = os.path.join(os.path.dirname(ROOT), "home-decor-blog", "legal")


def legal_pages():
    pages = []
    for out_name, src_name, label in LEGAL_FILES:
        src = os.path.join(LEGAL_DIR, src_name)
        md = open(src, encoding="utf-8").read()
        for k, v in PLACEHOLDER.items():
            md = md.replace(k, v)
        html_block = md_to_html(md)
        html_block = re.sub(r"^<h1>.*?</h1>\s*", "", html_block, count=1, flags=re.S)
        pills = "".join(f'<a href="{n}">{l}</a>' for n, _, l in LEGAL_FILES if n != out_name)
        pills += '<a href="contact.html">Contact</a>'
        body = f"""
<section class="container narrow legalhdr">
 <p class="eyebrow">Legal</p>
 <h1>{label}</h1>
 <p class="muted" style="max-width:68ch">{BRAND} (homedecorpad.com). This page is written to be readable, not to hide behind jargon. If anything here is unclear, email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
 <div class="pill-row">{pills}</div>
</section>
<section class="section" style="padding-top:18px"><div class="container narrow article">{html_block}</div></section>
"""
        desc = f"{label} for {BRAND} (homedecorpad.com) — written in plain English, covering cookies, data, ads, affiliate links and your choices."
        pages.append(page(out_name, f"{label} | {BRAND}", desc, body, 0,
                          schema=json.dumps({"@context": "https://schema.org", "@type": "WebPage", "name": label,
                                             "url": f"{DOMAIN}/{out_name}"})))
    return pages


# ------------------------------------------------------------------- extras
def write_extras():
    urls = [("", "1.0", "weekly"), ("blog.html", "0.9", "weekly"), ("start-here.html", "0.8", "monthly"),
            ("shop-my-home.html", "0.8", "monthly"), ("about.html", "0.5", "yearly"),
            ("contact.html", "0.5", "yearly")]
    urls += [(f"blog/{p['cat']}/{p['slug']}.html", "0.9", "monthly") for p in POSTS]
    urls += [("privacy-policy.html", "0.3", "yearly"), ("cookie-policy.html", "0.3", "yearly"),
             ("terms-of-use.html", "0.3", "yearly"), ("disclaimer.html", "0.3", "yearly"),
             ("affiliate-disclosure.html", "0.3", "yearly")]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u, pri, freq in urls:
        sm.append(f" <url><loc>{DOMAIN}/{u}</loc><lastmod>{BUILD_DATE}</lastmod>"
                  f"<changefreq>{freq}</changefreq><priority>{pri}</priority></url>")
    sm.append("</urlset>")
    write("sitemap.xml", "\n".join(sm) + "\n")
    write("robots.txt", f"""# {BRAND}
User-agent: *
Allow: /
Disallow: /404.html

Sitemap: {DOMAIN}/sitemap.xml
""")
    write("ads.txt", f"""# {BRAND} — Authorized Digital Sellers
# After AdSense approves your site, open AdSense > Account > ads.txt and replace
# the line below with the exact line AdSense shows you (it keeps the pub- number).
google.com, pub-XXXXXXXXXXXXXXXX, DIRECT, f08c47fec0942fa0
""")
    write("404.html", page_404()[1])
    write(".nojekyll", "")
    for d_ in ("assets",):
        os.makedirs(os.path.join(ROOT, d_), exist_ok=True)


def write(path, content):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)
    return full


def make_og_image():
    """Social share cards: one default + one per category, drawn in the site palette."""
    try:
        from PIL import Image, ImageDraw, ImageFont
    except Exception as e:
        print("  ! Pillow unavailable, skipping OG images:", e)
        return
    candidates = [os.path.join(ROOT, "assets", "fonts"),
                  os.path.abspath(os.path.join(ROOT, "..", "home-decor-blog", "fonts"))]
    fdir = next((c for c in candidates
                 if os.path.exists(os.path.join(c, "DMSerifDisplay-Regular.ttf"))), None)
    try:
        serif_b = ImageFont.truetype(os.path.join(fdir, "DMSerifDisplay-Regular.ttf"), 70)
        serif_s = ImageFont.truetype(os.path.join(fdir, "DMSerifDisplay-Regular.ttf"), 44)
        sans = ImageFont.truetype(os.path.join(fdir, "Poppins-Medium.ttf"), 25)
        sans_s = ImageFont.truetype(os.path.join(fdir, "Poppins-Medium.ttf"), 23)
    except Exception:
        serif_b = serif_s = sans = sans_s = ImageFont.load_default()
    W, H = 1200, 630

    def rgb(h):
        h = h.lstrip("#")
        return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))

    def draw_card(bg, wall, floor, accent, s2, s3, kicker, out):
        bg, wall, floor, accent, s2, s3 = map(rgb, (bg, wall, floor, accent, s2, s3))
        im = Image.new("RGB", (W, H), bg)
        dr = ImageDraw.Draw(im, "RGBA")
        # ---- floor
        dr.rectangle([0, 430, W, H], fill=floor)
        dr.rectangle([0, 428, W, 432], fill=(43, 38, 34, 26))
        # ---- arch (right of the text column)
        dr.pieslice([700, 110, 980, 390], 180, 360, fill=wall)
        dr.rectangle([700, 240, 980, 430], fill=wall)
        dr.arc([700, 110, 980, 390], 180, 360, fill=(43, 38, 34, 40), width=3)
        dr.ellipse([812, 168, 868, 224], fill=accent + (205,))
        # ---- pilasters / frames
        dr.rectangle([636, 236, 650, 430], fill=s2 + (120,))
        dr.rectangle([1036, 236, 1050, 430], fill=s2 + (120,))
        dr.rounded_rectangle([648, 150, 756, 236], 5, fill=s2 + (210,))
        dr.rounded_rectangle([676, 172, 728, 220], 3, fill=(250, 245, 237, 220))
        # ---- sofa
        dr.rounded_rectangle([708, 300, 1082, 344], 14, fill=(43, 38, 34, 200))
        dr.rounded_rectangle([694, 330, 1096, 406], 20, fill=accent + (255,))
        dr.rounded_rectangle([716, 344, 882, 398], 14, fill=(250, 245, 237, 115))
        dr.rounded_rectangle([908, 344, 1074, 398], 14, fill=(250, 245, 237, 115))
        dr.rounded_rectangle([694, 406, 1096, 430], 12, fill=accent + (255,))
        dr.rounded_rectangle([726, 430, 740, 452], 5, fill=(43, 38, 34, 150))
        dr.rounded_rectangle([1050, 430, 1064, 452], 5, fill=(43, 38, 34, 150))
        # ---- floor lamp
        dr.rectangle([1104, 250, 1112, 452], fill=(43, 38, 34, 175))
        dr.polygon([(1072, 252), (1144, 252), (1132, 208), (1084, 208)], fill=s3 + (255,))
        dr.rounded_rectangle([1088, 452, 1128, 460], 4, fill=(43, 38, 34, 175))
        # ---- basket on the floor
        dr.polygon([(596, 452), (688, 452), (676, 512), (608, 512)], fill=s3 + (235,))
        dr.rounded_rectangle([590, 444, 694, 458], 7, fill=accent + (215,))
        for x in range(604, 686, 16):
            dr.line([(x, 456), (x - 4, 510)], fill=(43, 38, 34, 40), width=3)
        # ---- rug
        dr.ellipse([806, 470, 976, 550], fill=s2 + (52,))
        # ---- text column
        dr.text((62, 68), BRAND, font=serif_b, fill="#2B2622")
        dr.text((66, 178), kicker, font=sans, fill=accent)
        dr.text((66, 222), "Designer-looking rooms", font=serif_s, fill="#2B2622")
        dr.text((66, 274), "without the designer budget.", font=serif_s, fill="#2B2622")
        dr.text((68, 352), "homedecorpad.com", font=sans_s, fill="#6F645B")
        im.save(os.path.join(ROOT, "assets", out), quality=88, optimize=True)

    pal = {0: ("#F7F1E8", "#EEE6DA", "#DCC9B3", "#B5533C", "#6E7B5A", "#C08B48"),
           1: ("#F8F2EA", "#EDE5D6", "#D8CAB4", "#6E7B5A", "#B5533C", "#C08B48"),
           2: ("#F6F1EA", "#E9E2D6", "#D5CCBB", "#A9803F", "#6E7B5A", "#B5533C"),
           3: ("#F5F2EA", "#E6E5D9", "#D2D0BF", "#5F7150", "#8A9B74", "#B5533C"),
           4: ("#F9F0E7", "#EFDFCE", "#DBC1A9", "#B5533C", "#A9803F", "#6E7B5A"),
           5: ("#F2F0EC", "#E3E2DC", "#CFCDC4", "#4F6B7A", "#C08B48", "#B5533C")}
    draw_card("#F7F1E8", "#EEE6DA", "#DCC9B3", "#B5533C", "#6E7B5A", "#C08B48",
              "Home decor ideas & looks for less", "og-default.jpg")
    for c in CATS:
        bg, wall, floor, accent, s2, s3 = pal[c["tone"] % len(pal)]
        draw_card(bg, wall, floor, accent, s2, s3, c["name"], f'og-{c["slug"]}.jpg')
    print("  + assets/og-default.jpg + %d category share images" % len(CATS))


POSTS = load_posts()
POST_BY_SLUG = {p["slug"]: p for p in POSTS}
REL = {p["slug"]: p.get("related", []) for p in POSTS}


def check_links():
    """Fail the build if a generated page links to something that does not exist."""
    import glob
    files = sorted(glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True))
    anchors = {f: set(re.findall(r'id="([^"]+)"', open(f, encoding="utf-8").read())) for f in files}
    broken = []
    for f in files:
        for m in re.finditer(r'(?:href|src)="([^"]+)"', open(f, encoding="utf-8").read()):
            u = m.group(1)
            if not u or u.startswith(("http", "mailto:", "data:", "#", "tel:")):
                continue
            path, _, frag = u.partition("#")
            target = os.path.normpath(os.path.join(os.path.dirname(f), path)) if path else f
            if path and not os.path.exists(target):
                broken.append(f"{os.path.relpath(f, ROOT)} -> {u}")
            elif frag and frag not in anchors.get(target, set()):
                broken.append(f"{os.path.relpath(f, ROOT)} -> {u} (missing anchor)")
    if broken:
        print("\n  BROKEN LINKS FOUND — fix the content before publishing:")
        for x in broken:
            print("   ", x)
        raise SystemExit(1)
    print(f"  link check: {len(files)} pages, 0 broken links")


def main():
    pages = [page_home(), page_blog(), page_start_here(), page_about(), page_contact(), page_shop()]
    pages += [page_post(p) for p in POSTS]
    pages += legal_pages()
    for path, html in pages:
        write(path, html)
    write_extras()
    make_og_image()
    check_links()
    total = len(pages) + 6
    print(f"built {len(pages)} HTML pages (+404), {len(POSTS)} posts, {len(LEGAL_FILES)} legal pages")
    # quick sanity checks
    bad = []
    for path, _ in pages:
        full = os.path.join(ROOT, path)
        txt = open(full, encoding="utf-8").read()
        for token in ("[BRAND NAME]", "[DOMAIN]", "[CONTACT EMAIL]", "[EFFECTIVE DATE]", "None", "{{"):
            if token in txt:
                bad.append(f"{path}: {token}")
    print("placeholder check:", "clean" if not bad else bad[:8])
    return total


if __name__ == "__main__":
    main()
