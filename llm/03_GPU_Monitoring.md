Yes! You can monitor GPU usage in **real-time** using the following tools:

### **1. Watch `nvidia-smi` (Terminal)**
Run:
```bash
watch -n 1 nvidia-smi
```
This updates `nvidia-smi` **every second**, showing GPU usage, memory usage, and processes in real-time.

Press **`Ctrl + C`** to stop.

---

### **2. Use `nvidia-smi dmon` (Detailed Monitoring)**
For a more detailed, **per-second breakdown**:
```bash
nvidia-smi dmon
```
This will show:
- GPU Utilization
- Memory Usage
- Power Consumption
- GPU Temperature  
Press **`Ctrl + C`** to stop.

---

### **3. Use `gpustat` (Better Readability)**
Install `gpustat` for a **cleaner real-time GPU summary**:
```bash
pip install gpustat
```
Run:
```bash
gpustat --interval 1
```
This will show a **real-time view** of GPU usage.

---

### **4. Use `htop` for CPU + GPU Monitoring**
Install `htop`:
```bash
sudo apt install htop
```
Run:
```bash
htop
```
Press **`F2`** → **Enable GPU Metrics** (if supported).

---

### **5. Use `nvtop` (Graphical GPU Monitor)**
For a **graphical, real-time GPU monitor**, install **nvtop**:
```bash
sudo apt install nvtop
```
Run:
```bash
nvtop
```
This will show a **real-time bar graph** of GPU usage.

---

### **🔹 Recommended: `watch -n 1 nvidia-smi` (Quick & Simple)**
For real-time DeepSeek monitoring, just run:
```bash
watch -n 1 nvidia-smi
```
This will let you see how much **VRAM** DeepSeek is using as you interact with it.

---

💡 **Which one do you prefer? Need help setting up `gpustat` or `nvtop`?** 🚀