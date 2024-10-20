from setuptools import setup, find_packages
from FuXLogger.__metadata__ import __version__ , __author__ , __project_name__ , __email__ , __license__ , __github_url__

def load_requirements(filepath: str = "requirements.txt") -> list[str]:
    try:
       with open(filepath, 'r') as f:
           return [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        return []
    except Exception:
        return []

setup(
    name=__project_name__,
    version=__version__,
    packages=find_packages(),
    author=__author__,
    author_email=__email__,
    description='A useful logging library for Python',
    long_description=open('Readme.md','r',encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url=__github_url__,
    requires=load_requirements(),  # 依赖
    license=__license__,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
