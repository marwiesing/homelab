# **🚀 From Zero to GitOps: Enhanced Roadmap with Lessons Learned & Next Steps**  

## **🌟 Phase 1: Infrastructure Setup & Preparation**  
The first step was setting up a **robust and automated environment** with **Ansible, GitLab, Docker, Kubernetes, and ArgoCD**. Along the way, we encountered and solved multiple challenges. Here’s a detailed breakdown.

### **✅ Step 1: Setting Up the Virtual Machines & Ansible**  
**🔹 Created & Configured VMs on Proxmox:**  
- **Linux Mint** → Workstation (Control Node)  
- **Ubuntu-1** → Control Plane for Kubernetes + GitLab Server  
- **Ubuntu-2** → Kubernetes Worker Node  
- **Rocky-1** → Kubernetes Worker Node  
- **Debian-1** → Kubernetes Worker Node  

**🔹 Set Up Ansible for Automation**  
- Configured **SSH Key-Based Authentication** across all machines  
- Created an **Ansible inventory file (`inventory.ini`)** for managing all hosts  
- Configured **Ansible `ansible.cfg`** for logging and YAML output  
- Ensured that all VMs were accessible using `ansible all -m ping`  

**🔹 Installed Essential Packages on All Machines**  
Used Ansible to install essential tools across all machines:  
```yaml
- name: Install common packages
  package:
    name:
      - vim
      - curl
      - git
      - htop
      - tmux
      - tree
      - net-tools
      - unzip
    state: present
```
✅ **Challenge Solved:**  
> **Issue:** Missing `sudo` password for running Ansible tasks.  
> **Solution:** Used `--ask-become-pass` and ensured user was in the **sudoers file**.  

---

## **🌟 Phase 2: Installing & Configuring GitLab**  
**🔹 Installed GitLab on Ubuntu-1 using Ansible**  
We used the **Geerlingguy GitLab Ansible Role** to install GitLab:  
```yaml
- name: Install GitLab on Ubuntu-1
  hosts: ubuntu-1
  become: yes
  roles:
    - geerlingguy.gitlab
```
✅ **Challenge Solved:**  
> **Issue:** GitLab installation required a **root user** to log in initially.  
> **Solution:** Retrieved the **root password** using:  
> ```bash
> sudo cat /etc/gitlab/initial_root_password
> ```  

**🔹 Configured GitLab for First Login**  
- Accessed **GitLab Web UI** at `http://192.168.0.100`  
- Created a **new user account**  
- Enabled repositories & SSH access  

✅ **Challenge Solved:**  
> **Issue:** GitLab was accessible in Firefox but **not in Chrome**.  
> **Solution:** Cleared browser cache and checked HTTPS settings.  

---

## **🌟 Phase 3: Installing Docker & Kubernetes**  
**🔹 Installed Docker on All Machines using Ansible**  
To ensure Kubernetes compatibility, we used Ansible to install **Docker CE**:  
```yaml
- name: Install Docker
  package:
    name: docker-ce
    state: present
```
✅ **Challenge Solved:**  
> **Issue:** Docker installation on **Linux Mint** failed due to incorrect repository.  
> **Solution:** Used Ubuntu’s **Focal Release** instead of an auto-detected version.  

**🔹 Installed Kubernetes (kubeadm, kubelet, kubectl) using Ansible**  
We used the **Geerlingguy Kubernetes Role** to install Kubernetes on all nodes:  
```yaml
- name: Install Kubernetes on all nodes
  hosts: all
  become: yes
  roles:
    - geerlingguy.kubernetes
```
✅ **Challenge Solved:**  
> **Issue:** Nodes couldn’t communicate due to missing `br_netfilter`.  
> **Solution:** Added the required sysctl settings:  
> ```yaml
> - name: Load br_netfilter module
>   modprobe:
>     name: br_netfilter
>     state: present
> ```

**🔹 Initialized Kubernetes Cluster on Ubuntu-1 (Control Plane)**
```bash
sudo kubeadm init --pod-network-cidr=192.168.0.0/16
```
✅ **Challenge Solved:**  
> **Issue:** The K8s API server failed due to a **port conflict (6443, 10259, 10257)**.  
> **Solution:** Reset K8s and reinstalled kubeadm:  
> ```bash
> sudo kubeadm reset
> sudo systemctl restart kubelet
> ```

**🔹 Joined Worker Nodes (Ubuntu-2, Rocky-1, Debian-1) to the Cluster**
```bash
sudo kubeadm join 192.168.0.100:6443 --token <TOKEN> --discovery-token-ca-cert-hash sha256:<HASH>
```
✅ **Challenge Solved:**  
> **Issue:** `kubelet` was **not ready** due to network plugin errors.  
> **Solution:** Installed **Weave Net CNI** instead of Calico:  
> ```bash
> kubectl apply -f https://reweave.azurewebsites.net/k8s/v1.32/net.yaml
> ```

---

## **🌟 Phase 4: Helm & ArgoCD Deployment**
**🔹 Installed Helm on Ubuntu-1**
```bash
helm version
```
✅ **Challenge Solved:**  
> **Issue:** Helm repo updates failed.  
> **Solution:** Manually added the repository using:  
> ```bash
> helm repo add stable https://charts.helm.sh/stable
> ```

**🔹 Installed ArgoCD with Helm**
```bash
helm repo add argo https://argoproj.github.io/argo-helm
helm repo update
kubectl create namespace argocd
helm install argocd argo/argo-cd --namespace argocd
```
✅ **Challenge Solved:**  
> **Issue:** ArgoCD’s UI was not accessible.  
> **Solution:** Exposed the service using `NodePort`:  
> ```bash
> kubectl patch svc argocd-server -n argocd -p '{"spec": {"type": "NodePort"}}'
> ```

✅ **Successfully Logged into ArgoCD Web UI!**  

---

# **📌 Next Steps: Remaining To-Do List**
## **🔹 1) Connect ArgoCD to GitLab (Source of Truth)**
🎯 **Goal:** ArgoCD should automatically sync applications from GitLab.

✅ **Tasks:**
- **[ ]** Configure GitLab SSH Access  
- **[ ]** Add SSH Key to GitLab:  
  ```bash
  cat ~/.ssh/id_rsa.pub
  ```
- **[ ]** Add GitLab Repo to ArgoCD  
  ```bash
  argocd repo add git@gitlab.ubuntu-01.local:myuser/myrepo.git --ssh-private-key-path ~/.ssh/id_rsa
  ```

---

## **🔹 2) Configure RBAC & Authentication for Security**
🎯 **Goal:** Secure ArgoCD with proper user access roles.

✅ **Tasks:**
- **[ ]** Define **ArgoCD RBAC Policies**  
- **[ ]** Restrict access to **admins & developers**  
- **[ ]** Enable **OAuth authentication (GitLab SSO)**  

---

## **🔹 3) Run kubectl from Linux Mint (Best Practice)**
🎯 **Goal:** Manage the K8s cluster from the **Linux Mint Workstation** instead of Ubuntu-1.

✅ **Tasks:**
- **[ ]** Install `kubectl` on Linux Mint  
- **[ ]** Copy the K8s config from Ubuntu-1 to Mint:  
  ```bash
  scp ubuntu-1:~/.kube/config ~/.kube/config
  ```
- **[ ]** Verify cluster access:  
  ```bash
  kubectl get nodes
  ```

---

## **🔹 4) Deploy Sample Applications to Test CI/CD**
🎯 **Goal:** Deploy & automate applications using GitLab CI/CD & ArgoCD.

✅ **Tasks:**
- **[ ]** Deploy a simple Nginx app  
- **[ ]** Automate deployments from **GitLab → ArgoCD → Kubernetes**  
- **[ ]** Monitor application rollouts with `kubectl`  

---

🔥 **We're nearly there!** Do you want to start with **GitLab SSH Setup** or **kubectl on Linux Mint** next? 🚀