Mathematical Foundations of Quantum Theory group home page (http://www.ime.unicamp.br/~mfq/)

## Image workflow

The site now supports a single preferred workflow for high-resolution photos.

### People pages

Store each person's page as a Hugo page bundle:

```text
mfq/content/english/people/jane-doe/
  index.md
  portrait.jpg
```

Reference the original image from front matter:

```yaml
---
title: "Jane Doe"
images:
  - "portrait.jpg"
summary: Researcher
categories: researcher
draft: false
---
```

The templates will crop and convert the original automatically for the homepage slider, the people page cards, and the single-person page.

### Gallery page

The gallery page is also a bundle. Add the original image file next to `mfq/content/english/gallery/index.md` and reference it in the shortcode:

```md
{{< image "new-event-photo.jpg" alt="MFQ event photo" >}}
```

Gallery images now use the original bundled file directly for maximum quality. The first images on the page are prioritized so the top of the gallery becomes usable sooner, and the gallery styling automatically adds rounded corners.

### Legacy fallbacks

All current people pages now keep their image file inside the page bundle. If you later recover a higher-resolution original for someone, replace the local file in that person's folder and keep the same front matter entry.
