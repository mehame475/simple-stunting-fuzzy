import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

def create_stunting_risk_system():
    """
    Creates and returns the fuzzy control system for stunting risk evaluation.
    Returns:
        tuple: (risk_sim, length, weight, risk)
    """
    # Define input variables
    length = ctrl.Antecedent(np.arange(40, 55.1, 0.1), 'panjang')
    weight = ctrl.Antecedent(np.arange(1000, 4501, 1), 'berat')

    # Define output variable
    x_risk = np.arange(0, 101, 1)
    risk = ctrl.Consequent(x_risk, 'risiko')

    # Membership functions for 'length'
    length['pendek'] = fuzz.trapmf(length.universe, [40, 40, 43, 47])
    length['normal'] = fuzz.trapmf(length.universe, [45, 49, 51, 53])
    length['panjang'] = fuzz.trapmf(length.universe, [51, 55, 55, 55])

    # Membership functions for 'weight'
    weight['rendah'] = fuzz.trapmf(weight.universe, [1000, 1000, 2000, 2500])
    weight['normal'] = fuzz.trapmf(weight.universe, [2000, 2500, 3500, 4000])
    weight['lebih']  = fuzz.trapmf(weight.universe, [3500, 4000, 4500, 4500])

    # Membership functions for 'risk'
    risk['sangat_rendah'] = fuzz.trimf(risk.universe, [0, 0, 20])
    risk['rendah']        = fuzz.trimf(risk.universe, [10, 25, 40])
    risk['sedang']        = fuzz.trimf(risk.universe, [35, 50, 65])
    risk['tinggi']        = fuzz.trimf(risk.universe, [60, 75, 90])
    risk['sangat_tinggi'] = fuzz.trimf(risk.universe, [80, 100, 100])

    # Define fuzzy rules (rule base)
    rules = [
        ctrl.Rule(length['pendek'] & weight['rendah'], risk['sangat_tinggi']),
        ctrl.Rule(length['normal'] & weight['rendah'], risk['tinggi']),
        ctrl.Rule(length['panjang'] & weight['rendah'], risk['sedang']),

        ctrl.Rule(length['pendek'] & weight['normal'], risk['tinggi']),
        ctrl.Rule(length['normal'] & weight['normal'], risk['rendah']),
        ctrl.Rule(length['panjang'] & weight['normal'], risk['sangat_rendah']),

        ctrl.Rule(length['pendek'] & weight['lebih'], risk['sedang']),
        ctrl.Rule(length['normal'] & weight['lebih'], risk['rendah']),
        ctrl.Rule(length['panjang'] & weight['lebih'], risk['sangat_rendah']),
    ]

    # Create control system and simulation
    risk_ctrl = ctrl.ControlSystem(rules)
    risk_sim = ctrl.ControlSystemSimulation(risk_ctrl)

    return risk_sim, length, weight, risk, rules


def get_linguistic_label(value):
    """
    Determines the linguistic label for a given fuzzy (crisp) value.
    """
    x_risk = np.arange(0, 101, 1)
    labels = {
        "Sangat Rendah": fuzz.trimf(x_risk, [0, 0, 20]),
        "Rendah": fuzz.trimf(x_risk, [10, 25, 40]),
        "Sedang": fuzz.trimf(x_risk, [35, 50, 65]),
        "Tinggi": fuzz.trimf(x_risk, [60, 75, 90]),
        "Sangat Tinggi": fuzz.trimf(x_risk, [80, 100, 100])
    }

    memberships = {
        label: fuzz.interp_membership(x_risk, mf, value)
        for label, mf in labels.items()
    }
    return max(memberships, key=memberships.get)
