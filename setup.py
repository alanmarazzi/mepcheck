from setuptools import setup

setup(name="mepcheck",
      version="0.0.2",
      description="Retrieve voting data for all MEPs and return them in a structured way",
      url="https://github.com/alanmarazzi/mepcheck",
      author="Alan Marazzi",
      author_email="alan.marazzi@gmail.com",
      license="MIT",
      packages=["mepcheck"],
      install_requires=[
              "beautifulsoup4",
              "prettytable",
              "requests"
          ],
      zip_safe=False,
      download_url='https://github.com/alanmarazzi/mepcheck/archive/master.zip',
      keywords=['voting', 'data', 'mep'],
      classifiers=[
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6'
      ])
