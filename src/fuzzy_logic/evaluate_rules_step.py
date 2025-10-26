import numpy as np

def evaluate_rules(rules, miu_height, miu_weight):
    rule_results = []
    for i, rule in enumerate(rules, 1):
        # Get antecendent and consequent
        antecedent_text = str(rule.antecedent).replace("&", "AND").replace("|", "OR")
        consequent_text = str(rule.consequent)
        
        # Find member value for input based keyword
        if "pendek" in antecedent_text:
            mui_h = miu_height['Pendek']
        elif "normal" in antecedent_text and "panjang" not in antecedent_text:
            mui_h = miu_height['Normal']
        else:
            mui_h = miu_height['Panjang']

        if "rendah" in antecedent_text:
            miu_w = miu_weight['Rendah']
        elif "lebih" in antecedent_text:
            miu_w = miu_weight['Lebih']
        else:
            miu_w = miu_weight['Normal']

        # Operator AND (min)
        strength = np.fmin(mui_h, miu_w)

        rule_results.append({
            "Aturan": f"Rule {i}",
            "Kondisi": antecedent_text,
            "Output": consequent_text,
            "Nilai Aktivasi": strength
        })

    return rule_results