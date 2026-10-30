# FedAvg: one complete round

Silent, captioned original teaching animation. Full participation; honest synchronous clients. Numerical data are invented.

Motion between local-step endpoints is visual interpolation, not additional optimization steps. The merging dots illustrate the weighted mean geometrically.

Algorithm source: [McMahan et al., Section 2 and Algorithm 1](https://proceedings.mlr.press/v54/mcmahan17a.html).

**00:00:00.000** — Two clients keep their data locally; the server coordinates one shared model.

**00:00:05.650** — Broadcast the same parameter to both clients: each starts at w = 1.

**00:00:13.150** — Use the model y = wx and mean squared error; take two local gradient steps.

**00:00:20.300** — First step: gradients -2 and -8 give different local updates.

**00:00:26.450** — Second step: both gradients are now -1.6. The endpoints are 1.36 and 1.96.

**00:00:33.800** — Clients send their final model parameters; their training examples stay local.

**00:00:42.250** — Full participation: one example at A, three at B. Their weights are 1/4 and 3/4.

**00:00:51.400** — The weighted mean is 1.81: three times closer to B than to A.

**00:01:00.850** — Broadcast w = 1.81. Repeat local training and aggregation until the chosen stopping rule.

**00:01:09.250** — Keeping data local is not a privacy guarantee: model updates can still reveal information.
