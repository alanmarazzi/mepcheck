FROM python:3.6

COPY . /mepcheck
COPY .meps /root
WORKDIR /mepcheck/mepcheck
RUN pip install -r ../requirements.txt &&\
    pip install pandas &&\
    pip install ../.

ENTRYPOINT ["python", "../mepcheckCLI.py"]
