from setuptools import setup

setup(name='FormatRosterData'
    ,version='0.1'
    ,description=''
    ,author='Troy1010'
    #,author_email=''
    #,url=''
    ,license=''
    ,packages=['FormatRosterData']
    ,zip_safe=False
    ,test_suite='nose.collector'
    ,tests_require=['nose','pandas']
    ,python_requires=">=3.6"
    ,install_requires=['pandas']
    ,setup_requires=['nose','pandas']
    )
