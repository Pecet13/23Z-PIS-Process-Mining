#!/bin/bash

sudo apt-get update

# ***********************************************************
#         Website deployment
# ***********************************************************
RESOURCE_GROUP="PIS"
WEB_APP_NAME="pismining"
ZIP_FILE="/home/pis/Frontend/Website.zip"

cd /home/pis/Frontend/Website
zip -r $ZIP_FILE .

az login
az webapp deployment source config-zip --resource-group $RESOURCE_GROUP --name $WEB_APP_NAME --src $ZIP_FILE

echo "Deployment to Azure Web App has been completed."


# ***********************************************************
#         Kafka VM Machine
# ***********************************************************
REMOTE_USER="ondrasz"
REMOTE_HOST="4.246.129.143"

CMD1="kafka/bin/kafka-zookeeper-start.sh kafka/config/zookeeper.properties"
CMD2="kafka/bin/kafka-server-start.sh kafka/config/server.properties"
CMD3="kafka/bin/connect-standalone.sh kafka/connect-standalone.properties kafka/jdbc.properties"
CMD4="python consumer.py"

ssh -T ${REMOTE_USER}@${REMOTE_HOST} << EOF
    ./${CMD1}
    ./${CMD2}
    ./${CMD3}
    ${CMD4}
EOF

# ***********************************************************
#         Start Loading Simulator
# ***********************************************************
cd /home/pis/Backend/LoadingSimulator
python loading_simulator.py 

