import setuptools

setuptools.setup(
    name='bexh-connector-aws-ecs',
    version='0.0.1',
    author='sethsaperstein',
    author_email='sethsaper@gmail.com',
    description='connector',
    long_description=open('README.md').read(),
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    include_package_data=True
)
