FROM python:3

RUN mkdir -p /web/vps
ADD setup.py /web
ADD vps /web/vps
RUN chown -R nobody /web

RUN pip install --upgrade pip setuptools
RUN cd /web && pip install .

EXPOSE 6968/tcp
EXPOSE 6969/tcp
CMD ["vps", "--debug"]
