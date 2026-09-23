# HomeDecorPad — deployment & CMS status

_Last updated: 23 September 2026_

## Two live copies right now — keep one

| URL | Repo | Status |
|---|---|---|
| `https://redlaxx.github.io/homedecorpad-site/` | `RedLaxx/homedecorpad-site` | ✅ live, **current build** — correct canonicals, `.nojekyll`, Pages CMS config, all content in Markdown. **Use this one.** |
| `https://redlaxx.github.io/HomeDecorPad/` | `RedLaxx/HomeDecorPad` | ✅ live but **out of date** — older build, canonicals still point at the unregistered `homedecorpad.com`, no CMS config. |

Two live copies of the same site make Google pick one and ignore the other. Once you are
happy with `homedecorpad-site`, delete the other repo:

### How to delete `RedLaxx/HomeDecorPad`

1. Open <https://github.com/RedLaxx/HomeDecorPad/settings> (you must be signed in as the owner).
2. Scroll to the very bottom of the page to the red **Danger Zone** panel.
3. Click **Delete this repository**.
4. A dialog opens. Type the full name exactly as shown — `RedLaxx/HomeDecorPad` — then click
   **I understand the consequences, delete this repository**.
5. Confirm with your password or 2FA prompt if GitHub asks.
6. Done. The repo disappears from your profile and
   `https://redlaxx.github.io/HomeDecorPad/` starts returning 404 within a minute.

**Before you delete, know what you are removing:** that repo is the older build (canonicals
still pointed at the unregistered domain, no CMS configuration). Nothing links to its URL —
neither the new site nor Pinterest — so nothing breaks. A full copy is saved at
`HomeDecorPad-repo-backup.tar.gz` (46 files) in the workspace if you ever want to look back.

**Softer alternatives if you are not ready to delete:**

| Instead of deleting | How | Effect |
|---|---|---|
| Take the site offline only | Repo → Settings → Pages → Source: **None** | URL goes 404, files stay on GitHub |
| Freeze it read-only | Repo → Settings → Danger Zone → **Archive this repository** | Nobody can push, url archived, files preserved |
| Leave it | — | Not recommended: Google sees two copies of the same content |

**After deleting, one small tidy-up:** the repository disappears from Pages CMS on its own.
Make sure the Pages CMS GitHub App still has access to `homedecorpad-site`
(<https://github.com/settings/installations> → Pages CMS → Configure → Repository access).

**If you would rather I do it for you:** the current fine-grained token cannot delete
repositories (that needs **Administration: Read and write** on that repo, or a classic token
with the `delete_repo` scope). Generate one with that permission and I will remove it and
verify the URL is gone.

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
