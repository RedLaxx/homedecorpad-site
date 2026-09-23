# HomeDecorPad — deployment & CMS status

_Last updated: 23 September 2026_

## Two live sites — keep one

| Live URL | Repo | State |
|---|---|---|
| **https://redlaxx.github.io/homedecorpad-site/** | `RedLaxx/homedecorpad-site` | ✅ **current** — CMS-managed content, correct canonicals, automatic rebuilds. **Keep this one.** |
| https://redlaxx.github.io/homedecorpad/ | `RedLaxx/homedecorpad` | ⚠️ old build, still live. Canonicals point at the unregistered `homedecorpad.com`, so it competes with your real site for search traffic. |

Both are public and serving the same articles. Google will pick one and ignore the other,
and right now it would pick the broken one. Delete the old repo (next section).

> Note: the old repo was originally named `HomeDecorPad`. It has since been renamed to
> `homedecorpad`, which moved its URL from `/HomeDecorPad/` to `/homedecorpad/`.

---

## How to delete `RedLaxx/homedecorpad`

1. Open <https://github.com/RedLaxx/homedecorpad/settings> (signed in as the owner).
2. Scroll to the very bottom of the page — the red **Danger Zone** panel.
3. Click **Delete this repository**.
4. In the dialog, type the name where prompted: `RedLaxx/homedecorpad`
   (GitHub may only ask for `homedecorpad` — type exactly what it shows).
5. Click **I understand the consequences, delete this repository**.
6. Confirm with your password or 2FA if asked.

Within about a minute, `https://redlaxx.github.io/homedecorpad/` returns 404 and your
CMS site is the only copy online.

### Softer options if you are not ready to delete

| Option | Where | Effect |
|---|---|---|
| Take it offline, keep the files | Repo → Settings → Pages → Source: **None** | URL goes 404, repo stays |
| Freeze it | Repo → Settings → Danger Zone → **Archive this repository** | Read-only, files preserved |
| Do nothing | — | Not advised: two copies of the same content compete in search |

### Want me to do it instead?

The token you provided cannot delete repositories. That needs either:
- a **fine-grained token** with **Administration: Read and write** on `RedLaxx/homedecorpad`, or
- a **classic token** with the `delete_repo` scope.

Generate one, and it is a single API call — I will confirm the URL is gone afterwards.

**Backup:** a full copy of that repo (46 files, including its `.pages.yml` and history
snapshot) is saved at `HomeDecorPad-repo-backup.tar.gz` in the workspace.

---

## Content is managed through Pages CMS

- Posts: `content/posts/*.md` · legal pages: `content/legal/*.md` · settings: `content/site.yml`
- Never edit the `.html` files — they are generated and get overwritten.
- Saves trigger the **Build site from content** workflow, which republishes in ~30 seconds.
- Full instructions: **`CMS-GUIDE.md`**

### What the build guards against now

| Situation | What happens |
|---|---|
| You rename a post (new slug) | Old URL becomes a permanent redirect — no broken Pinterest pins |
| You delete a post | Its page is removed from the site and the sitemap |
| A post links to a page that does not exist | The build **fails** and says which link, so nothing broken is published |
| You delete an uploaded image that a post still uses | Warning only — the image is dropped and the illustration takes its place |
| A post has no title or date | It is skipped with a warning |
| Rebuild runs on a different day | Legal dates do not change (they are settings, not build dates) |

---

## When homedecorpad.com is bought

1. Settings → Pages → Custom domain, plus the `A` records and `www` CNAME in `README.md`.
2. Pages CMS → **Site settings** → set `domain` to `https://homedecorpad.com`, save.
3. Enforce HTTPS, verify the domain in Pinterest, submit the sitemap in Search Console.

## Still outstanding before the AdSense application

- Publish more posts — 8 is the minimum, 15+ is safer.
- Turn on Google's GDPR message in AdSense (free CMP) for EEA traffic.
- Fill in `amazon_tag`, `formspree_id`, `adsense_client`, `ga4_id`, social URLs in
  Pages CMS → Site settings. No ad code loads until `adsense_client` is set.
