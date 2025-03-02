To schedule your `argocd-server` pod on the `ubuntu-2` node, you'll need to:

1. **Add a taint to `ubuntu-2`** so that only pods with the appropriate tolerations can be scheduled there.
2. **Update the ArgoCD Server deployment** to include:
   - A **toleration** that allows it to run on `ubuntu-2`.
   - A **node affinity rule** that prefers `ubuntu-2`.

### **Step 1: Add a Taint to `ubuntu-2`**
Run the following command to taint the `ubuntu-2` node:

```sh
kubectl taint nodes ubuntu-2 key=value:NoSchedule
```

This prevents any pods from being scheduled on `ubuntu-2` unless they have a matching toleration.

### **Step 2: Patch the ArgoCD Server Deployment**
You need to modify the `argocd-server` deployment to include both **tolerations** and **node affinity**.

#### **Option 1: Patch Deployment Directly**
You can patch it directly using:

```sh
kubectl patch deployment argocd-server -n argocd --type='merge' -p '{
  "spec": {
    "template": {
      "spec": {
        "tolerations": [
          {
            "key": "key",
            "operator": "Equal",
            "value": "value",
            "effect": "NoSchedule"
          }
        ],
        "affinity": {
          "nodeAffinity": {
            "requiredDuringSchedulingIgnoredDuringExecution": {
              "nodeSelectorTerms": [
                {
                  "matchExpressions": [
                    {
                      "key": "kubernetes.io/hostname",
                      "operator": "In",
                      "values": ["ubuntu-2"]
                    }
                  ]
                }
              ]
            }
          }
        }
      }
    }
  }
}'
```

#### **Option 2: Edit the Deployment YAML**
Alternatively, edit the deployment manually:

```sh
kubectl edit deployment argocd-server -n argocd
```

Add the following under `spec.template.spec`:

```yaml
tolerations:
  - key: "key"
    operator: "Equal"
    value: "value"
    effect: "NoSchedule"

affinity:
  nodeAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
      nodeSelectorTerms:
        - matchExpressions:
            - key: "kubernetes.io/hostname"
              operator: In
              values:
                - "ubuntu-2"
```

### **Step 3: Restart the Pod**
To apply the changes, delete the existing pod so it gets rescheduled:

```sh
kubectl delete pod -l app.kubernetes.io/name=argocd-server -n argocd
```

This should cause the new pod to be scheduled on `ubuntu-2`.

### **Step 4: Verify the Changes**
Check if the new pod is running on `ubuntu-2`:

```sh
kubectl get pods -o wide -n argocd
```

Also, ensure the tolerations and affinity were applied correctly:

```sh
kubectl describe pod <argocd-server-pod-name> -n argocd | grep -A5 "Tolerations"
kubectl describe pod <argocd-server-pod-name> -n argocd | grep -A5 "Node-Selectors"
```
