```sh
$ helm get values prometheus -n monitoring --all | grep 9100
      - --web.listen-address=:19100
      - containerPort: 19100
        hostPort: 19100
        name: metrics-19100
  - --web.listen-address=:19100
      port: 19100
      targetPort: 19100
        - 192.168.0.100:19100
        - 192.168.0.240:19100
        - 192.168.0.56:19100
        - 192.168.0.242:19100
    port: 9100
    targetPort: 9100
$ helm template prometheus prometheus-community/kube-prometheus-stack -n monitoring -f current-values.yaml | grep 9100
    - port: 9100
      targetPort: 9100
            - --web.listen-address=[$(HOST_IP)]:9100
              containerPort: 9100
              port: 9100
              port: 9100
```

Step 4: Patch the DaemonSet (If Needed)

If Helm still doesn’t apply 19100, patch the existing DaemonSet:
```sh
kubectl patch daemonset -n monitoring prometheus-prometheus-node-exporter \
  --type='json' -p='[
    {"op": "replace", "path": "/spec/template/spec/containers/0/livenessProbe/httpGet/port", "value": 19100},
    {"op": "replace", "path": "/spec/template/spec/containers/0/readinessProbe/httpGet/port", "value": 19100},
    {"op": "replace", "path": "/spec/template/spec/containers/0/ports/0/containerPort", "value": 19100},
    {"op": "replace", "path": "/spec/template/spec/containers/0/ports/0/name", "value": "metrics-19100"}
  ]'
```

Then restart the pods:
```sh
kubectl rollout restart daemonset -n monitoring prometheus-prometheus-node-exporter
```
Check Service and Endpoint:
```sh
kubectl get endpoints -n monitoring prometheus-prometheus-node-exporter

kubectl patch service -n monitoring prometheus-prometheus-node-exporter \
  --type='json' -p='[
    {"op": "replace", "path": "/spec/ports/0/port", "value": 19100},
    {"op": "replace", "path": "/spec/ports/0/targetPort", "value": 19100}
  ]'
```


If Helm ignores your YAML file, force it using --set:
```sh
helm upgrade --install prometheus prometheus-community/kube-prometheus-stack \
  -n monitoring -f current-values.yaml \
  --set nodeExporter.extraArgs[0]=--path.procfs=/proc \
  --set nodeExporter.extraArgs[1]=--path.sysfs=/sys \
  --set nodeExporter.extraArgs[2]=--web.listen-address=:19100 \
  --set nodeExporter.service.ports[0].port=19100 \
  --set nodeExporter.service.ports[0].targetPort=19100 \
  --set nodeExporter.daemonset.containers[0].args[0]=--web.listen-address=:19100 \
  --set nodeExporter.daemonset.containers[0].ports[0].containerPort=19100 \
  --set nodeExporter.daemonset.containers[0].ports[0].hostPort=19100 \
  --debug
```

node_cpu_seconds_total

315 ➝ Kubernetes Cluster Monitoring
6417 ➝ Kubernetes Cluster Overview
1860 ➝ Node Exporter Full


---
---

## Helm


Wenn dein `helm upgrade` die Änderungen nicht übernimmt, gibt es einige mögliche Ursachen und Lösungen:

---

## **🔍 1. Helm Upgrade richtig ausführen**
Versuche, das Upgrade explizit mit deiner `current-values.yaml` zu erzwingen:

```sh
helm upgrade prometheus prometheus-community/prometheus -n monitoring -f current-values.yaml --debug --atomic
```

### **Wichtige Flags:**
- `--debug` → Zeigt detaillierte Informationen an, falls Helm die Werte ignoriert.
- `--atomic` → Falls das Upgrade fehlschlägt, wird der alte Zustand beibehalten.

Falls `--debug` anzeigt, dass deine `values.yaml` ignoriert wird, kannst du das mit **`helm get values`** gegenchecken:

```sh
helm get values prometheus -n monitoring
```

Falls dort noch `targetPort: 9100` steht, könnte ein lokaler Cache oder ein vorheriges Helm-Release stören.

---

## **🛠 2. Alte Helm-Werte zurücksetzen**
Falls sich alte Werte festgesetzt haben, kannst du die Standardwerte überschreiben:

```sh
helm upgrade prometheus prometheus-community/prometheus -n monitoring --reset-values -f current-values.yaml
```

Falls das nicht hilft, könnte ein komplettes Löschen und Neuinstallieren helfen:

```sh
helm uninstall prometheus -n monitoring
helm install prometheus prometheus-community/prometheus -n monitoring -f current-values.yaml
```

---

## **🔄 3. Verhindert Helm eine Änderung am Service?**
Manchmal blockiert Helm Änderungen an bestehenden Services (`Service`-Resource in `nodeExporter`). Falls `targetPort` nicht übernommen wird, kannst du das Service-Manifest direkt prüfen:

```sh
kubectl get service -n monitoring prometheus-prometheus-node-exporter -o yaml
```

Falls dort noch `9100` steht, kannst du testen, ob ein Helm-Managed Label gesetzt ist:

```sh
kubectl annotate service -n monitoring prometheus-prometheus-node-exporter meta.helm.sh/release-name=prometheus --overwrite
```

Danach erzwinge nochmal ein `helm upgrade`.

---

## **🛠 4. Werte direkt im Chart überschreiben**
Falls `helm upgrade` die Werte nicht übernimmt, kannst du sie direkt im Chart setzen. Falls du `helm show values` prüfst:

```sh
helm show values prometheus-community/prometheus | grep nodeExporter -A 10
```

Falls `nodeExporter` andere Default-Werte nutzt, versuche sie mit einem `set`-Befehl zu überschreiben:

```sh
helm upgrade prometheus prometheus-community/prometheus -n monitoring \
  --set nodeExporter.service.ports[0].targetPort=19100 \
  --set nodeExporter.service.ports[0].port=19100
```

Danach nochmal die Werte checken:

```sh
helm get values prometheus -n monitoring
```

---

## **🚀 Fazit**
- **`helm upgrade` mit `-f current-values.yaml` erneut ausführen** (mit `--debug` prüfen).
- **Falls Werte nicht übernommen werden**, `helm upgrade --reset-values -f current-values.yaml`.
- **Falls das nicht hilft**, `helm uninstall` und `helm install` neu durchführen.
- **Falls Helm Services nicht updated**, prüfe mit `kubectl get service` und überschreibe Labels.

Falls das Problem weiterhin besteht, poste das Ergebnis von:

```sh
kubectl get service -n monitoring prometheus-prometheus-node-exporter -o yaml
helm get values prometheus -n monitoring
```
