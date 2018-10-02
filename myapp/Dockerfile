#
# Scala and sbt Dockerfile
#
# https://github.com/hseeberger/scala-sbt
#

# Pull base image
FROM openjdk:8-jdk


# Env variables
ENV SCALA_VERSION 2.12.6
ENV SBT_VERSION 1.2.3

# Scala expects this file
RUN touch /usr/lib/jvm/java-8-openjdk-amd64/release

# Install Scala
## Piping curl directly in tar
RUN \
  curl -fsL https://downloads.typesafe.com/scala/$SCALA_VERSION/scala-$SCALA_VERSION.tgz | tar xfz - -C /root/ && \
  echo >> /root/.bashrc && \
  echo "export PATH=~/scala-$SCALA_VERSION/bin:$PATH" >> /root/.bashrc

# Install sbt
RUN \
  curl -L -o sbt-$SBT_VERSION.deb https://dl.bintray.com/sbt/debian/sbt-$SBT_VERSION.deb && \
  dpkg -i sbt-$SBT_VERSION.deb && \
  rm sbt-$SBT_VERSION.deb && \
  apt-get update && \
  apt-get install sbt && \
  sbt sbtVersion

RUN apt-get clean
RUN apt-get update

RUN apt-get install -qy git
RUN apt-get install -qy locales
RUN apt-get install -qy nano
RUN apt-get install -qy tmux
RUN apt-get install -qy wget
RUN apt-get install -qy unzip
RUN apt-get install -qy vim

RUN wget https://archive.apache.org/dist/spark/spark-2.2.0/spark-2.2.0-bin-hadoop2.7.tgz
RUN tar zxf spark-2.2.0-bin-hadoop2.7.tgz
RUN export SPARK_HOME=/spark-2.2.0-bin-hadoop2.7
ENV PATH="/spark-2.2.0-bin-hadoop2.7/bin:${PATH}"
RUN echo "export PATH=/spark-2.2.0-bin-hadoop2.7/bin:$PATH" >> /root/.bashrc

RUN echo "Spark downlopaded"
RUN echo `pwd`

RUN apt-get update

# Define working directory
WORKDIR /root

COPY azkaban-solo-server-3.51.0-10-g49996e4a.zip /root/
RUN unzip azkaban-solo-server-3.51.0-10-g49996e4a.zip
RUN rm /root/azkaban-solo-server-3.51.0-10-g49996e4a/conf/azkaban.properties
COPY azkaban.properties /root/azkaban-solo-server-3.51.0-10-g49996e4a/conf/
COPY startup.sh /root/azkaban-solo-server-3.51.0-10-g49996e4a/


RUN apt-get install -qy maven


WORKDIR /root/azkaban-solo-server-3.51.0-10-g49996e4a
RUN chmod +x startup.sh


RUN ./bin/start-solo.sh
RUN echo `pwd`
CMD ["./startup.sh"]
#CMD ["bash"]