FROM quay.io/informaticslab/image-service-public

MAINTAINER niall.robinson@informaticslab.co.uk 

RUN apt-get update \
  && apt-get -y --force-yes install autoconf automake build-essential libass-dev libfreetype6-dev libav-tools libtheora-dev libtool libvdpau-dev libvorbis-dev pkg-config texi2html zlib1g-dev wget ffmpeg git \
  && rm -rf /var/lib/apt/lists/*

RUN wget http://www.tortall.net/projects/yasm/releases/yasm-1.2.0.tar.gz \
  && tar xvzf yasm-1.2.0.tar.gz \
  && cd yasm-1.2.0 \
  && ./configure && make -j 4 && make install

ENV PATH /opt/conda/bin:$PATH

ADD profile.py profile.py

CMD python2.7 profile.py