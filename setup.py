from setuptools import setup, find_packages
import codecs
import os

# here = os.path.abspath(os.path.dirname(__file__))

# with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
#     long_description = "\n" + fh.read()

VERSION = '0.0.9'
DESCRIPTION = 'A package for deploying Federated Learning using Docker and Ansible'
LONG_DESCRIPTION = 'Fill this'

# Setting up
setup(
    name="fed_deploy",
    version=VERSION,
    author="Mohamed Hemdan",
    author_email="<mhemdan@cern.ch>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    # long_description=long_description,
    include_package_data=True,
    install_requires=['setuptools>=61.0', 'ansible>=2.12'],
    package_dir={"": "src"},  # Optional
    packages=find_packages(where="src"),  # Required
    package_data={'': ['install_req.yaml', 'ansible.cfg', 'client_run.yaml', 'inventory.yaml', 'monitor_run.yaml', 'server_run.yaml', 'fed/client/Dockerfile', 'fed/server/Dockerfile', 'fed/monitor/Dockerfile']},
    # keywords=['python', 'video', 'stream', 'video stream', 'camera stream', 'sockets'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)




