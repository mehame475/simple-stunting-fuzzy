import numpy as np

def compute_agregate(risk, rule_results):
    x_risk = risk.universe
    aggregated = np.zeros_like(x_risk)

    # Combine each rule (max)
    for row in rule_results:
        strength = row["Nilai Aktivasi"]
        output_label = row["Output"]
        for key in risk.terms.keys():
            if key in output_label:
                mf = risk[key].mf
                activated = np.fmin(strength, mf)
                aggregated = np.fmax(aggregated, activated)

    return aggregated