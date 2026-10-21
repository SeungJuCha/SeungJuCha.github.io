#!/usr/bin/env python3
"""Build a zero-dependency, accessible academic site from content.json.

Edit content.json to update news, publications, education, or contact details.
Then run: python3 build.py
"""
from __future__ import annotations

import json
import re
from datetime import datetime
from html import escape
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
DATA = json.loads((ROOT / "content.json").read_text(encoding="utf-8"))


def h(value: object) -> str:
    return escape(str(value), quote=True)


def validate_url(url: str) -> str:
    """Only publish links with an explicit HTTPS URL."""
    if not url:
        return ""
    parsed = urlparse(url)
    if parsed.scheme != "https" or not parsed.netloc:
        raise ValueError(f"Expected an HTTPS URL, got: {url!r}")
    return h(url)


def external(url: str, text: str, css_class: str = "") -> str:
    url = validate_url(url)
    if not url:
        return h(text)
    klass = f' class="{h(css_class)}"' if css_class else ""
    return f'<a{klass} href="{url}" target="_blank" rel="noopener noreferrer">{h(text)}</a>'


def authors_html(authors: str) -> str:
    # Keep all authors as originally written in CV; emphasize the site owner.
    name = DATA["name"]
    escaped = h(authors)
    return escaped.replace(h(name), f'<strong>{h(name)}</strong>')


def arrow_icon() -> str:
    return '<svg aria-hidden="true" viewBox="0 0 20 20" fill="none"><path d="M5 15 15 5M6 5h9v9" stroke="currentColor" stroke-width="1.55" stroke-linecap="round" stroke-linejoin="round"/></svg>'


def download_icon() -> str:
    return '<svg aria-hidden="true" viewBox="0 0 20 20" fill="none"><path d="M10 3v10m0 0 4-4m-4 4L6 9M4 15v2h12v-2" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>'


def mail_icon() -> str:
    return '<svg aria-hidden="true" viewBox="0 0 20 20" fill="none"><rect x="2.7" y="4.5" width="14.6" height="11" rx="1.8" stroke="currentColor" stroke-width="1.4"/><path d="m3.5 6 6.5 5.1L16.5 6" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/></svg>'


def news_html() -> str:
    parts = []
    for item in DATA["news"]:
        headline = external(item.get("url", ""), item["headline"], "news-headline") if item.get("url") else f'<span class="news-headline">{h(item["headline"])}</span>'
        parts.append(f'''
        <article class="news-item">
          <time datetime="{h(item['year'])}" class="news-year">{h(item['year'])}</time>
          <span class="news-bullet" aria-hidden="true"></span>
          <div class="news-body">
            <h3>{headline}</h3>
            <p>{h(item['detail'])}</p>
          </div>
        </article>''')
    return "\n".join(parts)


def publications_html() -> str:
    out = []
    pubs = DATA["publications"]
    categories = list(dict.fromkeys(pub["category"] for pub in pubs))
    number = 0
    for cat in categories:
        items = [p for p in pubs if p["category"] == cat]
        out.append(f'''
        <div class="publication-group">
          <div class="group-heading"><h3>{h(cat)}</h3><span>{len(items):02d} publications</span></div>
          <div class="publication-list">''')
        for item in items:
            number += 1
            title = h(item["title"])
            if item.get("url"):
                title = external(item["url"], item["title"], "pub-title-link")
            award = f'<span class="pub-award">{h(item["award"])}</span>' if item.get("award") else ""
            action = f'<a class="pub-link" href="{validate_url(item["url"])}" target="_blank" rel="noopener noreferrer" aria-label="View paper: {h(item["title"])}">Paper {arrow_icon()}</a>' if item.get("url") else ""
            out.append(f'''
            <article class="publication-item">
              <div class="pub-index" aria-hidden="true">{number:02d}<span class="pub-index-line"></span></div>
              <div class="pub-main">
                <h4>{title}</h4>
                <p class="pub-authors">{authors_html(item["authors"])}</p>
                <div class="pub-meta"><span class="pub-venue">{h(item["venue"])}</span>{award}</div>
              </div>
              <div class="pub-action">{action}</div>
            </article>''')
        out.append('  </div>\n</div>')
    return "\n".join(out)


def education_html() -> str:
    parts = []
    for item in DATA["education"]:
        detail = f'<p class="education-detail">{h(item["detail"])}</p>' if item.get("detail") else ""
        parts.append(f'''
        <article class="education-item">
          <p class="education-period">{h(item["period"])}</p>
          <div>
            <h3>{h(item["degree"])}</h3>
            <p class="education-school">{h(item["school"])}</p>
            {detail}
          </div>
        </article>''')
    return "\n".join(parts)


def service_html() -> str:
    return "\n".join(f'<li><span>{h(item["name"])}</span><span class="service-role">{h(item["detail"])}</span></li>' for item in DATA["academic_service"])


def skills_html() -> str:
    return "\n".join(f'<div class="skill-row"><h4>{h(item["name"])}</h4><p>{h(item["items"])}</p></div>' for item in DATA["technical_skills"])


def render() -> str:
    scholar = validate_url(DATA["links"]["scholar"])
    github = validate_url(DATA["links"]["github"])
    linkedin = validate_url(DATA["links"]["linkedin"])
    chips = "\n".join(f'<span class="interest-chip">{h(interest)}</span>' for interest in DATA["research_interests"])
    email_main, email_other = DATA["emails"]
    contact_main = h(email_main)
    contact_other = h(email_other)
    cv_link = "./assets/SeungJu_Cha_CV.pdf"
    current_year = datetime.now().year
    schema = {
        "@context": "https://schema.org",
        "@type": "Person",
        "name": DATA["name"],
        "jobTitle": DATA["role"],
        "affiliation": {"@type": "CollegeOrUniversity", "name": DATA["institution"]},
        "sameAs": [DATA["links"]["scholar"], DATA["links"]["github"], DATA["links"]["linkedin"]]
    }
    schema_json = json.dumps(schema, ensure_ascii=False).replace('<', '\\u003c')
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#f7f9fc">
  <meta name="description" content="SeungJu Cha is a Ph.D. student in Artificial Intelligence at Hanyang University, working on diffusion and flow models, efficient generation, and physics-aware video generation.">
  <meta name="author" content="SeungJu Cha">
  <meta property="og:type" content="profile">
  <meta property="og:title" content="SeungJu Cha | AI Researcher">
  <meta property="og:description" content="Ph.D. Student in Artificial Intelligence at Hanyang University. Research in diffusion, flow models, and long-horizon video generation.">
  <meta property="og:image" content="assets/profile.jpg">
  <meta name="color-scheme" content="light">
  <title>SeungJu Cha | AI Researcher</title>
  <link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="styles.css">
  <script type="application/ld+json">{schema_json}</script>
  <script src="script.js" defer></script>
</head>
<body>
  <a href="#main" class="skip-link">Skip to content</a>
  <header class="site-header">
    <div class="header-inner wrap">
      <a href="#top" class="wordmark" aria-label="SeungJu Cha, home"><span class="wordmark-icon">SC<span>.</span></span><span class="wordmark-name">SeungJu Cha</span></a>
      <nav aria-label="Main navigation" class="nav-links">
        <a href="#news">News</a>
        <a href="#publications">Publications</a>
        <a href="#education">Education</a>
        <a href="#service">Service</a>
        <a class="nav-cv" href="{cv_link}" target="_blank" rel="noopener noreferrer">CV {arrow_icon()}</a>
      </nav>
    </div>
  </header>

  <main id="main">
    <section class="hero wrap" id="top" aria-label="Introduction">
      <div class="hero-content">
        <div class="small-label"><span class="label-rule"></span> HANYANG UNIVERSITY <span class="label-divider">/</span> REPUBLIC OF KOREA</div>
        <h1>SeungJu <span>Cha.</span></h1>
        <p class="hero-subtitle">{h(DATA['role'])}<br><span>{h(DATA['institution'])}</span></p>
        <p class="hero-description">{h(DATA['intro'])}</p>
        <div class="interests" aria-label="Research interests">{chips}</div>
        <div class="hero-contact">
          <div class="email-links">
            <a href="mailto:{contact_main}">{mail_icon()} {contact_main}</a>
            <a href="mailto:{contact_other}">{contact_other}</a>
          </div>
          <div class="social-links" aria-label="Academic and social profiles">
            <a href="{scholar}" target="_blank" rel="noopener noreferrer">Google Scholar {arrow_icon()}</a>
            <a href="{github}" target="_blank" rel="noopener noreferrer">GitHub {arrow_icon()}</a>
            <a href="{linkedin}" target="_blank" rel="noopener noreferrer">LinkedIn {arrow_icon()}</a>
            <a href="{cv_link}" target="_blank" rel="noopener noreferrer">Download CV {download_icon()}</a>
          </div>
        </div>
      </div>
      <div class="hero-portrait">
        <div class="portrait-backdrop"></div>
        <div class="portrait-frame">
          <picture>
            <source srcset="assets/profile.webp" type="image/webp">
            <img src="assets/profile.jpg" alt="Portrait of SeungJu Cha" width="591" height="787" fetchpriority="high">
          </picture>
        </div>
        <p class="portrait-caption"><span class="caption-circle"></span> ARTIFICIAL INTELLIGENCE RESEARCH</p>
      </div>
    </section>

    <div class="wrap"><div class="hero-bottom-rule"><span>RESEARCH • GENERATIVE MODELS • COMPUTER VISION</span><span class="down-indicator">SCROLL TO EXPLORE <span aria-hidden="true">↓</span></span></div></div>

    <section class="section wrap" id="news">
      <div class="section-heading">
        <div><p class="section-kicker">01 <span>—</span> LATEST UPDATES</p><h2>News<span class="heading-period">.</span></h2></div>
        <p class="section-description">Recent research highlights and academic updates.</p>
      </div>
      <div class="news-list">{news_html()}</div>
    </section>

    <section class="section wrap" id="publications">
      <div class="section-heading">
        <div><p class="section-kicker">02 <span>—</span> RESEARCH OUTPUT</p><h2>Publications<span class="heading-period">.</span></h2></div>
        <p class="section-description">Peer-reviewed publications across generative modeling, vision, and video understanding.</p>
      </div>
      {publications_html()}
    </section>

    <section class="section wrap" id="education">
      <div class="section-heading">
        <div><p class="section-kicker">03 <span>—</span> ACADEMIC PATH</p><h2>Education<span class="heading-period">.</span></h2></div>
        <p class="section-description">Academic training and research supervision.</p>
      </div>
      <div class="education-list">{education_html()}</div>
    </section>

    <section class="section wrap last-section" id="service">
      <div class="section-heading">
        <div><p class="section-kicker">04 <span>—</span> ACADEMIC CONTRIBUTIONS</p><h2>Service &amp; Skills<span class="heading-period">.</span></h2></div>
        <p class="section-description">Research community participation and technical expertise.</p>
      </div>
      <div class="service-grid">
        <div class="service-panel"><h3>Academic Service</h3><ul class="service-list">{service_html()}</ul></div>
        <div class="service-panel"><h3>Technical Skills</h3><div class="skill-list">{skills_html()}</div></div>
      </div>
    </section>
  </main>

  <footer class="site-footer">
    <div class="wrap footer-inner"><div><p class="footer-name">SeungJu Cha<span>.</span></p><p>Ph.D. Student · Hanyang University</p></div><div class="footer-right"><a href="mailto:{contact_main}">{contact_main} {arrow_icon()}</a><p>© {current_year} SeungJu Cha</p></div></div>
  </footer>
</body>
</html>
'''


def main() -> None:
    html = render()
    (ROOT / "index.html").write_text(html, encoding="utf-8")
    print(f"Updated index.html ({len(DATA['publications'])} publications, {len(DATA['news'])} news items)")


if __name__ == "__main__":
    main()
