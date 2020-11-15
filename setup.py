from setuptools import setup, find_packages

setup(
    author='Juan Emilio Zurita Macias',
    author_email='juanezm@ieee.org',
    name='s3-uploader',
    version='0.1',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.5, <4',
    install_requires=['click==7.1.2', 'pytest==6.1.2', 'boto3==1.16.18', 'moto==1.3.16'],
    entry_points={
        'console_scripts': ['s3-uploader-cli=s3uploader.entrypoints.cli:main'],
    }
)
