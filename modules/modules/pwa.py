# modules/pwa.py - DGMS Pit-Grade Zero-Network Offline Service Worker Engine
from fastapi import APIRouter
from fastapi.responses import Response

router = APIRouter(tags=["PWA Engine"])

SW_JS_CONTENT = """// MinePulse Industrial Service Worker - Offline First Architecture
const CACHE_NAME = 'minepulse-pit-vault-v1';
const CRITICAL_ASSETS = [
  '/',
  '/manifest.json',
  '/api/collieries',
  '/api/inspections'
];

self.addEventListener('install', (event) => {
  self.skipWaiting();
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(CRITICAL_ASSETS).catch(err => console.log('Precache fallback:', err));
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

// Intercept all requests: Return Offline Cache first, fetch network in background
self.addEventListener('fetch', (event) => {
  if (event.request.method !== 'GET') return;

  event.respondWith(
    caches.match(event.request).then((cachedResponse) => {
      if (cachedResponse) {
        // Fetch network update silently in background if online
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
      }).catch(() => {
        // Ultimate fallback to index if asset fails offline
        return caches.match('/');
      });
    })
  );
});
"""

MANIFEST_JSON_CONTENT = """{
  "name": "MinePulse AI Pit Portal",
  "short_name": "MinePulse",
  "start_url": "/",
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
    return Response(content=SW_JS_CONTENT, media_type="application/javascript")

@router.get("/manifest.json")
def get_manifest():
    return Response(content=MANIFEST_JSON_CONTENT, media_type="application/json")
  
