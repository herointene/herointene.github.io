"""Exercise the candidate site without sending analytics or posting comments."""

from __future__ import annotations

import argparse
from contextlib import contextmanager
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
import mimetypes
from pathlib import Path
import re
from threading import Thread
from urllib.parse import unquote, urlparse

from playwright.sync_api import expect, sync_playwright


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_args):
        pass


@contextmanager
def serve(directory: Path):
    server = ThreadingHTTPServer(("127.0.0.1", 0), partial(QuietHandler, directory=str(directory.resolve())))
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}"
    finally:
        server.shutdown()
        server.server_close()
        thread.join()


def isolate(context):
    for pattern in ["**/*googletagmanager.com/**", "**/*google-analytics.com/**"]:
        context.route(pattern, lambda route: route.fulfill(status=200, content_type="application/javascript", body=""))
    # An iframe stub checks asynchronous theme messages; no real comments are sent.
    def comments(route):
        if urlparse(route.request.url).path == "/client.js":
            route.fulfill(status=200, content_type="application/javascript", body="")
        else:
            route.fulfill(status=200, content_type="text/html", body="""<!doctype html><body>
              <script>window.addEventListener('message', e => {
                if (e.data.giscus) document.body.dataset.theme = e.data.giscus.setConfig.theme;
              });</script></body>""")
    context.route("https://giscus.app/**", comments)


def measure(page):
    return page.evaluate("""() => {
      const body = getComputedStyle(document.body);
      const selectors = ['.md-main__inner', '.md-content__inner', '.titlecard', '.tinggif img', '.titlecard p', '.jumbotron'];
      const boxes = Object.fromEntries(selectors.map(selector => {
        const element = document.querySelector(selector);
        const rect = element.getBoundingClientRect();
        const css = getComputedStyle(element);
        return [selector, {x: rect.x, y: rect.y, width: rect.width, height: rect.height,
          margin: css.margin, paddingTop: css.paddingTop, background: css.backgroundImage, color: css.color}];
      }));
      const header = Object.fromEntries(['.md-header__inner', '.md-header__title', '[data-md-component="palette"]', '.md-search']
        .map(selector => {
          const element = document.querySelector(selector);
          const rect = element.getBoundingClientRect();
          return [selector, rect.width || rect.height
            ? {x:rect.x, y:rect.y, width:rect.width, height:rect.height} : null];
        }));
      return {title: document.title, font: body.fontFamily, header,
        colors: Object.fromEntries(['--md-primary-fg-color', '--md-primary-bg-color', '--md-accent-fg-color',
          '--md-typeset-a-color', '--md-footer-bg-color', '--md-footer-bg-color--dark'].map(key => [key, body.getPropertyValue(key).trim()])),
        boxes};
    }""")


def compare_home(browser, base, output, label):
    results = {}
    for device, viewport in [("desktop", {"width": 1440, "height": 900}), ("mobile", {"width": 390, "height": 844})]:
        context = browser.new_context(viewport=viewport, color_scheme="light")
        isolate(context)
        page = context.new_page()
        errors = []
        page.on("pageerror", lambda error: errors.append(str(error)))
        page.goto(base, wait_until="networkidle")
        page.evaluate("document.fonts.ready")
        page.wait_for_timeout(600)  # Finish header transitions before taking evidence screenshots.
        assert page.locator(".tinggif img").evaluate("img => img.complete && img.naturalWidth > 0"), "Homepage animation missing"
        for scheme in ["light", "dark"]:
            if scheme == "dark":
                page.locator('label[for="__palette_1"]').click()
                expect(page.locator("body")).to_have_attribute("data-md-color-scheme", "slate")
            results[f"{device}-{scheme}"] = measure(page)
            page.screenshot(path=str(output / f"{label}-home-{device}-{scheme}.png"), full_page=True)
        assert not errors, errors
        context.close()
    return results


def exercise(browser, base, output):
    context = browser.new_context(viewport={"width": 1440, "height": 900}, color_scheme="light")
    isolate(context)
    page = context.new_page()
    errors = []
    tracking_requests = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    page.on("request", lambda request: tracking_requests.append(request.url)
            if "googletagmanager.com" in request.url or "google-analytics.com" in request.url else None)
    page.goto(base, wait_until="networkidle")
    assert page.locator('form[name="feedback"]').count() == 0, "Feedback changed homepage layout"
    assert not tracking_requests, "Local preview attempted production tracking"
    page.locator(".md-search__button").click()
    query = page.get_by_role("combobox", name="Search")
    expect(query).to_be_visible()
    for term, expected_text in [("宇宙飛船", "宇宙飛船在航行中"), ("緊急想念", "緊急想念"), ("椿象", "2025年終總結")]:
        query.fill(term)
        expect(page.get_by_role("dialog").last).to_contain_text(expected_text)
        page.wait_for_function("term => window.dataLayer.filter(e => e[0] === 'event' && e[1] === 'search' && e[2].search_term === term).length === 1", arg=term)
    page.screenshot(path=str(output / "candidate-search-chinese.png"))
    # Repeated input and a cleared partial query must not duplicate/search empty text.
    query.evaluate("input => input.dispatchEvent(new Event('input', {bubbles:true, composed:true}))")
    page.wait_for_timeout(850)
    assert page.evaluate("window.dataLayer.filter(e => e[0] === 'event' && e[1] === 'search').length") == 3
    query.fill("a cancelled query")
    query.fill("")
    page.wait_for_timeout(850)
    assert page.evaluate("window.dataLayer.filter(e => e[0] === 'event' && e[1] === 'search').length") == 3
    dialog = page.get_by_role("dialog").last
    sharing = dialog.get_by_role("button", name=re.compile("sharing"))
    sharing.click()
    expect(sharing).to_have_attribute("aria-pressed", "true")
    query.fill("宇宙飛船")
    expect(dialog).to_contain_text("2021:米綫與時空飛船")
    expect(dialog.locator('a[href*="poems/ch5/spaceship/"]')).to_have_count(0)
    page.screenshot(path=str(output / "candidate-search-tag-filter.png"))
    sharing.click()
    expect(sharing).to_have_attribute("aria-pressed", "false")
    expect(dialog).to_contain_text("宇宙飛船在航行中")
    query.fill("乙貓")
    # Fuzzy search may match the public cat-alpha story; the draft URL must never appear.
    expect(page.get_by_role("dialog").last).to_contain_text("result")
    expect(page.get_by_role("dialog").last.locator('a[href*="cat-beta"]')).to_have_count(0)
    query.press("Escape")

    page.goto(base + "/tech/vue-delivermethods/", wait_until="networkidle")
    # Zensical renders each SVG in a closed shadow root.
    expect(page.locator("div.mermaid")).to_have_count(2, timeout=30000)
    expect(page.locator("div.mermaid").first).to_be_visible()
    page.locator("div.mermaid").first.scroll_into_view_if_needed()
    page.evaluate("document.fonts.ready")
    page.screenshot(path=str(output / "candidate-mermaid.png"), full_page=True)
    tabs = page.locator(".tabbed-labels label")
    assert tabs.count() >= 2, "Code tabs missing"
    tabs.nth(1).click()
    assert page.locator('.tabbed-set > input:checked').count() > 0, "Code tab selection failed"

    page.goto(base + "/about/", wait_until="networkidle")
    assert page.locator(".giscus-frame").count() == 0
    page.locator('label[for="__palette_1"]').click()
    expect(page.locator('script[src="https://giscus.app/client.js"]')).to_have_attribute("data-theme", "transparent_dark")
    page.reload(wait_until="networkidle")
    expect(page.locator('script[src="https://giscus.app/client.js"]')).to_have_attribute("data-theme", "transparent_dark")
    page.evaluate("""() => {
      const frame = document.createElement('iframe');
      frame.className = 'giscus-frame';
      frame.src = 'https://giscus.app/migration-theme-check';
      document.querySelector('.giscus').appendChild(frame);
    }""")
    frame_body = page.frame_locator(".giscus-frame").locator("body")
    expect(frame_body).to_have_attribute("data-theme", "transparent_dark")
    page.locator('label[for="__palette_0"]').click()
    expect(frame_body).to_have_attribute("data-theme", "light")
    assert page.locator(".md-main__inner").evaluate("el => getComputedStyle(el).maxWidth") != "none", "Homepage styles leaked"
    feedback = page.locator('form[name="feedback"]')
    expect(feedback).to_be_visible()
    feedback.locator('[data-md-value="1"][type="submit"]').click()
    expect(feedback.locator('.md-feedback__note [data-md-value="1"]')).to_be_visible()
    expect(feedback.locator('[type="submit"]').first).to_be_disabled()
    events = page.evaluate("window.dataLayer.filter(e => e[0] === 'event' && e[1] === 'feedback').map(e => Array.from(e))")
    assert len(events) == 1 and events[0][2]["data"] == "1", "Feedback not recorded exactly once"
    assert page.evaluate("window.dataLayer.filter(e => e[0] === 'config').length") == 1, "GA initialized multiple times"
    page.screenshot(path=str(output / "candidate-about-feedback.png"), full_page=True)
    assert not tracking_requests, "Preview sent production analytics"
    assert not errors, errors
    context.close()
    return {"chinese_searches": 3, "draft_search_results": 0, "search_deduplication": True,
            "search_tag_filter": True, "mermaid": True, "code_tabs": True, "feedback_events": 1,
            "giscus_delayed_iframe_theme_sync": True, "preview_tracking_requests": 0, "page_errors": errors}


def exercise_mobile(browser, base, output):
    context = browser.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True)
    isolate(context)
    page = context.new_page()
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    page.goto(base + "/talk/2025-conclusion/", wait_until="networkidle")
    assert page.evaluate("document.documentElement.scrollWidth <= innerWidth"), "Article overflows mobile viewport"
    page.locator('.md-header__button[for="__search"]').click()
    query = page.get_by_role("combobox", name="Search")
    query.fill("椿象")
    expect(page.get_by_role("dialog").last).to_contain_text("2025年終總結")
    page.screenshot(path=str(output / "candidate-mobile-search.png"))
    query.press("Escape")
    page.locator('.md-header__button[for="__drawer"]').click()
    back = page.locator(".md-sidebar--primary label.md-nav__title")
    back.filter(has_text="年度總結").click()
    back.filter(has_text="mini Ted Talk").click()
    page.locator('.md-sidebar--primary a[href$="about/"]').click()
    page.wait_for_url("**/about/")
    assert not errors, errors
    context.close()
    return {"article_horizontal_overflow": False, "chinese_search": True, "navigation_to_about": True, "page_errors": errors}


def production_tracking(browser, site):
    """Render local files at the production origin and intercept every tracker."""
    context = browser.new_context()
    isolate(context)
    requests = []
    def local_page(route):
        relative = unquote(urlparse(route.request.url).path).lstrip("/")
        path = (site / relative).resolve()
        assert path.is_relative_to(site.resolve())
        if path.is_dir():
            path /= "index.html"
        if path.is_file():
            route.fulfill(path=str(path), content_type=mimetypes.guess_type(path.name)[0] or "application/octet-stream")
        else:
            route.fulfill(status=404, body="Not found")
    context.route("https://blog.wulited.com/**", local_page)
    context.on("request", lambda request: requests.append(request.url) if "googletagmanager.com" in request.url else None)
    page = context.new_page()
    for pathname in ["/", "/talk/2025-conclusion/"]:
        requests.clear()
        page.goto("https://blog.wulited.com" + pathname, wait_until="networkidle")
        assert sum("/gtag/js?id=G-NSSC5W311R" in url for url in requests) == 1
        assert sum("/gtm.js?id=GTM-PPTZT5H" in url for url in requests) == 1
        assert page.evaluate("window.dataLayer.filter(e => e[0] === 'config' && e[1] === 'G-NSSC5W311R').length") == 1
    context.close()
    return {"ga_initializations_per_document": 1, "gtm_loads_per_document": 1, "actual_tracking_blocked": True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site-dir", type=Path, default=Path("site"))
    parser.add_argument("--baseline", type=Path)
    parser.add_argument("--output", type=Path, default=Path("test-results/browser"))
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        try:
            with serve(args.site_dir) as base:
                report = {"homepage": compare_home(browser, base, args.output, "candidate"),
                          "interactions": exercise(browser, base, args.output),
                          "mobile": exercise_mobile(browser, base, args.output),
                          "production_tracking": production_tracking(browser, args.site_dir)}
            if args.baseline:
                with serve(args.baseline) as baseline_base:
                    original = compare_home(browser, baseline_base, args.output, "baseline")
                (args.output / "home-comparison.json").write_text(json.dumps(
                    {"candidate": report["homepage"], "baseline": original}, ensure_ascii=False, indent=2) + "\n")
                assert report["homepage"] == original, "Homepage layout, font or palette changed; inspect screenshots"
                report["homepage_matches_baseline"] = True
            (args.output / "checks.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
            print(json.dumps({key: value for key, value in report.items() if key != "homepage"}, ensure_ascii=False))
        finally:
            browser.close()


if __name__ == "__main__":
    main()
