import streamlit as st
import time

# Setup halaman
st.set_page_config(page_title="Smart Door Lock", page_icon="🔐")
st.title("🔐 Smart Door Lock System")

# Inisialisasi session state
if 'pin_terdaftar' not in st.session_state:
    st.session_state.pin_terdaftar = "1234"
if 'percobaan' not in st.session_state:
    st.session_state.percobaan = 0
if 'terkunci' not in st.session_state:
    st.session_state.terkunci = False
if 'pintu_terbuka' not in st.session_state:
    st.session_state.pintu_terbuka = False
if 'security_mode' not in st.session_state:
    st.session_state.security_mode = False
if 'last_activity' not in st.session_state:
    st.session_state.last_activity = time.time()

pin_master = "0000"
max_attempt = 3
waktu_timeout = 10  # detik untuk auto lock

# Fungsi untuk mengecek auto lock
def check_auto_lock():
    if st.session_state.pintu_terbuka:
        now = time.time()
        if now - st.session_state.last_activity > waktu_timeout:
            st.session_state.pintu_terbuka = False
            st.success("🔒 Pintu terkunci otomatis karena tidak ada aktivitas.")

check_auto_lock()

# Tombol Security Mode
col1, col2 = st.columns(2)
with col1:
    if st.button("🛡️ Toggle Security Mode"):
        st.session_state.security_mode = not st.session_state.security_mode
        if st.session_state.security_mode:
            st.warning("🛡️ Security Mode AKTIF. Semua akses dibatasi.")
        else:
            st.success("✅ Security Mode DINONAKTIFKAN.")
with col2:
    if st.session_state.pintu_terbuka and st.button("🔒 Kunci Pintu Manual"):
        st.session_state.pintu_terbuka = False
        st.success("🔒 Pintu berhasil dikunci secara manual.")

# Form input PIN
with st.form("form_pin"):
    input_pin = st.text_input("Masukkan PIN Anda:", type="password")
    submitted = st.form_submit_button("🔓 Buka Pintu / Akses")

if submitted:
    st.session_state.last_activity = time.time()  # update aktivitas terakhir

    if st.session_state.terkunci:
        st.error("🚨 Sistem terkunci. Silakan reset aplikasi.")

    elif st.session_state.security_mode:
        st.error("🛡️ Akses ditolak! Security Mode sedang AKTIF.")

    elif input_pin == st.session_state.pin_terdaftar:
        st.success("✅ Akses diterima. Pintu terbuka!")
        st.session_state.pintu_terbuka = True
        st.session_state.percobaan = 0

    elif input_pin == pin_master:
        st.info("🔐 Admin Mode aktif. Ganti PIN pengguna di bawah ini.")
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

# Tampilkan status pintu
st.markdown("---")
if st.session_state.pintu_terbuka:
    st.success("🚪 Status Pintu: TERBUKA")
else:
    st.info("🚪 Status Pintu: TERKUNCI")

if st.session_state.security_mode:
    st.warning("🛡️ Security Mode AKTIF")

# Tombol reset sistem jika terkunci
if st.session_state.terkunci:
    if st.button("🔄 Reset Sistem"):
        st.session_state.percobaan = 0
        st.session_state.terkunci = False
        st.success("✅ Sistem berhasil direset.")
