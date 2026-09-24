// The studio chat (founder 2026-09-24). Served from our own site (CSP script-src 'self'); the pages work without it.
// - the input box grows as you type; Enter sends on a keyboard (Shift+Enter for a new line); phones use the arrow
// - the paperclip shows the names of the files you picked
// - "Change something" buttons put the cursor in the input box
// - while we work, the page checks every 5 seconds and refreshes itself when something changes (no websockets)
(function () {
  "use strict";
  var form = document.getElementById("composer");
  var box = document.getElementById("composer-text");
  var touch = window.matchMedia && window.matchMedia("(pointer: coarse)").matches;

  function grow() {
    if (!box || box.closest(".big")) return;
    box.style.height = "auto";
    box.style.height = Math.min(box.scrollHeight, 220) + "px";
  }

  if (form && box) {
    var send = form.querySelector(".send");
    var file = form.querySelector('input[type="file"]');
    var ready = function () { return box.value.trim().length > 0 || (file && file.files.length > 0); };
    var sync = function () { if (send) send.disabled = !ready(); };
    box.addEventListener("input", function () { grow(); sync(); });
    box.addEventListener("keydown", function (e) {
      if (e.key === "Enter" && !e.shiftKey && !e.isComposing && !touch) {
        e.preventDefault();
        if (ready()) { if (form.requestSubmit) form.requestSubmit(); else form.submit(); }
      }
    });
    if (file) {
      file.addEventListener("change", function () {
        var out = document.getElementById(file.getAttribute("data-picked"));
        if (out) {
          out.textContent = "";
          Array.prototype.forEach.call(file.files, function (f) {
            var chip = document.createElement("span");
            chip.textContent = f.name;
            out.appendChild(chip);
          });
        }
        sync();
      });
    }
    form.addEventListener("submit", function (e) {
      if (!ready()) { e.preventDefault(); return; }
      if (send) { send.disabled = true; }
      form.setAttribute("aria-busy", "true");
    });
    grow();
    sync();
  }

  Array.prototype.forEach.call(document.querySelectorAll("[data-focus]"), function (b) {
    b.addEventListener("click", function () {
      var t = document.getElementById(b.getAttribute("data-focus"));
      if (t) { t.focus(); t.scrollIntoView({ block: "center", behavior: "smooth" }); }
    });
  });

  // starting points under the prompt box fill it in; the customer finishes the sentence
  Array.prototype.forEach.call(document.querySelectorAll("[data-fill]"), function (c) {
    c.addEventListener("click", function () {
      if (!box) return;
      box.value = c.getAttribute("data-fill");
      box.focus();
      box.setSelectionRange(box.value.length, box.value.length);
      box.dispatchEvent(new Event("input"));
    });
  });

  // open a thread at the moment that matters now (the newest message), not at the top
  var now = document.getElementById("now");
  if (now && now.getBoundingClientRect().top > window.innerHeight * 0.6) {
    now.scrollIntoView({ block: "start" });
    window.scrollBy(0, -90);
  }

  var poll = document.body.getAttribute("data-poll");
  if (poll && window.fetch) {
    var updated = document.body.getAttribute("data-updated");
    var line = document.body.getAttribute("data-line") || "";
    var tick = function () {
      fetch(poll, { credentials: "same-origin", cache: "no-store" })
        .then(function (r) { return r.ok ? r.json() : null; })
        .then(function (d) {
          if (d && (d.updated !== updated || (d.line || "") !== line)) { window.location.reload(); }
          else { window.setTimeout(tick, 5000); }
        })
        .catch(function () { window.setTimeout(tick, 10000); });
    };
    window.setTimeout(tick, 5000);
  }
})();
