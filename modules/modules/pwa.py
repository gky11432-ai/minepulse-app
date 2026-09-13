# modules/pwa.py - DGMS Enterprise Service Worker & Scope Handler
from fastapi import APIRouter
from fastapi.responses import Response

router = APIRouter(tags=["PWA Engine"])

SW_JS_CONTENT = """// MinePulse Offline Engine v10
const CACHE_NAME = 'minepulse-core-vault-v10';
const STATIC_ASSETS = [
  '/',
  '/manifest.json',
  '/vault',
  '/broadcast',
  '/sos'
];

self.addEventListener('install', (event) => {
  self.skipWaiting();
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(STATIC_ASSETS).catch((e) => console.log('Precache fallback:', e));
    })
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.map((k) => {
          if (k !== CACHE_NAME) return caches.delete(k);
        })
      );
    })
  );
  self.clients.claim();
});

self.addEventListener('fetch', (event) => {
  if (event.request.method !== 'GET') return;

  const url = new URL(event.request.url);

  // Dynamic APIs ko offline me fail hone par silent chhod do
  if (url.pathname.startsWith('/api/')) {
    event.respondWith(
      fetch(event.request).catch(() => new Response(JSON.stringify([]), {
        headers: { 'Content-Type': 'application/json' }
      }))
    );
    return;
  }

  // HTML pages aur UI assets ke liye: Cache first, fallback to offline root
  event.respondWith(
    caches.match(event.request).then((cached) => {
      if (cached) {
        // Background me update try karo
        fetch(event.request).then((fresh) => {
          if (fresh && fresh.status === 200) {
            caches.open(CACHE_NAME).then((c) => c.put(event.request, fresh));
          }
        }).catch(() => {});
        return cached;
      }

      return fetch(event.request).then((fresh) => {
        if (fresh && fresh.status === 200) {
          const clone = fresh.clone();
          caches.open(CACHE_NAME).then((c) => c.put(event.request, clone));
        }
        return fresh;
      }).catch(() => {
        return caches.match('/') || caches.match('/vault');
      });
    })
  );
});
"""

MANIFEST_JSON_CONTENT = """{
  "name": "MinePulse AI Pit Portal",
  "short_name": "MinePulse",
  "start_url": "/",
  "scope": "/",
  "display": "standalone",
  "background_color": "#020617",
  "theme_color": "#dc2626",
  "orientation": "portrait",
  "icons": [
    {
      "src": "https://cdn-icons-png.flaticon.com/512/1033/1033068.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "https://cdn-icons-png.flaticon.com/512/1033/1033068.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ]
}"""

@router.get("/sw.js")
def get_service_worker():
    return Response(
        content=SW_JS_CONTENT,
        media_type="application/javascript",
        headers={
            "Service-Worker-Allowed": "/",
            "Cache-Control": "no-cache, no-store, must-revalidate"
        }
    )

@router.get("/manifest.json")
def get_manifest():
    return Response(
        content=MANIFEST_JSON_CONTENT,
        media_type="application/json",
        headers={"Cache-Control": "no-cache"}
    )
  
