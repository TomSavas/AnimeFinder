from setuptools import setup

setup(
    name = "KissanimeEpisodeCounter",
    author = "Tom Savas",
    description = ("A simple program that calculates how many episodes have you watched on Kissanime"),
    url = "https://github.com/TomSavas/KissanimeEpisodeCounter",
    packages=['cfscrape'],
    install_requires = ['Js2Py==0.37', 'requests >= 2.0.0']
)