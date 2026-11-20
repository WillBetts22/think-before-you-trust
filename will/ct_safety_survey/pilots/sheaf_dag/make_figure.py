"""Plot reliability vs verification budget from results/sheaf_dag_results.json -> results/budget_sweep.png"""
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
r = json.load(open(os.path.join(HERE, "results", "sheaf_dag_results.json")))
sweep = r["budget_sweep_base"]
# fixed categorical order (validated default palette, slots 1-5); Random is the neutral floor
series = [
    ("D only (structure)", "#2a78d6", "o"),
    ("Conf x D", "#eb6834", "s"),
    ("Sheaf-DAG x D", "#1baf7a", "^"),
    ("Sheaf-tree x D (chain-only)", "#eda100", "v"),
    ("Dependency-aware (repo)", "#e87ba4", "D"),
    ("Random", "#8a8a85", "x"),
]
titles = {"default_conf": "Repo's default confidence model\n(confidence informative)",
          "overconfident": "Repo's 'overconfident' mode\n(false claims report high confidence)"}
fig, axes = plt.subplots(1, 2, figsize=(11, 4.2), sharey=True)
for ax, key in zip(axes, ["default_conf", "overconfident"]):
    budgets = sorted(int(b) for b in sweep[key])
    for name, col, mk in series:
        ys = [sweep[key][str(b)][name] for b in budgets]
        ax.plot(budgets, ys, color=col, marker=mk, ms=6, lw=2, label=name)
    ax.set_title(titles[key], fontsize=10)
    ax.set_xlabel("verification budget (checks; DAGs have ≤80 claims, mean ≈57)")
    ax.grid(alpha=0.25)
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)
axes[0].set_ylabel("reliability = 1 − undetected false / total")
axes[1].legend(fontsize=8, frameon=False, loc="lower right")
fig.suptitle("Pilot A (synthetic): sheaf-inconsistency selection vs. parent-project strategies, 200 DAGs per point "
             "(fabrication size a=2σ, q_consistent=0.9)", fontsize=10)
fig.tight_layout()
fig.savefig(os.path.join(HERE, "results", "budget_sweep.png"), dpi=130)
print("wrote results/budget_sweep.png")
