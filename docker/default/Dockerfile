FROM tomcat:8
RUN sed -i 's/debian testing main/debian testing main contrib non-free/' /etc/apt/sources.list

# Install general tools
RUN apt-get update && apt-get -y install --no-install-recommends \
        graphviz \
        libcurl4-openssl-dev \
        libxml2-dev \
        python-pip \
        git \
        cgroupfs-mount \
        maven \
        tcl \
        tk \
        apt-transport-https \
        software-properties-common \
        gnupg2

# Install Docker
RUN curl -fsSL https://download.docker.com/linux/$(. /etc/os-release; echo "$ID")/gpg | apt-key add -
RUN add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/$(. /etc/os-release; echo "$ID") \
   $(lsb_release -cs) \
   stable"
RUN apt-get update && apt-get -y install docker-ce

# Install wings
ADD ./config/pom.xml /wings-src/pom.xml
RUN mkdir /wings-src
WORKDIR /wings-src
RUN mvn package

# Add wings properties
RUN mkdir -p /opt/wings/storage/default
ADD ./config/default/portal.properties /opt/wings/storage/default/portal.properties

# Add Wings build to tomcat (Deploy)
RUN cp -R /wings-src/target/wings-portal-4.0-SNAPSHOT /usr/local/tomcat/webapps/wings-portal

# Add wings context file to the wings portal webapp
ADD ./config/default/wings-portal.xml /usr/local/tomcat/webapps/wings-portal/META-INF/context.xml

RUN sed -i 's/Resource name="UserDatabase" auth/Resource name="UserDatabase" readonly="false" auth/' /etc/tomcat8/server.xml
RUN sed -i 's/<\/tomcat-users>/  <user username="admin" password="4dm1n!23" roles="WingsUser,WingsAdmin"\/>\n<\/tomcat-users>/' /etc/tomcat8/tomcat-users.xml
ADD http://www.wings-workflows.org/downloads/docker/latest/portal/setenv.txt /setenv.sh
EXPOSE 8080

# Start WINGS
RUN chmod 755 /setenv.sh 
CMD /setenv.sh && service tomcat8 start && /bin/bash
