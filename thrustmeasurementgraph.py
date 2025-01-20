import sys
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QFileDialog, QLabel
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
# NABER 
class PlotWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Zagora Space İtki Zaman Grafiği")
        self.setGeometry(100, 100, 800, 600)
        
        # Ana widget ve layout
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)
        layout = QVBoxLayout(self.main_widget)
        
        # Grafik alanı
        self.canvas = FigureCanvas(plt.figure())
        layout.addWidget(self.canvas)
        
        # Dosya seçme butonu
        self.file_button = QPushButton("Dosya Seç", self)
        self.file_button.clicked.connect(self.select_file)
        layout.addWidget(self.file_button)

        # Grafiği güncelleme butonu
        self.update_button = QPushButton("Grafiği Güncelle", self)
        self.update_button.clicked.connect(self.plot_data)
        layout.addWidget(self.update_button)
        
        # Max itki değerini gösterecek etiket
        self.max_thrust_label = QLabel("Max İtki: N/A", self)
        layout.addWidget(self.max_thrust_label)

        self.file_path = None  # Dosya yolunu tutan değişken

    def select_file(self):
        file, _ = QFileDialog.getOpenFileName(self, "Dosya Seç", "", "Text Files (*.txt);;All Files (*)")
        if file:
            self.file_path = file
            print(f"Seçilen dosya: {self.file_path}")

    def plot_data(self):
        if not self.file_path:
            print("Lütfen bir dosya seçin.")
            return
        
        # Dosyayı oku
        time_data = []
        force_data = []

        try:
            with open(self.file_path, "r") as file:
                # Başlık satırını atla
                file.readline()
                for line in file:
                    try:
                        # Her satırda zaman ve itkiyi ayır
                        time_str, force_str = line.strip().split(", ")
                        time_data.append(float(time_str))  # Zamanı float olarak alıyoruz
                        force_data.append(float(force_str))
                    except ValueError:
                        continue
        except Exception as e:
            print(f"Hata: {e}")
            return

        # Veriyi NumPy dizisine dönüştür
        time_data = np.array(time_data)
        force_data = np.array(force_data)
        
        if len(time_data) == 0 or len(force_data) == 0:
            print("Veri boş, lütfen geçerli bir dosya seçin.")
            return

        # Max itki değerini hesapla ve göster
        max_thrust = np.max(force_data)
        self.max_thrust_label.setText(f"Max İtki: {max_thrust:.2f} Gram")

        # Yeni bir grafik oluştur
        self.canvas.figure.clear()
        ax = self.canvas.figure.add_subplot(111)
        ax.plot(time_data, force_data, label="İtki")
        ax.set_xlabel("Zaman (ms)")  # X eksenini ms cinsinden etiketliyoruz
        ax.set_ylabel("İtki (Gram)")
        ax.set_title("İtki-Zaman Grafiği")
        ax.grid(True)
        ax.legend()

        # Grafiği güncelle
        self.canvas.draw()

# PyQt5 uygulaması
def main():
    app = QApplication(sys.argv)
    window = PlotWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
