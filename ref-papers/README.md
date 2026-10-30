# Reference papers

This folder stores reading copies. The website should cite individual claims with a paper and section/page, rather than linking a bibliography alone. Local availability does not establish permission to republish a PDF; public pages can link to the official source.

## P001 — FedAvg

- Title: Communication-Efficient Learning of Deep Networks from Decentralized Data
- Authors: H. Brendan McMahan, Eider Moore, Daniel Ramage, Seth Hampson, Blaise Agüera y Arcas
- Venue: AISTATS 2017, PMLR 54, pp. 1273–1282
- Official record: https://proceedings.mlr.press/v54/mcmahan17a.html
- PDF source: https://proceedings.mlr.press/v54/mcmahan17a/mcmahan17a.pdf
- Local filename: `mcmahan-2017-fedavg.pdf`
- Start with: Section 2, especially Algorithm 1. Read Section 3 for experimental context before generalizing results.
- Role: primary source for the first algorithm study.

## P002 — FL research map

- Title: Advances and Open Problems in Federated Learning
- Authors: Peter Kairouz et al.
- Venue: Foundations and Trends in Machine Learning, 14(1–2), pp. 1–210, 2021
- DOI: https://doi.org/10.1561/2200000083
- Author manuscript: https://arxiv.org/abs/1912.04977v3
- PDF source: https://arxiv.org/pdf/1912.04977v3
- Local filename: `kairouz-2021-fl-open-problems-arxiv-v3.pdf`
- Version: arXiv v3, 9 March 2021; distinguish manuscript pagination from publisher pagination.
- Role: survey for organizing topics and finding original papers; not an exhaustive account of subsequent work.

## P003 — Recent architecture, synchronization, and security review

- Title: A Survey of Federated Learning: Advances in Architecture, Synchronization, and Security Threats
- Authors: Faisal Mahmud, Fahim Mahmud, Rashedur M. Rahman
- Venue: Computers, Materials & Continua
- Dates: publisher PDF published online 11 December 2025; issue listing is volume 86, issue 3, 2026. These refer to different publication stages.
- DOI: https://doi.org/10.32604/cmc.2025.073519
- PDF source: https://file.techscience.com/uploads/attached/file/20251211/20251211162907_74245.pdf
- Local filename: `mahmud-2025-fl-architecture-synchronization-security.pdf`
- Download status: not stored locally; publisher download returned HTTP 403. The PDF was accessible for reading through the web tool; use the source link above.
- Scope: architecture, synchronization, security, and a review of research from 2023–2025.
- Start with: Section 3 (taxonomy), Section 5 (fundamentals), and Section 8 (privacy and security).
- Role: a recent companion to P002 for developing the website's topic map.

## P004 — Privacy attacks and defenses

- Title: The Federation Strikes Back: A Survey of Federated Learning Privacy Attacks, Defenses, Applications, and Policy Landscape
- Authors: Joshua C. Zhao et al.
- Status: accepted to ACM Computing Surveys, as recorded on the author manuscript page.
- DOI: https://doi.org/10.1145/3724113
- Author manuscript: https://arxiv.org/abs/2405.03636v3
- Dates: first submitted 6 May 2024; v3 revised 22 March 2025.
- PDF source: https://arxiv.org/pdf/2405.03636v3
- Local filename: `zhao-2025-federation-strikes-back-arxiv-v3.pdf`
- Scope: privacy attacks, defenses, limitations, applications, and policy.
- Role: suggested first specialized survey for the secure-FL research direction.

## P005 — Security and privacy overview (preprint)

- Title: On the Security and Privacy of Federated Learning: A Survey with Attacks, Defenses, Frameworks, Applications, and Future Directions
- Authors: Daniel M. Jimenez-Gutierrez et al.
- Status: arXiv preprint; the consulted arXiv record does not identify a journal/conference publication.
- Version/date: v1, 19 August 2025.
- Author manuscript: https://arxiv.org/abs/2508.13730v1
- PDF source: https://arxiv.org/pdf/2508.13730v1
- Local filename: `jimenez-gutierrez-2025-fl-security-privacy-arxiv-v1.pdf`
- Scope: security attacks and defenses, privacy techniques, frameworks, and non-IID-related trade-offs.
- Role: additional recent coverage; verify particular claims against the original studies.

The newer entries were selected by checking their abstracts and publication/version metadata, not by completing a critical review of their full contents. This is a reading shortlist, not an exhaustive or ranked survey bibliography. Metadata checked: 2026-10-22.

## Evidence record to use in future concept pages

For each claim, record: claim ID, wording, source ID, section/page/algorithm, applicable assumptions, and whether it is a paper result, our interpretation, or our own experiment. Experiments should additionally record code version, configuration, data partition, random seeds, and metric definitions.

Added: 2026-10-22. Check the folder for actual PDF availability; source links remain the canonical records.

## Aggregation primary sources added 2026-10-30

Seven additional PDFs were downloaded from proceedings or author-hosted sources. These support the method notes; collection and source checks do not establish completed critical review.

### P006 — Federated Optimization in Heterogeneous Networks

- Authors: Tian Li, Anit Kumar Sahu, Manzil Zaheer, Maziar Sanjabi, Ameet Talwalkar, Virginia Smith
- Publication: MLSys 2, 429–450; Conference paper; proceedings PDF.
- Source: https://proceedings.mlsys.org/paper_files/paper/2020/hash/1f5fe83998a09396ebe6477d9475ba0c-Abstract.html
- PDF source: https://proceedings.mlsys.org/paper/2020/file/1f5fe83998a09396ebe6477d9475ba0c-Paper.pdf
- Reading copy: `li-2020-fedprox-mlsys.pdf`
- Reading anchor: Section 3, Algorithm 2 for the local proximal objective; Section 4 for analysis assumptions.
- Website note: [method note](../website/docs/dimensions/aggregation/fedprox.md)

### P007 — SCAFFOLD: Stochastic Controlled Averaging for Federated Learning

- Authors: Sai Praneeth Karimireddy, Satyen Kale, Mehryar Mohri, Sashank J. Reddi, Sebastian U. Stich, Ananda Theertha Suresh
- Publication: ICML · PMLR 119, 5132–5143; Conference paper.
- Source: https://proceedings.mlr.press/v119/karimireddy20a.html
- PDF source: https://proceedings.mlr.press/v119/karimireddy20a/karimireddy20a.pdf
- Reading copy: `karimireddy-2020-scaffold.pdf`
- Reading anchor: Section 4 and Algorithm 1: distinguish model and control updates, including cohort versus population denominators.
- Website note: [method note](../website/docs/dimensions/aggregation/scaffold.md)

### P008 — Adaptive Federated Optimization

- Authors: Sashank J. Reddi, Zachary Charles, Manzil Zaheer, Zachary Garrett, Keith Rush, Jakub Konečný, Sanjiv Kumar, H. Brendan McMahan
- Publication: ICLR 2021; Conference paper; author-hosted reading copy.
- Source: https://research.google/pubs/adaptive-federated-optimization/
- PDF source: https://sanjivk.com/adaptive_federated_optimization_ICLR2021.pdf
- Reading copy: `reddi-2021-adaptive-federated-optimization.pdf`
- Reading anchor: Section 3, Algorithms 1–2; inspect the reused displacement symbol and accumulator convention. Appendix B provides implementation details.
- Website note: [method note](../website/docs/dimensions/aggregation/fedopt.md)

### P009 — Byzantine-Robust Distributed Learning: Towards Optimal Statistical Rates

- Authors: Dong Yin, Yudong Chen, Kannan Ramchandran, Peter Bartlett
- Publication: ICML · PMLR 80, 5650–5659; Conference paper.
- Source: https://proceedings.mlr.press/v80/yin18a.html
- PDF source: https://proceedings.mlr.press/v80/yin18a/yin18a.pdf
- Reading copy: `yin-2018-byzantine-robust.pdf`
- Reading anchor: Section 3 for the two operators; Sections 4–5 for the statistical model and rates. Distinguish gradients from multi-step FL deltas.
- Website note: [method note](../website/docs/dimensions/aggregation/coordinate-wise-median.md)

### P010 — Machine Learning with Adversaries: Byzantine Tolerant Gradient Descent

- Authors: Peva Blanchard, El Mahdi El Mhamdi, Rachid Guerraoui, Julien Stainer
- Publication: NeurIPS 30 (NIPS 2017); Conference paper.
- Source: https://proceedings.neurips.cc/paper_files/paper/2017/hash/f4b9ec30ad9f68f89b29639786cb62ef-Abstract.html
- PDF source: https://proceedings.neurips.cc/paper/2017/file/f4b9ec30ad9f68f89b29639786cb62ef-Paper.pdf
- Reading copy: `blanchard-2017-krum.pdf`
- Reading anchor: Sections 3–4: resilience definition, nearest-neighbor score, and noise/count assumptions.
- Website note: [method note](../website/docs/dimensions/aggregation/krum.md)

### P011 — Robust Aggregation for Federated Learning

- Authors: Krishna Pillutla, Sham M. Kakade, Zaid Harchaoui
- Publication: IEEE Transactions on Signal Processing · 70, 1142–1154; Journal paper; stored author manuscript is arXiv v2.
- Source: https://arxiv.org/abs/1912.13445v2
- PDF source: https://arxiv.org/pdf/1912.13445v2
- Reading copy: `pillutla-2022-robust-aggregation-arxiv-v2.pdf`
- Reading anchor: Sections 2–3 for the geometric-median oracle and RFA; Appendix C for smoothed Weiszfeld convergence.
- Website note: [method note](../website/docs/dimensions/aggregation/geometric-median.md)

### P012 — Measuring the Effects of Non-Identical Data Distribution for Federated Visual Classification

- Authors: Tzu-Ming Harry Hsu, Hang Qi, Matthew Brown
- Publication: arXiv:1909.06335v1; Author preprint, September 2019.
- Source: https://arxiv.org/abs/1909.06335v1
- PDF source: https://arxiv.org/pdf/1909.06335v1
- Reading copy: `hsu-2019-fedavgm-arxiv-v1.pdf`
- Reading anchor: Section 4.2 for server momentum; distinguish the displayed recurrence from Nesterov momentum used in experiments.
- Website note: [method note](../website/docs/dimensions/aggregation/fedavgm.md)
