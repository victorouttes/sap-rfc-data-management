from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='sap_rfc_data_management',
    packages=[
        'sap_rfc_data_management',
    ],
    version='1.1.0',
    license='MIT',
    description='Automate some SAP transactions',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Victor Outtes',
    author_email='victor.outtes@gmail.com',
    url='https://github.com/victorouttes/sap-rfc-data-management',
    download_url='https://github.com/victorouttes/sap-rfc-data-management/archive/refs/tags/1.1.0.tar.gz',
    keywords=['sap', 'data', 'rfc', 'automate', 'ec3', 'pm'],
    install_requires=[
        'Cython~=0.29.23',
        'pyrfc~=2.5.0',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)