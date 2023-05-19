kubectl create secret generic {SECRET_NAME} \
--from-literal=MYSQL_USERNAME={MYSQL_USERNAME} \
--from-literal=MYSQL_PASSWORD={MYSQL_PASSWORD} \
--from-literal=MYSQL_URL={MYSQL_URL} \
--namespace={NAME_SPACE}