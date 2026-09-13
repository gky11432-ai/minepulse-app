# modules/pwa.py - Serves Service Worker & Manifest for 100% Offline PWA
from fastapi import APIRouter
from fastapi.responses import Response

router = APIRouter(tags=["PWA Engine"])

SW_JS_CONTENT = """// MinePulse Offline Service Worker
const CACHE_NAME = 'minepulse-v10-offline';

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(['/']);
    })
  );
  self.skipWaiting();
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
  event.respondWith(
    caches.match(event.request).then((cachedResponse) => {
      if (cachedResponse) {
        // Cache mil gaya, background me update check karo
        fetch(event.request).then((networkResponse) => {
          if (networkResponse && networkResponse.status === 200) {
            caches.open(CACHE_NAME).then((cache) => cache.put(event.request, networkResponse));
          }
        }).catch(() => {});
        return cachedResponse;
      }
      return fetch(event.request).then((networkResponse) => {
        if (networkResponse && networkResponse.status === 200) {
          const resClone = networkResponse.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(event.request, resClone));
        }
        return networkResponse;
      }).catch(() => caches.match('/'));
    })
  );
});
"""

MANIFEST_JSON_CONTENT = """{
  "name": "MinePulse AI DGMS Alert",
  "short_name": "MinePulse",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#020617",
  "theme_color": "#dc2626",
  "orientation": "portrait"
}"""

@router.get("/sw.js")
def get_service_worker():
    return Response(content=SW_JS_CONTENT, media_type="application/javascript")

@router.get("/manifest.json")
def get_manifest():
    return Response(content=MANIFEST_JSON_CONTENT, media_type="application/json")
  
