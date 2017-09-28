from setuptools import setup

setup(name="mepcheck",
      version="0.1",
      description="Retrieve voting data for all MEPs and return them in a structured way",
      url="https://github.com/alanmarazzi/mepcheck",
      author="Alan Marazzi",
      author_email="alan.marazzi@gmail.com",
      license="MIT",
      packages=["mepcheck"],
      zip_safe=False,
      download_url='https://github.com/alanmarazzi/mepcheck/archive/master.zip',
      keywords=['voting', 'data', 'mep'],
      classifiers=[
          'Programming Language :: Python :: 3'
      ])
