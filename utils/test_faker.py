import os , django , random

# Need to run this before calling models from application!
os.environ.setdefault("DJANGO_SETTINGS_MODULE" , "project.settings")
django.setup()

from track.models import Video, unit, Course, \
						 Article, Practice, Track

# from faker import Faker


# def create_items(n):
#     fake = Faker()
#     for _ in range(n):
#         fake_name = fake.name()
#         fake_description = fake.text()
#         fake_url = random.randint(1000, 1000000)

#         Video.objects.create(
#             VIDName = fake_name,
#             VIDDescription = fake_description,
#             VDIURL = fake_url
#         )
