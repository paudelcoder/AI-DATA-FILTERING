from setuptools import setup, find_packages

setup(
    name="ai_data_filtering",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "spacy>=3.0.0,<4.0.0",
        "requests",
        "beautifulsoup4",
        "google-cloud-language",
        "neo4j",
        "flask",
        "pytest",
    ],
    entry_points={
        "console_scripts": [
            "hinduism-ai=hinduism_ai.main:main_cli",
        ],
    },
)
