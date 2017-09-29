FROM debian:jessie
RUN sed -i 's/debian testing main/debian testing main contrib non-free/' /etc/apt/sources.list

# Install general tools
RUN apt-get update
RUN apt-get -y install graphviz unzip curl libssl-dev libcurl4-openssl-dev libxml2-dev python-pip tomcat8 git cgroupfs-mount maven

# Install WINGS
RUN mkdir -p /opt/wings/storage/default
ADD ./config/default/wings-portal.xml /etc/tomcat8/Catalina/localhost/wings-portal.xml
ADD ./config/default/portal.properties /opt/wings/storage/default/portal.properties
RUN mkdir /wings-src
ADD ./config/pom.xml /wings-src/pom.xml
RUN cd /wings-src && mvn package
RUN cp -R /wings-src/target/wings-portal-4.0 /opt/wings/server
RUN sed -i 's/Resource name="UserDatabase" auth/Resource name="UserDatabase" readonly="false" auth/' /etc/tomcat8/server.xml
RUN sed -i 's/=tomcat8/=root/' /etc/default/tomcat8
RUN sed -i 's/<\/tomcat-users>/  <user username="admin" password="4dm1n!23" roles="WingsUser,WingsAdmin"\/>\n<\/tomcat-users>/' /etc/tomcat8/tomcat-users.xml
ADD http://www.wings-workflows.org/downloads/docker/latest/portal/setenv.txt /setenv.sh
EXPOSE 8080

# Install Docker
RUN apt-get -y install --no-install-recommends apt-transport-https ca-certificates software-properties-common gnupg2
RUN curl -fsSL https://download.docker.com/linux/$(. /etc/os-release; echo "$ID")/gpg | apt-key add -
RUN add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/$(. /etc/os-release; echo "$ID") \
   $(lsb_release -cs) \
   stable"
RUN apt-get update && apt-get -y install docker-ce

# Start WINGS
RUN chmod 755 /setenv.sh 
CMD /setenv.sh && service tomcat8 start && /bin/bash
