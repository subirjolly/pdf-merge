from setuptools import setup, find_packages


setup(
    name='pdf_merge',
    version='1.0.0',
    description='PDF Merge Utility',
    author='Subir Jolly',
    author_email="subirjolly@gmail.com",
    license="Proprietary License.",
    packages=find_packages(exclude=["tests*"]),
    entry_points={
        'console_scripts': [
            'pdf_merge=pdf.merge:main',
            'pdf_rotate=pdf.rotate:main'
        ]
    },
)
