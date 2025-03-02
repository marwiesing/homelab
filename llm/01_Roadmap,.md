### 🚀 **Roadmap for Running DeepSeek LLM & DeepSeek Coder Locally on Linux Mint VM**  
Your goal is to run **DeepSeek LLM** and **DeepSeek Coder** in **Docker** on your **Linux Mint VM** with your **GTX 1080** GPU. Here's a structured roadmap:

---

## **🔹 1. System Preparation**
Before setting up DeepSeek, ensure your system is ready:
✅ **NVIDIA Driver & CUDA Check (Done)**
✅ **Virtual Environment (Done, but not needed for Docker)**
✅ **Install Docker & NVIDIA Container Toolkit**
```bash
sudo apt update && sudo apt install -y docker.io
```
**Enable Docker & Add User**  
```bash
sudo systemctl enable --now docker
sudo usermod -aG docker $USER
newgrp docker
```
**Install NVIDIA Docker Toolkit**
```bash
distribution=$(. /etc/os-release;echo $ID$VERSION_ID) && \
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add - && \
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
sudo apt update
sudo apt install -y nvidia-container-toolkit
sudo systemctl restart docker
```
**Test GPU with Docker:**
```bash
docker run --rm --gpus all nvidia/cuda:12.0-base nvidia-smi
```
---

## **🔹 2. Running DeepSeek LLM in Docker**
DeepSeek LLM is available via **Ollama**. Install **Ollama** and pull the model.

### **Install Ollama**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```
### **Start Ollama and Pull DeepSeek-R1**
```bash
ollama pull deepseek-r1
```
### **Run DeepSeek LLM**
```bash
ollama run deepseek-r1
```
**Verify it runs correctly** before moving to DeepSeek Coder.

---

## **🔹 3. Running DeepSeek Coder in Docker**
DeepSeek Coder is available via **Ollama** as well.

### **Pull and Run DeepSeek Coder**
```bash
ollama pull deepseek-coder
```
```bash
ollama run deepseek-coder
```

---

## **🔹 4. (Optional) Setting Up LM Studio for UI Access**
LM Studio provides a UI to interact with models.

### **Download & Install LM Studio**
[🔗 LM Studio Download](https://lmstudio.ai/)  
- Install the **Linux AppImage**
- **Run:**  
  ```bash
  chmod +x LMStudio.AppImage
  ./LMStudio.AppImage
  ```
- Configure **DeepSeek LLM** and **DeepSeek Coder** in the UI.

---

## **🔹 5. (Optional) VS Code Integration for DeepSeek Coder**
To integrate **DeepSeek Coder** with VS Code:
- Install the [DeepSeek Coder Extension](https://marketplace.visualstudio.com/items?itemName=deepseek.coder)
- Configure Ollama as a backend:
  ```json
  {
    "deepseek.model": "deepseek-coder",
    "deepseek.server": "http://localhost:11434"
  }
  ```
- Restart VS Code and test code completions.

---

## **🔹 6. Testing & Optimization**
✅ **Test DeepSeek LLM & DeepSeek Coder in the terminal**  
✅ **Check GPU usage:**  
```bash
nvidia-smi
```
✅ **Monitor Docker containers:**  
```bash
docker ps
```
✅ **Adjust model performance if needed** (e.g., set max GPU memory usage)

---

## **🔹 7. Automate & Persist Setup**
- **Create a Docker Compose file** for easy management.
- **Set up a script to start models on boot**.

---

### 🎯 **Next Steps**
1. **Try the Ollama models manually**
2. **Check GPU load with `nvidia-smi` while running DeepSeek**
3. **Decide if you want LM Studio UI or just CLI**
4. **Integrate with VS Code if needed**
5. **Optimize performance**

---

### **💡 Let me know which step you want to focus on first!** 🚀