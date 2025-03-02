### 🔍 **Summary of Your Current State**
1. **ArgoCD Server Location**  
   - `argocd-server` **is currently running on `rocky-1` (192.168.0.56)**, but you want it on **`ubuntu-2` (192.168.0.240)**.
   - The other ArgoCD components (`dex-server`, `redis`, `repo-server`, etc.) are already running on `ubuntu-2`.

2. **Service Type & Connectivity**  
   - `argocd-server` is set to **`ClusterIP`**, meaning it is only reachable **inside the cluster**.
   - No `NodePort` or `LoadBalancer` is currently configured.
   - **ArgoCD is not reachable externally** at `https://192.168.0.100:30189/` or any other external URL.

3. **Ingress Configuration**  
   - You have an **Ingress resource (`ingress.yaml`)**, but it is **not applied yet** (`kubectl get ingress -n argocd` shows no resources).
   - The Ingress expects `argocd.example.com`, but **DNS is not configured** yet.

4. **Networking & Cluster Setup**  
   - Your cluster consists of **four nodes**:
     - `ubuntu` (`192.168.0.100`) → **Control Plane (GitLab)**
     - `ubuntu-2` (`192.168.0.240`) → **Target Worker Node for ArgoCD**
     - `rocky-1` (`192.168.0.56`) → **Current ArgoCD Server Location**
     - `debian-1` (`192.168.0.242`) → **Additional Worker Node**
   - No `Taints` are currently set, meaning **Pods can be scheduled anywhere**.

---

### 🎯 **Roadmap to Desired State**
✅ **Goal:**  
- Move `argocd-server` to **`ubuntu-2`** using **Taints & Tolerations**.
- Make `argocd-server` accessible via **Ingress** at `argocd.example.com`.
- Configure **DNS** to map `argocd.example.com` to the correct IP.

---

## 🏗 **Step-by-Step Implementation Plan**

### **1️⃣ Apply a Taint to Ensure ArgoCD Runs on `ubuntu-2`**
To force `argocd-server` onto `ubuntu-2`, apply a Taint:

```sh
kubectl taint nodes ubuntu-2 dedicated=argocd:NoSchedule
```

Now, only Pods with a matching **Toleration** will be allowed on `ubuntu-2`.

### **2️⃣ Add a Toleration to the ArgoCD Server Deployment**
Edit the `argocd-server` Deployment:

```sh
kubectl edit deployment argocd-server -n argocd
```

Add the following under `spec.template.spec`:

```yaml
tolerations:
- key: "dedicated"
  operator: "Equal"
  value: "argocd"
  effect: "NoSchedule"
```

This ensures that `argocd-server` will now **only** be scheduled on `ubuntu-2`.

### **3️⃣ Delete & Restart the ArgoCD Server Pod**
After applying the Taint and Toleration, restart the Pod:

```sh
kubectl delete pod -n argocd -l app.kubernetes.io/name=argocd-server
```

Verify that `argocd-server` is now on `ubuntu-2`:

```sh
kubectl get pods -n argocd -o wide
```

### **4️⃣ Ensure Ingress Controller is Installed**
Before setting up the Ingress, verify that an **Ingress Controller** is running.

Check if you have an Nginx Ingress Controller:

```sh
kubectl get pods -n kube-system | grep ingress
```

If **not installed**, deploy it:

```sh
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/cloud/deploy.yaml
```

### **5️⃣ Apply the Ingress Resource**
Now that the Ingress Controller is running, apply your `ingress.yaml`:

```sh
kubectl apply -f ingress.yaml
```

Verify the Ingress is created:

```sh
kubectl get ingress -n argocd
```

### **6️⃣ Update DNS to Resolve `argocd.example.com`**
Since you're using a local cluster, update your **hosts file** on your machine (`/etc/hosts` or Windows `C:\Windows\System32\drivers\etc\hosts`):

```sh
192.168.0.240  argocd.example.com
```

Test with:

```sh
ping argocd.example.com
```

If this is for a **public DNS**, configure an `A` record pointing `argocd.example.com` to `192.168.0.240`.

### **7️⃣ Test the Setup**
Try accessing **ArgoCD via Ingress**:

```sh
curl -k https://argocd.example.com
```

Or open it in your browser:

🔗 **`https://argocd.example.com`**

If it doesn't work, check:

```sh
kubectl logs -n argocd deployment/argocd-server
kubectl describe ingress -n argocd
```

---

### 🎯 **Final Expected State**
✔ `argocd-server` **runs on `ubuntu-2`** due to **Taints & Tolerations**.  
✔ ArgoCD is **accessible via Ingress** at `https://argocd.example.com`.  
✔ DNS is **configured** to point to `192.168.0.240`.  

---

💡 **Next Steps**
- If authentication issues arise, reset the ArgoCD admin password:

  ```sh
  kubectl -n argocd patch secret argocd-secret \
    -p '{"stringData": {"admin.password": "", "admin.passwordMtime": ""}}'
  ```

- If TLS is misconfigured, create a self-signed certificate or use `cert-manager`.

---

This roadmap should get you fully set up! 🚀 Let me know if you hit any issues.