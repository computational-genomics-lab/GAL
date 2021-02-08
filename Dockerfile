# From this base-image / starting-point
FROM ubuntu:20.04

# set noninteractive
ENV DEBIAN_FRONTEND=noninteractive

# apt-update
RUN apt-get update
RUN apt-get install -y vim \
    less \
    python3 \
    python3-pip \
    nodejs \
    npm \
    git

# MySQL server setup
ENV MYSQL_PWD test
RUN echo "mysql-server mysql-server/root_password password $MYSQL_PWD" | debconf-set-selections
RUN echo "mysql-server mysql-server/root_password_again password $MYSQL_PWD" | debconf-set-selections
RUN apt-get -y install mysql-server
RUN usermod -d /var/lib/mysql/ mysql
RUN printf "[client]\nlocal_infile=1\n"  >> /etc/mysql/mysql.conf.d/mysqld.cnf

# galpy setup
# RUN git clone https://github.com/computational-genomics-lab/GAL.git
RUN pip3 install cryptography
COPY . GAL/
RUN pip3 install GAL/.
RUN galpy -NU False

# galweb setup
RUN npm install GAL/galweb/
RUN npm i pm2 -g
RUN pm2 start /GAL/galweb/index.js

# RUN pm2 startup
EXPOSE 5000

# initiate entrypoint; mysql
# copy
COPY .github/workflows/entrypoint.sh /tmp/entrypoint.sh
RUN chmod 755 /tmp/entrypoint.sh
# run
RUN bash "/tmp/entrypoint.sh" -r TRUE
ENTRYPOINT bash "/tmp/entrypoint.sh" -e TRUE && bash