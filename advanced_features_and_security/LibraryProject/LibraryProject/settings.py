# ...existing code...

# ...existing code...

# ...existing code...

# ...existing code...

import os
from pathlib import Path

# ...existing code...

BASE_DIR = Path(__file__).resolve().parent.parent

# ...existing code...

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs/django.log',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'WARNING',
            'propagate': True,
        },
    },
}

# =========================
# Security settings
# =========================

# Redirect all HTTP traffic to HTTPS
SECURE_SSL_REDIRECT = True

# Use HTTP Strict Transport Security (HSTS)
SECURE_HSTS_SECONDS = 31536000  # 1 year in seconds
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Only send session cookies over HTTPS
SESSION_COOKIE_SECURE = True

# Only send CSRF cookies over HTTPS
CSRF_COOKIE_SECURE = True

# Additional secure headers (recommended)
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'