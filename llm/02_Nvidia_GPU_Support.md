### **🚀 Summary: Fixing NVIDIA GPU Support in Docker on a New VM**  

If you face **NVIDIA GPU issues in Docker** on your next VM, follow these steps to **quickly fix it**:

---

### **1️⃣ Install NVIDIA Container Toolkit**
Manually download and install the required packages:

```bash
# Download NVIDIA Container Toolkit and dependencies
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/libnvidia-container1_1.14.0-1_amd64.deb
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/libnvidia-container-tools_1.14.0-1_amd64.deb
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/nvidia-container-toolkit-base_1.14.0-1_amd64.deb
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/nvidia-container-toolkit_1.14.0-1_amd64.deb

# Install the packages
sudo dpkg -i libnvidia-container1_1.14.0-1_amd64.deb
sudo dpkg -i libnvidia-container-tools_1.14.0-1_amd64.deb
sudo dpkg -i nvidia-container-toolkit-base_1.14.0-1_amd64.deb
sudo dpkg -i nvidia-container-toolkit_1.14.0-1_amd64.deb

# Verify the installation
nvidia-container-cli --version
```

---

### **2️⃣ Configure Docker to Use NVIDIA Runtime**
If `/etc/docker/daemon.json` does not exist, create it:

```bash
sudo tee /etc/docker/daemon.json > /dev/null <<EOF
{
  "runtimes": {
    "nvidia": {
      "path": "/usr/bin/nvidia-container-runtime",
      "runtimeArgs": []
    }
  },
  "default-runtime": "nvidia"
}
EOF
```

---

### **3️⃣ Restart Docker**
Apply the new configuration:

```bash
sudo systemctl restart docker
sudo systemctl status docker
```

---

### **4️⃣ Pull and Run a CUDA Image**
**⚠️ `nvidia/cuda:latest` is not available! Use a specific version.**

Find available CUDA images:

```bash
curl -s https://hub.docker.com/v2/repositories/nvidia/cuda/tags/ | jq '.results[].name'
```

Pull a working image (e.g., CUDA 12.1.1 with Ubuntu 22.04):

```bash
docker pull nvidia/cuda:12.1.1-runtime-ubuntu22.04
```

Run **NVIDIA-SMI** inside the container:

```bash
docker run --rm --gpus all nvidia/cuda:12.1.1-runtime-ubuntu22.04 nvidia-smi
```

**Expected output:**  
- Shows **CUDA version**
- Detects **GPU (e.g., GTX 1080)**
- Confirms **driver compatibility**

---

### **✅ Quick Check if GPU is Working**
```bash
nvidia-smi
docker run --rm --gpus all nvidia/cuda:12.1.1-runtime-ubuntu22.04 nvidia-smi
```

---

### **🎯 Next Steps**
- If setting up **DeepSeek LLM**, use this CUDA image as your base.
- If PyTorch is needed, install it inside a container:
  ```bash
  docker run --rm --gpus all -it nvidia/cuda:12.1.1-runtime-ubuntu22.04 bash
  pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
  python -c "import torch; print(torch.cuda.is_available())"
  ```

---

### **🔥 TL;DR**
1. **Install NVIDIA Container Toolkit**
2. **Configure Docker to use NVIDIA runtime**
3. **Restart Docker**
4. **Pull a valid CUDA image**
5. **Run `nvidia-smi` inside Docker**

---

Now, when you set up your next VM, just **copy-paste these steps** and you’ll be up and running in no time! 🚀💡