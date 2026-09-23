# HomeDecorPad — static blog, ready for GitHub Pages

A complete, dependency-free static home decor blog: 8 full-length guides, 11 supporting
and legal pages, an original SVG illustration system, category share images, sitemap,
robots.txt, ads.txt and AdSense-ready legal pages.

**No build step is required to deploy.** The HTML in this folder is finished output.
You can upload it to GitHub exactly as it is.

---

## 1. What is in this folder

```
index.html               Home page
start-here.html          "Start here" hub (positioning + your first projects)
blog.html                All guides, filterable by room + search
shop-my-home.html        Shoppable budget decor (affiliate hub)
about.html               About (editorial standards, how the site makes money)
contact.html             Contact + "work with us" (form has a placeholder ID)
404.html                 Friendly not-found page (GitHub Pages uses this automatically)
privacy-policy.html      \
cookie-policy.html        |
terms-of-use.html         >  AdSense-ready legal pages, brand name filled in
disclaimer.html           |
affiliate-disclosure.html/
blog/<category>/<slug>.html    8 posts (~700-900 words each, plus checklists,
                                shopping tables and FAQ blocks)
assets/og-*.jpg           Social share images (1 default + 1 per category)
sitemap.xml  robots.txt  ads.txt  .nojekyll
_build/                  The generator (optional — see section 7)
```

Everything is self-contained: illustrations are inline SVG, CSS is inlined in every page,
and JavaScript is a single newsletter form + the cookie banner. The only external request
is Google Fonts, and the site still looks correct if you delete it (it falls back to Georgia).

---

## 2. Put it on GitHub (web upload — about 3 minutes)

1. Go to <https://github.com/new> and create a repository, e.g. `homedecorpad-site`.
   Set it to **Public** (GitHub Pages needs public on free accounts). Do **not** add a README.
2. On the empty repo page, click **uploading an existing file**.
3. Drag the *contents* of this `homedecorpad` folder into the browser window — `index.html`,
   `blog`, `assets`, and the rest. Do not drag the outer folder itself, and do not upload
   the `_build` folder unless you want the generator on GitHub too (it is harmless either way).
4. Commit the changes.
5. In the repo: **Settings → Pages → Source: Deploy from a branch → Branch: `main` / `(root)`
   → Save**. Wait 1–2 minutes.
6. Your site is live at `https://<your-username>.github.io/<repo-name>/`.

The `.nojekyll` file is included on purpose — it stops GitHub Pages from processing the
files and keeps every path working.

### Optional: via command line

```bash
git init
git add .
git commit -m "HomeDecorPad launch"
git branch -M main
git remote add origin https://github.com/<your-username>/<repo-name>.git
git push -u origin main
```

---

## 3. Custom domain (do this when you buy homedecorpad.com)

1. Buy the domain (Namecheap, Cloudflare, Porkbun are all fine).
2. In GitHub: **Settings → Pages → Custom domain**, enter `homedecorpad.com`, save.
3. At your registrar, add these DNS records:

   | Type  | Name | Value |
   |---|---|---|
   | A | @ | 185.199.108.153 |
   | A | @ | 185.199.109.153 |
   | A | @ | 185.199.110.153 |
   | A | @ | 185.199.111.153 |
   | CNAME | www | `<your-username>.github.io` |

4. Wait for DNS (minutes to a few hours), then tick **Enforce HTTPS** in the Pages settings.
5. Create a plain text file named `CNAME` in the repository root containing exactly
   `homedecorpad.com` and commit it. GitHub usually does this for you when you set the
   custom domain — if it does, leave it alone.

> If your final domain or brand differs, the site text uses `HomeDecorPad` and
> `homedecorpad.com`. The legal pages are the only place you must update carefully — they
> name the domain and the operator. Use find-and-replace across the HTML files.

---

## 4. Launch checklist (in this order)

- [ ] **AdSense** — apply at <https://adsense.google.com>. When approved:
      - Uncomment the AdSense script block in the `<head>` of every page, replacing
        `ca-pub-XXXXXXXXXXXXXXXX` with your publisher ID. (It is currently a commented-out
        block, so nothing loads and nothing breaks before approval.)
      - Replace the placeholder line in `ads.txt` with the exact line AdSense shows you.
      - Drop your ad units into the slots marked `Ad slot — paste your AdSense unit here`.
        There is one on the homepage area and inside posts; search for `ad-slot`.
- [ ] **Google Analytics 4** — uncomment the GA4 block in the `<head>` and add your
      `G-XXXXXXXXXX` ID. (Optional but useful for knowing which rooms people read.)
- [ ] **Pinterest** — add the `<meta name="p:domain_verify" ...>` tag in the `<head>`
      (there is a placeholder comment there), verify your domain, then claim the site on
      Pinterest so your pins carry your profile and analytics attribute your traffic.
- [ ] **Amazon Associates** — replace `YOUR-AMAZON-TAG-20` with your real tracking ID.
      It lives in the "Shop My Home" page links and in the Amazon search links inside
      posts. One find-and-replace across all HTML files does it.
- [ ] **Contact form** — create a free form at <https://formspree.io>, then replace
      `YOUR_FORM_ID` in `contact.html`.
- [ ] **Newsletter** — the sign-up forms are intentionally inert. When you pick a provider
      (Kit, MailerLite, Beehiiv), point the form at their action URL and delete the
      `alert(...)` handler. Search for `Newsletter is not connected`.
- [ ] **Search Console** — verify the domain and submit `sitemap.xml`.
- [ ] **Social links** — the footer icons currently link to `#`. Replace with your real
      Pinterest, Instagram, Facebook and YouTube URLs.
- [ ] **Consent banner** — the built-in banner is a simple notice with an Accept/Reject
      choice, stored in `localStorage`. It is enough for a first launch, but for EEA/UK
      traffic Google AdSense requires a **Google-certified CMP**. Turn on Google's own
      GDPR message in AdSense (**Privacy & messaging → GDPR**), which is free, and keep
      this banner for non-EEA visitors.

---

## 5. Editing content

**Text edits** — open the HTML file in any editor (VS Code, or GitHub's own pencil icon).
Posts live in `blog/<category>/<slug>.html`. The structure is plain HTML with no templating,
so you can edit a headline, a price or a paragraph directly and commit.

**Adding a post without the generator** — copy an existing post file, keep the `<head>`
block and the surrounding header/footer, replace the `<article>` content, then add a link
to it in `blog.html` and an entry in `sitemap.xml`.

---

## 6. Housekeeping that matters for AdSense approval

- **Publish consistently for a few weeks first.** 8 posts is around the minimum; 15–20
  looks considerably safer, and adding the two fall/holiday guides before applying is time
  well spent.
- **Keep the legal pages accurate.** The privacy policy already covers Google cookies,
  third-party vendors, the Ads Settings opt-out and your CMP requirement. If you add an
  email provider or an ad network, update the cookie table in `cookie-policy.html`.
- **Put your real name or business name in the legal pages** where it currently says
  "the operator of HomeDecorPad" if you register a business — networks and regulators
  expect a real legal entity.
- **Do not publish AI-generated photos as product shots or room photos you claim to have
  taken.** The illustrations on this site are original vector artwork and are described as
  such on the About page. Keep that honest if you add photography later — Pinterest now
  labels AI-modified content, and readers punish it in home decor.

---

## 7. The generator in `_build/` (optional)

The site was generated from Python data files: `theme.py` (design system, SVG art, page
shell), `articles1.py` / `articles2.py` (post content), `build.py` (assembly + the markdown
converter for the legal pages). Rebuild everything with:

```bash
cd homedecorpad
python3 _build/build.py
```

Requirements: Python 3 and Pillow (only for regenerating the share images).
If you do not want to use Python, ignore `_build/` entirely — the site is complete without it.

**Local preview before you upload:**

```bash
cd homedecorpad
python3 -m http.server 8000
# open http://localhost:8000
```

---

## 8. Where the matching Pinterest assets live

The 20 board covers, the 3 profile covers and the board titles/descriptions are in the
sibling folder `home-decor-blog/` (`covers/`, `pinterest-boards.md`, `pinterest-bio.md`).
The pin copy for each post is already written into the bottom of every post page —
open a post and look for "Copy-and-paste pin title & description".

---

© 2026 HomeDecorPad. All rights reserved.
