# Blog posts

Each `.md` file here is one post. The frontmatter at the top of the file holds the
title, date, category, summary, tags and illustration; everything below the second
`---` is the article body in Markdown.

Edited through Pages CMS (forms) or directly on GitHub. After a change, the
**Build site from content** workflow regenerates the HTML automatically — never edit
the `.html` files in `blog/`, they are generated output.

Component blocks available in the body:

    :::callout Title      ... :::
    :::steps              (contains a numbered list) ... :::
    :::shop Title         (contains a | Item | Detail | Price | table) ... :::
    :::ad
    :::note               (small muted paragraph) ... :::

A `## Frequently asked questions` section with `### question` headings becomes an
accordion and gets FAQ markup for Google.

Link to other pages with a leading slash (`/blog.html#small-space`) and to other
posts with `post:` plus the slug (`post:one-room-three-budgets-cozy-bedroom`).

Full guide: see `CMS-GUIDE.md` in the repository root.
