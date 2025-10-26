import skfuzzy as fuzz

def compute_membership_degrees(length, weight, input_length, input_weight):
    # length fuzzification
    miu_length = {
        'Pendek': fuzz.interp_membership(length.universe, length['pendek'].mf, input_length),
        'Normal': fuzz.interp_membership(length.universe, length['normal'].mf, input_length),
        'Panjang': fuzz.interp_membership(length.universe, length['panjang'].mf, input_length)
    }

    # weigth fuzzification
    miu_weight = {
        'Rendah': fuzz.interp_membership(weight.universe, weight['rendah'].mf, input_weight),
        'Normal': fuzz.interp_membership(weight.universe, weight['normal'].mf, input_weight),
        'Lebih': fuzz.interp_membership(weight.universe, weight['lebih'].mf, input_weight)
    }

    return miu_length, miu_weight