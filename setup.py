from setuptools import setup, find_packages

setup(
    name='audio_image_embedder',
    version='0.1.0',  # Update this version as necessary
    author='Shyam Mondal',
    author_email='info@damoadarglobal.com',
    description='A package to embed audio into images and extract it back.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/neuralshyam/audio_image_embedder',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # Update as necessary
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
