(() => {
  "use strict";

  const analytics = document.getElementById("__analytics");
  const track = (event, values) => {
    if (analytics && typeof window.gtag === "function") {
      window.gtag("event", event, { ...values, send_to: analytics.dataset.property });
    }
  };

  // Zensical's search dialog is created after the page loads.
  let searchTimer;
  let lastSearch = "";
  let pendingSearch = "";
  const searchInput = (event) => event.composedPath().find((node) =>
    node instanceof HTMLInputElement &&
    node.matches('input[type="search"], input[role="combobox"][aria-autocomplete="list"]') &&
    node.closest('[data-md-component="search"], [role="dialog"], dialog'));
  const reportSearch = () => {
    clearTimeout(searchTimer);
    if (pendingSearch && pendingSearch !== lastSearch) {
      track("search", { search_term: pendingSearch });
      lastSearch = pendingSearch;
    }
  };
  document.addEventListener("input", (event) => {
    const input = searchInput(event);
    if (!input) return;

    clearTimeout(searchTimer);
    pendingSearch = input.value.trim();
    if (!pendingSearch) {
      lastSearch = "";
      return;
    }
    searchTimer = setTimeout(reportSearch, 750);
  }, true);
  document.addEventListener("focusout", (event) => {
    if (searchInput(event)) reportSearch();
  }, true);
  document.addEventListener("keydown", (event) => {
    if (event.key === "Enter" && searchInput(event)) reportSearch();
  }, true);
  window.addEventListener("pagehide", reportSearch);

  const feedback = document.forms.feedback;
  if (feedback) {
    feedback.hidden = false;
    feedback.addEventListener("submit", (event) => {
      event.preventDefault();
      if (!event.submitter || feedback.firstElementChild.disabled) return;
      const rating = event.submitter.dataset.mdValue;
      track("feedback", { page: location.pathname, data: rating });
      feedback.firstElementChild.disabled = true;
      for (const note of feedback.querySelectorAll(".md-feedback__note [data-md-value]")) {
        note.hidden = note.dataset.mdValue !== rating;
      }
    });
  }

  const syncComments = () => {
    const theme = document.body.dataset.mdColorScheme === "slate" ? "transparent_dark" : "light";
    const script = document.querySelector('script[src="https://giscus.app/client.js"]');
    if (script) script.dataset.theme = theme;
    const frame = document.querySelector(".giscus-frame");
    if (frame && frame.contentWindow) {
      frame.contentWindow.postMessage({ giscus: { setConfig: { theme } } }, "https://giscus.app");
    }
  };

  syncComments();
  new MutationObserver(syncComments).observe(document.body, {
    attributes: true, attributeFilter: ["data-md-color-scheme"]
  });
  const comments = document.querySelector(".giscus");
  if (comments) {
    new MutationObserver(syncComments).observe(comments, { childList: true });
    comments.addEventListener("load", syncComments, true);
  }
})();
