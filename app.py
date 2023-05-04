import pytube
import webbrowser, os

from threading import *
import sys
from PyQt5 import QtWidgets, QtCore, uic
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow

class MyWindow(QMainWindow):

    def __init__(self):
        super(MyWindow, self).__init__()
        self.size = None
        self.path = None
        uic.loadUi('main.ui', self)
        self.format_cb.addItems(['Audio', 'Video'])
        self.browse_btn.hide()
        self.handleButtons()

    def handleButtons(self):
        self.download_btn.clicked.connect(self.thread)
        self.browse_btn.clicked.connect(self.browsefile)

    def browsefile(self):
        webbrowser.open(os.path.realpath(self.path))
        self.browse_btn.hide()

    def thread(self):
        t1 = Thread(target=self.Download)
        t1.start()

    def on_progress(self, stream, chunk, bytes_remaining):
        videoprogress = (round(100 - (bytes_remaining / self.size) * 100))
        self.progressBar.setValue(videoprogress)

    def on_complete(self,stream,filepath):
        self.browse_btn.show()


    def Download(self):
        self.path = self.path_lineEdit.text()
        url = self.url_lineEdit.text()
        status = 'Connecting, Please wait...'+'\n'
        self.status_label.setText(status)
        video = pytube.YouTube(url, on_progress_callback=self.on_progress, on_complete_callback=self.on_complete)
        Streams = video.streams

        Format = self.format_cb.currentText()

        if Format == 'Audio':
            Filter = Streams.get_audio_only(subtype='mp4')
        if Format == 'Video':
            Filter = Streams.get_highest_resolution()
        status = status + 'Now downloading:' + video.title + '\n'

        self.status_label.setText(status)
        self.size = Filter.filesize
        sizer = round(Filter.filesize / 1000000)
        status = status + 'Size:' +  str(sizer) + 'MB' + '\n'
        self.status_label.setText(status)

        Filter.download(self.path)
        status += 'Done!' + '\n'
        self.status_label.setText(status)

        self.browse_btn.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.setWindowTitle("YoutubeDownloader")
    #window.setWindowIcon(QIcon(''))
    window.show()
    sys.exit(app.exec_())
