from setuptools import setup, find_packages

setup(
    name='nse_scraper',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'requests',
        'pandas',
        'streamlit'
    ],
    entry_points={
        'console_scripts': [
            'nse-scraper=nse_scraper.streamlit_app:main',
        ],
    },
)
