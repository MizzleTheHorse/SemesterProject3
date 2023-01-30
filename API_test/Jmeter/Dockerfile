FROM java:8

ARG JMETER_VERSION="5.4.1" 

# install Jmeter
RUN cd /opt \
 && wget https://archive.apache.org/dist/jmeter/binaries/apache-jmeter-${JMETER_VERSION}.tgz \
 && tar xzf apache-jmeter-${JMETER_VERSION}.tgz \
 && rm apache-jmeter-${JMETER_VERSION}.tgz


COPY ./test /opt/apache-jmeter-5.4.1/bin
WORKDIR /opt/apache-jmeter-5.4.1/bin

RUN mkdir results

#./jmeter -n -t functional_test.jmx -l functional_log -e -o /opt/apache-jmeter-5.4.1/bin/test to generate dashboard repports

CMD ./jmeter -n -t functional_test.jmx -l functional_log.jtl && ./jmeter -n -t load_test.jmx -l load_log.jtl 




