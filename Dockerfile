FROM ubuntu:15.10
RUN rm /bin/sh && ln -s /bin/bash /bin/sh
RUN apt-get install apt-utils -y
RUN apt-get -y update && apt-get install -y git libtiff5-dev libjpeg8-dev zlib1g-dev \
    libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk python3-dev python3-setuptools
RUN apt-get install build-essential zlib1g zlib1g-dev zlibc libruby1.9 libxml2 libxml2-dev libxslt-dev -y
RUN mkdir /data; cd /data; git clone https://github.com/ericls/tushe/
RUN apt-get install python3-venv -y
RUN mkdir /data/Envs; cd /data/Envs/;pyvenv-3.4 tushe --without-pip
RUN ls /data/Envs/
RUN source /data/Envs/tushe/bin/activate
RUN apt-get install libreadline6 libreadline6-dev lib32ncurses5-dev -y
RUN apt-get install curl python3-dev -y
ENV PATH /data/Envs/tushe/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/opt/X11/bin
RUN curl https://bootstrap.pypa.io/get-pip.py | python
RUN cd /data/tushe; pip install -r requirements.txt; pip install uwsgi
RUN curl https://gist.githubusercontent.com/ericls/fe24bc7d4215362da1e1/raw/0fd1690f8e00145cc1b5a1cdbe2cbe3cafc454d8/settings.py > /data/tushe/settings.py
RUN curl https://gist.githubusercontent.com/ericls/093532dfa8731a0338a6/raw/65d9d81a6be45a05e95911a7c264193025c3a0b0/uwsgi.ini > /data/tushe/uwsgi.ini
EXPOSE 3333
RUN mkdir -p /data/tushe/static/uploads
ENTRYPOINT /data/Envs/tushe/bin/uwsgi --ini /data/tushe/uwsgi.ini