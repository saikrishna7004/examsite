var dataCacheName = 'examsitedatacache';
var cacheName = 'examsitecache';
var filesToCache = [
    '/static/manifest.json',
    '/offline',
    '/static/home/logo.png',
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.3.0/css/font-awesome.css',
    '/static/jquery-3.6.0.min.js',
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css',
    'https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.6/umd/popper.min.js',
    'https://stackpath.bootstrapcdn.com/bootstrap/4.2.1/js/bootstrap.min.js',
    '/static/bootstrap-5.0.1/js/bootstrap.bundle.min.js',
    '/static/a076d05399.js'
];


self.addEventListener('install', (event) => {
    console.log('[ServiceWorker] Install');
    event.waitUntil(
        caches.open(cacheName).then(function (cache) {
            console.log('[ServiceWorker] Caching app shell');
            return cache.addAll(filesToCache);
        })
    );
});

self.addEventListener('activate', (event) => {
    console.log('[ServiceWorker] Activate');
    event.waitUntil(
        caches.keys().then(function (keyList) {
            return Promise.all(keyList.map(function (key) {
                if (key !== cacheName && key !== dataCacheName) {
                    console.log('[ServiceWorker] Removing old cache', key);
                    return caches.delete(key);
                }
            }));
        })
    );
    return self.clients.claim();
});

self.addEventListener('fetch', (event) => {
    // console.log('Inside the fetch handler:', event);
    // console.log('Fetch event for ', event.request.url);
    event.respondWith(
        caches.match(event.request).then(function (response) {
            if (response) {
                // console.log('Found ', event.request.url, ' in cache');
                return response;
            }
            // console.log('Network request for ', event.request.url);
            return fetch(event.request)

        }).catch(function (error) {

            return caches.match('/offline');

        })
    );
});