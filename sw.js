const CACHE_NAME = 'mb-barberos-v1790726218';
const ASSETS = [
  './',
  './index.html',
  './app.js',
  './logo_cropped.png',
  'https://cdn.tailwindcss.com',
  'https://cdn.jsdelivr.net/npm/chart.js',
  'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css',
];

// Install: cache all assets
self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      // Cache local files reliably; external CDN best-effort
      return cache.addAll(['./index.html', './app.js', './logo_cropped.png']).then(() => {
        return Promise.allSettled(
          ['https://cdn.tailwindcss.com', 'https://cdn.jsdelivr.net/npm/chart.js',
           'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css',
           'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap']
            .map(url => fetch(url).then(r => cache.put(url, r)).catch(() => {}))
        );
      });
    })
  );
  self.skipWaiting();
});

// Activate: clear old caches
self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k)))
    )
  );
  self.clients.claim();
});

// Fetch: cache-first strategy
self.addEventListener('fetch', (e) => {
  e.respondWith(
    caches.match(e.request).then(cached => {
      if (cached) return cached;
      return fetch(e.request).then(response => {
        if (response && response.status === 200 && e.request.method === 'GET') {
          const clone = response.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(e.request, clone));
        }
        return response;
      }).catch(() => {
        // If offline and nothing in cache, return a fallback for HTML
        if (e.request.destination === 'document') {
          return caches.match('./index.html');
        }
      });
    })
  );
});
