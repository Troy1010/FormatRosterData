from setuptools import setup

cRequires = ('nose','pandas','XlsxWriter','openpyxl')

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
    ,tests_require=[*cRequires]
    ,python_requires=">=3.6"
    ,install_requires=[*cRequires]
    ,setup_requires=[*cRequires]
    )
