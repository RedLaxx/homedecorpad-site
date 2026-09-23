# HomeDecorPad — deployment & CMS status

_Last updated: 23 September 2026_

## Two live copies right now — keep one

| URL | Repo | Status |
|---|---|---|
| `https://redlaxx.github.io/homedecorpad-site/` | `RedLaxx/homedecorpad-site` | ✅ live, **current build** — correct canonicals, `.nojekyll`, Pages CMS config, all content in Markdown. **Use this one.** |
| `https://redlaxx.github.io/HomeDecorPad/` | `RedLaxx/HomeDecorPad` | ✅ live but **out of date** — older build, canonicals still point at the unregistered `homedecorpad.com`, no CMS config. |

Two live copies of the same site make Google pick one and ignore the other. Once you are
happy with `homedecorpad-site`, delete the other repo (Settings → scroll to the bottom →
Delete this repository).

## Content is now managed through Pages CMS

- Posts live in `content/posts/*.md` — Markdown with frontmatter, not HTML.
- `content/site.yml` holds brand, domain, email, Amazon tag, AdSense ID, GA4 ID,
  Pinterest code and social links.
- `_build/build.py` regenerates every HTML page from those files.
- Guide: **`CMS-GUIDE.md`**

**The one manual step remaining:** the rebuild-on-save workflow.

Copy `_build/workflow-build.yml` to `.github/workflows/build.yml` in the repo
(Add file → Create new file → paste → commit). GitHub refuses to let a personal access
token create workflow files without the `workflow` scope, so this cannot be pushed for you.

Without it, Pages CMS saves your edits to `content/` but the live HTML only updates when
the build runs. With it, publishing is automatic about 30 seconds after you hit Save.

## When homedecorpad.com is bought

1. Add the domain in **Settings → Pages → Custom domain**, plus the four `A` records and a
   `www` CNAME (table in `README.md`).
2. In Pages CMS → **Site settings**, set `domain` to `https://homedecorpad.com`, save.
3. Enforce HTTPS, then verify the domain in Pinterest and submit the sitemap in Search Console.

## Still outstanding before the AdSense application

- Add the workflow file (above), then publish 5–10 more posts — 8 is the minimum, 15+ is safer.
- Turn on Google's own GDPR message in AdSense (free CMP) for EEA traffic.
- Fill in `amazon_tag`, `formspree_id`, `adsense_client`, `ga4_id` and the social URLs in
  Pages CMS → Site settings. Until `adsense_client` is set, no ad code loads at all.
