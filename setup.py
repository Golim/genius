from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='genius-lyrics',
    version='1.1',
    scripts=['genius.py'],
    author="Matteo Golinelli",
    author_email="matteogolinelli97@gmail.com",
    description="Find the lyrics of the song you are listening to directly from your Linux terminal",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/golim/genius",
    install_requires=[
        'beautifulsoup4',
    ],
    keywords = ['GENIUS', 'LYRICS', 'TERMINAL'],
)