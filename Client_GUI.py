from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton, QVBoxLayout, QGridLayout
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt, QTimer

import sys
import cv2
import numpy as np
import networking
import mode_switcher

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image + 12 Buttons")
        self.setFixedSize(1200, 800)

        central = QWidget()
        layout = QVBoxLayout(central)

        # Top: picture
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.image_label, 3)

        self.timer = QTimer()
        self.timer.setInterval(10)  # 10 ms timer
        self.timer.timeout.connect(self.get_frame)
        self.timer.start()

        # Bottom: 2 rows x 6 columns of buttons
        grid = QGridLayout()
        for i in range(12):
            if i == 10:
                btn = QPushButton("Manual Mode")
            elif i == 11:
                btn = QPushButton("STOP")
            else:
                btn = QPushButton(f"Button {i+1}")
            btn.setFixedSize(180, 80)
            btn.clicked.connect(lambda checked, n=i + 1: self.button_send_program_switch(n))
            grid.addWidget(btn, i // 6, i % 6)
        button_widget = QWidget()
        button_widget.setLayout(grid)

        layout.addWidget(button_widget, 1)

        self.setCentralWidget(central)

    def get_frame(self):
        frame = networking.get_image_data()  # get the latest frame data from the networking thread
        # print(type(frame), frame.shape)
        # w.update_image(cv2.imencode('.png', frame)[1].tobytes())
        if frame is None:
            return
        self.update_image(frame)

    def update_image(self, image_data):

        # Expect a 3D BGR numpy array (h, w, 3)
        if isinstance(image_data, np.ndarray) and image_data.ndim == 3 and image_data.shape[2] == 3:
            h, w = image_data.shape[:2]
            rgb = cv2.cvtColor(image_data, cv2.COLOR_BGR2RGB)
            qimg = QImage(rgb.data, w, h, rgb.strides[0], QImage.Format.Format_RGB888).copy()
            pixmap = QPixmap.fromImage(qimg)
        else:
            pixmap = QPixmap()
            if not pixmap.loadFromData(image_data):
                return
        self.image_label.setPixmap(
            pixmap.scaled(1000, 600, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))

    def stop_timer(self):
        self.timer.stop()

    def button_send_program_switch(self, mode_num):
        mode_switcher.change_mode(mode_num)