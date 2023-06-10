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



## Prometheus 使用說明 (德晏）
1. 列出使用的 promql 以及希望搜集的指標、指標代表依據
2. alert manager 實作過程

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
在輸入以下指令後，k6會將測試結果輸入進influxdb當中 並由grafana進行呈現 \
``` diff
# (我的k6資料夾位於wsl中的/mnt/c/distriFinal資料夾內)
docker-compose up -d influxdb grafana
docker-compose run -v /mnt/c/distriFinal/k6/samples:/scripts/samples k6 run /scripts/samples/script.js
```


4. 串接、視覺化資料的過程
