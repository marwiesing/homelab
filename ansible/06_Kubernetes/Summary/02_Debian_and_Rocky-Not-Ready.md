Below is a detailed summary of the issue we encountered and a step-by-step guide you can follow in the future if you need to reset your VMs and Kubernetes cluster.

---

### **Summary of the Issue**

**Problem:**  
Your two worker nodes (debian-1 and rocky-1) were reporting as “NotReady” in the cluster. On closer inspection, the nodes and several critical system pods (like kube-proxy and weave-net) were failing to start. The error messages indicated that the container runtime’s network wasn’t ready, with a recurring error stating:  
```
open /run/systemd/resolve/resolv.conf: no such file or directory
```

**Cause:**  
The CNI plugin (in this case, weave-net) was expecting a DNS configuration file at `/run/systemd/resolve/resolv.conf`, which did not exist on your system. This misconfiguration prevented the plugin from initializing, thereby blocking network communication between your worker nodes and the control plane.

---

### **Step-by-Step Troubleshooting and Resolution Guide**

1. **Verify Node and Pod Status:**
   - Run the following commands to inspect node conditions and identify the error:
     ```bash
     kubectl get nodes -o wide
     kubectl describe node <node-name>
     ```
   - Check the conditions under each node. You may see an error like:
     ```
     container runtime network not ready: Network plugin returns error: cni plugin not initialized
     ```

2. **Inspect Pod Events:**
   - Look at the logs and events for the affected pods (e.g., kube-proxy and weave-net) using:
     ```bash
     kubectl describe pod kube-proxy-<pod-id> -n kube-system
     kubectl describe pod weave-net-<pod-id> -n kube-system
     ```
   - Notice recurring errors mentioning the missing `/run/systemd/resolve/resolv.conf`.

3. **Check for the Missing DNS File:**
   - Log in to each affected worker node (debian-1 and rocky-1) and verify if the file exists:
     ```bash
     ls -l /run/systemd/resolve/resolv.conf
     ```
   - If the file is missing, it confirms that the CNI plugin cannot find the DNS configuration it needs.

4. **Create the Expected Directory and Symlink:**
   - **Create the Directory:**
     ```bash
     sudo mkdir -p /run/systemd/resolve
     ```
   - **Create the Symlink:**  
     Link your existing DNS configuration from `/etc/resolv.conf` to the expected location:
     ```bash
     sudo ln -s /etc/resolv.conf /run/systemd/resolve/resolv.conf
     ```
   - Verify that the symlink was created:
     ```bash
     ls -l /run/systemd/resolve/resolv.conf
     ```
     You should see an output like:
     ```
     lrwxrwxrwx 1 root root 16 ... /run/systemd/resolve/resolv.conf -> /etc/resolv.conf
     ```

5. **Restart Container Runtime and Kubelet:**
   - Restart containerd:
     ```bash
     sudo systemctl restart containerd
     ```
   - Restart the kubelet service:
     ```bash
     sudo systemctl restart kubelet
     ```

6. **Verify the Fix:**
   - On your control-plane node, run:
     ```bash
     kubectl get nodes -o wide
     ```
   - Confirm that all nodes, including debian-1 and rocky-1, are now in the **Ready** state.
   - Check that system pods (kube-proxy, weave-net, etc.) have moved past the ContainerCreating/Initializing phases:
     ```bash
     kubectl get pods -n kube-system -o wide
     ```

7. **Additional Debugging (if needed):**
   - If the issue persists, review the logs for kubelet and containerd:
     ```bash
     journalctl -u kubelet
     journalctl -u containerd
     ```
   - Ensure there are no other errors or misconfigurations, especially around your CNI plugin or firewall settings.

---

### **Future VM and Cluster Resets**

When resetting your VMs and Kubernetes cluster in the future, keep this guide handy. Before deploying your cluster, verify that:
- Your DNS configuration file (`/etc/resolv.conf`) is correct.
- The expected directory `/run/systemd/resolve` exists or is properly linked.
- Only one CNI plugin is active (avoid conflicts if you previously had both Calico and weave-net installed).

By following these steps, you should be able to quickly identify and resolve any issues related to CNI initialization and ensure that your worker nodes can successfully join the cluster and communicate with the control-plane.

---

This comprehensive guide should help you replicate the solution efficiently whenever needed.