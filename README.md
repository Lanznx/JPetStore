# 分散式系統 操作說明

## GKE 架設說明 (Google Kubernetes Engine)
1. Create gke cluster, you can use GUI on google cloud platform or read following document to create cluster by command line

- [Deploy an app to a GKE cluster](https://cloud.google.com/kubernetes-engine/docs/deploy-app-cluster#create_cluster)
- [Deploy an app in a container image to a GKE cluster](https://cloud.google.com/kubernetes-engine/docs/quickstarts/deploy-app-container-image)
- [Create an Autopilot cluster](https://cloud.google.com/kubernetes-engine/docs/how-to/creating-an-autopilot-cluster)

2. open cloud shell and clone this repository
```
git clone https://github.com/ocar1053/JPetStore.git
```
3. open cloud editor and connect to cluster then apply yml file
```
cd .\JPetStore\k3s\config\
kubectl apply -f ./namespace.yml
kubectl create secret generic {SECRET_NAME} \
--from-literal=MYSQL_USERNAME={MYSQL_USERNAME} \
--from-literal=MYSQL_PASSWORD={MYSQL_PASSWORD} \
--from-literal=MYSQL_URL={MYSQL_URL} \
--namespace={NAME_SPACE}
k3s kubectl apply -f ./ 

```
4. set load balancer to expose service public ip
```
kubectl expose deployment jpetstore-backend-deployment --type="LoadBalancer" -n jpetstore
```
5. Enter public ip in browser to access jpetstore

![image](https://github.com/ocar1053/JPetStore/assets/64206644/6ecac045-92fb-4573-a93f-0a39d3d381e7)


## Prometheus 以及 Grafana 架設說明 (頤賢）

1. open cloud shell and input following command
```
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add stable https://kubernetes-charts.storage.googleapis.com/
helm repo update
helm install prometheus prometheus-community/kube-prometheus-stack
```
2. create node port service
```
kubectl expose deployment prometheus-grafana --name my-np-service     --type NodePort --protocol TCP --port 80 --target-port 3000
```
3. set load balancer to expose service public ip
```
kubectl expose deployment prometheus-grafana --name granfana-service --type="LoadBalancer" --port 3087 --target-port 3000
```

4. Enter public ip in browser to access grafana

![image](https://github.com/ocar1053/JPetStore/assets/64206644/c3b253f5-90ac-4a51-a325-157e416445ef)



## Prometheus 使用說明 (德晏）
### PromQL
There are three main target metrics for us to monitor: 
1. CPU Usage of JPetStore Pods
```
sum(rate(container_cpu_usage_seconds_total{namespace="jpetstore"}[30s])) by (namespace)
```
2. Memory Usage
```
max(container_memory_working_set_bytes/on(container, pod) kube_pod_container_resource_limit{resource="memory"})
```
3. Number of HTTP Requests/Responses
```
irate(prometheus_http_response_size_bytes_sum[1m])
```

### Alertmanager
1. Set additional monitoring rules for prometheus in values.yaml, according to our target metrics.
2. Set alertmanager routes, includings alert rules in values.yaml.
3. update helm charts
```
helm upgrade prometheus prometheus-community/kube-prometheus-stack -f values.yaml
```


## K6 壓力測試說明
1. 如何安裝

* 建立一個新資料夾，並透過git clone <網址>將jpetstore更新進該資料夾內 \
接著在同一個資料夾下載k6

* **Linux**

```
sudo gpg -k
sudo gpg --no-default-keyring --keyring /usr/share/keyrings/k6-archive-keyring.gpg --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys C5AD17C747E3415A3642D57D77C6C491D6AC1D69
echo "deb [signed-by=/usr/share/keyrings/k6-archive-keyring.gpg] https://dl.k6.io/deb stable main" | sudo tee /etc/apt/sources.list.d/k6.list
sudo apt-get update
sudo apt-get install k6
```

* **Docker**
```
docker pull grafana/k6
```

2. 如何使用（打哪些指令可以跑或是輸出 output）

* 在k6資料夾內新增一個samples資料夾 \
並在samples內新增script.js檔案 \
裡面打上壓力測試的設定 \
設定完成後，在samples資料夾內輸入
```
k6 run script.js
```
便可以成功執行測試

3. grafana、influxdb 安裝

* **範例** \
首先要透過以下指令取得主機的IP地址，並將地址填入docker-compose的指令當中 \
這樣才能成功將測試資料發進網站
```
hostname -I
```
* 在輸入以下指令後，k6會將測試結果輸入進influxdb當中 並由grafana進行呈現
``` diff
# (我的k6資料夾位於wsl中的/mnt/c/distriFinal資料夾內)
docker-compose up -d influxdb grafana
docker-compose run -v /mnt/c/distriFinal/jpetstore-6/k6/samples:/scripts/samples k6 run -e JPETSTORE_IP=<自己的主機IP> /scripts/samples/script.js
```

4. 串接、視覺化資料的過程
