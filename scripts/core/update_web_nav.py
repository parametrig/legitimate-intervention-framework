from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class NavItem:
    label: str
    href: str
    active: bool = False


@dataclass(frozen=True)
class ResearchMenuItem:
    label: str
    href: str
    active: bool = False


RESEARCH_MENU = (
    ("All charts", "research/all/"),
    ("Threat", "research/threat/"),
    ("Intervention", "research/intervention/"),
    ("Efficiency", "research/efficiency/"),
    ("Framework", "research/framework/"),
)


def _html_attrs(attrs: dict[str, str]) -> str:
    if not attrs:
        return ""
    return " " + " ".join(f"{k}=\"{v}\"" for k, v in attrs.items())


def _render_link(item: NavItem) -> str:
    attrs = {}
    if item.active:
        attrs["class"] = "active"
    return f"<a href=\"{item.href}\"{_html_attrs(attrs)}>{item.label}</a>"


def _render_research_dropdown(root_prefix: str, active_subpath: str) -> str:
    research_href = f"{root_prefix}research/"

    menu_links: list[str] = []
    for label, subpath in RESEARCH_MENU:
        href = f"{root_prefix}{subpath}"
        is_active = active_subpath == subpath
        attrs = " class=\"active\"" if is_active else ""
        menu_links.append(f"<a href=\"{href}\"{attrs}>{label}</a>")

    research_active = active_subpath.startswith("research/")
    research_attrs = " class=\"active\"" if research_active else ""

    return (
        "<div class=\"nav-dropdown\">"
        f"<a href=\"{research_href}\"{research_attrs}>Research</a>"
        "<div class=\"nav-dropdown-menu\">"
        + "".join(menu_links)
        + "</div></div>"
    )


def build_nav_html(root_prefix: str, active_page: str, active_research_subpath: str | None = None) -> str:
    items: list[str] = []

    if active_page != "home":
        home_href = "./" if root_prefix == "" else f"{root_prefix}"
        items.append(_render_link(NavItem("Legitimate Overrides", home_href)))

    items.append(_render_link(NavItem("Summary", f"{root_prefix}summary/", active=active_page == "summary")))

    if active_research_subpath is None:
        active_research_subpath = "research/" if active_page == "research" else ""
    items.append(_render_research_dropdown(root_prefix, active_research_subpath))

    items.append(_render_link(NavItem("Database", f"{root_prefix}database.html", active=active_page == "database")))
    items.append(_render_link(NavItem("About", f"{root_prefix}about.html", active=active_page == "about")))

    return "<nav class=\"nav-links\">" + "".join(items) + "</nav>"


def replace_nav_in_html(html: str, new_nav_html: str) -> str:
    end_token = "</nav>"

    # Be resilient to formatting/minification differences.
    nav_class_token = 'class="nav-links"'
    class_pos = html.find(nav_class_token)
    if class_pos == -1:
        return html

    start = html.rfind("<nav", 0, class_pos)
    if start == -1:
        return html

    end = html.find(end_token, class_pos)
    if end == -1:
        return html

    end += len(end_token)
    return html[:start] + new_nav_html + html[end:]


def iter_html_pages(web_dir: Path) -> Iterable[Path]:
    for path in web_dir.rglob("*.html"):
        if path.name.startswith("."):
            continue
        yield path


def detect_page_context(path: Path) -> tuple[str, str, str | None]:
    rel = path.as_posix()

    if rel.endswith("/web/index.html"):
        return ("", "home", None)

    if rel.endswith("/web/about.html"):
        return ("", "about", None)

    if rel.endswith("/web/database.html"):
        return ("", "database", None)

    if rel.endswith("/web/summary/index.html"):
        return ("../", "summary", None)

    if rel.endswith("/web/research/index.html"):
        return ("../", "research", "research/")

    if rel.endswith("/web/research/all/index.html"):
        return ("../../", "research", "research/all/")

    if "/web/research/" in rel and rel.endswith("/index.html"):
        # theme pages: /web/research/<theme>/index.html
        parts = rel.split("/web/research/")[1].split("/")
        if parts and parts[0] and parts[0] != "index.html":
            theme = parts[0]
            return ("../../", "research", f"research/{theme}/")

    # default: treat as top-level web page
    return ("", "home", None)


def main() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    web_dir = repo_root / "web"

    updated = 0

    for page in iter_html_pages(web_dir):
        root_prefix, active_page, active_research_subpath = detect_page_context(page)

        html = page.read_text(encoding="utf-8")
        new_nav = build_nav_html(root_prefix, active_page, active_research_subpath)
        new_html = replace_nav_in_html(html, new_nav)

        if new_html != html:
            page.write_text(new_html, encoding="utf-8")
            updated += 1

    print(f"Updated navbar in {updated} page(s).")


if __name__ == "__main__":
    main()
