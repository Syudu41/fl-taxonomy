# FedAvg: one complete round

Silent, captioned original teaching animation. Full participation; honest synchronous clients. Numerical data are invented.

Algorithm source: [McMahan et al., Section 2 and Algorithm 1](https://proceedings.mlr.press/v54/mcmahan17a.html).

**00:00:00.600** — Two honest clients participate. Their raw examples remain local.

**00:00:07.300** — The server sends w = 1 to both clients. Model parameters travel; training data do not.

**00:00:15.000** — Each client takes two full-batch gradient steps with learning rate 0.1.

**00:00:21.100** — Client A: gradient −2 gives 1.20. Client B: gradient −8 gives 1.80.

**00:00:27.800** — The next gradients are evaluated at different local parameters: 1.20 and 1.80.

**00:00:36.500** — Averaging B’s three identical losses leaves the mean loss (2w − 4)².

**00:00:41.100** — Clients return 1.36 and 1.96. The server has not seen their raw examples.

**00:00:49.800** — Full participation: weights are 1/4 and 3/4. They reflect sample counts, not trust.

**00:01:04.000** — The new global model is 1.81. Broadcast it again and repeat until the stopping rule is met.

**00:01:12.200** — Keeping data local is not a privacy guarantee. This example assumes honest, synchronous clients.
