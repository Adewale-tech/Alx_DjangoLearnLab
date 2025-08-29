INSTALLED_APPS = [
    # ...other installed apps...
    'relationship_app',
]

AUTH_USER_MODEL = 'relationship_app.CustomUser'

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/login/'