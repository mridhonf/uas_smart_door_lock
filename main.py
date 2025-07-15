import streamlit as st

# Set judul
st.set_page_config(page_title="Smart Door Lock", page_icon="🔐")
st.title("🔐 Smart Door Lock System")

# Inisialisasi state
if 'pin_terdaftar' not in st.session_state:
    st.session_state.pin_terdaftar = "1234"
if 'percobaan' not in st.session_state:
    st.session_state.percobaan = 0
if 'terkunci' not in st.session_state:
    st.session_state.terkunci = False

pin_master = "0000"
max_attempt = 3

# Form input PIN
with st.form("form_pin"):
    input_pin = st.text_input("Masukkan PIN Anda:", type="password")
    submitted = st.form_submit_button("🔓 Buka Pintu")

# Logika Akses
if submitted:
    if st.session_state.terkunci:
        st.error("🚨 Sistem terkunci. Silakan reset aplikasi.")
    elif input_pin == st.session_state.pin_terdaftar:
        st.success("✅ Akses diterima. Pintu terbuka!")
        st.session_state.percobaan = 0  # reset percobaan
    elif input_pin == pin_master:
        st.info("🔐 Akses Admin terdeteksi. Ganti PIN pengguna di bawah ini.")
        new_pin = st.text_input("Masukkan PIN baru (4 digit):", max_chars=4, key="ubah_pin")
        if new_pin:
            if len(new_pin) == 4 and new_pin.isdigit():
                st.session_state.pin_terdaftar = new_pin
                st.success("✅ PIN berhasil diubah.")
                st.session_state.percobaan = 0
            else:
                st.error("❌ PIN harus 4 digit angka.")
    else:
        st.session_state.percobaan += 1
        sisa = max_attempt - st.session_state.percobaan
        st.warning(f"❌ PIN salah! Sisa percobaan: {sisa}")
        if st.session_state.percobaan >= max_attempt:
            st.session_state.terkunci = True
            st.error("🚨 Terlalu banyak percobaan! Sistem terkunci.")

# Tambahkan tombol reset jika terkunci
if st.session_state.terkunci:
    if st.button("🔄 Reset Sistem"):
        st.session_state.percobaan = 0
        st.session_state.terkunci = False
        st.success("Sistem berhasil direset.")
