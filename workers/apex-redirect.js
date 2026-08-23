export default {
  async fetch(request) {
    const url = new URL(request.url);
    if (url.hostname !== "carwashmgmt.com") {
      return fetch(request);
    }

    const dest =
      "https://www.carwashmgmt.com" + url.pathname + url.search + url.hash;
    const html = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Car Wash Management</title>
  <meta http-equiv="refresh" content="0;url=${dest}">
  <script>
    (async function () {
      try {
        if ("serviceWorker" in navigator) {
          const regs = await navigator.serviceWorker.getRegistrations();
          await Promise.all(regs.map((r) => r.unregister()));
        }
        if (window.caches) {
          const keys = await caches.keys();
          await Promise.all(keys.map((k) => caches.delete(k)));
        }
      } catch (e) {}
      location.replace(${JSON.stringify(dest)});
    })();
  </script>
</head>
<body>Redirecting to <a href="${dest}">Car Wash Management</a>…</body>
</html>`;

    return new Response(html, {
      headers: {
        "content-type": "text/html; charset=utf-8",
        "cache-control": "no-store, max-age=0",
      },
    });
  },
};
