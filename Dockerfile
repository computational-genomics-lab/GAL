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

# galpy setup
RUN git clone https://github.com/computational-genomics-lab/GAL.git
RUN pip3 install GAL/.
RUN galpy -NU False

# galweb setup
RUN npm install GAL/galweb/
RUN npm start --prefix GAL/galweb
EXPOSE 5000
CMD ["node", "GAL/galweb/index.js"]

# initiate entrypoint; mysql
# copy
COPY .github/workflows/entrypoint.sh /tmp/entrypoint.sh
RUN chmod 755 /tmp/entrypoint.sh
# run
ENTRYPOINT bash "/tmp/entrypoint.sh" && bash
