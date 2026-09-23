# -*- coding: utf-8 -*-
"""HomeDecorPad — content engine.

Reads the Markdown files in content/posts/*.md and renders them into the
site's HTML components (callouts, steps, shop boxes, FAQ accordions).
Hand-written so the build needs no third-party dependencies and runs on a
bare GitHub Actions runner.

Authoring reference (this is what Pages CMS gives you a form for):

    ---
    title:  SEO title (also the <title> and <h1>)
    date:   2026-08-04
    category: get-the-look
    dek:    one-sentence summary used for cards, meta description and OG
    intro:  the lede paragraph shown above the fold
    tags:   [warm minimalist, living room]
    motif:  arch
    related: [other-post-slug]
    draft:  false
    ---

    ## A heading
    Normal **markdown** with [links](/blog.html#color) or [links](post:some-slug).

    :::callout Optional title
    Highlighted tip.
    :::

    :::steps
    1. **Step title.** What to do.
    :::

    :::shop Shop title
    _Optional note line._
    | Item | Detail | Price |
    | --- | --- | --- |
    | Chunky knit throw | 50x60 in | $25-40 |
    :::

    ## Frequently asked questions
    ### The question?
    The answer.
"""
import re
import html as _html


# --------------------------------------------------------------------- YAML-ish
def _split_flow(s):
    """Split `a, "b, c", d` on top-level commas."""
    out, buf, quote = [], [], None
    for ch in s:
        if quote:
            buf.append(ch)
            if ch == quote:
                quote = None
        elif ch in "\"'":
            quote = ch
            buf.append(ch)
        elif ch == ",":
            out.append("".join(buf).strip())
            buf = []
        else:
            buf.append(ch)
    if buf:
        out.append("".join(buf).strip())
    return out


def _scalar(v):
    v = v.strip()
    if v == "":
        return ""
    if v in ("null", "~"):
        return None
    if v.lower() in ("true", "yes"):
        return True
    if v.lower() in ("false", "no"):
        return False
    if len(v) > 1 and v[0] == '"' and v[-1] == '"':
        return v[1:-1].replace('\\"', '"').replace("\\n", "\n").replace("\\\\", "\\")
    if len(v) > 1 and v[0] == "'" and v[-1] == "'":
        return v[1:-1].replace("''", "'")
    if re.fullmatch(r"-?\d+", v):
        return int(v)
    if re.fullmatch(r"-?\d+\.\d+", v):
        return float(v)
    if v.startswith("[") and v.endswith("]"):
        inner = v[1:-1].strip()
        return [] if not inner else [_scalar(x) for x in _split_flow(inner)]
    return v


def parse_frontmatter(text):
    """Return (data, body). Tolerant of the way CMS editors re-serialise YAML."""
    lines = text.replace("\r\n", "\n").split("\n")
    if not lines or lines[0].strip() not in ("---", "+++"):
        return {}, text
    close = None
    for i in range(1, len(lines)):
        if lines[i].strip() in ("---", "..."):
            close = i
            break
    if close is None:
        return {}, text
    fm, body = lines[1:close], "\n".join(lines[close + 1:])

    data, key, i = {}, None, 0
    while i < len(fm):
        raw = fm[i]
        if not raw.strip() or raw.lstrip().startswith("#"):
            i += 1
            continue
        if raw.startswith((" ", "\t")) and key:
            stripped = raw.strip()
            if stripped.startswith("- "):
                data.setdefault(key, [])
                if isinstance(data[key], list):
                    data[key].append(_scalar(stripped[2:]))
                i += 1
                continue
            i += 1
            continue
        m = re.match(r"^([A-Za-z0-9_\-]+):\s*(.*)$", raw)
        if not m:
            i += 1
            continue
        key, val = m.group(1), m.group(2).strip()
        if val in ("|", "|-", ">", ">-"):
            block, i = [], i + 1
            while i < len(fm) and (fm[i].startswith((" ", "\t")) or not fm[i].strip()):
                block.append(fm[i][2:] if fm[i].startswith("  ") else fm[i].strip())
                i += 1
            data[key] = ("\n" if val.startswith("|") else " ").join(x for x in block).strip()
            continue
        if val == "":
            nxt = fm[i + 1].strip() if i + 1 < len(fm) else ""
            if nxt.startswith("- "):
                data[key] = []
                i += 1
                while i < len(fm) and fm[i].startswith((" ", "\t")) and fm[i].strip().startswith("- "):
                    data[key].append(_scalar(fm[i].strip()[2:]))
                    i += 1
                continue
            data[key] = ""
            i += 1
            continue
        data[key] = _scalar(val)
        i += 1
    return data, body


# ---------------------------------------------------------------------- inline
def inline(t, resolve):
    t = _html.escape(t, quote=False)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)

    def link(m):
        label, href = m.group(1), m.group(2)
        return f'<a href="{_html.escape(resolve(href), quote=True)}">{label}</a>'

    t = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", link, t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<![\w*])\*([^*\n]+)\*(?!\*)", r"<em>\1</em>", t)
    t = re.sub(r"(?<![\w_])_([^_\n]+)_(?!_)", r"<em>\1</em>", t)
    return t


# ---------------------------------------------------------------------- tokens
def _tokenize(body):
    lines = body.replace("\r\n", "\n").split("\n")
    blocks, i = [], 0
    while i < len(lines):
        ln = lines[i]
        if not ln.strip():
            i += 1
            continue
        if ln.startswith(":::"):
            head = ln.strip().strip(":").strip()
            inner, i = [], i + 1
            while i < len(lines) and not lines[i].startswith(":::"):
                inner.append(lines[i])
                i += 1
            i += 1
            blocks.append(("component", head, "\n".join(inner)))
            continue
        m = re.match(r"^(#{1,6})\s+(.*)$", ln)
        if m:
            blocks.append(("heading", len(m.group(1)), m.group(2).strip()))
            i += 1
            continue
        if re.match(r"^\s*([-*_])(\s*\1){2,}\s*$", ln):
            blocks.append(("hr", 0, ""))
            i += 1
            continue
        if ln.lstrip().startswith("|"):
            rows, i = [], i
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                rows.append(lines[i].strip())
                i += 1
            blocks.append(("table", 0, rows))
            continue
        if re.match(r"^\s*[-*+]\s+", ln):
            items, i = [], i
            while i < len(lines) and re.match(r"^\s*[-*+]\s+", lines[i]):
                items.append(re.sub(r"^\s*[-*+]\s+", "", lines[i]).strip())
                i += 1
            blocks.append(("ul", 0, items))
            continue
        if re.match(r"^\s*\d+[.)]\s+", ln):
            items, i = [], i
            while i < len(lines) and re.match(r"^\s*\d+[.)]\s+", lines[i]):
                items.append(re.sub(r"^\s*\d+[.)]\s+", "", lines[i]).strip())
                i += 1
            blocks.append(("ol", 0, items))
            continue
        if ln.lstrip().startswith(">"):
            quote, i = [], i
            while i < len(lines) and lines[i].lstrip().startswith(">"):
                quote.append(lines[i].lstrip()[1:].strip())
                i += 1
            blocks.append(("quote", 0, " ".join(quote)))
            continue
        para, i = [ln.strip()], i + 1
        while i < len(lines) and lines[i].strip() and not re.match(
                r"^(#{1,6}\s|:::|\s*[-*+]\s|\s*\d+[.)]\s|>|\|)", lines[i]):
            para.append(lines[i].strip())
            i += 1
        blocks.append(("para", 0, " ".join(para)))
    return blocks


def _table(rows, resolve):
    cells = [[c.strip() for c in r.strip().strip("|").split("|")] for r in rows]
    if len(cells) >= 2 and set("".join(cells[1])) <= set("-: "):
        heads, body = cells[0], cells[2:]
    else:
        heads, body = cells[0], cells[1:]
    out = ["<table><thead><tr>" + "".join(f"<th>{inline(c, resolve)}</th>" for c in heads)
           + "</tr></thead><tbody>"]
    for r in body:
        r = (r + [""] * len(heads))[:len(heads)]
        out.append("<tr>" + "".join(f"<td>{inline(c, resolve)}</td>" for c in r) + "</tr>")
    out.append("</tbody></table>")
    return "".join(out)


def _shop_from_table(rows, resolve):
    """Shop boxes read better as a styled list than a plain table."""
    cells = [[c.strip() for c in r.strip().strip("|").split("|")] for r in rows]
    body = cells[2:] if len(cells) >= 2 and set("".join(cells[1])) <= set("-: ") else cells[1:]
    out = ["<ul>"]
    for r in body:
        r = (r + [""] * 3)[:3]
        desc = f'<span class="d">{inline(r[1], resolve)}</span>' if r[1] else ""
        price = f'<span class="p">{inline(r[2], resolve)}</span>' if r[2] else ""
        out.append(f'<li><span><b>{inline(r[0], resolve)}</b>{desc}</span>{price}</li>')
    out.append("</ul>")
    return "".join(out)


AD_SLOT = '<div class="ad-slot">Ad slot &mdash; paste your AdSense unit here</div>'
FAQ_HEADING = re.compile(r"frequently asked questions|^faq$", re.I)


def _inner(text, resolve):
    """Render a nested block (inside callouts, shop boxes)."""
    html, _ = render(text, resolve, faq_heading=False)
    return html


def _render_block(kind, arg, payload, resolve):
    if kind == "para":
        return f"<p>{inline(payload, resolve)}</p>"
    if kind == "ul":
        return "<ul>" + "".join(f"<li>{inline(x, resolve)}</li>" for x in payload) + "</ul>"
    if kind == "ol":
        return "<ol>" + "".join(f"<li>{inline(x, resolve)}</li>" for x in payload) + "</ol>"
    if kind == "quote":
        return f"<blockquote>{inline(payload, resolve)}</blockquote>"
    if kind == "hr":
        return "<hr>"
    if kind == "table":
        return _table(payload, resolve)
    if kind == "component":
        name, _, rest = arg.partition(" ")
        title = rest.strip()
        if name == "ad":
            return AD_SLOT
        if name == "callout":
            head = f"<h4>{inline(title, resolve)}</h4>" if title else ""
            return f'<div class="callout">{head}{_inner(payload, resolve)}</div>'
        if name == "steps":
            items = []
            for k, a, p in _tokenize(payload):
                if k in ("ol", "ul"):
                    items += p
                elif k == "para":
                    items.append(p)
            return '<ol class="steps">' + "".join(f"<li>{inline(x, resolve)}</li>" for x in items) + "</ol>"
        if name == "shop":
            parts = [f"<h3>{inline(title, resolve)}</h3>"] if title else []
            for k, a, p in _tokenize(payload):
                if k == "table":
                    parts.append(_shop_from_table(p, resolve))
                elif k == "para":
                    parts.append(f'<p class="muted">{inline(p, resolve)}</p>')
                else:
                    parts.append(_render_block(k, a, p, resolve))
            return '<div class="shop">' + "".join(parts) + "</div>"
        if name == "note":
            return f'<p class="muted">{inline(payload.strip(), resolve)}</p>'
        if name == "pincard":
            return ""      # the page builder adds the pin call-to-action itself
        return _inner(payload, resolve)
    return ""


def render(body, resolve, faq_heading=True):
    """Markdown -> (html, faq_items) where faq_items = [(question, answer_html), ...]."""
    blocks = _tokenize(body)
    parts, faq, faq_open = [], [], False

    def flush():
        nonlocal faq_open
        if faq_open:
            inner = "".join(f"<details><summary>{inline(q, resolve)}</summary>{a}</details>"
                            for q, a in faq)
            parts.append(f'<div class="faq">{inner}</div>')
            faq_open = False

    i = 0
    while i < len(blocks):
        kind, arg, payload = blocks[i]
        if kind == "heading":
            level, text = arg, payload
            if faq_heading and level == 2 and FAQ_HEADING.search(text.strip()):
                flush()
                faq_open = True
                i += 1
                continue
            if faq_open and level <= 2:
                flush()
            if faq_open and level == 3:
                answer, j = [], i + 1
                while j < len(blocks) and blocks[j][0] != "heading":
                    k, a, p = blocks[j]
                    answer.append(_render_block(k, a, p, resolve))
                    j += 1
                faq.append((text, "".join(answer)))
                i = j
                continue
            parts.append(f"<h{level}>{inline(text, resolve)}</h{level}>")
            i += 1
            continue
        parts.append(_render_block(kind, arg, payload, resolve))
        i += 1
    flush()

    # one ad slot per post, placed above the FAQ block or after the third heading
    if not any("ad-slot" in p for p in parts):
        faq_idx = next((n for n, p in enumerate(parts) if p.startswith('<div class="faq"')), None)
        h2s = [n for n, p in enumerate(parts) if p.startswith("<h2")]
        if faq_idx is not None and faq_idx > 2:
            parts.insert(faq_idx, AD_SLOT)          # just above the FAQ block
        elif len(h2s) >= 3:
            parts.insert(h2s[2], AD_SLOT)           # before the third section
        elif h2s:
            parts.insert(h2s[-1] + 1, AD_SLOT)      # after the last section, never first
    return "\n".join(p for p in parts if p.strip()), faq
