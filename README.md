# 分散式系統 操作說明

## GKE 架設說明 (Google Kubernetes Engine)

## Prometheus 以及 Grafana 架設說明 (頤賢）

## Prometheus 使用說明 (德晏）
1. 列出使用的 promql 以及希望搜集的指標、指標代表依據
2. alert manager 實作過程

## K6 壓力測試說明
1. 如何安裝

下載k6
Linux

```
sudo gpg -k
sudo gpg --no-default-keyring --keyring /usr/share/keyrings/k6-archive-keyring.gpg --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys C5AD17C747E3415A3642D57D77C6C491D6AC1D69
echo "deb [signed-by=/usr/share/keyrings/k6-archive-keyring.gpg] https://dl.k6.io/deb stable main" | sudo tee /etc/apt/sources.list.d/k6.list
sudo apt-get update
sudo apt-get install k6

```

Docker
```
docker pull grafana/k6
```

2. 如何使用（打哪些指令可以跑或是輸出 output）
3. grafana、influxdb 安裝
4. 串接、視覺化資料的過程
