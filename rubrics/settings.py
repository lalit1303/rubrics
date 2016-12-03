import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SECRET_KEY = 'y$$z5mkac83!1#kvgslx_y(fk)mqknpkj0p8q+&qq+)dtje!2&'

ROOT_URLCONF = 'rubrics.urls'

WSGI_APPLICATION = 'rubrics.wsgi.application'

INSTALLED_APPS = (
    'rubrics',
)

MIDDLEWARE_CLASSES = (
)

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'rubrics',
        'USER': 'root',
        'PASSWORD': 'lalit1303',
        'HOST': 'localhost',
        'PORT': '3306'
    }
}
