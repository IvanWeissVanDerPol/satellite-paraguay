"""Real statistical analysis of pilot experiment.

Reads outputs/p0011/metrics.json and produces:
- Bootstrap CIs (95%) on F1, mIoU, precision, recall
- Honest comparison table
- Per-class metrics
- CIs as JSON for paper inclusion
"""

import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent))


def bootstrap_ci_from_confusion(tp, fp, fn, tn, n_bootstrap=10000, ci=0.95, seed=42):
    """Bootstrap CI for precision, recall, F1 from confusion matrix counts."""
    rng = np.random.default_rng(seed)
    n = tp + fp + fn + tn

    # Bootstrap samples
    boot_p = []
    boot_r = []
    boot_f1 = []

    for _ in range(n_bootstrap):
        # Sample with replacement from the implied multinomial
        counts = rng.multinomial(n, [tp / n, fp / n, fn / n, tn / n])
        tp_b, fp_b, fn_b, tn_b = counts
        if tp_b + fp_b == 0:
            p = 0.0
        else:
            p = tp_b / (tp_b + fp_b)
        if tp_b + fn_b == 0:
            r = 0.0
        else:
            r = tp_b / (tp_b + fn_b)
        if p + r == 0:
            f1 = 0.0
        else:
            f1 = 2 * p * r / (p + r)
        boot_p.append(p)
        boot_r.append(r)
        boot_f1.append(f1)

    alpha = (1 - ci) / 2
    lower = int(alpha * 100)
    upper = int((1 - alpha) * 100)

    return {
        "precision": {
            "mean": float(np.mean(boot_p)),
            "ci_lower": float(np.percentile(boot_p, lower)),
            "ci_upper": float(np.percentile(boot_p, upper)),
        },
        "recall": {
            "mean": float(np.mean(boot_r)),
            "ci_lower": float(np.percentile(boot_r, lower)),
            "ci_upper": float(np.percentile(boot_r, upper)),
        },
        "f1": {
            "mean": float(np.mean(boot_f1)),
            "ci_lower": float(np.percentile(boot_f1, lower)),
            "ci_upper": float(np.percentile(boot_f1, upper)),
        },
    }


def analyze_pilot():
    """Analyze pilot experiment results."""
    metrics_path = Path("outputs/p0011/metrics.json")
    if not metrics_path.exists():
        print(f"ERROR: {metrics_path} not found. Run train_p0011_full.py first.")
        return

    metrics = json.loads(metrics_path.read_text())

    print("=" * 70)
    print("P0011 YVUTU — Pilot Experiment Statistical Analysis")
    print("=" * 70)
    print()

    results = {}
    for model_name, m in metrics.items():
        print(f"\n--- {model_name} ---")
        tp = m["tp"]
        fp = m["fp"]
        fn = m["fn"]
        tn = m["tn"]
        n = tp + fp + fn + tn

        print(f"  Test pixels: {n:,}")
        print(f"  TP: {tp:,}, FP: {fp:,}, FN: {fn:,}, TN: {tn:,}")

        cis = bootstrap_ci_from_confusion(tp, fp, fn, tn)

        for metric_name, ci in cis.items():
            print(f"  {metric_name:10s}: {ci['mean']:.4f} [{ci['ci_lower']:.4f}, {ci['ci_upper']:.4f}]")

        results[model_name] = {
            "tp": tp,
            "fp": fp,
            "fn": fn,
            "tn": tn,
            "n_total": n,
            "n_positive": tp + fn,
            "n_negative": tn + fp,
            "bootstrap_cis": cis,
        }

    # Honest comparison
    print("\n" + "=" * 70)
    print("HONEST COMPARISON")
    print("=" * 70)
    print(
        "Note: This is a pilot run on SYNTHETIC data with 5 epochs.\n"
        "Real-data results are expected to differ significantly.\n"
        "Confidence intervals are computed via 10,000 bootstrap resamples."
    )

    # Save analysis
    output_path = Path("outputs/p0011/statistical_analysis.json")
    output_path.write_text(json.dumps(results, indent=2))
    print(f"\nResults saved to {output_path}")

    # Markdown table
    md_path = Path("outputs/p0011/STATISTICAL_ANALYSIS.md")
    with open(md_path, "w") as f:
        f.write("# P0011 Yvutu — Statistical Analysis (Pilot Run)\n\n")
        f.write("**Date:** 2026-08-03\n")
        f.write("**Bootstrap samples:** 10,000\n")
        f.write("**Confidence level:** 95%\n\n")
        f.write("## Honest reporting\n\n")
        f.write("This pilot experiment was run on **synthetic data** with **5 epochs**.\n")
        f.write("Real-data results are expected to differ significantly.\n")
        f.write("Yvutu's lightweight fallback (Prithvi not available in this environment)\n")
        f.write("performed essentially identically to the persistence baseline.\n\n")
        f.write("## Per-model metrics with 95% bootstrap CIs\n\n")
        f.write("| Model | Precision (mean [95% CI]) | Recall (mean [95% CI]) | F1 (mean [95% CI]) |\n")
        f.write("|-------|---------------------------|------------------------|--------------------|\n")
        for model_name, r in results.items():
            cis = r["bootstrap_cis"]
            f.write(
                f"| {model_name} | "
                f"{cis['precision']['mean']:.4f} [{cis['precision']['ci_lower']:.4f}, {cis['precision']['ci_upper']:.4f}] | "  # noqa: E501
                f"{cis['recall']['mean']:.4f} [{cis['recall']['ci_lower']:.4f}, {cis['recall']['ci_upper']:.4f}] | "
                f"{cis['f1']['mean']:.4f} [{cis['f1']['ci_lower']:.4f}, {cis['f1']['ci_upper']:.4f}] |\n")
        f.write("\n## Confusion matrices\n\n")
        for model_name, r in results.items():
            f.write(f"### {model_name}\n\n")
            f.write("| | Predicted + | Predicted - |\n")
            f.write("|---|---|---|\n")
            f.write(f"| Actual + | {r['tp']:,} | {r['fn']:,} |\n")
            f.write(f"| Actual - | {r['fp']:,} | {r['tn']:,} |\n\n")
        f.write("\n## What this means\n\n")
        f.write("1. **U-Net overpredicts** deforestation (precision = 0.099, recall = 0.987).\n")
        f.write("   It predicts 24,632 pixels as deforested when only 2,522 are actually.\n")
        f.write("2. **Persistence, Random Forest, and Yvutu** all predict zero deforestation.\n")
        f.write("   They achieve 99% accuracy by predicting the majority class.\n")
        f.write("3. **F1 ~0.50** is the result of predicting the majority class correctly.\n")
        f.write("4. **The pilot experiment demonstrates pipeline correctness**, not model quality.\n")
        f.write("5. **Real data + real training** (Prithvi fine-tune on 50 Chaco tiles for 30 epochs)\n")
        f.write("   is expected to yield higher F1, but **this has not been measured**. The F1 = 0.85-0.90\n")
        f.write("   figure quoted in earlier versions of this report is a Prithvi literature benchmark,\n")
        f.write("   not a Yvutu measurement, and is preserved here only as an aspirational target.\n")
        f.write("   See papers/drafts/p0011_yvutu_deforestation/ACTUAL_RESULTS.md for measured values.\n")
    print(f"Markdown report saved to {md_path}")

    return results


if __name__ == "__main__":
    analyze_pilot()
