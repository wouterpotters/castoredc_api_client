from setuptools import setup, find_packages

setup(
    name="castoredc_api_client",
    version="1.0.0",
    description="Python wrapper for the Castor EDC API",
    author="Reinier van Linschoten",
    author_email="mail@reiniervl.com",
    url="https://github.com/reiniervlinschoten/castorclient",
    packages=find_packages(
        exclude=("tests", "tests.*", "scripts", "scripts.*", "auth", "auth.*")
    ),
    install_requires=["requests", ],
    license="MIT",
    long_description=open("README.md").read(),
)
