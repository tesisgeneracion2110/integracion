FROM ubuntu:18.04


RUN apt-get update
RUN apt-get install -y git
RUN apt-get install wget

#instalar python
RUN apt-get update
RUN apt install -y python3-pip
RUN apt-get install -y nano
RUN pip3 install requests
RUN pip3 install wget



RUN mkdir content

RUN cd content && git clone https://github.com/tesisgeneracion2110/integration.git

RUN cd content/integration && \
    wget -O shallow.mid https://github.com/mathigatti/midi2voice/blob/master/inputs/shallow.mid?raw=true && \
    wget -O shallow.txt https://raw.githubusercontent.com/mathigatti/midi2voice/master/inputs/shallow.txt && \
    pip3 install Flask
    
#RUN cd content/integration && \ 
#    python3 web_service.py


