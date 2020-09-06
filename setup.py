import setuptools

with open('README.md', 'r') as f:
    longDescription = f.read()

setuptools.setup(
    name='pygame-widgets',
    version='0.2.2',
    author='AustL',
    author_email='21chydra@gmail.com',
    description='Widgets for use with Pygame',
    long_description=longDescription,
    long_description_content_type='text/markdown',
    url='https://github.com/AustL/PygameWidgets',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    python_requires='>=3.6',
    license='MIT',
    install_requires=['pygame==2.0.0dev8']
)
