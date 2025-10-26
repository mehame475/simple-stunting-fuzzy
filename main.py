import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Variabel input
panjang = ctrl.Antecedent(np.arange(40, 55.1, 0.1), 'panjang')
berat = ctrl.Antecedent(np.arange(1000, 4501, 1), 'berat')

# Domain risiko stunting (0–100)
x_risiko = np.arange(0, 101, 1)

# Variabel output
risiko = ctrl.Consequent(x_risiko, 'risiko')

# Panjang: Pendek (P1), Normal (P2), Panjang (P3)
panjang['pendek'] = fuzz.trapmf(panjang.universe, [40, 40, 43, 47])
panjang['normal'] = fuzz.trapmf(panjang.universe, [45, 49, 51, 53])
panjang['panjang'] = fuzz.trapmf(panjang.universe, [51, 55, 55, 55])

# Berat: Rendah (B1), Normal (B2), Lebih (B3)
berat['rendah'] = fuzz.trapmf(berat.universe, [1000, 1000, 2000, 2500])
berat['normal'] = fuzz.trapmf(berat.universe, [2000, 2500, 3500, 4000])
berat['lebih']  = fuzz.trapmf(berat.universe, [3500, 4000, 4500, 4500])

risiko['sangat_rendah'] = fuzz.trimf(risiko.universe, [0, 0, 20])
risiko['rendah']        = fuzz.trimf(risiko.universe, [10, 25, 40])
risiko['sedang']        = fuzz.trimf(risiko.universe, [35, 50, 65])
risiko['tinggi']        = fuzz.trimf(risiko.universe, [60, 75, 90])
risiko['sangat_tinggi'] = fuzz.trimf(risiko.universe, [80, 100, 100])

rules = [
    ctrl.Rule(panjang['pendek'] & berat['rendah'], risiko['sangat_tinggi']),
    ctrl.Rule(panjang['normal'] & berat['rendah'], risiko['tinggi']),
    ctrl.Rule(panjang['panjang'] & berat['rendah'], risiko['sedang']),

    ctrl.Rule(panjang['pendek'] & berat['normal'], risiko['tinggi']),
    ctrl.Rule(panjang['normal'] & berat['normal'], risiko['rendah']),
    ctrl.Rule(panjang['panjang'] & berat['normal'], risiko['sangat_rendah']),

    ctrl.Rule(panjang['pendek'] & berat['lebih'], risiko['sedang']),
    ctrl.Rule(panjang['normal'] & berat['lebih'], risiko['rendah']),
    ctrl.Rule(panjang['panjang'] & berat['lebih'], risiko['sangat_rendah']),
]

# Fungsi keanggotaan fuzzy
vlr = fuzz.trimf(x_risiko, [0, 0, 20])      # Sangat Rendah
lr  = fuzz.trimf(x_risiko, [10, 25, 40])    # Rendah
m   = fuzz.trimf(x_risiko, [35, 50, 65])    # Sedang
h   = fuzz.trimf(x_risiko, [60, 75, 90])    # Tinggi
vh  = fuzz.trimf(x_risiko, [80, 100, 100])  # Sangat Tinggi

# Gabungkan ke dalam dict
labels = {
    "Sangat Rendah": vlr,
    "Rendah": lr,
    "Sedang": m,
    "Tinggi": h,
    "Sangat Tinggi": vh
}

# Fungsi untuk menentukan label linguistik utama
def get_linguistic_label(value):
    memberships = {label: fuzz.interp_membership(x_risiko, mf, value)
                   for label, mf in labels.items()}
    best_label = max(memberships, key=memberships.get)
    return best_label

# Bangun sistem
risiko_ctrl = ctrl.ControlSystem(rules)
risiko_sim = ctrl.ControlSystemSimulation(risiko_ctrl)

# Contoh input: Panjang=46 cm, Berat=2400 g
risiko_sim.input['panjang'] = 46
risiko_sim.input['berat'] = 2400

# Jalankan inferensi fuzzy
risiko_sim.compute()

print(f"Hasil Risiko Stunting (0 - 100): {risiko_sim.output['risiko']}")
print(f"{get_linguistic_label(float(risiko_sim.output['risiko']))}")
