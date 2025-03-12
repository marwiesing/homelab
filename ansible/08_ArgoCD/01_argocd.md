```bash

marwiesing@ubuntu:~$ helm version
version.BuildInfo{Version:"v3.17.1", GitCommit:"980d8ac1939e39138101364400756af2bdee1da5", GitTreeState:"clean", GoVersion:"go1.23.5"}

marwiesing@ubuntu:~$ helm repo add argo https://argoproj.github.io/argo-helm
"argo" has been added to your repositories

marwiesing@ubuntu:~$ helm repo update
Hang tight while we grab the latest from your chart repositories...
...Successfully got an update from the "argo" chart repository
Update Complete. ⎈Happy Helming!⎈

marwiesing@ubuntu:~$ kubectl create namespace argocd
namespace/argocd created

marwiesing@ubuntu:~$ helm install argocd argo/argo-cd --namespace argocd
NAME: argocd
LAST DEPLOYED: Sat Feb 22 20:10:30 2025
NAMESPACE: argocd
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
In order to access the server UI you have the following options:

1. kubectl port-forward service/argocd-server -n argocd 8080:443

    and then open the browser on http://localhost:8080 and accept the certificate

2. enable ingress in the values file `server.ingress.enabled` and either
      - Add the annotation for ssl passthrough: https://argo-cd.readthedocs.io/en/stable/operator-manual/ingress/#option-1-ssl-passthrough
      - Set the `configs.params."server.insecure"` in the values file and terminate SSL at your ingress: https://argo-cd.readthedocs.io/en/stable/operator-manual/ingress/#option-2-multiple-ingress-objects-and-hosts


After reaching the UI the first time you can login with username: admin and the random password generated during the installation. You can find the password by running:

kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d

(You should delete the initial secret afterwards as suggested by the Getting Started Guide: https://argo-cd.readthedocs.io/en/stable/getting_started/#4-login-using-the-cli)

marwiesing@ubuntu:~$ kubectl get pods -n argocd
NAME                                                READY   STATUS    RESTARTS   AGE
argocd-application-controller-0                     1/1     Running   0          117s
argocd-applicationset-controller-5d597bcf96-ljjq8   1/1     Running   0          117s
argocd-dex-server-54556bfdcc-68klh                  1/1     Running   0          117s
argocd-notifications-controller-d5f5b55b4-xx59z     1/1     Running   0          117s
argocd-redis-7df98f7b57-lwcz4                       1/1     Running   0          117s
argocd-repo-server-5bb8b9c494-bqw2g                 1/1     Running   0          117s
argocd-server-95cd75b5c-r9snl                       1/1     Running   0          117s

marwiesing@ubuntu:~$ kubectl patch svc argocd-server -n argocd -p '{"spec": {"type": "NodePort"}}'
service/argocd-server patched

marwiesing@ubuntu:~$ kubectl get svc -n argocd
NAME                               TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)                      AGE
argocd-applicationset-controller   ClusterIP   10.99.191.81     <none>        7000/TCP                     2m44s
argocd-dex-server                  ClusterIP   10.109.173.2     <none>        5556/TCP,5557/TCP            2m44s
argocd-redis                       ClusterIP   10.108.194.247   <none>        6379/TCP                     2m44s
argocd-repo-server                 ClusterIP   10.101.244.11    <none>        8081/TCP                     2m44s
argocd-server                      NodePort    10.104.199.254   <none>        80:30189/TCP,443:31272/TCP   2m44s

marwiesing@ubuntu:~$ kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
SR-gCeJKOUPEhlIN
Xcfv8rm9VWvCWOIh -- new
```