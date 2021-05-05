import os
import sys

project = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(project)
os.environ["DJANGO_SETTINGS_MODULE"] = "scraping_service.settings"

import django
django.setup()
from django.db import DatabaseError
from scraping.parsers import *
from scraping.models import Vacancy, City, Language, Error


parsers = (
    (work, 'https://www.work.ua/jobs-kyiv-python/'),
    (rabota, 'https://rabota.ua/zapros/python/%D1%83%D0%BA%D1%80%D0%B0%D0%B8%D0%BD%D0%B0'),
    (dou, 'https://jobs.dou.ua/vacancies/?category=Python&search=%D0%9A%D0%B8%D0%B5%D0%B2'),
    (djinni, 'https://djinni.co/jobs/keyword-python/kyiv/')
)


city = City.objects.filter(slug='kyiv').first()
language = Language.objects.filter(slug='python').first()

jobs, errors = [], []


for func, url in parsers:
    j, e = func(url)
    jobs += j
    errors += e

for job in jobs:
    v = Vacancy(city=city, language=language, **job)
    try:
        v.save()
    except DatabaseError:
        pass

if errors:
    er = Error(data=errors).save()

# with open('vacancies.txt', 'w', encoding='utf-8') as f:
#     f.write(str(jobs))
