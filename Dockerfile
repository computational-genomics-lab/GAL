# From this base-image / starting-point
#
# FROM ubuntu:16.04
FROM ubuntu:latest
#
# Authorship
#
MAINTAINER tsucheta@gmail.com

ENV DEBIAN_FRONTEND=noninteractive
#
# Pull in packages from testing
#
RUN apt-get update && apt-get install -y vim \
                                python3 \
                                python3-pymysql \
                                python3-pyparsing \
                                apache2

#
#Augustus Dependency software
#

RUN apt-get -y install libboost-iostreams-dev
RUN apt-get -y install zlib1g-dev
RUN apt-get -y install libgsl0-dev
RUN apt-get -y install libsqlite3-dev
RUN apt-get -y install libboost-graph-dev
RUN apt-get -y install liblpsolve55-dev
RUN apt-get -y install bamtools libbamtools-dev
RUN apt-get -y install gawk
RUN apt-get -y install cmake \
                        g++

#Augustus installation
#

COPY /GAL_code/software/augustus-3.2.2 /opt/augustus
RUN cd /opt/augustus && \
        make && \
        make install
RUN chmod 777 /usr/local/bin/augustus

#
# copy GAL background code
#
RUN mkdir /usr/GAL
COPY GAL_code/backend/ /usr/GAL/
RUN chmod 755 /usr/GAL/WebScript/web_upload.py
RUN chmod 755 /usr/GAL/WebScript/scheduler.py
RUN chmod 777 /usr/GAL/WebScript/data.stack
RUN chmod 777 /usr/GAL/gal.log
#
#Blast Set up
#
RUN apt-get -y install ncbi-blast+
COPY /GAL_code/BlastDB /opt/BlastDB
#
#LASTZ setup
#
COPY /GAL_code/software/lastz-distrib /opt/lastz-distrib

#
#SignalP
#
# COPY /GAL_code/software/signalp-3.0 /opt/signalp-3.0
COPY /GAL_code/software/signalp-4.1 /opt/signalp-4.1

#
#HmmPfam
#
COPY /GAL_code/software/pfam /opt/pfam
COPY /GAL_code/software/hmmer-3.1b2 /opt/hmmer-3.1b2
RUN cd /opt/hmmer-3.1b2 && \
        ./configure && \
        make && \
        make install
#
#TMHMM
#
COPY /GAL_code/software/tmhmm-2.0c /opt/tmhmm-2.0c

#
# GeneMark Setup
#
COPY /GAL_code/software/gmsuite /opt/gmsuite
RUN cp /opt/gmsuite/gm_key ~/.gm_key
RUN chown -R www-data:www-data /root
RUN mkdir /home/www-data
RUN cp /opt/gmsuite/gm_key /home/www-data/.gm_key
RUN sed -i -e "\$aexport HOME=/home/www-data " /etc/apache2/envvars


#
#EMBOSS program Setup
#
RUN apt-get update
RUN apt-get -y install emboss
RUN mv /usr/bin/primer3_core /usr/bin/primer32_core
COPY /GAL_code/software/transfac32/site.dat /tmp/
COPY /GAL_code/software/rebase /tmp/
RUN tfextract -infile /tmp/site.dat
RUN rebaseextract -infile /tmp/withrefm.703 -protofile /tmp/proto.703

#
#setup frontend part
#
RUN mkdir /tmp/gal_tmp
RUN chmod 1777 /tmp/gal_tmp
RUN rm /var/www/html/index.html
COPY GAL_code/frontend /var/www/html/

RUN mkdir /tmp/tmp
RUN chmod 1777 /tmp/tmp
RUN ln -s /tmp/tmp /var/www/html/tmp

#
#setting mysql server and running /usr/GAL/main.py
#
RUN apt-get update
ENV MYSQL_PWD test
RUN echo "mysql-server mysql-server/root_password password $MYSQL_PWD" | debconf-set-selections
RUN echo "mysql-server mysql-server/root_password_again password $MYSQL_PWD" | debconf-set-selections
RUN apt-get -y install mysql-server
#RUN apt-get -q -y install mysql-server
RUN usermod -d /var/lib/mysql/ mysql
ADD set-mysql-password.sh /tmp/set-mysql-password.sh
RUN chmod 755 /tmp/set-mysql-password.sh
RUN . /tmp/set-mysql-password.sh
#
#setting phpmyadmin
#
RUN apt-get -q -y install phpmyadmin
RUN sed -i -e "\$aServerName localhost " /etc/apache2/apache2.conf
#RUN sed -i -e "\$aInclude /etc/phpmyadmin/apache.conf" /etc/apache2/apache2.conf

#
#PHP upload limit
#
RUN sed -i 's/upload_max_filesize = 2M/upload_max_filesize = 256M/' /etc/php/7.4/apache2/php.ini
RUN sed -i 's/post_max_size = 8M/post_max_size = 256M/' /etc/php/7.4/apache2/php.ini

COPY GAL_code/URL-Based /usr/URL-Based

COPY GAL_code/scripts /usr/scripts/
RUN cpan -i HTML::Parse
RUN cpan -i HTML::Strip

COPY init_mysql.sh /tmp/init_mysql.sh
RUN chmod 777 /tmp/init_mysql.sh
ENTRYPOINT sh "/tmp/init_mysql.sh" && service apache2 start && bash


