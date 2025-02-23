### **🚀 Setting Up Linux Mint as a Kubernetes Client**  

We'll configure **Linux Mint** to manage the Kubernetes cluster remotely, so you don’t have to SSH into `Ubuntu-1` every time.  

✅ Install **kubectl** on Linux Mint  
✅ Copy Kubernetes **admin config** from `Ubuntu-1`  
✅ Verify **Linux Mint can communicate with the cluster**  

---

## **1️⃣ Install `kubectl` on Linux Mint**  
Run this on **Linux Mint**:  
```bash
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl
sudo mv kubectl /usr/local/bin/
```
Test the installation:  
```bash
kubectl version --client
```
✅ **Expected output:**  
```
Client Version: v1.32.2
```

---

## **2️⃣ Copy the Kubernetes Admin Config from `Ubuntu-1`**  
On **Ubuntu-1**, run:  
```bash
sudo cat /etc/kubernetes/admin.conf
```
You'll see something like:  
```yaml
apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: XYZ...
    server: https://192.168.0.100:6443
...
users:
- name: kubernetes-admin
  user:
    client-certificate-data: ABC...
```

Now, on **Linux Mint**, create a directory:  
```bash
mkdir -p ~/.kube
```
Copy the config from Ubuntu-1 and save it as:  
```bash
nano ~/.kube/config
```
Paste the **entire content** of `admin.conf`, then save (`Ctrl+X`, `Y`, `Enter`).

---

## **3️⃣ Test Connection from Linux Mint**  
Run:  
```bash
kubectl get nodes
```
✅ **Expected output (once the cluster is fully set up):**  
```
NAME        STATUS   ROLES           AGE   VERSION
ubuntu-1    Ready    control-plane   5m    v1.32.2
ubuntu-2    Ready    worker          3m    v1.32.2
rocky-1     Ready    worker          3m    v1.32.2
debian-1    Ready    worker          3m    v1.32.2
```
If you get an error like `certificate signed by unknown authority`, we might need to **fix permissions**.

---

## **4️⃣ Fix Permissions (If Needed)**
If `kubectl get nodes` gives an error, try this on **Linux Mint**:  
```bash
export KUBECONFIG=~/.kube/config
chmod 600 ~/.kube/config
```
Then try again:  
```bash
kubectl get nodes
```

---

### **🎉 Done! Linux Mint is Now Your K8s Client!**
✔️ **`kubectl` installed on Linux Mint**  
✔️ **Admin config copied from Ubuntu-1**  
✔️ **Linux Mint can manage the K8s cluster remotely**  

💡 **Next Step:**  
👉 **Initialize Kubernetes on `Ubuntu-1`** (`kubeadm init`)  
👉 **Join Worker Nodes (`kubeadm join`)**  

Let me know when you're ready! 🚀🔥