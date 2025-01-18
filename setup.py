from setuptools import setup, find_packages

setup(
    name='pictures_master',
    version='0.1',
    install_requires=[
        # 'pillow',
        'pyside6',
        'adb-shell[usb]',
    ],
    packages=find_packages()
)
