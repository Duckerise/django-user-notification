from setuptools import find_packages, setup

VERSION = "0.1"

setup(
    name="ducker-notifications",
    version=VERSION,
    description="Django library for managing and sending notifications to users over different mediums.",
    url="https://github.com/Duckerise/ducker-notifications",
    author="Duckerise Team",
    author_email="duckerise@gmail.com",
    license="MIT",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "django-ckeditor==6.4.2",
    ],
)
