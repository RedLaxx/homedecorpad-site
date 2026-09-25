# -*- coding: utf-8 -*-
"""HomeDecorPad — site builder.

Run:  python3 _build/build.py
Writes a complete static site into the repo root: HTML pages, sitemap,
robots.txt, ads.txt, .nojekyll, assets and README.
No third-party build tools required to deploy.
"""
import os, re, sys, json, glob, shutil, datetime, html as _html
import urllib.parse as urllib_parse

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import theme
from theme import (CSS, head, footer, consent, comments_section, art, art_raw, ICON, header, TONES, share_bar)
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

def load_yaml_file(fname):
    """Load a simple yaml file (home.yml, navigation.yml) with or without frontmatter."""
    path = os.path.join(CONTENT, fname)
    if not os.path.exists(path):
        return {}
    raw = open(path, encoding="utf-8").read()
    fm, _ = md_engine.parse_frontmatter(raw)
    if fm:
        return fm
    # plain yaml fallback
    try:
        import yaml as _yaml
        return _yaml.safe_load(raw) or {}
    except Exception:
        # very simple key: value parser for flat files
        data = {}
        for line in raw.splitlines():
            line=line.strip()
            if not line or line.startswith("#"):
                continue
            if ":" in line:
                k,v=line.split(":",1)
                data[k.strip()]=v.strip().strip("\"'")
        return data


SETTINGS = load_settings()
HOME_SETTINGS = load_yaml_file("home.yml")
NAV_SETTINGS = load_yaml_file("navigation.yml")
FOOTER_SETTINGS = load_yaml_file("footer.yml")
# Load editable pages
PAGES_SETTINGS = {}
for _pname in ["start-here", "about", "contact", "shop-my-home", "shop-now", "blog"]:
    _data = load_yaml_file(f"pages/{_pname}.yml")
    if _data:
        PAGES_SETTINGS[_pname] = _data
LEGAL_EFFECTIVE = fmt_date(SETTINGS.get("legal_effective_date"), LAUNCH_DATE)
LEGAL_UPDATED = fmt_date(SETTINGS.get("legal_updated_date"), LAUNCH_DATE)
theme.BRAND = BRAND = SETTINGS.get("brand") or "HomeDecorPad"
DOMAIN = (os.environ.get("SITE_DOMAIN") or SETTINGS.get("domain") or "https://homedecorpad.com").rstrip("/")
theme.DOMAIN = DOMAIN
theme.EMAIL = EMAIL = SETTINGS.get("email") or "hello@homedecorpad.com"
theme.HOME = HOME_SETTINGS
theme.NAV = NAV_SETTINGS
theme.FOOTER = FOOTER_SETTINGS
theme.PAGES = PAGES_SETTINGS
TAG = theme.AMAZON_TAG = SETTINGS.get("amazon_tag") or "YOUR-AMAZON-TAG-20"
theme.FORMSPREE_ID = SETTINGS.get("formspree_id") or "YOUR_FORM_ID"
theme.ADSENSE_CLIENT = str(SETTINGS.get("adsense_client") or "").strip()
theme.GA4_ID = str(SETTINGS.get("ga4_id") or "").strip()
theme.PINTEREST_VERIFY = str(SETTINGS.get("pinterest_verify") or "").strip()
_social = SETTINGS.get("social")
theme.SOCIAL = {k: str(v or "").strip() for k, v in _social.items()} if isinstance(_social, dict) else {}
# Giscus / Cusdis comments
theme.GISCUS_ENABLED = bool(SETTINGS.get("giscus_enabled"))
theme.GISCUS_REPO = str(SETTINGS.get("giscus_repo") or "RedLaxx/homedecorpad-site").strip()
theme.GISCUS_REPO_ID = str(SETTINGS.get("giscus_repo_id") or "R_kgDOUoGanw").strip()
theme.GISCUS_CATEGORY = str(SETTINGS.get("giscus_category") or "General").strip()
theme.GISCUS_CATEGORY_ID = str(SETTINGS.get("giscus_category_id") or "").strip()
theme.GISCUS_MAPPING = str(SETTINGS.get("giscus_mapping") or "pathname").strip()
theme.GISCUS_THEME = str(SETTINGS.get("giscus_theme") or "light").strip()
theme.COMMENT_SYSTEM = str(SETTINGS.get("comment_system") or "giscus").strip()
theme.CUSDIS_ENABLED = bool(SETTINGS.get("cusdis_enabled"))
theme.CUSDIS_APP_ID = str(SETTINGS.get("cusdis_app_id") or "").strip()
theme.CUSDIS_HOST = str(SETTINGS.get("cusdis_host") or "https://cusdis.com").strip().rstrip("/")
theme.CUSDIS_THEME = str(SETTINGS.get("cusdis_theme") or "light").strip()

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


def slugify(text):
    """'My Post: 5 Ideas!' -> 'my-post-5-ideas'.

    Pages CMS names new files from the title automatically; this is the safety
    net for anything hand-written or edited, so a URL never contains spaces,
    capitals or punctuation.
    """
    import unicodedata
    s = unicodedata.normalize("NFKD", str(text))
    s = s.encode("ascii", "ignore").decode("ascii")
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s).strip("-").lower()
    return re.sub(r"-{2,}", "-", s)[:80] or "post"


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
        # AUTO slug: frontmatter slug override, else filename (which Pages CMS auto-generates from title), else title itself
        raw_slug = (fm.get("slug") or "").strip() or fn[:-3] or fm.get("title") or "post"
        slug = slugify(raw_slug)
        cat = str(fm.get("category") or "living-room")
        if cat not in CAT:
            raise SystemExit(f"{fn}: unknown category '{cat}'. "
                             f"Valid values: {', '.join(sorted(CAT))}")
        if slug in SLUG_CAT:
            raise SystemExit(f"{fn}: slug '{slug}' is already used by another post. "
                             f"Give one of them a different filename or slug.")
        SLUG_CAT[slug] = cat
        staged.append((slug, cat, fm, body_md))

    out = []
    for slug, cat, fm, body_md in staged:
        html, faq = md_engine.render(body_md, lambda h, d=2: resolve_link(h, d))
        html = drop_missing_images(html, slug)
        # featured_image is new primary field, hero_image kept for backwards compat
        feat_img = str(fm.get("featured_image") or fm.get("hero_image") or "").strip()
        out.append({
            "slug": slug, "cat": cat,
            "title": str(fm.get("title") or slug),
            "h1": str(fm.get("h1") or fm.get("title") or slug),
            "date": str(fm.get("date") or BUILD_DATE)[:10],
            "dek": str(fm.get("dek") or ""),
            "intro": str(fm.get("intro") or ""),
            "tags": list(fm.get("tags") or []),
            "motif": str(fm.get("motif") or CAT[cat]["motif"]),
            "hero_image": feat_img,
            "featured_image": feat_img,
            "related": list(fm.get("related") or []),
            "body": html, "faq": faq,
        })
    out.sort(key=lambda p: p["date"], reverse=True)
    return out


def load_comments():
    """Read content/comments/*.yml and group approved comments by post_slug."""
    folder = os.path.join(CONTENT, "comments")
    if not os.path.exists(folder):
        return {}
    grouped = {}
    for fn in sorted(os.listdir(folder)):
        if fn.lower() == "readme.md" or fn.startswith("_"):
            continue
        if not (fn.endswith(".yml") or fn.endswith(".yaml") or fn.endswith(".md")):
            continue
        raw = open(os.path.join(folder, fn), encoding="utf-8").read()
        fm, _ = md_engine.parse_frontmatter(raw)
        # support both frontmatter and plain yaml (no PyYAML needed on GitHub)
        if not fm:
            txt = raw.strip()
            # if wrapped in --- frontmatter, extract inner
            if txt.startswith("---"):
                # remove first --- line
                parts = txt.split("---")
                if len(parts) >= 3:
                    txt = parts[1]
            # try yaml if available
            try:
                import yaml as _yaml
                fm = _yaml.safe_load(txt) or {}
            except Exception:
                # simple key: value parser
                fm = {}
                lines = txt.splitlines()
                i = 0
                while i < len(lines):
                    line = lines[i]
                    m = re.match(r"^\s*(post_slug|author|date|body|approved)\s*:\s*(.*)$", line)
                    if m:
                        k, v = m.group(1), m.group(2).strip()
                        if k == "body":
                            # body may be on same line or multiline
                            if v in ("|", ">", "|-", ">-"):
                                # collect indented lines
                                body_lines = []
                                i += 1
                                while i < len(lines) and (lines[i].startswith("  ") or lines[i].startswith("\t") or not lines[i].strip()):
                                    body_lines.append(lines[i].lstrip())
                                    i += 1
                                fm[k] = "\n".join(body_lines).strip()
                                continue
                            else:
                                # strip quotes
                                fm[k] = v.strip("\"'").strip()
                        elif k == "approved":
                            fm[k] = v.lower() in ("true", "yes", "1")
                        else:
                            fm[k] = v.strip("\"'").strip()
                    i += 1
        if not fm.get("post_slug") or not fm.get("body"):
            continue
        if fm.get("approved") is False:
            continue
        if "approved" in fm and not fm.get("approved"):
            continue
        # if approved key missing, require explicit true for safety (avoid drafts)
        if "approved" not in fm:
            continue
        slug = slugify(str(fm.get("post_slug")))
        entry = {
            "author": str(fm.get("author") or "Anonymous").strip()[:60],
            "date": str(fm.get("date") or BUILD_DATE)[:10],
            "body": str(fm.get("body") or "").strip()[:2000],
        }
        grouped.setdefault(slug, []).append(entry)
    # sort each post's comments by date ascending
    for k in grouped:
        grouped[k].sort(key=lambda c: c["date"])
    return grouped


def load_custom_pages():
    """Read content/custom-pages/*.md and *.yml with frontmatter — each becomes /slug.html"""
    folder = os.path.join(CONTENT, "custom-pages")
    if not os.path.exists(folder):
        return []
    out = []
    for fn in sorted(os.listdir(folder)):
        if fn.lower() == "readme.md" or fn.startswith("_"):
            continue
        if not (fn.endswith(".md") or fn.endswith(".yml") or fn.endswith(".yaml")):
            continue
        raw = open(os.path.join(folder, fn), encoding="utf-8").read()
        fm, body_md = md_engine.parse_frontmatter(raw)
        # if no frontmatter and plain yaml file (like press-kit.yml with --- delimiters and body after)
        # md_engine.parse_frontmatter already handles --- frontmatter
        # For plain .yml without --- but with body after ---? try fallback
        if not fm:
            # try yaml load for whole file
            try:
                import yaml as _yaml
                # split at first --- that separates frontmatter and body if present
                if raw.strip().startswith("---"):
                    # find second ---
                    parts = raw.split("---")
                    if len(parts) >= 3:
                        fm = _yaml.safe_load(parts[1]) or {}
                        body_md = "---".join(parts[2:]).strip()
                    else:
                        fm = _yaml.safe_load(raw) or {}
                else:
                    fm = _yaml.safe_load(raw) or {}
                    body_md = fm.pop("body", "") if isinstance(fm, dict) else ""
            except Exception:
                fm = {}
                body_md = ""
        if not fm or not fm.get("title"):
            print(f"  ! skipping custom-pages/{fn} — no title")
            continue
        if fm.get("draft") is True:
            continue
        raw_slug = (fm.get("slug") or "").strip() or fn.rsplit(".",1)[0] or fm.get("title") or "page"
        slug = slugify(raw_slug)
        # avoid collision with existing hardcoded pages
        if slug in ("index","blog","start-here","about","contact","shop-my-home","privacy-policy","cookie-policy","terms-of-use","disclaimer","affiliate-disclosure","404"):
            print(f"  ! skipping custom-pages/{fn} — slug '{slug}' collides with built-in page")
            continue
        # render body markdown
        html_body, _ = md_engine.render(body_md or fm.get("body") or "", lambda h, d=0: resolve_link(h, d))
        html_body = drop_missing_images(html_body, slug)
        out.append({
            "slug": slug,
            "title": str(fm.get("title") or slug),
            "h1": str(fm.get("h1") or fm.get("title") or slug),
            "eyebrow": str(fm.get("eyebrow") or ""),
            "lede": str(fm.get("lede") or ""),
            "description": str(fm.get("description") or fm.get("dek") or "")[:300],
            "hero_image": str(fm.get("hero_image") or "").strip(),
            "body": html_body,
        })
    out.sort(key=lambda p: p["slug"])
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
    # clean URL without .html — GitHub Pages serves /blog/cat/slug for /blog/cat/slug.html
    return f'{"../"*depth}blog/{cat}/{slug}'


def amz(q):
    return "https://www.amazon.com/s?k=" + q.replace(" ", "+") + "&tag=" + TAG


REWRITE_RE = re.compile(r'href="(?:\.\./)+([a-z0-9\-]+(?:\.html)?)(#[a-z0-9\-]+)?"')

def rewrite_links(block, depth):
    """Turn the ../..-style links inside article HTML into depth-correct links — clean without .html."""
    def rep(m):
        base, frag = m.group(1), m.group(2) or ""
        name = base[:-5] if base.endswith(".html") else base
        if name in POST_BY_SLUG:
            href = post_url(name, depth)
        else:
            # strip .html for clean URL
            clean_base = base[:-5] if base.endswith(".html") else base
            href = "../" * depth + clean_base
        return f'href="{href}{frag}"'
    block = REWRITE_RE.sub(rep, block)
    return block.replace("#room-guides", "#categories")


def drop_missing_images(html, slug):
    """Remove images whose file is missing from the repo, and say so.

    A deleted upload should never leave a broken image on a live page, and
    should never block publishing. Pages and links still fail loudly; images
    degrade quietly back to the illustration.
    """
    missing = []

    def repl(m):
        src = _html.unescape(m.group(1))
        rel = urllib_parse.unquote(src)
        while rel.startswith("../"):
            rel = rel[3:]
        rel = rel.lstrip("/")
        if rel.startswith(("http://", "https://", "data:")):
            return m.group(0)
        if os.path.exists(os.path.join(ROOT, rel)):
            return m.group(0)
        missing.append(rel)
        return ""

    out = re.sub(r'<img\s+src="([^"]+)"[^>]*>', repl, html)
    out = re.sub(r"<figure[^>]*>\s*(?:<figcaption>.*?</figcaption>)?\s*</figure>", "", out, flags=re.S)
    for rel in missing:
        print(f"  ! {slug}: image missing from the repo, removed from the page — {rel}")
    return out


def asset_url(path, depth=0):
    """Turn a content path like /assets/uploads/my photo.jpg into a correct URL.

    Uploaded filenames often contain spaces; browsers tolerate them but the
    encoded form is what belongs in the HTML (and what the link checker expects).
    """
    rel = str(path or "").lstrip("/")
    if not rel:
        return ""
    prefix = "../" * depth
    if rel.startswith(("http://", "https://")):
        prefix = ""
    return prefix + _encode_asset(rel)


def _encode_asset(u):
    for ch, enc in ((" ", "%20"), ("(", "%28"), (")", "%29")):
        u = u.replace(ch, enc)
    return u


def hero_available(p):
    img = p.get("featured_image") or p.get("hero_image") or ""
    if not img:
        return False
    rel = urllib_parse.unquote(str(img)).lstrip("/")
    return os.path.exists(os.path.join(ROOT, rel))


def cover_html(p, depth=0, cls_art="c4x3"):
    """Card artwork: an uploaded featured photo when the editor set one, else the illustration."""
    if hero_available(p):
        img = p.get("featured_image") or p.get("hero_image") or ""
        return (f'<div class="cover {cls_art}"><img src="{asset_url(img, depth)}" alt="" '
                f'style="width:100%;height:100%;object-fit:cover" loading="lazy"></div>')
    return art(p["motif"], CAT[p["cat"]]["tone"], cls_art)


def card(p, depth=0, cls_art="c4x3", searchable=True):
    c = CAT[p["cat"]]
    data = f' data-cat="{p["cat"]}" data-text="{_html.escape((p["title"]+" "+p["dek"]+" "+" ".join(p["tags"])).lower(), quote=True)}"' if searchable else ""
    cover = cover_html(p, depth, cls_art)
    return f"""<article class="card"{data}>
 {cover}
 <div class="body">
  <span class="chip">{c["name"]}</span>
  <h3><a href="{post_url(p['slug'], depth)}">{p['title']}</a></h3>
  <p>{short(p['dek'])}</p>
  <div class="btnrow cardbtn"><a class="btn sm ghost" href="{post_url(p['slug'], depth)}">View post</a></div>
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
 <div>{form}<p class="muted" style="color:#A79C8F;margin:12px 0 0;font-size:13px">By subscribing you agree to our <a href="{('../'*depth)}privacy-policy" style="color:#C9BFB2;text-decoration:underline">Privacy Policy</a>.</p></div>
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
def _resolve_home_url(u, depth=0):
    """Resolve home.yml URL that may be /path, post:slug, or full http — cleans /index.html and .html to clean URLs"""
    if not u:
        return ""
    u = str(u).strip()
    if u.startswith("post:"):
        try:
            return post_url(u[5:].strip(), depth)
        except Exception:
            return f"blog#{u[5:].strip()}"
    if u.startswith(("http://","https://","#","mailto:")):
        return u
    # clean /index.html -> /
    if u in ("/index.html", "index.html", "/"):
        return "./" if depth==0 else "../"*depth
    # strip leading / and remove index.html and .html extension
    u = u.lstrip("/")
    u = u.replace("/index.html", "/").replace("index.html", "")
    # strip .html but keep fragment
    if "#" in u:
        base, frag = u.split("#",1)
        if base.endswith(".html"):
            base = base[:-5]
        u = f"{base}#{frag}"
    else:
        if u.endswith(".html"):
            u = u[:-5]
    if u in ("", "/"):
        return "./" if depth==0 else "../"*depth
    return u

def page_home():
    h = HOME_SETTINGS or {}
    feat = POSTS[0] if POSTS else None
    # counts
    latest_count = int(h.get("latest_count") or 6)
    rest = POSTS[1:1+latest_count] if POSTS else []

    # hero — static or slider
    slider_enabled = bool(h.get("slider_enabled"))
    slider_posts_slugs = h.get("slider_posts") or []
    slider_title = h.get("slider_title") or "Top 5 this month"
    slider_autoplay = int(h.get("slider_autoplay") or 5)
    slider_show_dots = bool(h.get("slider_show_dots", True))
    slider_show_arrows = bool(h.get("slider_show_arrows", True))

    # Build slider slides from top 5 slugs
    slider_slides = []
    for slug in slider_posts_slugs[:5]:
        slug = slugify(str(slug))
        if slug in POST_BY_SLUG:
            slider_slides.append(POST_BY_SLUG[slug])
    # fallback to most recent 5 if not enough
    if len(slider_slides) < 5:
        for p in POSTS:
            if p not in slider_slides:
                slider_slides.append(p)
            if len(slider_slides) >=5:
                break

    hero_eyebrow = h.get("hero_eyebrow") or "Home decor ideas · looks for less"
    hero_title = h.get("hero_title") or "Designer-looking rooms without the designer budget."
    hero_lede = h.get("hero_lede") or "Practical room ideas, shoppable budget swaps and paint palettes you can recreate this weekend — for real homes with real budgets."
    hero_image = (h.get("hero_image") or "").strip()
    hero_motif = (h.get("hero_motif") or "hero").strip()
    if hero_image:
        rel = hero_image.lstrip("/")
        if os.path.exists(os.path.join(ROOT, rel)):
            hero_art = f'<div class="art"><img src="{asset_url(hero_image,0)}" alt="" style="width:100%;height:100%;object-fit:cover" loading="eager"></div>'
        else:
            hero_art = f'<div class="art">{art_raw(hero_motif, 4)}</div>'
    else:
        hero_art = f'<div class="art">{art_raw(hero_motif, 4)}</div>'

    btns_cfg = h.get("hero_buttons") or [
        {"label":"Start here","url":"/start-here","style":"primary"},
        {"label":"Browse all decor ideas","url":"/blog","style":"ghost"},
    ]
    btn_html = ""
    for b in btns_cfg:
        if not isinstance(b, dict):
            continue
        label = (b.get("label") or "").strip()
        url = _resolve_home_url(b.get("url") or "")
        style = (b.get("style") or "primary").lower()
        if not label or not url:
            continue
        cls = "btn" if style=="primary" else "btn ghost" if style=="ghost" else "btn"
        if style=="outline":
            cls="btn ghost"
        btn_html += f'<a class="{cls}" href="{url}">{label}</a>'

    badges = h.get("trust_badges") or ["Budget-first picks","Renter friendly","New ideas weekly"]
    trust_html = "".join(f'<span>{ICON["check"]}{b}</span>' for b in badges if b)

    # Build hero HTML — slider or static
    if slider_enabled and slider_slides:
        # Build slides HTML
        slides_html = ""
        dots_html = ""
        for idx, p in enumerate(slider_slides):
            active = " active" if idx==0 else ""
            # cover
            cover = cover_html(p, 0, "c3x2")
            cat = CAT[p["cat"]]
            # title and link
            post_link = post_url(p["slug"])
            slides_html += f"""
  <div class="slide{active}" data-index="{idx}">
   <div class="slide-img">{cover}</div>
   <div class="slide-body">
    <p class="eyebrow">{slider_title} · {idx+1}/5</p>
    <span class="chip">{cat['name']}</span>
    <h2><a href="{post_link}">{p['title']}</a></h2>
    <p class="muted" style="margin:8px 0 0">{short(p['dek'], 120)}</p>
    <div class="meta" style="margin-top:12px"><span>{d(p['date'])}</span><i></i><span>{read_label(p)}</span></div>
    <div class="btnrow"><a class="btn sm" href="{post_link}">View post</a><a class="btn sm ghost" href="{post_link}">Read now →</a></div>
   </div>
  </div>"""
            dots_html += f'<button class="dot{" active" if idx==0 else ""}" data-slide="{idx}" aria-label="Go to slide {idx+1}"></button>'

        arrows_html = ""
        if slider_show_arrows:
            arrows_html = '<button class="arrow prev" aria-label="Previous">‹</button><button class="arrow next" aria-label="Next">›</button>'

        hero_html = f"""
<section class="container hero-slider-wrap">
 <div class="hero-slider" data-autoplay="{slider_autoplay}">
  <div class="slides">
   {slides_html}
  </div>
  {arrows_html}
  {'<div class="dots">'+dots_html+'</div>' if slider_show_dots else ''}
 </div>
 <div class="hero-static-below">
  <div>
   <p class="eyebrow">{hero_eyebrow}</p>
   <h1>{hero_title}</h1>
   <p class="lede">{hero_lede}</p>
   <div class="btnrow">{btn_html}</div>
   <div class="trust">{trust_html}</div>
  </div>
  {hero_art}
 </div>
</section>
<script>
(function(){{
  var slider = document.querySelector('.hero-slider');
  if(!slider) return;
  var slides = slider.querySelectorAll('.slide');
  var dots = slider.querySelectorAll('.dot');
  var prev = slider.querySelector('.arrow.prev');
  var next = slider.querySelector('.arrow.next');
  var current = 0;
  var autoplay = parseInt(slider.getAttribute('data-autoplay')||'5')*1000;
  var timer = null;

  function go(n){{
    current = (n+slides.length)%slides.length;
    slides.forEach(function(s,i){{s.classList.toggle('active', i===current);}});
    dots.forEach(function(d,i){{d.classList.toggle('active', i===current);}});
  }}
  function nextSlide(){{go(current+1);}}
  function prevSlide(){{go(current-1);}}
  function start(){{if(autoplay>0){{timer=setInterval(nextSlide, autoplay);}}}}
  function stop(){{if(timer){{clearInterval(timer);timer=null;}}}}

  if(next) next.addEventListener('click', function(){{stop();nextSlide();start();}});
  if(prev) prev.addEventListener('click', function(){{stop();prevSlide();start();}});
  dots.forEach(function(d){{
    d.addEventListener('click', function(){{
      stop();
      go(parseInt(d.getAttribute('data-slide')));
      start();
    }});
  }});
  slider.addEventListener('mouseenter', stop);
  slider.addEventListener('mouseleave', start);
  // touch swipe
  var startX=0;
  slider.addEventListener('touchstart', function(e){{startX=e.touches[0].clientX;stop();}}, {{passive:true}});
  slider.addEventListener('touchend', function(e){{
    var endX=e.changedTouches[0].clientX;
    if(endX-startX>50) prevSlide();
    else if(startX-endX>50) nextSlide();
    start();
  }}, {{passive:true}});
  start();
}})();
</script>
"""
    else:
        hero_html = f"""
<section class="container hero">
 <div>
  <p class="eyebrow">{hero_eyebrow}</p>
  <h1>{hero_title}</h1>
  <p class="lede">{hero_lede}</p>
  <div class="btnrow">
   {btn_html}
  </div>
  <div class="trust">
   {trust_html}
  </div>
 </div>
 {hero_art}
</section>
"""

    # browse by room
    browse_title = h.get("browse_title") or "Browse by room"
    browse_link_text = h.get("browse_link_text") or "All 10 room guides →"
    browse_link_url = _resolve_home_url(h.get("browse_link_url") or "/blog")
    chips = "".join(f'<a href="blog#{c["slug"]}">{c["name"]}</a>' for c in CATS[:8])

    # featured
    featured_eyebrow = h.get("featured_eyebrow") or "Featured"
    featured_title = h.get("featured_title") or "This week's idea"
    if feat:
        feat_html = f"""
 <article class="feature">
  {cover_html(feat, 0, 'c3x2')}
  <div class="body">
   <span class="chip">{CAT[feat['cat']]['name']}</span>
   <h2><a href="{post_url(feat['slug'])}">{feat['title']}</a></h2>
   <p>{feat['dek']}</p>
   <div class="meta"><span>{d(feat['date'])}</span><i></i><span>{read_label(feat)}</span></div>
   <div class="btnrow"><a class="btn sm" href="{post_url(feat['slug'])}">View post</a></div>
  </div>
 </article>"""
    else:
        feat_html = "<p>No posts yet.</p>"

    # latest
    latest_eyebrow = h.get("latest_eyebrow") or "Latest"
    latest_title = h.get("latest_title") or "Fresh decor ideas"
    latest_link_text = h.get("latest_link_text") or "See everything →"
    latest_link_url = _resolve_home_url(h.get("latest_link_url") or "/blog")

    # signature
    sig_eyebrow = h.get("signature_eyebrow") or "Signature series"
    sig_title = h.get("signature_title") or "One room, three budgets"
    sig_desc = h.get("signature_description") or "Every room, styled three ways — a $150 refresh, a $500 upgrade and a full makeover. You get the exact shopping list and the order to buy things in, so you never waste money on the wrong piece first."
    sig_image = (h.get("signature_image") or "").strip()
    sig_motif = (h.get("signature_motif") or "arch").strip()
    if sig_image and os.path.exists(os.path.join(ROOT, sig_image.lstrip("/"))):
        sig_cover = f'<div class="cover"><img src="{asset_url(sig_image,0)}" alt="" style="width:100%;height:100%;object-fit:cover"></div>'
    else:
        sig_cover = f'<div class="cover">{art_raw(sig_motif, 5)}</div>'
    sig_links_cfg = h.get("signature_links") or [
        {"label":"Cozy bedroom: $150 / $500 / $1,500","url":"post:one-room-three-budgets-cozy-bedroom"},
        {"label":"Warm minimalist living room under $250","url":"post:warm-minimalist-living-room-under-250"},
        {"label":"All Get the Look for Less guides","url":"/blog#get-the-look"},
    ]
    sig_links_html = ""
    for l in sig_links_cfg:
        if not isinstance(l, dict):
            continue
        label = (l.get("label") or "").strip()
        url = _resolve_home_url(l.get("url") or "")
        if label and url:
            sig_links_html += f'<li><a href="{url}">{label}</a></li>'

    # start here
    sh_eyebrow = h.get("start_here_eyebrow") or "Start here"
    sh_title = h.get("start_here_title") or "New to the site? Read these first"
    sh_link_text = h.get("start_here_link_text") or "How it works →"
    sh_link_url = _resolve_home_url(h.get("start_here_link_url") or "/start-here")
    sh_cards_cfg = h.get("start_here_cards") or [
        {"title":"Fix the room before you shop it","description":"Twelve layout mistakes that make a room feel small — every fix is free.","link_text":"Read the layout guide →","link_url":"post:living-room-layout-mistakes"},
        {"title":"Choose the palette","description":"Eight neutral-anchored colour palettes with proportions that actually work at home.","link_text":"See the palettes →","link_url":"post:home-decor-color-palettes-2027"},
    ]
    sh_cards_html = ""
    for c in sh_cards_cfg:
        if not isinstance(c, dict):
            continue
        title = (c.get("title") or "").strip()
        desc = (c.get("description") or "").strip()
        lt = (c.get("link_text") or "").strip()
        lu = _resolve_home_url(c.get("link_url") or "")
        if not title:
            continue
        sh_cards_html += f'<div class="prosebox"><h3 style="margin-top:0">{title}</h3><p class="muted">{desc}</p><p><a href="{lu}">{lt}</a></p></div>'

    body = f"""{hero_html}

<section class="section tight"><div class="container">
 <div class="sec-head"><h2 style="font-size:22px">{browse_title}</h2><a href="{browse_link_url}">{browse_link_text}</a></div>
 <div class="cats">{chips}</div>
</div></section>

<section class="section" id="categories"><div class="container">
 <div class="sec-head"><div><p class="eyebrow">{featured_eyebrow}</p><h2>{featured_title}</h2></div></div>
 {feat_html}
</div></section>

<section class="section"><div class="container">
 <div class="sec-head"><div><p class="eyebrow">{latest_eyebrow}</p><h2>{latest_title}</h2></div><a href="{latest_link_url}">{latest_link_text}</a></div>
 <div class="grid">{''.join(card(p) for p in rest)}</div>
</div></section>

<section class="section"><div class="container">
 <div class="panel split">
  {sig_cover}
  <div class="pad">
   <p class="eyebrow">{sig_eyebrow}</p>
   <h2>{sig_title}</h2>
   <p class="muted">{sig_desc}</p>
   <ul>
    {sig_links_html}
   </ul>
  </div>
 </div>
</div></section>

<section class="section"><div class="container">
 <div class="sec-head"><div><p class="eyebrow">{sh_eyebrow}</p><h2>{sh_title}</h2></div><a href="{sh_link_url}">{sh_link_text}</a></div>
 <div class="grid two">
  {sh_cards_html}
 </div>
</div></section>

{newsletter()}
"""
    desc = "Home decor ideas, budget room makeovers, paint palettes and shoppable looks for less. Practical decorating for real homes — new guides every week."
    schema = json.dumps({"@context": "https://schema.org", "@type": "WebSite", "name": BRAND,
                         "url": DOMAIN + "/", "description": desc,
                         "publisher": {"@type": "Organization", "name": BRAND}})
    return page("index.html", f"{BRAND} — Home Decor Ideas, Room Makeovers & Looks for Less",
                desc, body, 0, canonical="", schema=schema)


def page_blog():
    cfg = PAGES_SETTINGS.get("blog") or {}
    eyebrow = cfg.get("eyebrow") or "All decor ideas"
    h1 = cfg.get("h1") or "Room guides, budget makeovers & home finds"
    lede = cfg.get("lede") or "Every guide is written to be used, not just saved: what to do first, what it costs, and what to skip. Newest posts first."
    search_placeholder = cfg.get("search_placeholder") or "Search: small apartment, rug, paint..."
    empty_text = cfg.get("empty_text") or "No guides match that search yet — try a room name like bedroom or a topic like rug."
    title = cfg.get("title") or f"All Decor Ideas — Room Guides & Budget Makeovers | {BRAND}"
    display_mode = (cfg.get("display_mode") or "grid").lower()
    show_filters = cfg.get("show_filters", True)
    posts_per_page = int(cfg.get("posts_per_page") or 0)

    all_posts = POSTS[:]
    total = len(all_posts)
    if posts_per_page and posts_per_page > 0:
        visible_posts = all_posts[:posts_per_page]
    else:
        visible_posts = all_posts

    chips_html = ""
    if show_filters:
        chips = "".join(f'<button type="button" data-f="{c["slug"]}">{c["name"]}</button>' for c in CATS)
        chips_html = f'<div class="cats" id="filters"><button type="button" class="on" data-f="all">All guides</button>{chips}</div>'

    if display_mode == "list":
        posts_html = '<div class="post-list" style="display:flex;flex-direction:column;gap:16px">'
        for p in visible_posts:
            posts_html += f'<article class="card list" data-cat="{p["cat"]}" data-text="{(p["title"]+" "+p["dek"]+" "+" ".join(p["tags"])).lower()}"><div class="body"><span class="chip">{CAT[p["cat"]]["name"]}</span><h3><a href="{post_url(p["slug"])}">{p["title"]}</a></h3><p class="muted" style="font-size:14px;margin:6px 0">{p["dek"][:160]}</p><div class="meta"><span>{d(p["date"])}</span><i></i><span>{read_label(p)}</span></div><a class="btn sm" href="{post_url(p["slug"])}">View post</a></div></article>'
        posts_html += '</div>'
    else:
        if visible_posts:
            first = visible_posts[0]
            first_html = f'<article class="feature catwide" data-cat="{first["cat"]}" data-text="{(first["title"]+" "+first["dek"]).lower()}">{cover_html(first, 0, "c3x2")}<div class="body"><span class="chip">{CAT[first["cat"]]["name"]}</span><h3><a href="{post_url(first["slug"])}">{first["title"]}</a></h3><p>{first["dek"]}</p><div class="meta"><span>{d(first["date"])}</span><i></i><span>{read_label(first)}</span></div><div class="btnrow"><a class="btn sm" href="{post_url(first["slug"])}">View post</a></div></div></article>'
            rest = visible_posts[1:]
            rest_html = "".join(card(p) for p in rest)
            posts_html = f'{first_html}<div class="grid" style="margin-top:22px">{rest_html}</div>'
        else:
            posts_html = '<p class="muted">No posts yet — daily auto-posts will appear here starting at 3 AM UTC.</p>'

    body = f"""
<section class="section tight"><div class="container" id="categories">
 <p class="eyebrow">{eyebrow}</p>
 <h1>{h1}</h1>
 <p class="lede" style="max-width:62ch">{lede}</p>
 <p class="muted" style="font-size:13.5px;margin-top:8px">{total} posts — newest first</p>
 <div class="field" style="margin:24px 0 18px;max-width:520px">
  <input type="search" id="q" placeholder="{search_placeholder}" aria-label="Search guides">
 </div>
 {chips_html}
 <p class="muted" id="empty" style="display:none">{empty_text}</p>
</div></section>

<section class="section"><div class="container">
 <div id="blog-posts">
  {posts_html}
 </div>
</div></section>

{newsletter(0, dark=False)}

<script>
(function(){{
 var q=document.getElementById('q'), btns=document.querySelectorAll('#filters button'), container=document.getElementById('blog-posts'), empty=document.getElementById('empty'), active='all';
 function run(){{
  var term=(q.value||'').toLowerCase().trim(), shown=0;
  var cards=container.querySelectorAll('.card, .feature');
  cards.forEach(function(cd){{
    var dataCat=cd.getAttribute('data-cat')||'';
    var txt=(cd.getAttribute('data-text')||cd.textContent||'').toLowerCase();
    var catOk = (active==='all'||dataCat===active);
    if(!dataCat && active!=='all'){{
      var chip=cd.querySelector('.chip');
      var chipTxt=chip?chip.textContent.toLowerCase():'';
      catOk = chipTxt.indexOf(active.replace('-',' '))>-1 || chipTxt.indexOf(active)>-1;
      if(active==='all') catOk=true;
    }}
    var termOk = !term||txt.indexOf(term)>-1;
    var ok = catOk && termOk;
    cd.style.display=ok?'':'none';
    if(ok) shown++;
  }});
  if(empty) empty.style.display=shown?'none':'block';
 }}
 if(q) q.addEventListener('input',run);
 if(btns) btns.forEach(function(b){{b.addEventListener('click',function(){{
  active=b.getAttribute('data-f');
  btns.forEach(function(x){{x.classList.toggle('on',x===b);}});
  run();
 }});}});
}})();
</script>
"""
    desc = cfg.get("description") or f"Browse all {total} HomeDecorPad guides newest first: living room, bedroom, small apartments, color palettes, kitchen and more."
    schema = json.dumps({"@context": "https://schema.org", "@type": "CollectionPage", "name": "All decor ideas",
                         "url": DOMAIN + "/blog", "publisher": {"@type": "Organization", "name": BRAND}})
    return page("blog.html", title, desc, body, 0, canonical="blog", schema=schema)


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
    feat_img = p.get("featured_image") or p.get("hero_image") or ""
    hero = (f'<img src="{asset_url(feat_img, depth)}" '
            f'alt="{_html.escape(p["title"], quote=True)}" style="width:100%;height:100%;object-fit:cover">') \
        if hero_available(p) else art_raw(p["motif"], c["tone"])
    pin_title = p["title"][:100]
    pin_desc = (p["dek"] + " " + " ".join("#" + t.replace(" ", "") for t in p["tags"][:3]))[:480]

    # --- Related ideas: auto-generate if manual related is empty or incomplete ---
    manual_rel = REL.get(p["slug"], []) or []
    manual_valid = [s for s in manual_rel if s in POST_BY_SLUG and s != p["slug"]]

    def auto_related():
        # Exclude current and already manually chosen
        excluded = set(manual_valid) | {p["slug"]}
        # Candidates from same category first, then others
        same_cat = [cand for cand in POSTS if cand["cat"] == p["cat"] and cand["slug"] not in excluded]
        other_cat = [cand for cand in POSTS if cand["cat"] != p["cat"] and cand["slug"] not in excluded]

        p_tags = set(t.lower().strip() for t in (p.get("tags") or []) if t)
        # Score by tag overlap, then date (newest first)
        def score_list(lst):
            scored = []
            for cand in lst:
                cand_tags = set(t.lower().strip() for t in (cand.get("tags") or []) if t)
                overlap = len(p_tags & cand_tags) if p_tags else 0
                # date is YYYY-MM-DD, lexicographically sortable newest first
                scored.append((overlap, cand["date"], cand))
            # sort by overlap desc, date desc
            scored.sort(key=lambda x: (x[0], x[1]), reverse=True)
            return [c[2] for c in scored]

        ordered = score_list(same_cat) + score_list(other_cat)
        return ordered

    # Build final related list: manual first, then auto to fill up to 3
    related_posts = []
    for slug in manual_valid:
        if slug in POST_BY_SLUG:
            related_posts.append(POST_BY_SLUG[slug])
    if len(related_posts) < 3:
        for cand in auto_related():
            if cand not in related_posts and cand["slug"] != p["slug"]:
                related_posts.append(cand)
            if len(related_posts) >= 3:
                break

    rel_cards = "".join(card(rp, depth) for rp in related_posts[:3])

    home_href = '../'*depth if depth else './'
    body = f"""
<article>
 <div class="container narrow post-head">
  <p class="crumb"><a href="{home_href}">Home</a> / <a href="{'../'*depth}blog#{c['slug']}">{c['name']}</a></p>
  <span class="chip">{c['name']}</span>
  <h1>{p['h1']}</h1>
  <p class="lede">{p['intro']}</p>
  <div class="meta"><span>By the {BRAND} team</span><i></i><span>{d(p['date'])}</span><i></i><span>{read_label(p)}</span></div>
  {share_bar(p, depth, "top")}
 </div>
 <div class="container narrow">
  <div class="post-hero">{hero}<div class="tag"><span>{c['name']} &middot; {BRAND}</span></div></div>
 </div>
 <div class="container narrow article">
  {body_html}
  {share_bar(p, depth, "bottom")}
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
  <div class="share">Found this useful? <a href="{'../'*depth}blog#{c['slug']}">More {c['name'].lower()} guides →</a> &nbsp;&middot;&nbsp; <a href="{'../'*depth}affiliate-disclosure">How we make money</a></div>
 </div>
</article>

<section class="section"><div class="container">
 <div class="sec-head"><div><p class="eyebrow">Keep reading</p><h2>Related ideas</h2></div><a href="{'../'*depth}blog">All guides →</a></div>
 <div class="grid">{rel_cards}</div>
</div></section>

{comments_section('../'*depth, post=p, comments=COMMENTS.get(p['slug'], []))}

{newsletter(depth)}
"""
    schemas = [{"@context": "https://schema.org", "@type": "Article", "headline": p["h1"],
                "description": p["dek"], "datePublished": p["date"], "dateModified": p["date"],
                "articleSection": c["name"], "keywords": ", ".join(p["tags"]),
                "author": {"@type": "Organization", "name": BRAND},
                "publisher": {"@type": "Organization", "name": BRAND,
                              "logo": {"@type": "ImageObject", "url": DOMAIN + "/assets/og-default.jpg"}},
                "image": f"{DOMAIN}/assets/og-{p['cat']}.jpg",
                "mainEntityOfPage": {"@type": "WebPage", "@id": f"{DOMAIN}/blog/{p['cat']}/{p['slug']}"}}]
    fs = faq_schema(p["faq"])
    if fs:
        schemas.append(json.loads(fs))
    schema = json.dumps(schemas[0]) if len(schemas) == 1 else json.dumps({"@context": "https://schema.org", "@graph": schemas})
    return page(f"blog/{p['cat']}/{p['slug']}.html",
                f"{p['title']} | {BRAND}", p["dek"], body, depth,
                canonical=f"blog/{p['cat']}/{p['slug']}", schema=schema, og=f"assets/og-{p['cat']}.jpg")


def page_start_here():
    cfg = PAGES_SETTINGS.get("start-here") or {}
    # Editable fields with fallbacks
    title = cfg.get("title") or f"Start Here — How to Decorate on a Budget | {BRAND}"
    h1 = cfg.get("h1") or "Make your home look designed — without a designer budget"
    eyebrow = cfg.get("eyebrow") or "Start here"
    lede = cfg.get("lede") or f"{BRAND} is a small library of decor ideas that are actually finishable. Every guide answers three questions: what do I do first, what does it cost, and what can I skip?"
    # buttons
    btns_cfg = cfg.get("buttons") or [{"label":"Browse all guides","url":"/blog","style":"primary"},{"label":"Shop the looks","url":"/shop-my-home","style":"ghost"}]
    btn_html = ""
    for b in btns_cfg:
        if not isinstance(b, dict):
            continue
        label = b.get("label","")
        url = _resolve_home_url(b.get("url",""))
        style = (b.get("style") or "primary").lower()
        cls = "btn" if style=="primary" else "btn ghost"
        if label and url:
            btn_html += f'<a class="{cls}" href="{url}">{label}</a>'

    # how it works
    how_title = cfg.get("how_it_works_title") or "How this site works"
    how_body = cfg.get("how_it_works_body") or ""
    how_html = md_to_html(how_body) if how_body else "<p>Most decor content is aimed at people with a renovation budget...</p>"

    # method
    method_title = cfg.get("method_title") or "The four-step method we use in every room"
    method_steps = cfg.get("method_steps") or []
    method_html = ""
    if method_steps:
        for s in method_steps:
            t = s.get("title","") if isinstance(s, dict) else ""
            b = s.get("body","") if isinstance(s, dict) else ""
            if t or b:
                method_html += f'<li><b>{t}</b> {b}</li>'
        method_html = f"<ol class='steps'>{method_html}</ol>"
    else:
        method_html = """<ol class="steps"><li><b>Edit.</b> Clear every surface...</li></ol>"""

    callout_title = cfg.get("callout_title") or "The rule behind all of it"
    callout_body = cfg.get("callout_body") or "Spend on the things your eye lands on — the rug, the lighting, the bedding — and save on the things it does not."
    known_for_title = cfg.get("known_for_title") or "What we are known for"
    known_for_items = cfg.get("known_for_items") or []
    known_html = ""
    if known_for_items:
        for it in known_for_items:
            txt = it.get("text","") if isinstance(it, dict) else ""
            ll = it.get("link_label","") if isinstance(it, dict) else ""
            lu = _resolve_home_url(it.get("link_url","")) if isinstance(it, dict) else ""
            if txt:
                if ll and lu:
                    known_html += f'<li>{txt} <a href="{lu}">{ll}</a>.</li>'
                else:
                    known_html += f'<li>{txt}</li>'
        known_html = f"<ul>{known_html}</ul>"
    else:
        known_html = "<ul><li>...</li></ul>"

    # picks
    picks_cfg = cfg.get("picks") or [
        {"slug":"living-room-layout-mistakes","title":"Fix the room before you shop it","kicker":"Living room","description":"Twelve free layout fixes..."},
        {"slug":"home-decor-color-palettes-2027","title":"Pick your palette","kicker":"Color & paint","description":"Eight palettes..."},
    ]
    picks_eyebrow = cfg.get("picks_eyebrow") or "Start somewhere"
    picks_title = cfg.get("picks_title") or "Pick your first project"
    picks_link_text = cfg.get("picks_link_text") or ""
    picks_link_url = _resolve_home_url(cfg.get("picks_link_url") or "")
    cards = ""
    for item in picks_cfg:
        if not isinstance(item, dict):
            continue
        slug = item.get("slug","")
        pick_title = item.get("title","")
        kicker = item.get("kicker","")
        sub = item.get("description","")
        if not slug or slug not in POST_BY_SLUG:
            continue
        p_ = POST_BY_SLUG[slug]
        cards += (f'<article class="card">{cover_html(p_, 0, "c3x2")}'
                  f'<div class="body"><span class="chip">{kicker or CAT[p_["cat"]]["name"]}</span>'
                  f'<h3><a href="{post_url(slug)}">{pick_title or p_["title"]}</a></h3><p>{sub or p_["dek"]}</p>'
                  f'<div class="btnrow cardbtn"><a class="btn sm ghost" href="{post_url(slug)}">View post</a></div>'
                  f'<div class="meta"><span>{read_label(p_)}</span></div></div></article>')

    coming_title = cfg.get("coming_next_title") or "What is coming next"
    coming_body = cfg.get("coming_next_body") or "Kitchen and dining styling..."
    coming_html = md_to_html(coming_body)

    body = f"""
<section class="section tight"><div class="container narrow">
 <p class="eyebrow">{eyebrow}</p>
 <h1>{h1}</h1>
 <p class="lede">{lede}</p>
 <div class="btnrow">{btn_html}</div>
</div></section>

<section class="section"><div class="container narrow">
 <h2>{how_title}</h2>
 {how_html}

 <h2>{method_title}</h2>
 {method_html}

 <div class="callout"><h4>{callout_title}</h4><p>{callout_body}</p></div>

 <h2>{known_for_title}</h2>
 {known_html}
</div></section>

<section class="section"><div class="container">
 <div class="sec-head"><div><p class="eyebrow">{picks_eyebrow}</p><h2>{picks_title}</h2></div>{f'<a href="{picks_link_url}">{picks_link_text}</a>' if picks_link_text else ''}</div>
 <div class="grid">{cards}</div>
</div></section>

<section class="section"><div class="container narrow prosebox">
 <h2 style="margin-top:0">{coming_title}</h2>
 {coming_html}
</div></section>

{newsletter()}
"""
    desc = cfg.get("description") or "New here? These are the guides to read first: free layout fixes, colour palettes, small-space ideas and budget looks for less. Start decorating in an afternoon."
    return page("start-here.html", title, desc, body, 0, canonical="start-here",
                schema=json.dumps({"@context": "https://schema.org", "@type": "AboutPage", "name": "Start Here",
                                   "url": DOMAIN + "/start-here",
                                   "publisher": {"@type": "Organization", "name": BRAND}}))


def page_about():
    cfg = PAGES_SETTINGS.get("about") or {}
    title = cfg.get("title") or f"About {BRAND} — Budget-First Home Decor"
    h1 = cfg.get("h1") or f"About {BRAND}"
    eyebrow = cfg.get("eyebrow") or "About"
    lede = cfg.get("lede") or f"{BRAND} is a home decor site for people who want a room that looks considered — on a normal budget, in a normal apartment, without a renovation."
    sections = cfg.get("sections") or []
    if sections:
        sec_html = ""
        for sec in sections:
            if not isinstance(sec, dict):
                continue
            heading = sec.get("heading") or ""
            body_md = sec.get("body") or ""
            is_callout = sec.get("callout")
            body_html = md_to_html(body_md) if body_md else ""
            if is_callout:
                sec_html += f'<div class="callout"><h4>{heading}</h4>{body_html}</div>'
            else:
                if heading:
                    sec_html += f'<h2>{heading}</h2>'
                sec_html += body_html
    else:
        sec_html = f"""
 <h2>Why this site exists</h2><p>Interior design content usually shows you the after photo and hides the invoice...</p>
"""
    body = f"""
<section class="section tight"><div class="container narrow">
 <p class="eyebrow">{eyebrow}</p>
 <h1>{h1}</h1>
 <p class="lede">{lede}</p>
</div></section>

<section class="section"><div class="container narrow article">
 {sec_html}
</div></section>

{newsletter()}
"""
    desc = cfg.get("description") or f"About {BRAND}: a budget-first home decor site for renters and small-space dwellers. Our editorial standards, how we make money, and how to work with us."
    return page("about.html", title, desc, body, 0, canonical="about",
                schema=json.dumps({"@context": "https://schema.org", "@type": "AboutPage", "name": f"About {BRAND}",
                                   "url": DOMAIN + "/about", "publisher": {"@type": "Organization", "name": BRAND}}))


def page_contact():
    cfg = PAGES_SETTINGS.get("contact") or {}
    title = cfg.get("title") or f"Contact & Work With Us | {BRAND}"
    h1 = cfg.get("h1") or "Get in touch"
    eyebrow = cfg.get("eyebrow") or "Contact"
    lede = cfg.get("lede") or "Questions about a guide, a product recommendation, or working together? Send a message — we read everything and reply to most emails within two business days."
    form_title = cfg.get("form_title") or "Send a message"
    form_note = cfg.get("form_note") or f"This form uses your Formspree ID from Site settings."
    other_title = cfg.get("other_title") or "Other ways to reach us"
    other_body_md = cfg.get("other_body") or ""
    other_html = md_to_html(other_body_md) if other_body_md else f"""<p><b>Email:</b> <a href="mailto:{EMAIL}">{EMAIL}</a></p><p><b>Pinterest:</b> Follow {BRAND}</p>"""
    faq_title = cfg.get("faq_title") or "Common questions"
    faqs = cfg.get("faqs") or []
    faq_html = ""
    for f in faqs:
        if not isinstance(f, dict):
            continue
        q = f.get("q","")
        a = f.get("a","")
        if q and a:
            faq_html += f"<details><summary>{q}</summary><p>{a}</p></details>"
    if not faq_html:
        faq_html = """<details><summary>Can I ask you to recommend a product for my room?</summary><p>Yes — send the room...</p></details>"""

    body = f"""
<section class="section tight"><div class="container narrow">
 <p class="eyebrow">{eyebrow}</p>
 <h1>{h1}</h1>
 <p class="lede">{lede}</p>
</div></section>

<section class="section"><div class="container">
 <div class="panel split">
  <div class="pad">
   <h2 style="margin-top:0">{form_title}</h2>
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
    <p class="muted" style="margin-top:14px">{form_note} <a href="https://formspree.io" rel="noopener" target="_blank">Formspree</a> form ID.</p>
   </form>
  </div>
  <div class="pad" style="background:#FBF6EF">
   <h2 style="margin-top:0">{other_title}</h2>
   {other_html}
   <div class="btnrow"><a class="btn sm ghost" href="affiliate-disclosure">See our disclosure</a></div>
  </div>
 </div>
</div></section>

<section class="section"><div class="container narrow">
 <h2>{faq_title}</h2>
 <div class="faq">
  {faq_html}
 </div>
</div></section>
"""
    desc = cfg.get("description") or f"Contact {BRAND}: reader questions, corrections, press and brand partnerships. Email {EMAIL} — replies within two business days."
    schema = json.dumps({"@context": "https://schema.org", "@type": "ContactPage", "name": f"Contact {BRAND}",
                         "url": DOMAIN + "/contact", "publisher": {"@type": "Organization", "name": BRAND}})
    return page("contact.html", title, desc, body, 0, canonical="contact", schema=schema)


def page_shop():
    cfg = PAGES_SETTINGS.get("shop-my-home") or {}
    title = cfg.get("title") or f"Shop My Home — Budget Decor We Actually Use | {BRAND}"
    h1 = cfg.get("h1") or "Shop the looks (and how our links work)"
    eyebrow = cfg.get("eyebrow") or "Shop my home"
    lede = cfg.get("lede") or f"These are the pieces we actually use in our own rooms, at the price we would pay. If you buy through a link here, {BRAND} may earn a small commission — at no extra cost to you. It never changes what makes the list."
    # buttons
    btns_cfg = cfg.get("buttons") or [{"label":"See the budget looks","url":"/blog#get-the-look","style":"primary"},{"label":"Read the disclosure","url":"/affiliate-disclosure","style":"ghost"}]
    btn_html = ""
    for b in btns_cfg:
        if not isinstance(b, dict):
            continue
        label = b.get("label","")
        url = _resolve_home_url(b.get("url",""))
        style = (b.get("style") or "primary").lower()
        cls = "btn" if style=="primary" else "btn ghost"
        if label and url:
            btn_html += f'<a class="{cls}" href="{url}">{label}</a>'

    def room_from_cfg(rc):
        # rc is dict with title, slug, tone, motif, note, items
        t_title = rc.get("title") or "Room"
        slug = rc.get("slug") or "living-room"
        tone = int(rc.get("tone") or 0)
        motif = rc.get("motif") or "arch"
        note = rc.get("note") or "Typical prices at the time of writing."
        items = rc.get("items") or []
        lis = ""
        for it in items:
            if not isinstance(it, dict):
                continue
            n = it.get("name","")
            note_it = it.get("note","")
            price = it.get("price","")
            if not n:
                continue
            lis += f'<li><span><b><a href="{amz(n)}" target="_blank" rel="nofollow sponsored noopener">{n}</a></b><span class="d">{note_it}</span></span><span class="p">{price}</span></li>'
        return f"""<div class="post-hero narrow" style="aspect-ratio:16/9;margin-bottom:0">{art_raw(motif, tone)}<div class="tag"><span>{t_title} &middot; shoppable</span></div></div>
<div class="shop"><h3>{t_title}</h3>
<p class="muted">{note} Links go to Amazon search results — see our <a href="affiliate-disclosure">disclosure</a>.</p>
<ul>{lis}</ul></div>"""

    rooms_cfg = cfg.get("rooms")
    if rooms_cfg:
        rooms_html = "".join(room_from_cfg(r) for r in rooms_cfg if isinstance(r, dict))
    else:
        # fallback old hardcoded
        def room_old(title, slug, tone, motif, items):
            lis = "".join(f'<li><span><b><a href="{amz(n)}" target="_blank" rel="nofollow sponsored noopener">{n}</a></b><span class="d">{note}</span></span><span class="p">{price}</span></li>' for n, note, price in items)
            return f"""<div class="post-hero narrow" style="aspect-ratio:16/9;margin-bottom:0">{art_raw(motif, tone)}<div class="tag"><span>{title} &middot; shoppable</span></div></div><div class="shop"><h3>{title}</h3><p class="muted">Typical prices...</p><ul>{lis}</ul></div>"""
        rooms_html = room_old("Warm minimalist living room", "living-room", 4, "arch", [("Chunky knit throw, oat","50×60 in","$25–40")]) + room_old("Cozy layered bedroom","bedroom",1,"portrait",[("Washed cotton duvet cover","Oat","$45–70")])

    how_title = cfg.get("how_to_title") or "How to shop a room without wasting money"
    how_steps = cfg.get("how_to_steps") or []
    if how_steps:
        steps_html = "".join(f'<li><b>{s.get("title","")}</b> {s.get("body","")}</li>' for s in how_steps if isinstance(s, dict))
        steps_html = f"<ol class='steps'>{steps_html}</ol>"
    else:
        steps_html = "<ol class='steps'><li><b>Buy the anchor first.</b> The rug...</li></ol>"

    sizing_title = cfg.get("sizing_title") or "Sizing before shopping"
    sizing_body = cfg.get("sizing_body") or "Measure your room..."
    not_title = cfg.get("not_link_title") or "What we do not link to"
    not_body = cfg.get("not_link_body") or "We do not recommend dropshipped decor..."

    body = f"""
<section class="section tight"><div class="container narrow">
 <p class="eyebrow">{eyebrow}</p>
 <h1>{h1}</h1>
 <p class="lede">{lede}</p>
 <div class="btnrow">{btn_html}</div>
</div></section>

<section class="section"><div class="container narrow">{rooms_html}</div></section>

<section class="section"><div class="container narrow">
 <h2>{how_title}</h2>
 {steps_html}
 <div class="callout"><h4>{sizing_title}</h4><p>{sizing_body}</p></div>

 <h2>{not_title}</h2>
 <p class="muted">{not_body}</p>
</div></section>

{newsletter()}
"""
    desc = cfg.get("description") or "Shoppable budget decor: the pieces we actually use in living rooms, bedrooms and small apartments, with typical prices and how our affiliate links work."
    return page("shop-my-home.html", title, desc, body, 0, canonical="shop-my-home",
                schema=json.dumps({"@context": "https://schema.org", "@type": "CollectionPage", "name": "Shop My Home",
                                   "url": DOMAIN + "/shop-my-home",
                                   "publisher": {"@type": "Organization", "name": BRAND}}))


def page_shop_now():
    cfg = PAGES_SETTINGS.get("shop-now") or {}
    title = cfg.get("title") or f"Shop Now — 30 Trending Home Decor Finds for 2026-2027 | {BRAND}"
    h1 = cfg.get("h1") or "Shop Now — 30 Pinterest-Predicted Finds"
    eyebrow = cfg.get("eyebrow") or "Shop Now — Trending before Jan 2027"
    lede = cfg.get("lede") or "Pinterest Predicts 2026 says Neo Deco, FunHaus, Cool Blue and Extra Celestial will dominate through January 2027. We hunted IKEA, Amazon and more for the 30 shoppable pieces."
    desc = cfg.get("description") or "30 trending home decor products from IKEA, Amazon and more predicted by Pinterest to trend before Jan 2027."
    intro_title = cfg.get("intro_title") or "Pinterest Predicts 2026 → Jan 2027"
    intro_body = cfg.get("intro_body") or "Neo Deco, FunHaus, Cool Blue, Extra Celestial — 30 products."

    btns_cfg = cfg.get("buttons") or []
    btn_html = ""
    for b in btns_cfg:
        if not isinstance(b, dict):
            continue
        label = b.get("label","")
        url = _resolve_home_url(b.get("url",""))
        style = (b.get("style") or "primary").lower()
        cls = "btn" if style=="primary" else "btn ghost"
        if label and url:
            btn_html += f'<a class="{cls}" href="{url}">{label}</a>'

    products = cfg.get("products") or []
    cards_html = ""
    for prod in products:
        if not isinstance(prod, dict):
            continue
        name = prod.get("name","")
        if not name:
            continue
        trend = prod.get("trend","")
        price = prod.get("price","")
        store = prod.get("store","")
        image = prod.get("image","")
        url = prod.get("url","")
        amazon_url = prod.get("amazon_url","")
        desc_p = prod.get("desc","")

        # fix amazon tag if placeholder
        if "YOUR-AMAZON-TAG-20" in url and TAG != "YOUR-AMAZON-TAG-20":
            url = url.replace("YOUR-AMAZON-TAG-20", TAG)
        if amazon_url and "YOUR-AMAZON-TAG-20" in amazon_url and TAG != "YOUR-AMAZON-TAG-20":
            amazon_url = amazon_url.replace("YOUR-AMAZON-TAG-20", TAG)

        img_src = asset_url(image, 0) if image else ""
        img_tag = f'<img src="{img_src}" alt="{_html.escape(name, quote=True)}" loading="lazy" decoding="async" style="width:100%;height:100%;object-fit:cover">' if img_src else '<div style="width:100%;height:100%;background:#F1E8DB;display:flex;align-items:center;justify-content:center;color:#999">No image</div>'

        # buttons: primary is main url, secondary is amazon alt if different
        btns = ""
        if url:
            label_btn = f"Shop at {store}" if store and "Amazon" not in store else "Shop on Amazon" if "amazon" in url.lower() else "Shop Now"
            if "ikea" in url.lower():
                label_btn = "Shop at IKEA"
            elif "amazon" in url.lower():
                label_btn = "Shop on Amazon"
            btns += f'<a class="btn sm" href="{url}" target="_blank" rel="nofollow sponsored noopener" style="background:#1A1A1A;color:#fff;border:1.5px solid #1A1A1A;border-radius:999px;padding:9px 16px;font-size:13px;font-weight:600;text-decoration:none;display:inline-block">{_html.escape(label_btn)}</a>'
        if amazon_url and amazon_url != url:
            btns += f'<a class="btn sm ghost" href="{amazon_url}" target="_blank" rel="nofollow sponsored noopener" style="border-radius:999px;padding:9px 16px;font-size:13px;font-weight:600">Amazon alt</a>'

        cards_html += f'''
<article class="card" style="display:flex;flex-direction:column;overflow:hidden">
  <div class="cover c4x3" style="background:#F7F3EF;overflow:hidden">{img_tag}</div>
  <div class="body" style="padding:16px 18px 18px;display:flex;flex-direction:column;flex:1">
    {f'<span class="chip" style="background:#FFF0E8;border:1px solid #FADAC9;color:#B5533C;font-size:11px;padding:4px 9px;border-radius:999px;width:fit-content;margin-bottom:8px">{_html.escape(trend)}</span>' if trend else ''}
    <h3 style="font-size:17.5px;line-height:1.3;margin:0 0 6px"><a href="{url}" target="_blank" rel="nofollow sponsored noopener" style="color:var(--ink);border:0">{_html.escape(name)}</a></h3>
    <p class="muted" style="font-size:14px;line-height:1.5;margin:0 0 12px;flex:1">{_html.escape(desc_p)}</p>
    <div style="display:flex;justify-content:space-between;align-items:center;margin-top:auto;gap:12px">
      <span style="font-weight:700;color:#3A5A40;font-size:15px">{_html.escape(str(price))}</span>
      <span style="font-size:11.5px;color:#999">{_html.escape(store)}</span>
    </div>
    <div class="btnrow" style="margin-top:12px;gap:8px">{btns}</div>
  </div>
</article>
'''

    body = f"""
<section class="section tight"><div class="container narrow">
 <p class="eyebrow">{_html.escape(eyebrow)}</p>
 <h1>{_html.escape(h1)}</h1>
 <p class="lede">{_html.escape(lede)}</p>
 <div class="btnrow">{btn_html}</div>
</div></section>

<section class="section" style="padding-top:18px"><div class="container narrow">
 <div style="background:#FFF8F0;border:1px solid #F0D9C5;border-radius:16px;padding:18px 20px;margin:0 0 28px;font-size:15px;line-height:1.6">
  <b>{_html.escape(intro_title)}:</b> {_html.escape(intro_body)} We sourced 30 real products from <b>IKEA, Amazon, CB2, West Elm</b> with affiliate links.
 </div>
</div></section>

<section class="section" style="padding-top:0"><div class="container">
 <div class="grid" style="grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:24px">{cards_html}</div>
</div></section>

<section class="section"><div class="container narrow">
 <div style="background:#F6F5F2;border:1px solid #E8E0D8;border-radius:16px;padding:20px 22px;margin:0">
  <h3 style="margin:0 0 8px;font-size:19px">How we picked these 30</h3>
  <p style="margin:0;font-size:14.5px;line-height:1.6;color:#555">We cross-referenced <b>Pinterest Predicts 2026</b> (Neo Deco +100% bar cart, +80% red marble, +40% pendant, +35% brass/banquette; FunHaus +130% circus interior, +40% striped; Cool Blue +50% icy blue; Extra Celestial +115% opalescent; Laced Up +105% lace; Cabbage Crush), <b>Pinterest Spring 2026</b> (aubergine kitchen +495%, sage/cream +410%, moody blue +325%, Calacatta Viola +260%, white oak/black +625%, reading nook +245%), and <b>IKEA 2026 Style Guide</b> (Joycore, Floral Daydream, Art of Storage, Rebel Pink, STOCKHOLM 2025).</p>
 </div>
</div></section>

{newsletter()}
"""
    return page("shop-now.html", title, desc, body, 0, canonical="shop-now",
                schema=json.dumps({"@context": "https://schema.org", "@type": "CollectionPage", "name": "Shop Now — 30 Trending Finds",
                                   "url": DOMAIN + "/shop-now",
                                   "publisher": {"@type": "Organization", "name": BRAND}}))


def page_custom(p):
    """Render a custom page from content/custom-pages/ — /slug.html"""
    slug = p["slug"]
    # hero image if exists
    hero_html = ""
    if p.get("hero_image"):
        rel_path = p["hero_image"].lstrip("/")
        if os.path.exists(os.path.join(ROOT, rel_path)):
            hero_html = f'<div class="container narrow"><div class="post-hero" style="aspect-ratio:16/9"><img src="{asset_url(p["hero_image"],0)}" alt="" style="width:100%;height:100%;object-fit:cover"></div></div>'
    body = f"""
<section class="section tight"><div class="container narrow">
 {f'<p class="eyebrow">{p["eyebrow"]}</p>' if p.get("eyebrow") else ''}
 <h1>{p["h1"]}</h1>
 {f'<p class="lede">{p["lede"]}</p>' if p.get("lede") else ''}
</div></section>
{hero_html}
<section class="section"><div class="container narrow article">
 {p["body"]}
</div></section>

{newsletter()}
"""
    desc = p.get("description") or p["lede"] or f"{p['title']} — {BRAND}"
    return page(f"{slug}.html", p["title"], desc, body, 0,
                canonical=f"{slug}",
                schema=json.dumps({"@context": "https://schema.org", "@type": "WebPage", "name": p["title"],
                                   "url": DOMAIN + f"/{slug}",
                                   "publisher": {"@type": "Organization", "name": BRAND}}))


def page_404():
    body = f"""
<section class="section"><div class="container narrow center">
 <p class="eyebrow">404</p>
 <h1>That page has moved out</h1>
 <p class="lede">The link is broken or the guide has been renamed. Try one of these instead:</p>
 <div class="btnrow" style="justify-content:center">
  <a class="btn" href="./">Home</a>
  <a class="btn ghost" href="blog">All decor ideas</a>
  <a class="btn ghost" href="start-here">Start here</a>
 </div>
</div></section>
<section class="section"><div class="container">
 <div class="grid">
  {''.join(card(p) for p in POSTS[:3])}
 </div>
</div></section>
"""
    return page("404.html", f"Page not found | {BRAND}", "That page does not exist. Browse the room guides instead.", body, 0, canonical="404")


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
    "/disclosure/": "affiliate-disclosure", "/affiliate-disclosure/": "affiliate-disclosure",
    "/cookie-policy/": "cookie-policy", "/privacy-policy/": "privacy-policy",
    "/terms-of-use/": "terms-of-use", "/disclaimer/": "disclaimer", "/contact/": "contact",
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
    ("privacy-policy", "privacy-policy.md", "Privacy Policy"),
    ("cookie-policy", "cookie-policy.md", "Cookie Policy"),
    ("terms-of-use", "terms-of-use.md", "Terms of Use"),
    ("disclaimer", "disclaimer.md", "Disclaimer"),
    ("affiliate-disclosure", "affiliate-disclosure.md", "Affiliate & Advertising Disclosure"),
]
# Legal pages are content: they ship inside the repo so the build works anywhere.
LEGAL_DIR = os.path.join(CONTENT, "legal")
if not os.path.isdir(LEGAL_DIR):                     # convenience for local working copies
    alt = os.path.join(os.path.dirname(ROOT), "home-decor-blog", "legal")
    if os.path.isdir(alt):
        LEGAL_DIR = alt


def legal_pages():
    pages = []
    for out_name, src_name, label in LEGAL_FILES:
        src = os.path.join(LEGAL_DIR, src_name)
        if not os.path.exists(src):
            raise SystemExit(f"Missing legal source file: {src}\n"
                             f"Expected the legal Markdown in content/legal/")
        md = open(src, encoding="utf-8").read()
        for k, v in PLACEHOLDER.items():
            md = md.replace(k, v)
        html_block = md_to_html(md)
        html_block = re.sub(r"^<h1>.*?</h1>\s*", "", html_block, count=1, flags=re.S)
        pills = "".join(f'<a href="{n}">{l}</a>' for n, _, l in LEGAL_FILES if n != out_name)
        pills += '<a href="contact">Contact</a>'
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
        # Write as .html file for correct MIME type, but canonical clean without .html
        pages.append(page(f"{out_name}.html", f"{label} | {BRAND}", desc, body, 0, canonical=out_name,
                          schema=json.dumps({"@context": "https://schema.org", "@type": "WebPage", "name": label,
                                             "url": f"{DOMAIN}/{out_name}"})))
    return pages


# ------------------------------------------------------------------- extras
def write_extras():
    urls = [("", "1.0", "weekly"), ("blog", "0.9", "weekly"), ("start-here", "0.8", "monthly"),
            ("shop-my-home", "0.8", "monthly"), ("about", "0.5", "yearly"),
            ("contact", "0.5", "yearly")]
    urls += [(f"blog/{p['cat']}/{p['slug']}", "0.9", "monthly") for p in POSTS]
    urls += [("privacy-policy", "0.3", "yearly"), ("cookie-policy", "0.3", "yearly"),
             ("terms-of-use", "0.3", "yearly"), ("disclaimer", "0.3", "yearly"),
             ("affiliate-disclosure", "0.3", "yearly")]
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
COMMENTS = load_comments()
print(f"  comments: {sum(len(v) for v in COMMENTS.values())} approved across {len(COMMENTS)} posts")
CUSTOM_PAGES = load_custom_pages()
print(f"  custom pages: {len(CUSTOM_PAGES)}")


REDIRECTS_FILE = os.path.join(CONTENT, "redirects.yml")


def load_redirects():
    """Old URL -> new URL, kept in content/redirects.yml so renames never 404.

    Pinterest pins and Google results point at exact URLs. When a post's slug
    changes, the old address keeps working instead of dropping the traffic.
    """
    if not os.path.exists(REDIRECTS_FILE):
        return {}
    data, _ = md_engine.parse_frontmatter("---\n" + open(REDIRECTS_FILE, encoding="utf-8").read() + "\n---")
    return {k: str(v).strip() for k, v in data.items()
            if isinstance(v, str) and v.strip() and not k.startswith("_")}


def save_redirects(mapping):
    lines = ["# Renamed pages: old path -> new path.",
             "# The build writes a redirect at each old path, so existing links keep working.",
             ""]
    lines += [f"{k}: {v}" for k, v in sorted(mapping.items())]
    with open(REDIRECTS_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def redirect_stub(rel_old, rel_new):
    up = "../" * (rel_old.count("/"))
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<title>Moved</title>
<link rel="canonical" href="{DOMAIN}/{rel_new}">
<meta name="robots" content="noindex,follow">
<meta http-equiv="refresh" content="0; url={up}{rel_new}">
</head><body style="font-family:Georgia,serif;padding:40px;line-height:1.6">
<p>This page moved to <a href="{up}{rel_new}">{DOMAIN}/{rel_new}</a>.</p>
</body></html>
"""


def write_redirects(generated):
    redirects = load_redirects()
    n = 0
    for old, new in redirects.items():
        if old in generated or not os.path.exists(os.path.join(ROOT, new)):
            continue
        write(old, redirect_stub(old, new))
        n += 1
    if n:
        print(f"  redirects: {n} old URL(s) pointing at current pages")


def retire_stale_pages(generated):
    """Handle posts whose URL changed (a renamed slug, or a new slug from Pages CMS).

    Without this, renaming a post leaves the old HTML file on the site as a
    duplicate page — which is exactly what happened on the live site when the
    CMS wrote a new slug. Any blog page we did not generate this run is either
    turned into a redirect stub (when a current post shares its headline, i.e. it
    was renamed) or deleted.
    """
    titles = {}
    for p in POSTS:
        clean = _html.unescape(re.sub(r"<[^>]+>", "", p["h1"]))
        titles[re.sub(r"\s+", " ", clean).strip().lower()] = p

    removed, redirected = [], []
    known_redirects = load_redirects()
    for old in glob.glob(os.path.join(ROOT, "blog", "*", "*.html")):
        rel = os.path.relpath(old, ROOT).replace(os.sep, "/")
        if rel in generated or rel in known_redirects:
            continue
        txt = open(old, encoding="utf-8").read()
        heading = re.search(r"<h1[^>]*>(.*?)</h1>", txt, re.S)
        key = ""
        if heading:
            key = re.sub(r"\s+", " ", _html.unescape(re.sub(r"<[^>]+>", "", heading.group(1)))).strip().lower()
        target = titles.get(key)
        if target:
            new_rel = f'blog/{target["cat"]}/{target["slug"]}.html'
            redirects = load_redirects()
            if redirects.get(rel) != new_rel:
                redirects[rel] = new_rel
                save_redirects(redirects)
                print(f"  remembered redirect: {rel} -> {new_rel}")
            depth_up = "../" * 2
            write(rel, f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<title>Moved: {_html.escape(target['title'])}</title>
<link rel="canonical" href="{DOMAIN}/{new_rel}">
<meta name="robots" content="noindex,follow">
<meta http-equiv="refresh" content="0; url={depth_up}{new_rel}">
</head><body style="font-family:Georgia,serif;padding:40px;line-height:1.6">
<p>This guide moved to <a href="{depth_up}{new_rel}">{_html.escape(target['title'])}</a>.</p>
</body></html>
""")
            redirected.append(f"{rel} -> {new_rel}")
        else:
            os.remove(old)
            removed.append(rel)
    for d_ in glob.glob(os.path.join(ROOT, "blog", "*")):
        if os.path.isdir(d_) and not os.listdir(d_):
            os.rmdir(d_)
    for r in redirected:
        print(f"  redirect stub: {r}")
    for r in removed:
        print(f"  removed stale page: {r}")


def check_links():
    """Fail the build if a generated page links to something that does not exist — handles clean URLs without .html."""
    import glob
    files = sorted(glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True))
    skip_names = {"preview.html", "bookmarklet.html"}
    files = [f for f in files if os.path.basename(f) not in skip_names]
    anchors = {f: set(re.findall(r'id="([^"]+)"', open(f, encoding="utf-8").read())) for f in files}
    broken, warnings = [], []
    import urllib.parse
    def exists_clean(t, original_path=""):
        # Handle absolute / links as ROOT-relative
        if original_path.startswith("/"):
            # / -> ROOT/index.html, /about -> ROOT/about.html, /blog#... -> ROOT/blog.html
            clean = original_path.lstrip("/")
            if clean == "":
                clean = "index.html"
            # try ROOT/clean.html first
            if os.path.exists(os.path.join(ROOT, clean + ".html")) and not clean.endswith(".html"):
                return os.path.join(ROOT, clean + ".html")
            if os.path.exists(os.path.join(ROOT, clean)):
                p = os.path.join(ROOT, clean)
                if os.path.isfile(p):
                    return p
                if os.path.isdir(p) and os.path.exists(os.path.join(p, "index.html")):
                    return os.path.join(p, "index.html")
                # for /blog where both dir and .html exist, prefer .html
                if os.path.exists(os.path.join(ROOT, clean + ".html")):
                    return os.path.join(ROOT, clean + ".html")
            # fallback to index.html for /
            if clean in ("", "index.html"):
                return os.path.join(ROOT, "index.html")
            return None
        # t is absolute filesystem path without fragment — handle clean URLs
        if os.path.exists(t + ".html"):
            return t + ".html"
        if os.path.exists(t):
            if os.path.isfile(t):
                return t
            if os.path.isdir(t) and os.path.exists(os.path.join(t, "index.html")):
                return os.path.join(t, "index.html")
            return t if os.path.isfile(t) else None
        return None

    for f in files:
        for m in re.finditer(r'(?:href|src)="([^"]+)"', open(f, encoding="utf-8").read()):
            u = _html.unescape(m.group(1))
            if not u or u.startswith(("http", "mailto:", "data:", "#", "tel:", "javascript:")):
                continue
            if "{{" in u or "}}" in u or "'+ " in u or " +'" in u or u.startswith("'+") or u.endswith("+'") or ("+" in u and "liveUrl" in u):
                continue
            u = urllib.parse.unquote(u)
            path, _, frag = u.partition("#")
            if not path:
                target_file = f
                target_exists = True
            else:
                target = os.path.normpath(os.path.join(os.path.dirname(f), path)) if not path.startswith("/") else path
                found = exists_clean(target, original_path=path)
                if not found:
                    if u.rsplit(".", 1)[-1].lower() in ("jpg", "jpeg", "png", "webp", "gif", "svg", "mp4"):
                        warnings.append(f"{os.path.relpath(f, ROOT)} -> {u}")
                        continue
                    broken.append(f"{os.path.relpath(f, ROOT)} -> {u}")
                    continue
                target_file = found
                target_exists = True
            if frag and target_exists:
                # check anchor in target file (or its .html version)
                if frag not in anchors.get(target_file, set()):
                    # also check if anchor is a category id like living-room — those are in blog.html
                    # For blog#living-room, target is blog.html, anchor should be in that file
                    # Our anchors dict already has ids from that file, so if not found, it's broken
                    # But we allow blog#* anchors to pass if they are category slugs (they are generated as ids)
                    if not (os.path.basename(target_file) == "blog.html" and frag in [c["slug"] for c in CATS]):
                        broken.append(f"{os.path.relpath(f, ROOT)} -> {u} (missing anchor)")
    for w in warnings:
        print(f"  ! missing image (page still published): {w}")
    if broken:
        print("\n  BROKEN LINKS FOUND — fix the content before publishing:")
        for x in broken:
            print("   ", x)
        raise SystemExit(1)
    print(f"  link check: {len(files)} pages, 0 broken links")


def main():
    pages = [page_home(), page_blog(), page_start_here(), page_about(), page_contact(), page_shop(), page_shop_now()]
    pages += [page_post(p) for p in POSTS]
    pages += [page_custom(p) for p in CUSTOM_PAGES]
    pages += legal_pages()
    for path, html in pages:
        write(path, html)
    write_extras()
    make_og_image()
    generated = {p for p, _ in pages} | {"404.html"}
    retire_stale_pages(generated)
    write_redirects(generated)
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
