from setuptools import setup

setup(
    name="django-user-notification",
    version="0.0.1",
    python_requires=">=3.8",
    authors="Miradil Zeynalli, Konul Mammadova and Huseyn Abduallabayli",
    long_description="Django library for managing and sending notifications to users over different mediums.",
    install_requires=["django==3.2.13", "django-ckeditor==6.4.2", "pytest-django==4.5.2"],
)
