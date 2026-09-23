# Connecting Pages CMS to HomeDecorPad

Pages CMS (<https://pagescms.org>) gives you a proper editing interface for this site:
log in with GitHub, get forms for every post field, a Markdown editor for the article body,
an image uploader, and a Site settings page — all committing to your repository.

**The catch, and how this site handles it:** Pages CMS edits *content files*, not finished
HTML. So the 8 posts now live as Markdown in `content/posts/`, and a GitHub Action rebuilds
the HTML automatically after every save. You never touch HTML again.

```
content/posts/*.md  ──save from Pages CMS──▶  GitHub Action runs _build/build.py  ──▶  HTML committed  ──▶  GitHub Pages publishes
```

---

## 1. Connect it (once, ~3 minutes)

1. Go to **<https://app.pagescms.org>** and click **Sign in with GitHub**.
2. Approve the **Pages CMS** GitHub App when prompted. Choose **Only select repositories**
   and pick your site repository (e.g. `homedecorpad-site` — see section 6 about which repo).
3. Pages CMS reads `.pages.yml` from the repository root. You should land on a sidebar with
   **Blog posts** and **Site settings**. That's it — it is connected.
4. If it shows an error, the branch it opens must be the one containing `.pages.yml`
   (select `main` in the branch switcher at the top of the dashboard).

## 2. Install the rebuild workflow (once)

Without this step your edits save to GitHub but the site keeps showing the old HTML.

1. In GitHub, open your repository → **Add file → Create new file**.
2. Name it exactly: `.github/workflows/build.yml`
3. Paste the contents of `_build/workflow-build.yml` (it's in this repo so you can open it
   and copy) and click **Commit changes**.
4. Go to the **Actions** tab. You should see a workflow called *Build site from content*.
   Run it once with **Run workflow** to confirm it goes green.

> Why manual? GitHub refuses to let a personal access token create workflow files unless it
> has the `workflow` scope. If you regenerate your token with that box ticked, this file can
> be pushed for you instead.

## 3. Everyday publishing

1. **Pages CMS → Blog posts → Add entry.**
2. Fill in the fields (see the reference below) and write the body in Markdown.
3. Leave **Draft** ticked while you work. Untick it to publish.
4. **Save.** Pages CMS commits the Markdown file.
5. The Action rebuilds the site — usually under a minute. **Actions** tab shows progress;
   green means live.

## 4. Writing a post

| Field | What it does |
|---|---|
| **SEO title** | Headline, browser tab and Google title. Keyword first, under 60 characters. |
| **URL slug** | The address: `homedecorpad.com/blog/living-room/small-entryway-ideas.html`. Lowercase-with-hyphens. Pages CMS fills this in from the title on first save. **If you change it later, the build writes a redirect at the old address automatically** — nothing 404s. |
| **Headline** | Only if the on-page headline should differ from the SEO title. |
| **Publish date** | Sorts the site. Future dates are fine — the post appears with that date. |
| **Category** | Sets the URL folder, the card artwork and the section on the Decor Ideas page. |
| **Summary** | One or two sentences used on cards, in Google results and in the pin description. |
| **Intro paragraph** | The lede under the headline. |
| **Tags** | Keywords. Also used to build the Pinterest pin description. |
| **Illustration** | The drawn cover artwork. |
| **Hero photo** | Optional upload that replaces the illustration. Your own photos do best. |
| **Related posts** | Slugs of other posts for the "Keep reading" row. |
| **Draft** | Hide or publish. |
| **Article body** | The post itself, in Markdown. |

### Body syntax

Normal Markdown: `## Heading`, `### Sub-heading`, `**bold**`, `- bullets`, `1. numbers`,
`[link text](/blog.html#color)`.

Links: start with `/` for any page on the site (`/shop-my-home.html`,
`/blog.html#small-space`) — the builder rewrites them correctly for every page depth.
To link another post, use `post:` and its slug: `[the bedroom guide](post:one-room-three-budgets-cozy-bedroom)`.

Four component blocks, each starting and ending on its own line:

```
:::callout The $0 move most people skip
Clear the surfaces before you buy anything. Editing is free.
:::

:::steps
1. **Buy the anchor first.** The rug sets the palette.
2. **Buy textiles second.** Throws and covers change a room fastest.
:::

:::shop Shop the bedroom look
*Affiliate links — see our [disclosure](/affiliate-disclosure.html).*
| Item | Detail | Price |
| --- | --- | --- |
| Washed cotton duvet cover | Oat or warm white | $45-70 |
| Boucle lumbar pillow | 14x24 in | $18-28 |
:::

:::ad
```

FAQ accordions (these also generate the FAQ markup Google can show in search results):

```
## Frequently asked questions

### Do I need to repaint?

No — but if you are repainting anyway, choose a warm off-white.
```

One ad slot is inserted automatically in every post (above the FAQ, or after the third
section). Add `:::ad` if you want a second one.

## 5. Images

Upload through any **Hero photo** field or the media browser. Files land in
`assets/uploads/` and are served from `/assets/uploads/...`.

Keep uploads under ~300 KB (compress at tinypng.com), width 1200–1600 px, JPG or WebP.
For Pinterest pins, use 2:3 — images made from the same file get the whole frame.

## 6. Site settings (the page you'll use most)

**Pages CMS → Site settings** edits `content/site.yml`. This is where you turn things on:

| Setting | What happens when you fill it in |
|---|---|
| `domain` | Canonical tags, Open Graph URLs, sitemap and robots.txt. Change this the day you connect `homedecorpad.com`, then rebuild. |
| `email` | Footer and legal pages. |
| `amazon_tag` | Your affiliate tag is applied to every Amazon search link on the Shop page. |
| `formspree_id` | Wakes up the contact form. |
| `adsense_client` | `ca-pub-…` — turns the AdSense script on site-wide. Leave empty and no ad code loads. |
| `ga4_id` | `G-…` — turns on Google Analytics 4. |
| `pinterest_verify` | Adds the Pinterest domain-verification meta tag. |
| `social` | Footer icons. Remove a URL to hide that icon. |

After changing settings, rebuild (Actions → *Build site from content* → Run workflow), or
just save any post to trigger it.

## 7. Which repository?

The site currently exists in two:

- **`HomeDecorPad`** — the repo that is live at `https://redlaxx.github.io/HomeDecorPad/`.
  Your token could not write to it, so it still has the older build (canonicals pointing at
  the unregistered domain) and no `.pages.yml`.
- **`homedecorpad-site`** — has the current build with all of the above, but Pages is still
  switched off.

Pick one. The simplest path: **Settings → Pages → Deploy from a branch → `main` / (root)**
on `homedecorpad-site`, connect Pages CMS to that repo, then delete the other one so Google
doesn't see two copies of the site.

## 8. What the build does for you

- **Redirects on rename.** Change a post's slug and the old URL becomes a redirect stub
  pointing at the new one, instead of leaving a duplicate page behind.
- **Duplicate cleanup.** Any blog page that is no longer generated is removed, so deleting
  or renaming posts cannot leave orphans on the site.
- **Broken-link check.** If a post links to a page that does not exist, the build fails and
  the run goes red in the Actions tab instead of publishing a 404.
- **Sanity check on frontmatter.** A post with no title or date is skipped with a warning
  rather than being published half-built.
- **Legal dates are settings**, not build dates — rebuilds cannot quietly change the
  effective date on your policy pages.

## 9. If something breaks

- **Edits saved but the site is unchanged** → open the **Actions** tab and read the log for
  the *Build site from content* run. A red run means the build stopped deliberately (most
  often a broken link in the post you just edited).
- **A post has two URLs** → it should not happen; the build retires pages it no longer
  generates. If you see it, check the newest build ran after your edit.
- **The Action fails with a category error** → the Category field has a value that isn't in
  the list. Re-pick it in Pages CMS.
- **A post vanished** → check the Draft toggle.
- **Never edit the `.html` files by hand.** They are generated; the next rebuild overwrites
  them. Edit `content/` instead.
- **Prices, links, text** → all editable from the CMS. Nothing needs a developer.
