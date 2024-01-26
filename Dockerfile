FROM python:3.11.7

COPY pyassist.py /usr/src/pyassist.py

WORKDIR /usr/src

CMD ["python", "pyassist.py"]
