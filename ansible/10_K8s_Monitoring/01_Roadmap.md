### **Step-by-Step Setup for Kubernetes Monitoring**
Since you've already installed **Fluentd**, but don't know what to do with it, I’ll guide you on:
1. **Configuring Fluentd to send logs to Loki** (since you chose Loki)
2. **Installing K9s, Prometheus, and Grafana** for full monitoring

---

## **1️⃣ Fluentd Configuration (Forward Logs to Loki)**
Since Fluentd is installed but unconfigured, let's set it up to forward logs to **Loki**.

### **Step 1: Create a ConfigMap for Fluentd**
Fluentd needs a configuration file to define where logs go. Apply this YAML:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: fluentd-config
  namespace: kube-system
data:
  fluent.conf: |
    <source>
      @type tail
      path /var/log/containers/*.log
      pos_file /var/log/fluentd-containers.log.pos
      tag kubernetes.*
      format json
    </source>

    <match kubernetes.**>
      @type loki
      url http://loki:3100
      buffer_chunk_limit 2M
      buffer_queue_limit 8
      flush_interval 10s
    </match>
```

### **Step 2: Mount the ConfigMap in Fluentd Pods**
Edit your Fluentd **DaemonSet** (or Deployment) to mount this ConfigMap:

```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: fluentd
  namespace: kube-system
spec:
  template:
    spec:
      volumes:
        - name: config-volume
          configMap:
            name: fluentd-config
      containers:
        - name: fluentd
          volumeMounts:
            - name: config-volume
              mountPath: /fluentd/etc/
```

Apply the changes:

```sh
kubectl apply -f fluentd-config.yaml
kubectl rollout restart daemonset fluentd -n kube-system
```

📌 **What this does**: 
- Collects logs from all pods (`/var/log/containers/*.log`)
- Sends logs to Loki (`http://loki:3100`)

🚀 **Next Step: Install Loki to receive logs!**

---

## **2️⃣ Install Loki (Log Aggregation)**
Loki is used to store logs and integrates with Grafana.

### **Step 1: Install Loki with Helm**
```sh
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
helm install loki grafana/loki-stack -n monitoring --create-namespace
```

Check if it's running:
```sh
kubectl get pods -n monitoring
```

👉 **Loki should now be running!** Logs from Fluentd should start flowing into it.

---

## **3️⃣ Install Prometheus & Grafana**
These will collect and visualize Kubernetes metrics.

### **Step 1: Install Prometheus**
```sh
helm install prometheus grafana/prometheus -n monitoring
```

Check if it's running:
```sh
kubectl get pods -n monitoring
```

### **Step 2: Install Grafana**
```sh
helm install grafana grafana/grafana -n monitoring
```

Get the Grafana admin password:
```sh
kubectl get secret grafana -n monitoring -o jsonpath="{.data.admin-password}" | base64 --decode
```

👉 **Access Grafana**:  
- Run: `kubectl port-forward svc/grafana 3000:80 -n monitoring`
- Open: `http://localhost:3000`
- Login with `admin` and the retrieved password.

---

## **4️⃣ Install K9s (CLI Monitoring Tool)**
K9s gives you a **real-time, terminal-based** view of your Kubernetes cluster.

### **Step 1: Install K9s**
On **Ubuntu/Linux**:
```sh
curl -sS https://webinstall.dev/k9s | bash
```

Check installation:
```sh
k9s
```

🚀 **Now, you can explore your cluster interactively!**

---

## **5️⃣ Verify Everything**
### **Check Prometheus Metrics**
```sh
kubectl port-forward svc/prometheus 9090:9090 -n monitoring
```
Visit **`http://localhost:9090`** and query metrics.

### **Check Loki Logs in Grafana**
1. Open **Grafana**
2. Add **Loki** as a data source (`http://loki:3100`)
3. Use **Explore** to check logs.

### **Check Fluentd Logs**
```sh
kubectl logs -l app=fluentd -n kube-system
```
You should see logs flowing to Loki.

---

## **🎯 Summary of Installed Tools**
✅ **Fluentd** → Collects logs and sends to **Loki**  
✅ **Loki** → Stores logs for visualization in **Grafana**  
✅ **Prometheus** → Collects cluster metrics  
✅ **Grafana** → Dashboards for **Prometheus & Loki**  
✅ **K9s** → Real-time CLI monitoring  

🚀 **Now your Kubernetes cluster has full monitoring!** 🚀

Do you need a **custom Grafana dashboard for Kubernetes?** Let me know! 😊