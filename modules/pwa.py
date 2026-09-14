# modules/pwa.py - Robust Pit-Safe Service Worker Engine
from fastapi import APIRouter
from fastapi.responses import Response

router = APIRouter(tags=["PWA Engine"])

SW_JS_CONTENT = """// MinePulse Pure Resilient Service Worker v60
const CACHE_NAME = 'minepulse-app-v60';

self.addEventListener('install', (e) => {
  self.skipWaiting();
  e.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(['/', '/manifest.json']))
  );
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys().then((keys) => Promise.all(
      keys.map((k) => { if (k !== CACHE_NAME) return caches.delete(k); })
    ))
  );
  self.clients.claim();
});

self.addEventListener('fetch', (e) => {
  if (e.request.method !== 'GET') return;

  const url = new URL(e.request.url);

  // API calls fail silently to empty JSON when offline
  if (url.pathname.startsWith('/api/')) {
    e.respondWith(
      fetch(e.request).catch(() => new Response(JSON.stringify([]), {
        headers: { 'Content-Type': 'application/json' }
      }))
    );
    return;
  }

  // HTML UI Cache First
  e.respondWith(
    caches.match(e.request).then((cached) => {
      if (cached) {
        fetch(e.request).then((fresh) => {
          if (fresh && fresh.status === 200) {
            caches.open(CACHE_NAME).then((c) => c.put(e.request, fresh));
          }
        }).catch(() => {});
        return cached;
      }
      return fetch(e.request).then((fresh) => {
        if (fresh && fresh.status === 200) {
          const clone = fresh.clone();
          caches.open(CACHE_NAME).then((c) => c.put(e.request, clone));
        }
        return fresh;
      }).catch(() => caches.match('/'));
    })
  );
});
"""

MANIFEST_JSON_CONTENT = """{
  "name": "MinePulse AI Pit Station",
  "short_name": "MinePulse",
  "start_url": "/",
  "scope": "/",
  "display": "standalone",
  "background_color": "#020617",
  "theme_color": "#dc2626",
  "orientation": "portrait"
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
    return Response(content=MANIFEST_JSON_CONTENT, media_type="application/json")
  
