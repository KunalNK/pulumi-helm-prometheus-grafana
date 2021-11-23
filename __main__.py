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

