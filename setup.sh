#!/usr/bin/env bash
# Ubuntu 18.04 BIONIC BEAVER
sudo apt-get install openjdk-8-jre-headless -y && \
sudo apt-get install openjdk-8-jdk-headless -y && \
wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add - && \
sudo apt-get install apt-transport-https && \
echo "deb https://artifacts.elastic.co/packages/6.x/apt stable main" | sudo tee -a /etc/apt/sources.list.d/elastic-6.x.list && \
sudo apt-get update && sudo apt-get install elasticsearch && \
sudo vim /etc/elasticsearch/elasticsearch.yml && \
# EDIT AND UNCOMMENT network.host: 0.0.0.0
printf "\n\nEDIT AND UNCOMMENT network.host: 0.0.0.0 IN /etc/elasticsearch/elasticsearch.yml\n\n"
