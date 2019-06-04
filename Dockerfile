FROM python:3.6

COPY . /mepcheck

WORKDIR /mepcheck/mepcheck
RUN pip install -r ../requirements.txt &&\
    pip install pandas &&\
    pip install ../. &&\
    python savemeps.py

ENTRYPOINT ["python", "../mepcheckCLI.py"]
