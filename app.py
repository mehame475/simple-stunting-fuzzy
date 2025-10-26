import streamlit as st
import matplotlib.pyplot as plt
from src.fuzzy_logic.stunting_risk_system import create_stunting_risk_system, get_linguistic_label
from src.fuzzy_logic.fuzzyfication_step import compute_membership_degrees
from src.fuzzy_logic.evaluate_rules_step import evaluate_rules
from src.fuzzy_logic.agregate_step import compute_agregate

st.set_page_config(page_title="Sistem Prediksi Risiko Stunting", page_icon="🧒")

# Initialize fuzzy system in session state
if 'risk_sim' not in st.session_state:
    risk_sim, length, weight, risk, rules = create_stunting_risk_system()
    st.session_state.risk_sim = risk_sim
    st.session_state.length = length
    st.session_state.weight = weight
    st.session_state.risk = risk
    st.session_state.rules = rules
else:
    # Retrieve from session state if already created
    risk_sim = st.session_state.risk_sim
    length = st.session_state.length
    weight = st.session_state.weight
    risk = st.session_state.risk
    rules = st.session_state.rules

# ----------------------------
# Streamlit UI
# ----------------------------
st.title("Sistem Prediksi Risiko Stunting")
st.write("Masukkan panjang dan berat badan anak untuk memprediksi tingkat risiko stunting.")

# User input form
with st.form("input_form"):
    st.header("Masukkan Data Anak")

    length_input = st.number_input(
        "Panjang Badan (cm)",
        min_value=40.0,
        max_value=55.0,
        value=46.0,
        step=0.1,
        help="Rentang panjang badan 40.0 - 55.0 cm"
    )

    weight_input = st.number_input(
        "Berat Badan (g)",
        min_value=1000,
        max_value=4500,
        value=2400,
        step=10,
        help="Rentang berat badan 1000 - 4500 g"
    )

    submitted = st.form_submit_button("Prediksi Risiko")

# ----------------------------
# Fuzzy Inference Process
# ----------------------------
if submitted:
    try:
        # Step 1: Assign user inputs to the fuzzy system
        risk_sim.input['panjang'] = length_input
        risk_sim.input['berat'] = weight_input

        # Step 2: Run fuzzy computation
        risk_sim.compute()

        # Step 3: Get crisp output and linguistic label
        risk_value = risk_sim.output['risiko']
        risk_label = get_linguistic_label(risk_value)

        # Display results
        st.subheader("Hasil Prediksi")

        # Create 2 columns for metrics
        col1, col2 = st.columns(2)

        with col1:
            st.metric(label="Nilai Risiko (0-100)", value=f"{risk_value:.2f}%")

        with col2:
            st.metric(label="Kategori Risiko", value=risk_label)

        # -------------------------------------
        # Detailed fuzzy process visualization
        # -------------------------------------
        with st.expander("Lihat Langkah-langkah Proses Fuzzy"):
            # --- Step 1: Fuzzification ---
            st.markdown("### 1. Fuzzifikasi: Menentukan Derajat Keanggotaan")

            # Calculate membership degrees for each input
            miu_length, miu_weight = compute_membership_degrees(length, weight, length_input, weight_input)

            st.write("**Derajat Keanggotaan Panjang Badan:**")
            st.table([miu_length])
            st.write("**Derajat Keanggotaan Berat Badan:**")
            st.table([miu_weight])

            # --- Step 2: Rule Evaluation ---
            st.markdown("### 2. Evaluasi Aturan: Menentukan Nilai Output Tiap Aturan")
            st.write("Aturan yang dievaluasi:")
            rule_results = evaluate_rules(rules, miu_length, miu_weight)
            st.dataframe(rule_results)

            # --- Step 3: Aggregation ---
            st.markdown("### 3. Agregasi (Penggabungan Hasil Aturan)")
            x_risk = risk.universe
            aggregated = compute_agregate(risk, rule_results)

            # Plot aggregated membership function
            fig_aggr, ax3 = plt.subplots(figsize=(8, 3))
            ax3.plot(x_risk, aggregated, 'k', linewidth=1.5)
            ax3.set_title("Hasil Agregasi (Sebelum Defuzzifikasi)")
            ax3.set_xlabel("Risiko (%)")
            ax3.set_ylabel("Derajat Keanggotaan")
            st.pyplot(fig_aggr)

            # --- Step 4: Defuzzification ---
            st.markdown("### 4. Defuzzifikasi: Menentukan Nilai Akhir")
            fig_final, ax4 = plt.subplots(figsize=(8, 3))
            for term in risk.terms:
                ax4.plot(x_risk, risk[term].mf, label=term)
            ax4.fill_between(x_risk, aggregated, color='gray', alpha=0.3, label='Agregasi')
            ax4.axvline(risk_value, color='r', linestyle='--', label='Centroid')
            ax4.set_title("Defuzzifikasi (Hasil Akhir)")
            ax4.legend()
            st.pyplot(fig_final)

    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")

# -------------------------------------
# Fuzzy System Details Visualization
# -------------------------------------
with st.expander("Lihat Detail Sistem Fuzzy"):
    st.subheader("Variabel dan Fungsi Keanggotaan")

    st.write("Input: Variabel Panjang Badan")
    length.view()
    st.pyplot(plt.gcf())
    plt.close()

    st.write("Input: Variabel Berat Badan")
    weight.view()
    st.pyplot(plt.gcf())
    plt.close()

    st.write("Output: Variabel Risiko Stunting")
    risk.view()
    st.pyplot(plt.gcf())
    plt.close()
