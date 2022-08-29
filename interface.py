import sys
import os
import subprocess
import re
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QFormLayout, QVBoxLayout, QWidget, QHBoxLayout, \
    QLabel, QCheckBox, QPushButton, QTextEdit, QProgressBar
from PyQt5.QtWidgets import QFileDialog


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.setWindowTitle("Fake Image Detector")
        self.setGeometry(600, 200, 600, 400)  # Первые две координаты смешение окна, последние две-размеры окна.
        self.setFixedSize(600, 450)
        self.widget = QWidget()

        self.main_lay = QVBoxLayout(self)

        self.panel = ControlPanel()
        self.main_lay.addWidget(self.panel)

        self.widget.setLayout(self.main_lay)
        self.setCentralWidget(self.widget)
        self.show()


class ControlPanel(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()

        self.layout = QVBoxLayout(self)
        self.label_methods = QLabel('Choose methods to detect', self)
        self.layout.addWidget(self.label_methods)
        self.method_layout = QHBoxLayout(self)
        self.method_1 = QCheckBox("Metadata and ELA", self)
        self.method_2 = QCheckBox("ELA2", self)
        self.method_3 = QCheckBox("Face SpoffNet", self)
        self.method_4 = QCheckBox("Face MobileNetV2", self)
        self.method_layout.addWidget(self.method_1)
        self.method_layout.addWidget(self.method_2)
        self.method_layout.addWidget(self.method_3)
        self.method_layout.addWidget(self.method_4)
        self.layout.addLayout(self.method_layout)
        self.layout.setAlignment(Qt.AlignTop)

        self.path_layout = QHBoxLayout(self)
        self.label_path = QLabel('Choose image path', self)
        self.layout.addWidget(self.label_path)

        self.search_button = QPushButton('...', self)
        self.path_field = QTextEdit()
        self.path_field.setPlaceholderText("PATH to image")
        self.path_field.setReadOnly(True)
        self.path_field.setMaximumSize(450, 28)
        self.path_field.setMinimumSize(450, 28)
        self.path_layout.addWidget(self.path_field)
        self.path_layout.addWidget(self.search_button)
        self.layout.addLayout(self.path_layout)

        self.browser = WinBrowser()

        self.search_button.clicked.connect(self.browser.search_files)
        self.search_button.clicked.connect(self.print_path)
        self.search_button.clicked.connect(self.reset_progress_bar)

        self.start_layout = QHBoxLayout()
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setMaximumSize(450, 23)
        self.progress_bar.setMinimumSize(450, 23)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.start_layout.addWidget(self.progress_bar)
        self.start_button = QPushButton('Start', self)
        self.start_button.clicked.connect(self.start)
        self.start_layout.addWidget(self.start_button)
        self.layout.addLayout(self.start_layout)

        self.result_layout = QFormLayout()
        self.result_label_1 = QLabel('...')
        self.result_label_2 = QLabel('...')
        self.result_label_3 = QLabel('...')
        self.result_label_4 = QLabel('...')
        self.result_label_5 = QLabel('...')
        self.result_layout.addRow(QLabel('Name of method'), QLabel('Result'))
        self.result_layout.setHorizontalSpacing(50)
        self.result_layout.setVerticalSpacing(20)
        self.result_layout.addRow(QLabel('Metadata (1.1) : '), self.result_label_1)
        self.result_layout.addRow(QLabel('ELA (1.2) : '), self.result_label_2)
        self.result_layout.addRow(QLabel('ELA (2) : '), self.result_label_3)
        self.result_layout.addRow(QLabel('Face SpoffNet (3) : '), self.result_label_4)
        self.result_layout.addRow(QLabel('FaceMobileNet_v2 (4) : '), self.result_label_5)
        self.layout.addSpacing(30)
        self.layout.addLayout(self.result_layout)
        self.layout.addStretch(5)
        self.layout.addSpacing(40)

        self.setLayout(self.layout)

    def print_path(self):
        self.path_field.setText(self.browser.filename)

    def checking_methods(self):
        self.reset_progress_bar()

        if self.method_1.checkState():
            self.image_manipulation_detection()
        self.progress_bar.setValue(40)

        if self.method_2.checkState():
            self.error_level_analysis()
        self.progress_bar.setValue(60)

        if self.method_3.checkState():
            self.face_spoffnet()
        self.progress_bar.setValue(80)

        if self.method_4.checkState():
            self.face_mobilenetv2()
        self.progress_bar.setValue(100)

    def image_manipulation_detection(self):
        path = os.path.abspath('method_ela_1/method_ela_1.py')
        param = str(self.path_field.toPlainText())

        proc = subprocess.Popen(["python", path, "-p", param], stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()
        proc.wait()

        print(out.decode("utf-8"))
        regex = r"(?<=\().+(?=\))"
        result = re.findall(regex, out.decode("utf-8"))
        result = result[len(result) - 1]
        result = result.replace('\\n', '')
        result = result.split(", ")

        self.result_label_1.setText(result[0])
        self.result_label_2.setText(result[1])

    def error_level_analysis(self):
        from method_ela_2 import method_ela_2 as ela2
        res, prob = ela2.method_ela_2(str(self.path_field.toPlainText()))
        self.result_label_3.setText(f"{res}! Probability: {prob}")

    def face_spoffnet(self):
        from method_face_spoffnet import method_face_spoffnet as spoff
        res, prob = spoff.method_face_spoffnet(str(self.path_field.toPlainText()))
        self.result_label_4.setText(f"{res}! Probability: {prob}")

    def face_mobilenetv2(self):
        from method_face_mobilenetv2 import method_face_mobilenetv2 as mobile
        res, prob = mobile.method_face_mobilenetv2(str(self.path_field.toPlainText()))
        self.result_label_5.setText(f"{res}! Probability: {prob}")

    def start(self):
        self.result_label_1.setText('...')
        self.result_label_2.setText('...')
        self.result_label_3.setText('...')
        self.result_label_4.setText('...')
        self.result_label_5.setText('...')

        if self.path_field.toPlainText() != '':
            self.checking_methods()
        else:
            self.path_field.setPlaceholderText("Please, choose image path")

    def reset_progress_bar(self):
        self.progress_bar.setValue(0)


class WinBrowser(QWidget):
    def __init__(self):
        super().__init__()
        self.filename = ''

    def search_files(self):
        file_name = QFileDialog.getOpenFileName(self, 'Open file', 'C:\\',
                                                'Images (*.jpg)')
        self.filename = file_name[0]


def start_app():
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())


if __name__ == '__main__':
    start_app()
