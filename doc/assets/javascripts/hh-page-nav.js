// Previous/Next page footer nav.
//
// Zensical doesn't render Material's own prev/next footer nav (checked the
// built HTML directly - no .md-footer__link markup at all, on any page).
// This rebuilds it from the already-rendered primary sidebar rather than a
// second copy of the page order: that sidebar already lists every real page
// in the same order as mkdocs.yml's nav:, mixed in with the current page's
// own on-page anchors (#heading-slug) - filtering those out by "no # in the
// href" leaves exactly the flat page list, with no separate data source to
// keep in sync.
//
// Runs on document$, not DOMContentLoaded: this theme uses instant loading
// (navigation.instant), which swaps content via history.pushState rather
// than a real page load after the first one - a plain DOMContentLoaded
// listener would only ever fire once and never run again on later
// in-app navigations. document$ is Material's own documented hook for
// exactly this (an RxJS observable that re-fires after every content swap).
document$.subscribe(function () {
  var footerArt = document.querySelector(".hh-footer-art");
  if (!footerArt) return;

  // A previous injection (from before an instant-navigation swap) would
  // otherwise still be sitting in the DOM alongside a freshly-rendered one.
  var stale = document.querySelector(".hh-page-nav");
  if (stale) stale.remove();

  var links = Array.prototype.slice.call(
    document.querySelectorAll(".md-sidebar--primary a.md-nav__link[href]")
  );

  var seen = {};
  var pages = [];
  links.forEach(function (a) {
    var href = a.getAttribute("href") || "";
    if (href.indexOf("#") !== -1) return; // on-page anchor, not a real page
    var path = new URL(href, location.href).pathname;
    if (seen[path]) return;
    seen[path] = true;
    pages.push({ title: a.textContent.trim(), href: a.href, path: path });
  });

  var currentPath = location.pathname;
  var idx = pages.findIndex(function (p) {
    return p.path === currentPath;
  });
  if (idx === -1) return;

  var prev = idx > 0 ? pages[idx - 1] : null;
  var next = idx < pages.length - 1 ? pages[idx + 1] : null;
  if (!prev && !next) return;

  function makeLink(entry, dir, label) {
    var a = document.createElement("a");
    a.href = entry.href;
    a.className = "hh-page-nav__link hh-page-nav__link--" + dir;

    var labelSpan = document.createElement("span");
    labelSpan.className = "hh-page-nav__label";
    labelSpan.textContent = label;

    var titleSpan = document.createElement("span");
    titleSpan.className = "hh-page-nav__title";
    titleSpan.textContent = entry.title;

    a.appendChild(labelSpan);
    a.appendChild(titleSpan);
    return a;
  }

  var nav = document.createElement("nav");
  nav.className = "hh-page-nav";
  nav.appendChild(prev ? makeLink(prev, "prev", "Previous") : document.createElement("span"));
  nav.appendChild(next ? makeLink(next, "next", "Next") : document.createElement("span"));

  footerArt.parentNode.insertBefore(nav, footerArt);
});
