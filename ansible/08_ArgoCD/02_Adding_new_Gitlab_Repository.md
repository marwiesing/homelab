### **Updated Guide: Adding a New GitLab Repository to ArgoCD**
*Optimized for a minimal ArgoCD repo-server environment*  

---

## **Step 1: Verify SSH Connection to GitLab**
Before adding the repository to ArgoCD, confirm that SSH authentication works.

```bash
ssh -T git@192.168.0.100
```

✅ Expected output:
```bash
Welcome to GitLab, @your-username!
```
If this fails, ensure your SSH keys are added to GitLab.

---

## **Step 2: Ensure GitLab is Reachable from the Kubernetes Cluster**
Since `argocd-repo-server` runs in a minimal container environment without `ping`, `curl`, or `nc`, **use a temporary debug pod** to check connectivity.

### **1️⃣ Deploy a Debug Pod (BusyBox)**
Run:
```bash
kubectl run -it --rm debug --image=busybox -- sh
```
This starts a temporary container with network utilities.

### **2️⃣ Check Connectivity to GitLab**
Inside the debug pod, run:

#### **🔹 Test if GitLab is reachable via ping:**
```sh
ping -c 4 192.168.0.100
```

✅ Expected output:
```bash
64 bytes from 192.168.0.100: seq=0 ttl=63 time=0.615 ms
```
If it fails, check network policies or firewalls blocking access.

#### **🔹 Test SSH Port (22) with `nc` (Netcat)**
```sh
nc -zv 192.168.0.100 22
```
✅ Expected output:
```bash
192.168.0.100 (22) open
```

#### **🔹 Test HTTP(S) Access (for Webhooks or GitOps API)**
```sh
wget --spider http://192.168.0.100
```
✅ Expected output:
```bash
Connecting to 192.168.0.100 (192.168.0.100):80... connected.
```

#### **🔹 Exit the Debug Pod**
Type:
```sh
exit
```

If GitLab is **not reachable**, check your Kubernetes network settings, firewall rules, or DNS resolution.

---

## **Step 3: Add the GitLab Repository in ArgoCD**
Use the **correct SSH repository format** and bypass known hosts verification:

```bash
argocd repo add git@192.168.0.100:homelab/my-repo.git \
  --ssh-private-key-path ~/.ssh/id_rsa \
  --insecure-skip-server-verification
```

✅ Expected output:
```bash
Repository 'git@192.168.0.100:homelab/my-repo.git' added
```

---

## **Step 4: Verify the Repository Addition**
List all repositories registered in ArgoCD:

```bash
argocd repo list
```

✅ Expected output:
```
TYPE  NAME  REPO                                             INSECURE  OCI    LFS    CREDS  STATUS      MESSAGE  PROJECT
git         git@192.168.0.100:homelab/firstproject.git       true      false  false  false  Successful           
git         git@192.168.0.100:homelab/signature_project.git  true      false  false  false  Successful   
```
If the **STATUS** is `Successful`, the repository is correctly configured.

---

## **Step 5: Create an ArgoCD Application Using the Repository**
To deploy applications from the new repository:

```bash
argocd app create my-app \
  --repo git@192.168.0.100:homelab/my-repo.git \
  --path / \
  --dest-server https://kubernetes.default.svc \
  --dest-namespace default
```

### **Deploy the Application**
```bash
argocd app sync my-app
```

### **Check Application Status**
```bash
argocd app get my-app
```

---

## **Troubleshooting**
### **❌ Issue: "No such host" error**
```bash
failed to list refs: dial tcp: lookup gitlab.ubuntu-01.local on 10.96.0.10:53: no such host
```
✅ **Solution:**
- Use the **GitLab IP address** (`192.168.0.100`) instead of the hostname (`gitlab.ubuntu-01.local`).
- Verify network connectivity inside the Kubernetes cluster using the **debug pod** method.

---

## **Final Summary: Quick Commands**
1️⃣ **Check SSH Connection:**
   ```bash
   ssh -T git@192.168.0.100
   ```
2️⃣ **Deploy a Debug Pod:**
   ```bash
   kubectl run -it --rm debug --image=busybox -- sh
   ```
3️⃣ **Test GitLab Network Connectivity in Debug Pod:**
   ```sh
   ping -c 4 192.168.0.100
   nc -zv 192.168.0.100 22
   wget --spider http://192.168.0.100
   exit
   ```
4️⃣ **Add the GitLab Repository to ArgoCD:**
   ```bash
   argocd repo add git@192.168.0.100:homelab/my-repo.git \
     --ssh-private-key-path ~/.ssh/id_rsa \
     --insecure-skip-server-verification
   ```
5️⃣ **Verify the Repository in ArgoCD:**
   ```bash
   argocd repo list
   ```
6️⃣ **Create an ArgoCD Application:**
   ```bash
   argocd app create my-app \
     --repo git@192.168.0.100:homelab/my-repo.git \
     --path / \
     --dest-server https://kubernetes.default.svc \
     --dest-namespace default
   ```
7️⃣ **Deploy the Application:**
   ```bash
   argocd app sync my-app
   ```

This updated guideline ensures a reliable and structured way to add new GitLab repositories to ArgoCD while handling minimal container environments. 🚀




---

### 🔍 **Issue: ArgoCD Rejecting Absolute Path (`/`)**  
The error:  
```sh
rpc error: code = InvalidArgument desc = application spec for my-app is invalid: InvalidSpecError: Unable to generate manifests in /: rpc error: code = Unknown desc = /: app path is absolute
```
ArgoCD **does not accept absolute paths (`/`)** when specifying the `--path` argument.

---

### ✅ **Solution: Use a Relative Path**  
Instead of `/`, you need to specify the relative path **inside your Git repository** where the Kubernetes manifests (YAML files) exist.

### 🔧 **Steps to Fix**
1. **Verify your repository structure**  
   Check where your Kubernetes manifests (`deployment.yaml`, `service.yaml`, `kustomization.yaml`, etc.) are located:
   ```sh
   git clone git@192.168.0.100:homelab/signature_project.git
   cd signature_project
   tree -L 2
   ```
   Example output:
   ```
   .
   ├── manifests
   │   ├── deployment.yaml
   │   ├── service.yaml
   │   ├── kustomization.yaml
   ├── README.md
   ├── some-other-folder
   ```

2. **Use the correct path**  
   If your YAML files are inside `manifests/`, then update your command:
   ```sh
   argocd app create signature_project \
     --repo git@192.168.0.100:homelab/signature_project.git \
     --path manifests \
     --dest-server https://kubernetes.default.svc \
     --dest-namespace default
   ```

3. **Verify the application status**  
   ```sh
   argocd app get signature_project
   ```

4. **Sync the application**  
   ```sh
   argocd app sync signature_project
   ```

---

### 🔥 **Next Steps**
- Ensure your **repository has Kubernetes manifests** in a structured folder.
- Use **a relative path** in the `--path` argument.
- Run `argocd app get <app-name>` to check if ArgoCD successfully detects your app.

🚀 Now ArgoCD should correctly pull and deploy your manifests!