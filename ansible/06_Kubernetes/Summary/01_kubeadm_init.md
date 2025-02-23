marwiesing@ubuntu:~$ sudo kubeadm init --pod-network-cidr=192.168.0.0/16
[init] Using Kubernetes version: v1.32.2
[preflight] Running pre-flight checks
[preflight] Pulling images required for setting up a Kubernetes cluster
[preflight] This might take a minute or two, depending on the speed of your internet connection
[preflight] You can also perform this action beforehand using 'kubeadm config images pull'
W0222 10:12:25.761467   13475 checks.go:846] detected that the sandbox image "registry.k8s.io/pause:3.8" of the container runtime is inconsistent with that used by kubeadm.It is recommended to use "registry.k8s.io/pause:3.10" as the CRI sandbox image.
[certs] Using certificateDir folder "/etc/kubernetes/pki"
[certs] Generating "ca" certificate and key
[certs] Generating "apiserver" certificate and key
[certs] apiserver serving cert is signed for DNS names [kubernetes kubernetes.default kubernetes.default.svc kubernetes.default.svc.cluster.local ubuntu] and IPs [10.96.0.1 192.168.0.100]
[certs] Generating "apiserver-kubelet-client" certificate and key
[certs] Generating "front-proxy-ca" certificate and key
[certs] Generating "front-proxy-client" certificate and key
[certs] Generating "etcd/ca" certificate and key
[certs] Generating "etcd/server" certificate and key
[certs] etcd/server serving cert is signed for DNS names [localhost ubuntu] and IPs [192.168.0.100 127.0.0.1 ::1]
[certs] Generating "etcd/peer" certificate and key
[certs] etcd/peer serving cert is signed for DNS names [localhost ubuntu] and IPs [192.168.0.100 127.0.0.1 ::1]
[certs] Generating "etcd/healthcheck-client" certificate and key
[certs] Generating "apiserver-etcd-client" certificate and key
[certs] Generating "sa" key and public key
[kubeconfig] Using kubeconfig folder "/etc/kubernetes"
[kubeconfig] Writing "admin.conf" kubeconfig file
[kubeconfig] Writing "super-admin.conf" kubeconfig file
[kubeconfig] Writing "kubelet.conf" kubeconfig file
[kubeconfig] Writing "controller-manager.conf" kubeconfig file
[kubeconfig] Writing "scheduler.conf" kubeconfig file
[etcd] Creating static Pod manifest for local etcd in "/etc/kubernetes/manifests"
[control-plane] Using manifest folder "/etc/kubernetes/manifests"
[control-plane] Creating static Pod manifest for "kube-apiserver"
[control-plane] Creating static Pod manifest for "kube-controller-manager"
[control-plane] Creating static Pod manifest for "kube-scheduler"
[kubelet-start] Writing kubelet environment file with flags to file "/var/lib/kubelet/kubeadm-flags.env"
[kubelet-start] Writing kubelet configuration to file "/var/lib/kubelet/config.yaml"
[kubelet-start] Starting the kubelet
[wait-control-plane] Waiting for the kubelet to boot up the control plane as static Pods from directory "/etc/kubernetes/manifests"
[kubelet-check] Waiting for a healthy kubelet at http://127.0.0.1:10248/healthz. This can take up to 4m0s
[kubelet-check] The kubelet is healthy after 501.718351ms
[api-check] Waiting for a healthy API server. This can take up to 4m0s
[api-check] The API server is healthy after 4.000959687s
[upload-config] Storing the configuration used in ConfigMap "kubeadm-config" in the "kube-system" Namespace
[kubelet] Creating a ConfigMap "kubelet-config" in namespace kube-system with the configuration for the kubelets in the cluster
[upload-certs] Skipping phase. Please see --upload-certs
[mark-control-plane] Marking the node ubuntu as control-plane by adding the labels: [node-role.kubernetes.io/control-plane node.kubernetes.io/exclude-from-external-load-balancers]
[mark-control-plane] Marking the node ubuntu as control-plane by adding the taints [node-role.kubernetes.io/control-plane:NoSchedule]
[bootstrap-token] Using token: u6cul7.m0sjchh42mx6zyur
[bootstrap-token] Configuring bootstrap tokens, cluster-info ConfigMap, RBAC Roles
[bootstrap-token] Configured RBAC rules to allow Node Bootstrap tokens to get nodes
[bootstrap-token] Configured RBAC rules to allow Node Bootstrap tokens to post CSRs in order for nodes to get long term certificate credentials
[bootstrap-token] Configured RBAC rules to allow the csrapprover controller automatically approve CSRs from a Node Bootstrap Token
[bootstrap-token] Configured RBAC rules to allow certificate rotation for all node client certificates in the cluster
[bootstrap-token] Creating the "cluster-info" ConfigMap in the "kube-public" namespace
[kubelet-finalize] Updating "/etc/kubernetes/kubelet.conf" to point to a rotatable kubelet client certificate and key
[addons] Applied essential addon: CoreDNS
[addons] Applied essential addon: kube-proxy

Your Kubernetes control-plane has initialized successfully!

To start using your cluster, you need to run the following as a regular user:

  mkdir -p $HOME/.kube
  sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
  sudo chown $(id -u):$(id -g) $HOME/.kube/config

Alternatively, if you are the root user, you can run:

  export KUBECONFIG=/etc/kubernetes/admin.conf

You should now deploy a pod network to the cluster.
Run "kubectl apply -f [podnetwork].yaml" with one of the options listed at:
  https://kubernetes.io/docs/concepts/cluster-administration/addons/

Then you can join any number of worker nodes by running the following on each as root:

sudo kubeadm join 192.168.0.100:6443 --token u6cul7.m0sjchh42mx6zyur \
	--discovery-token-ca-cert-hash sha256:72d25713808b6eb2ab05b386cb898700a95d3efd2c17512a4ae6b6153217a0ed 

----

### **🔍 Fixing Node Roles & Renaming Nodes in Kubernetes**  

Right now, your nodes show **no roles (`<none>`)**, and the names are incorrect (`debian`, `localhost.localdomain`, etc.).  

---

## **✅ 1️⃣ Assign the Worker Role to Worker Nodes**  
By default, worker nodes don’t get a role assigned automatically. We need to **label them as `worker`** manually.

Run the following **on Ubuntu-1 (Control Plane):**  
```bash
kubectl label node ubuntu2 node-role.kubernetes.io/worker=worker
kubectl label node debian node-role.kubernetes.io/worker=worker
kubectl label node localhost.localdomain node-role.kubernetes.io/worker=worker
```
✅ Now check:  
```bash
kubectl get nodes
```
**Expected output:**  
```
NAME                    STATUS     ROLES           AGE     VERSION
debian-1                NotReady   worker          3m5s    v1.32.2
rocky-1                 NotReady   worker          87s     v1.32.2
ubuntu-1                Ready      control-plane   41m     v1.32.2
ubuntu-2                Ready      worker          5m27s   v1.32.2
```

---

## **✅ 2️⃣ Rename Kubernetes Nodes Properly**  
Kubernetes **does not support renaming nodes directly**, so we need to **remove and rejoin** them with the correct name.

### **🔹 Step 1: Drain & Remove the Worker Nodes**  
Run the following **on Ubuntu-1 (Control Plane):**  
```bash
kubectl drain debian --ignore-daemonsets --delete-emptydir-data
kubectl drain localhost.localdomain --ignore-daemonsets --delete-emptydir-data
kubectl drain ubuntu2 --ignore-daemonsets --delete-emptydir-data
```
Now remove them from Kubernetes:  
```bash
kubectl delete node debian
kubectl delete node localhost.localdomain
kubectl delete node ubuntu2
```

---

### **🔹 Step 2: Reset the Worker Nodes**  
Run this **on each worker node (debian, rocky, ubuntu-2):**  
```bash
sudo kubeadm reset -f
sudo hostnamectl set-hostname debian-1   # Change this on each worker node accordingly
sudo reboot
```
📌 **Repeat for each node, using the correct name:**  
- `debian-1`
- `rocky-1`
- `ubuntu-2`

---

### **🔹 Step 3: Rejoin the Workers with Correct Names**  
After the nodes reboot, **log back into each worker node** and rejoin Kubernetes:  
```bash
sudo kubeadm join 192.168.0.100:6443 --token u6cul7.xxx \
        --discovery-token-ca-cert-hash sha256:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```
_(Use the correct token and hash from your cluster.)_  

---

### **🔹 Step 4: Verify Everything is Correct**  
On Ubuntu-1 (Control Plane), check the nodes again:  
```bash
kubectl get nodes
```
✅ **Expected output (after a few minutes):**  
```
NAME        STATUS   ROLES           AGE   VERSION
ubuntu-1    Ready    control-plane   45m   v1.32.2
ubuntu-2    Ready    worker          3m    v1.32.2
rocky-1     Ready    worker          3m    v1.32.2
debian-1    Ready    worker          3m    v1.32.2
```

---

### **🎉 Done! Kubernetes Nodes Are Correctly Named & Labeled!**  
✔️ **Nodes have the correct names**  
✔️ **Workers are labeled as `worker`**  
✔️ **Cluster is now properly structured**  

📌 **Next Step:** Install **Helm (Kubernetes Package Manager) on Ubuntu-1**  
Let me know when you're ready! 🚀🔥