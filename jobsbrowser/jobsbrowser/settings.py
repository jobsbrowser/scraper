# -*- coding: utf-8 -*-

# Scrapy settings for jobsbrowser project

BOT_NAME = 'jobsbrowser'
USER_AGENT = ('Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) '
              'AppleWebKit/536.26 (KHTML, like Gecko) '
              'Version/6.0 Mobile/10A5376e Safari/8536.25')

SPIDER_MODULES = ['jobsbrowser.spiders']
NEWSPIDER_MODULE = 'jobsbrowser.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'jobsbrowser (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html# ownload-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'jobsbrowser.pipelines.JobsbrowserPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html# ttpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# Storage
STORAGE_SERVICE_ADD_URL = 'http://localhost:5000/offers'
STORAGE_SERVICE_RETRIEVE_URL = 'http://localhost:5000/offers'
STORAGE_SERVICE_UPDATE_URL = 'http://localhost:5000/offers'

# Date format
INPUT_DATE_FORMATS = ['%Y-%m-%d', '%d.%m.%Y']
OUTPUT_DATE_FORMAT = '%Y-%m-%d'

# Pracuj spider settings
PRACUJ_OFFERS_FROM_LAST_N_DAYS = None
PRACUJ_CATEGORIES = {
    '5015001': 'Administrowanie bazami danych i storage',
    '5015002': 'Administrowanie sieciami',
    '5015003': 'Administrowanie systemami',
    '5015004': 'Bezpieczeństwo / Audyt',
    '5015005': 'Wdrożenia ERP',
    '5015006': 'Wsparcie techniczne / Helpdesk',
    '5015007': 'Zarządzanie usługami',
    '5016001': 'Analiza biznesowa',
    '5016002': 'Architektura',
    '5016003': 'Programowanie',
    '5016004': 'Testowanie',
    '5016005': 'Zarządzanie projektem',
    '5013001': 'E-marketing / SEM / SEO',
    '5013002': 'Media społecznościowe',
    '5013003': 'Projektowanie',
    '5013004': 'Sprzedaż / e-Commerce',
    '5013005': 'Tworzenie stron WWW / Technologie internetowe',
}
