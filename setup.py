import os
from setuptools import setup


long_desc = ""
if os.path.exists('README.md'):
    with open('README.md', 'r', encoding='utf-8') as f:
        long_desc = f.read()

setup(
    name='codaramac',
    version='2.0.0',
    description='A robust multi-platform CLI utility for managing and spoofing MAC addresses.',
    long_description=long_desc,
    long_description_content_type='text/markdown',
    author='Codara Software Solutions',
    author_email='contact@codara.lk',
    url='https://codara.lk', 
    license='MIT',
    py_modules=['codaramc'], 
    install_requires=[],
    entry_points={
        'console_scripts': [
            'codaramac = codaramc:main', 
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent', 
        'Environment :: Console',
        'Topic :: Security',
        'Topic :: System :: Networking',
    ]
)
