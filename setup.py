
from setuptools import setup, find_packages

setup(name='hodor_picontroller',
    version='1.1',
    description='Door Controller',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'hodor_watcher=hodor_controller.watcher:main',
            'hodor_slacker=hodor_slackbot.hodor_slacker:main'
        ]
    },
    test_suite="unit_test_suite")
