from setuptools import setup

setup(
    name='Volt_PL_Ultra-5_25.6V_200Ah',
    author='Chmielarczyk Robert',
    author_email='chmielar@student.agh.edu.pl',
    version='0.1',
    packages=['pylontech'],
    install_requires=['pyserial', 'construct', 'json', 'BytesIO', 'os', 'datetime'],
)