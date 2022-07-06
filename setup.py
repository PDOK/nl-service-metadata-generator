import os
from setuptools import setup, find_packages
from pathlib import Path

with open('README.md') as f:
    README = f.read()

def get_data_files():
    files = []
    for file_path in Path('metadata_generator/data').glob('**/*.*'):
        path_string = str(file_path)
        # strip metadata_generator/ from path:
        path_import = os.path.join(*(path_string.split(os.path.sep)[1:]))
        files.append(path_import)
    return  {'metadata_generator': files}

setup(
    name='ngr-metadata-generator-2',
    version='0.1',
    description='PDOK Service Metadata generator',
    long_description=README,
    author='Anton Bakker',
    author_email='anton.bakker@kadaster.nl',
    packages=find_packages(exclude=('tests', 'docs')),
    package_data=get_data_files(),
    include_package_data=True,
    setup_requires=['wheel'],
    install_requires=[
        'Jinja2==2.11.3',
        'Click==7.0',
        'lxml==4.9.1',
        'markupsafe==2.0.1'
    ],
    entry_points='''
        [console_scripts]
        gen-md=metadata_generator.cli:generate_service_metadata_command
        generate-metadata=metadata_generator.cli:generate_service_metadata_command
    ''',
)
