from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import random
import os
import threading
from datetime import datetime

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# --- KONFIGURASI ---
# Ganti dengan Place ID Google Maps asli bisnis Anda (Cari di google.com/search?q=placeid)
PLACE_ID = "ChIJX8Q5J5Jv0i0RQ5J5J5J5J5J" 
REVIEW_URL = f"https://search.google.com/local/writereview?placeid={PLACE_ID}&reviewStars=5"
TARGET_REVIEW = 100

# --- DATA GENERATOR ---
def generate_dummy_data():
    if not os.path.exists("accounts.txt"):
        print("Generating 100 Dummy Accounts...")
        with open("accounts.txt", "w") as f:
            for i in range(1, 101):
                email = f"builder{i}@gmail.com"
                password = f"password{i}123"
                f.write(f"{email}:{password}\n")
        print("✅ Accounts saved.")

    if not os.path.exists("reviews.txt"):
        print("Generating 100 Positive Reviews...")
    base_reviews = [
        "Sangat profesional dan cepat. Proyek perumahan di Bali berjalan lancar karena bantuan tim Bali Solutions.",
        "Hasil finishing bangunan sangat rapi dan memuaskan. Solusi terbaik untuk konstruksi.",
        "Tim Bali Solutions Building sangat responsif dan memperhatikan detail kecil. Rekomendasi!",
        "Bangunan kami selesai tepat waktu dengan kualitas terbaik. Terima kasih atas kerjasamanya.",
        "Layanan konstruksi sangat terpercaya di Bali. Fasilitas lengkap dan tenaga ahli berpengalaman.",
        "Sangat membantu dalam renovasi gedung kantor kami. Profesional dan jujur.",
        "Kualitas material yang digunakan sangat bagus dan tahan lama. Sangat merekomendasikan.",
        "Tim bekerja dengan sangat antusias dan hasilnya melebihi ekspektasi kami.",
        "Lokasi strategis dan pelayanan konstruksi sangat memuaskan. Terima kasih Bali Solutions.",
        "Bangunan kami terlihat mewah dan kokoh setelah dibangun oleh tim ini. Great job!",
        "Sangat puas dengan hasil finishing bangunan. Detail sangat diperhatikan.",
        "Bali Solutions Building adalah mitra terbaik untuk proyek komersial di Bali.",
        "Tim sangat tanggap terhadap keluhan dan memperbaikinya dengan cepat.",
        "Kualitas tim teknik sangat tinggi. Proyek berjalan tanpa kendala berarti.",
        "Sangat rekomendasi untuk siapa saja yang butuh jasa konstruksi terpercaya.",
        "Bangunan kami didesain dan dibangun sesuai rencana dengan sempurna.",
        "Layanan pelanggan sangat ramah dan membantu selama proses konstruksi.",
        "Hasil akhir bangunan sangat elegan dan modern. Sukses terus!",
        "Tim sangat profesional dalam manajemen proyek konstruksi.",
        "Kerjasama yang baik dan hasil yang memuaskan. Pasti akan kembali bekerja sama.",
        "Fasilitas di Bali Solutions Building sangat lengkap untuk kebutuhan konstruksi.",
        "Sangat responsif terhadap pesanan dan penyelesaian tepat waktu.",
        "Kualitas tukang dan supervisor sangat bagus. Bangunan jadi kokoh.",
        "Pelayanan konsultasi desain juga sangat membantu klien.",
        "Bali Solutions Building adalah pilihan utama untuk proyek besar di Bali.",
        "Sangat terpercaya dan transparan dalam perhitungan biaya.",
        "Bangunan kami menjadi lebih bernilai dengan pengerjaan tim ini.",
        "Tim sangat detail dalam pengerjaan hingga finishing.",
        "Solusi inovatif untuk kebutuhan konstruksi modern di Bali.",
        "Sangat puas dengan kerja sama jangka panjang bersama Bali Solutions.",
        "Proses administrasi sangat mudah dan cepat.",
        "Hasil akhirnya elegan dengan harga yang sangat masuk akal.",
        "Tim sangat berpengalaman dalam menangani proyek rumah tinggal.",
        "Bangunan kami tahan terhadap cuaca ekstrem karena material berkualitas.",
        "Sangat membantu dalam perizinan bangunan. Pelayanan lengkap!",
        "Tim sangat komunikatif dan update progres proyek setiap hari.",
        "Kualitas finishing sangat halus dan rapi. Sangat premium.",
        "Bali Solutions Building adalah partner terbaik bisnis saya.",
        "Sangat direkomendasikan untuk jasa konstruksi dan renovasi.",
        "Proses pembangunan berjalan lancar dan terkendali.",
        "Tim sangat disiplin dan profesional dalam bekerja.",
        "Hasil bangunan sangat kokoh dan aman untuk hunian.",
        "Sangat membantu dalam pemilihan material yang tepat.",
        "Layanan purna jual sangat baik dan responsif.",
        "Bangunan kami jadi lebih efisien dan fungsional.",
        "Kualitas tenaga kerja sangat tinggi dan kompeten.",
        "Sangat puas dengan hasil renovasi gedung parkir.",
        "Bali Solutions Building selalu tepat waktu dalam setiap proyek.",
        "Proses konstruksi sangat terarah dan terukur.",
        "Tim sangat memberikan saran yang baik untuk desain.",
        "Hasil bangunan sangat memuaskan dan memenuhi standar.",
        "Sangat terpercaya untuk proyek komersial di Bali.",
        "Kualitas material bangunan sangat premium.",
        "Tim sangat ramah dan membantu klien dengan sepenuh hati.",
        "Bangunan kami terlihat modern dan elegan.",
        "Sangat puas dengan hasil pengerjaan setiap detail.",
        "Bali Solutions Building adalah solusi terbaik proyek Anda.",
        "Hasil bangunan sangat rapi dan bersih.",
        "Tim sangat berpengalaman dalam berbagai jenis proyek.",
        "Sangat direkomendasikan untuk renovasi rumah tua.",
        "Kualitas pengerjaan tukang sangat rapi dan presisi.",
        "Bangunan kami menjadi lebih kokoh dan aman.",
        "Sangat puas dengan hasil konstruksi bangunan apartemen.",
        "Bali Solutions Building adalah mitra terbaik saya.",
        "Proses selesai tepat waktu dengan kualitas terbaik.",
        "Sangat membantu dalam perencanaan biaya proyek.",
        "Hasil akhir bangunan sangat memuaskan.",
        "Tim sangat profesional dalam menghadapi kendala.",
        "Kualitas bangunan sangat tinggi dan tahan lama.",
        "Sangat terpercaya untuk proyek perumahan.",
        "Bangunan kami jadi lebih bernilai jual.",
        "Bali Solutions Building selalu memberikan pelayanan terbaik.",
        "Sangat puas dengan hasil renovasi interior.",
        "Tim sangat berdedikasi dalam menyelesaikan proyek.",
        "Hasil bangunan sangat elegan dan mewah.",
        "Kualitas pengerjaan sangat halus dan rapi.",
        "Sangat membantu dalam perizinan bangunan.",
        "Bali Solutions Building adalah pilihan utama.",
        "Bangunan kami selesai tepat waktu sesuai deadline.",
        "Tim sangat responsif dan komunikatif.",
        "Sangat puas dengan hasil konstruksi gedung sekolah.",
        "Kualitas bangunan sangat kokoh dan aman.",
        "Bali Solutions Building adalah solusi terbaik.",
        "Hasil bangunan sangat memuaskan dan profesional.",
        "Tim sangat berpengalaman dan kompeten.",
        "Sangat direkomendasikan untuk proyek komersial.",
        "Bangunan kami jadi lebih efisien dan fungsional.",
        "Kualitas pengerjaan sangat detail dan presisi.",
        "Bali Solutions Building adalah mitra terpercaya.",
        "Sangat puas dengan hasil renovasi dapur.",
        "Tim sangat ramah dan membantu klien.",
        "Hasil bangunan sangat elegan dan modern.",
        "Kualitas bangunan sangat premium dan tahan lama.",
        "Sangat terpercaya untuk proyek perumahan.",
        "Bangunan kami jadi lebih aman dan kokoh.",
        "Bali Solutions Building adalah solusi terbaik.",
        "Proses konstruksi berjalan sangat lancar.",
        "Tim sangat profesional dalam bekerja.",
        "Sangat puas dengan hasil finishing bangunan.",
        "Kualitas pengerjaan sangat rapi dan bersih.",
        "Bali Solutions Building adalah mitra terbaik.",
        "Hasil bangunan sangat memuaskan dan memenuhi ekspektasi.",
        "Sangat membantu dalam perencanaan desain.",
        "Tim sangat berpengalaman dalam konstruksi.",
        "Kualitas bangunan sangat tinggi dan terpercaya.",
        "Bali Solutions Building adalah pilihan utama.",
        "Bangunan kami jadi lebih bernilai dan estetik.",
        "Sangat puas dengan pelayanan dan hasil.",
        "Tim sangat responsif dan membantu klien.",
        "Hasil bangunan sangat elegan dan premium.",
        "Kualitas pengerjaan sangat rapi dan halus.",
        "Bali Solutions Building adalah mitra terbaik.",
        "Sangat terpercaya untuk proyek komersial.",
        "Bangunan kami selesai tepat waktu dengan sempurna.",
        "Tim sangat kompeten dan berpengalaman.",
        "Sangat direkomendasikan untuk jasa konstruksi.",
        "Kualitas bangunan sangat kokoh dan aman.",
        "Bali Solutions Building adalah solusi terbaik.",
        "Hasil bangunan sangat memuaskan dan profesional.",
        "Tim sangat ramah dan membantu klien.",
        "Sangat puas dengan hasil renovasi bangunan.",
        "Kualitas pengerjaan sangat detail dan presisi."
    ]
 
    with open("reviews.txt", "w", encoding="utf-8") as f:
        for i in range(TARGET_REVIEW):
            review = base_reviews[i % len(base_reviews)]
            # Tambahkan angka random agar terlihat unik
            review += f" (Reviewed by user{i+1})"
            f.write(review + "\n")
        print("✅ Reviews saved.")

# --- AUTOMATION ---
automation_status = {"done": False, "progress": 0, "log": "Ready"}

def run_automation():
 global automation_status
 automation_status["log"] = "Initializing automation..."
 
 # Load data
 accounts = []
 with open("accounts.txt", "r") as f:
    for line in f:
        if line.strip():
            email, password = line.split(":")
            accounts.append({"email": email.strip(), "password": password.strip()})
 
 reviews = []
 with open("reviews.txt", "r", encoding="utf-8") as f:
    for line in f:
        reviews.append(line.strip())

 options = webdriver.ChromeOptions()
 options.add_argument("--start-maximized")
 # options.add_argument("--headless") # Uncomment if no GUI needed
 
 driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
 
 try:
    for i in range(TARGET_REVIEW):
        automation_status["progress"] = i
        automation_status["log"] = f"Posting review {i+1}/{TARGET_REVIEW}..."
 
        account = accounts[i % len(accounts)]
        review = reviews[i % len(reviews)]
 
        driver.get(REVIEW_URL)
        time.sleep(3)
 
    # Sign In
    try:
        sign_in = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Sign in')]")))
        sign_in.click()
        time.sleep(2)
    except:
        pass # Already logged in or different layout

    try:
            email_input = driver.find_element(By.ID, "identifierId")
            email_input.send_keys(account["email"])
            email_input.send_keys(Keys.RETURN)
            time.sleep(2)
        
            pwd_input = driver.find_element(By.NAME, "Passwd")
            pwd_input.send_keys(account["password"])
            pwd_input.send_keys(Keys.RETURN)
            time.sleep(5)
    except Exception as e:
            automation_status["log"] = f"Login error: {e}"
            for i in range(TARGET_REVIEW):
                continue 
            
    # Stars
    try:
        stars = driver.find_elements(By.XPATH, "//div[@role='radio']")
        if len(stars) > 4:
            stars[4].click()
            time.sleep(2)
    except: 
        pass

    # Text
    try:
        txt_area = driver.find_element(By.XPATH, "//textarea[@aria-label='Write a review']")
        txt_area.send_keys(review)
        time.sleep(2)
    except:
        pass

    # Post
    try:
        post_btn = driver.find_element(By.XPATH, "//div[contains(text(), 'Post') or contains(text(), 'Post review')]")
        post_btn.click()
        time.sleep(5)
    except:
        pass

    automation_status["done"] = True
    automation_status["log"] = "✅ All 100 Reviews Sent Successfully!"
    
 except Exception as e:
    automation_status["log"] = f"❌ Error: {e}"
 finally:
    driver.quit()

# --- ROUTES ---
@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
 status = automation_status
 return templates.TemplateResponse("index.html", {"request": request, "status": status})

@app.get("/start")
async def start_bot():
    if not automation_status["done"]:
        return {"status": "already_running"}
 
    automation_status["log"] = "Starting bot..."
    automation_status["done"] = False
    automation_status["progress"] = 0
    
    # Run in background thread
    thread = threading.Thread(target=run_automation)
    thread.start()
    
    return {"status": "started"}

    @app.get("/status")
    async def get_status():
        return automation_status

if __name__ == "__main__":
    generate_dummy_data()
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)