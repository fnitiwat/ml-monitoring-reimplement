import os
import random
import numpy as np
from typing import Callable
from prometheus_client import Histogram
from prometheus_fastapi_instrumentator import Instrumentator, metrics
from prometheus_fastapi_instrumentator.metrics import Info


NAMESPACE = os.environ.get("METRICS_NAMESPACE", "fastapi")
SUBSYSTEM = os.environ.get("METRICS_SUBSYSTEM", "model")


instrumentator = Instrumentator(
    # should_group_status_codes=True,
    # should_ignore_untemplated=True,
    # should_respect_env_var=True,
    # should_instrument_requests_inprogress=True,
    # excluded_handlers=["/metrics"],
    # env_var_name="ENABLE_METRICS",
    # inprogress_name="fastapi_inprogress",
    # inprogress_labels=True,
)

# TODO:
# custom metric
# avg class per sec (couter)
# process time (instant vector)
# pred prob lower than threshold (alert) (histogram)
def pred_prob_model_output(
    metric_name: str = "pred_prob_model_output",
    metric_doc: str = "pred_prob_model_output",
    metric_namespace: str = "",
    metric_subsystem: str = "",
    buckets=(0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, float("inf")),
) -> Callable[[Info], None]:
    METRIC = Histogram(
        metric_name,
        metric_doc,
        buckets=buckets,
    )
    def instrumentation(info: Info) -> None:
        if info.modified_handler == "/predict":
            # pred_prob = info.response.body
            pred_prob = random.uniform(0, 1)
            if pred_prob:
                METRIC.observe(float(pred_prob))

    return instrumentation


instrumentator.add(
    pred_prob_model_output(metric_namespace=NAMESPACE, metric_subsystem=SUBSYSTEM)
)

instrumentator.add(
    metrics.request_size(
        should_include_handler=True,
        should_include_method=True,
        should_include_status=True,
        metric_namespace=NAMESPACE,
        metric_subsystem=SUBSYSTEM,
    )
)
instrumentator.add(
    metrics.response_size(
        should_include_handler=True,
        should_include_method=True,
        should_include_status=True,
        metric_namespace=NAMESPACE,
        metric_subsystem=SUBSYSTEM,
    )
)
instrumentator.add(
    metrics.latency(
        should_include_handler=True,
        should_include_method=True,
        should_include_status=True,
        metric_namespace=NAMESPACE,
        metric_subsystem=SUBSYSTEM,
    )
)
instrumentator.add(
    metrics.requests(
        should_include_handler=True,
        should_include_method=True,
        should_include_status=True,
        metric_namespace=NAMESPACE,
        metric_subsystem=SUBSYSTEM,
    )
)