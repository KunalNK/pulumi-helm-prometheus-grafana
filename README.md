
# Deploying Prometheus & Grafana application on Kubernetes Cluster using Pulumi & Helm Charts.

## Prerequisites
```
1. A running Kubernetes Cluster.
2. kubectl cli.
3. helm package manager.
4. Pulumi tool.
5. Add the stable repo "helm repo add stable https://charts.helm.sh/stable"

```

1. Create a directory:

```
mkdir pulumi-helm-prometheus-grafana && cd pulumi-helm-prometheus-grafana

```

2. Now inside the directory "pulumi-helm-prometheus-grafana" run the following command to fetch prometheus & grafana repo.

```
helm fetch --untar stable/prometheus

helm fetch --untar stable/grafana

```
3. Create a new Pulumi project:

```
pulumi new kubernetes-python --force

```
4. Next, replace the contents of __main__.py file with the following code.

```
from pulumi_kubernetes.helm.v3 import Chart, LocalChartOpts

prometheus = Chart(
    "prometheus",
    LocalChartOpts(
        path="C:/Users/kunal/pulumi-tutorials/pulumi-helm/helm-prom-grafana/prometheus",
    ),
)

grafana = Chart(
    "grafana",
    LocalChartOpts(
        path="C:/Users/kunal/pulumi-tutorials/pulumi-helm/helm-prom-grafana/grafana",
    ),
)

```

5. Now, go to grafana folder & open the values.yaml file to change the service type to "LoadBalancer" & customize the grafana login password as shown below
```
## Expose the grafana service to be accessed from outside the cluster (LoadBalancer service).
## or access it from within the cluster (ClusterIP service). Set the service type and the port to serve it.
## ref: http://kubernetes.io/docs/user-guide/services/
##
service:
  type: LoadBalancer
  port: 80
  targetPort: 3000
```

```
# Administrator credentials when not using an existing secret (see below)
adminUser: admin
adminPassword: "admin"

```
6. Similarly, go to prometheus folder & open the values.yaml file to change service type to "LoadBalancer" as shown below

```
## List of IP addresses at which the Prometheus server service is available
## Ref: https://kubernetes.io/docs/user-guide/services/#external-ips
    ##
    externalIPs: []

    loadBalancerIP: ""
    loadBalancerSourceRanges: []
    servicePort: 9090
    sessionAffinity: None
    type: LoadBalancer
    
```

7. Run `pulumi up` to preview and deploy changes.  After the preview is shown you will be
    prompted if you want to continue or not.
```
 +   pulumi:pulumi:Stack                                                    Testing-dev                            creating.      
 +   │  ├─ kubernetes:rbac.authorization.k8s.io/v1beta1:ClusterRole         prometheus-kube-state-metrics          created        
 +   │  ├─ kubernetes:rbac.authorization.k8s.io/v1beta1:ClusterRole         prometheus-alertmanager                created        
 +   ├─ kubernetes:helm.sh/v3:Chart                                         prometheus                             creating       
 +   │  ├─ kubernetes:rbac.authorization.k8s.io/v1beta1:ClusterRoleBinding  prometheus-kube-state-metrics          created        
 +   │  ├─ kubernetes:rbac.authorization.k8s.io/v1beta1:ClusterRole         prometheus-pushgateway                 created        
 +   pulumi:pulumi:Stack                                                    Testing-dev                            creating.      
 +   pulumi:pulumi:Stack                                                    Testing-dev                            created     1  
 +   │  ├─ kubernetes:rbac.authorization.k8s.io/v1beta1:ClusterRoleBinding  prometheus-pushgateway                 created        
 +   │  ├─ kubernetes:apps/v1:DaemonSet                                     default/prometheus-node-exporter       created        
 +   │  ├─ kubernetes:core/v1:ServiceAccount                                default/prometheus-kube-state-metrics  created        
 +   │  ├─ kubernetes:core/v1:ServiceAccount                                default/prometheus-alertmanager        created        
 +   │  ├─ kubernetes:core/v1:ServiceAccount                                default/prometheus-node-exporter       created        
 +   │  ├─ kubernetes:core/v1:ServiceAccount                                default/prometheus-pushgateway         created        
 +   │  ├─ kubernetes:core/v1:ServiceAccount                                default/prometheus-server              created        
 +   │  ├─ kubernetes:core/v1:ConfigMap                                     default/prometheus-alertmanager        created        
 +   │  ├─ kubernetes:core/v1:ConfigMap                                     default/prometheus-server              created        
 +   │  ├─ kubernetes:core/v1:PersistentVolumeClaim                         default/prometheus-alertmanager        created        
 +   │  ├─ kubernetes:core/v1:PersistentVolumeClaim                         default/prometheus-server              created  

```


8. Now, verify the status of pods running inside the kubernetes cluster by running the following command.

```
kubectl get po

```
Output:

```
NAME                                             READY   STATUS    RESTARTS   AGEgrafana-5c68c78f6d-wtf6f                      1/1     Running   0          6m14s
prometheus-alertmanager-679cdb7745-6bhq9         2/2     Running   0          6m13s
prometheus-kube-state-metrics-5f89586745-6tvlr   1/1     Running   0          6m13s
prometheus-node-exporter-ckgb5                   1/1     Running   0          6m21sprometheus-pushgateway-ccd864fc6-8btrk      1/1     Running   0          6m11s
prometheus-server-544c49b55c-xphgj               2/2     Running   0          6m10s

```
9. Now, check the service type, by running the following command.

```
kubectl get svc

```
Output:

```
NAME                            TYPE           CLUSTER-IP       EXTERNAL-IP      PORT(S)          AGEgrafana                      LoadBalancer   10.245.134.170   167.172.14.91    3000:30724/TCP   7m6s
kubernetes                      ClusterIP      10.245.0.1       <none>           443/TCP          12m
prometheus-alertmanager         NodePort       10.245.126.149   <none>           80:30000/TCP     6m58s
prometheus-kube-state-metrics   ClusterIP      10.245.252.54    <none>           8080/TCP         7m1s
prometheus-node-exporter        ClusterIP      None             <none>           9100/TCP         6m58s
prometheus-pushgateway          ClusterIP      10.245.55.43     <none>           9091/TCP         6m57s
prometheus-server               LoadBalancer   10.245.90.226    137.184.240.61   80:32662/TCP     6m57s

```
10. Copy the EXTERNAL-IP of prometheus & grafana server, paste in the browser to see the output of prometheus server.(Note: Prometheus server accessible at port 80 & Grafana server at port 3000)

11. To clean up resources, run `pulumi destroy` and answer the confirmation question at the prompt.
