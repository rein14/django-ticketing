var staticCacheName = "django-pwa-v" + new Date().getTime();
var filesToCache = [
    '/offline',

    // '/css/django-pwa-app.css',

    // 'https://code.jquery.com/jquery-3.6.0.min.js',
    // 'https://cdn.jsdelivr.net/npm/onscreen@1.4.0/dist/on-screen.umd.min.js',
    // 'https://cdnjs.cloudflare.com/ajax/libs/popper.js/2.9.2/umd/popper.min.js',
    // 'https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.min.js',
    // 'https://cdn.jsdelivr.net/npm/smoothscroll-polyfill@0.4.4/dist/smoothscroll.min.js',
    // 'https://cdn.jsdelivr.net/npm/sweetalert2@11.4.10/dist/sweetalert2.all.min.js',
    // 'https://cdnjs.cloudflare.com/ajax/libs/simplebar/5.3.6/simplebar.min.js',
    // // '/static/assets/js/vanillajs-datepicker/dist/js/datepicker.min.js',
    // 'https://buttons.github.io/buttons.js',
    // '/static/notifications/notify.js',
    // 'https://cdnjs.cloudflare.com/ajax/libs/jqueryui/1.12.1/jquery-ui.min.js',
    // 'https://cdnjs.cloudflare.com/ajax/libs/toastr.js/latest/toastr.min.js',
    // 'https://cdn.datatables.net/v/bs4/dt-1.11.5/r-2.2.9/datatables.min.css',
    // 'https://cdn.datatables.net/v/bs4/dt-1.11.5/r-2.2.9/datatables.min.js',
    // 'https://cdn.datatables.net/1.11.5/js/dataTables.bootstrap5.min.js',
    // 'https://cdnjs.cloudflare.com/ajax/libs/bootstrap-datetimepicker/4.17.47/js/bootstrap-datetimepicker.min.js',
    // 'https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.27.0/moment.min.js',
    // '/static/assets/js/volt.js',
    // 'https://cdn.jsdelivr.net/npm/sweetalert2@11.4.10/dist/sweetalert2.min.css',
    // 'https://cdn.jsdelivr.net/npm/notyf@3.10.0/notyf.min.js',
    // '/static/assets/css/volt.css',
    // 'https://appsrv1-147a1.kxcdn.com/volt-dashboard-pro-v131/vendor/@fortawesome/fontawesome-free/css/all.min.css',
    // '/static/cms/js/ajax.js',
    // '/static/bootstrap_datepicker_plus/css/datepicker-widget.css',
    // '/static/bootstrap_datepicker_plus/js/datepicker-widget.js',
    // '/static/js/ajax_fileupload.js',
    // '/static/js/jquery-fileupload/jquery.fileupload.js',
    // '/static/js/jquery-fileupload/jquery.iframe-transport.js',
    // '/static/js/jquery-fileupload/jquery.ui.widget.js',
    // '/static/account/css/signin.css',
    // 'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap',
    // '/static/django_select2/django_select2.css',
    // '/static/webpush/webpush.js',
    // // '/static/js/notifications.js',

    
    // '/images/icons/icon-72x72.png',
    // '/images/icons/icon-96x96.png',
    // '/images/icons/icon-128x128.png',
    // '/images/icons/icon-144x144.png',
    // '/images/icons/icon-152x152.png',
    // '/images/icons/icon-192x192.png',
    // '/images/icons/icon-384x384.png',
    // '/images/icons/icon-512x512.png',
    // '/static/images/icons/splash-640x1136.png',
    // '/static/images/icons/splash-750x1334.png',
    // '/static/images/icons/splash-1242x2208.png',
    // '/static/images/icons/splash-1125x2436.png',
    // '/static/images/icons/splash-828x1792.png',
    // '/static/images/icons/splash-1242x2688.png',
    // '/static/images/icons/splash-1536x2048.png',
    // '/static/images/icons/splash-1668x2224.png',
    // '/static/images/icons/splash-1668x2388.png',
    // '/static/images/icons/splash-2048x2732.png'
];

// Cache on install
self.addEventListener("install", event => {
    this.skipWaiting();
    event.waitUntil(
        caches.open(staticCacheName)
        .then(cache => {
            return cache.addAll(filesToCache);
        })
    )
});

// Clear cache on activate
self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames
                .filter(cacheName => (cacheName.startsWith("django-pwa-")))
                .filter(cacheName => (cacheName !== staticCacheName))
                .map(cacheName => caches.delete(cacheName))
            );
        })
    );
});

// Serve from Cache
self.addEventListener("fetch", event => {
    event.respondWith(
        caches.match(event.request)
        .then(response => {
            return response || fetch(event.request);
        })
        .catch(() => {
            return caches.match('offline');
        })
    )
});