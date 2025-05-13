from setuptools import find_packages, setup

setup(name = "e-commerce-bot",
    version="0.01",
    author="Udo Nweke",
    autho_email = "unwek001@gmail.com",
    packages = find_packages(),
    install_requires = ['langchain-astradb', 'langchain']

)