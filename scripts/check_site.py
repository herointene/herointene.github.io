"""Check published pages, URLs, draft exclusion and assets after a clean build."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from urllib.parse import urljoin
import xml.etree.ElementTree as ET

from bs4 import BeautifulSoup


DRAFT = Path("talk/cat-beta.md")


def page_path(source: Path) -> Path:
    if source.name == "index.md":
        return source.with_suffix(".html")
    return source.with_suffix("") / "index.html"


def page_url(source: Path) -> str:
    if source.name == "index.md":
        parent = source.parent.as_posix()
        return "" if parent == "." else parent + "/"
    return source.with_suffix("").as_posix() + "/"


def parse(path: Path) -> BeautifulSoup:
    return BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")


def article_text(soup: BeautifulSoup) -> str:
    article = soup.select_one("article.md-content__inner")
    assert article is not None, "Article missing"
    for element in article.select("script, style, svg, .md-tags, .md-feedback, .giscus, #__comments"):
        element.decompose()
    text = article.get_text(" ", strip=True)
    # Restored icons replace these two literal names in the original build.
    for icon in [":simple-css3:", ":simple-tableau:"]:
        text = text.replace(icon, "")
    return " ".join(text.split())


def check(site: Path, docs: Path, baseline: Path | None = None) -> dict:
    domain = (docs / "CNAME").read_text().strip()
    site_url = f"https://{domain}/"
    sources = sorted(path.relative_to(docs) for path in docs.rglob("*.md")
                     if not any(part.startswith(".") for part in path.relative_to(docs).parts)
                     and path.relative_to(docs) != DRAFT)
    expected_urls = {urljoin(site_url, page_url(source)) for source in sources}
    assert (site / "CNAME").read_bytes() == (docs / "CNAME").read_bytes(), "CNAME changed"
    sitemap = ET.parse(site / "sitemap.xml")
    actual_urls = {node.text for node in sitemap.findall(".//{*}loc")}
    assert actual_urls == expected_urls, f"Sitemap mismatch: {actual_urls ^ expected_urls}"

    compared = 0
    tags_checked = 0
    for source in sources:
        path = page_path(source)
        soup = parse(site / path)
        canonical = soup.select_one('link[rel="canonical"]')
        assert canonical and canonical["href"] == urljoin(site_url, page_url(source)), f"Canonical changed: {source}"
        if baseline:
            old = parse(baseline / path)
            selector = "article h1[id], article h2[id], article h3[id], article h4[id], article h5[id], article h6[id]"
            anchors = lambda document: [(node.name, node["id"]) for node in document.select(selector)]
            assert anchors(soup) == anchors(old), f"Heading anchors changed: {source}"
            tags = lambda document: [node.get_text(strip=True) for node in document.select(".md-tags .md-tag")]
            assert tags(soup) == tags(old), f"Tags changed: {source}"
            if tags(soup):
                article = soup.select_one("article.md-content__inner")
                elements = article.find_all(True)
                assert elements.index(soup.select_one(".md-tags")) < elements.index(article.find("h1")), f"Tags no longer above article: {source}"
                tags_checked += 1
            assert article_text(soup) == article_text(old), f"Article text changed: {source}"
            compared += 1

    assets = 0
    for asset in docs.rglob("*"):
        relative = asset.relative_to(docs)
        if asset.is_file() and asset.suffix != ".md" and not any(part.startswith(".") for part in relative.parts):
            assert (site / relative).read_bytes() == asset.read_bytes(), f"Asset changed or missing: {relative}"
            assets += 1

    # Check the complete tree, including search indexes and copied source files.
    for generated in site.rglob("*"):
        if not generated.is_file():
            continue
        relative = generated.relative_to(site).as_posix()
        assert "cat-beta" not in relative, f"Draft published: {relative}"
        if generated.suffix in {".html", ".json", ".xml", ".txt", ".md"}:
            assert b"cat-beta" not in generated.read_bytes(), f"Draft reference leaked: {relative}"
    index = json.loads((site / "search.json").read_text()) if (site / "search.json").exists() else json.loads((site / "search/search_index.json").read_text())
    locations = {item["location"].split("#")[0] for item in index.get("items", index.get("docs", []))}
    assert {page_url(source) for source in sources} <= locations, "Public pages missing from search"
    assert "talk/cat-beta/" not in locations, "Draft in search"
    assert parse(site / "index.html").title.get_text() == "艇仔粥 TingZaiZuk", "Homepage title changed"

    return {"public_pages": len(sources), "sitemap_urls": len(actual_urls), "assets": assets,
            "baseline_pages_compared": compared, "tag_pages_compared": tags_checked,
            "draft_published": False,
            "homepage_animation_sha256": hashlib.sha256((site / "assets/tinggif.gif").read_bytes()).hexdigest()}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site-dir", type=Path, default=Path("site"))
    parser.add_argument("--docs-dir", type=Path, default=Path("docs"))
    parser.add_argument("--baseline", type=Path)
    parser.add_argument("--report", type=Path, default=Path("test-results/site-checks.json"))
    args = parser.parse_args()
    report = check(args.site_dir, args.docs_dir, args.baseline)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(report, ensure_ascii=False))


if __name__ == "__main__":
    main()
