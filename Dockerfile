#BUILD
#docker build -t ros-helloworld .

# sudo apt-get install python3-dev python3-rpi.gpio




FROM ros:iron-ros-core
LABEL authors="dadouuu"
WORKDIR /home
# Copier le fichier requirements.txt dans le conteneur
#RUN apt-get update && apt-get install -y \
#    python3-pip \
#    libcairo2-dev \
#    pkg-config \
#    python3-dev


# Installer Python 3 et pip
RUN apt-get update && apt-get install -y python3 python3-pip

EXPOSE 4421

#COPY packages.txt /home/packages.txt
#COPY requirements.txt /home/requirements.txt
COPY . /home/
#RUN git clone https://github.com/duvamduvam/DadouUtils.git
#RUN mv DadouUtils dadou_utils

#RUN apt-get update && cat /tmp/packages.txt | xargs apt-get install -y
RUN apt-get install -y \
    python3 \
    python3-pip \
    libcairo2-dev \
    pkg-config \
    python3-dev \
    libgirepository1.0-dev \
    libasound2-dev

# Installer les bibliothèques Python à partir du fichier requirements.txt
RUN pip3 install -r /home/requirements.txt
#COPY hello-ros.py /home/
#CMD ["python3", "hello-ros.py"]
CMD ["python3", "main.py"]
#ENTRYPOINT ["top", "-b"]