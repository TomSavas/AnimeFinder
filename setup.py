from setuptools import setup

setup(
    name = "KissToMal",
    author = "Tom Savas",
    description = ("Kissanime to Mal bookmark (list) converter"),
    url = "https://github.com/TomSavas/KissToMal",
    packages=['cfscrape'],
    install_requires = ['Js2Py==0.37', 'requests >= 2.0.0']
)
