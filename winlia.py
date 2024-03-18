from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QApplication, QLineEdit, QTextEdit
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont

class CustomMessage(QWidget):
    def __init__(self, message, css, duration=None):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.initUI(message, css)
        if duration:
            QTimer.singleShot(duration, self.close)
        screen_geometry = QApplication.desktop().screenGeometry()
        self.setGeometry(screen_geometry.width() - 700, 0, 700, screen_geometry.height() - 700)

    def initUI(self, message, css):

        layout = QVBoxLayout()
        
        self.text_display = QTextEdit()
        #self.text_display.setPlainText()
        self.text_display.setFont(QFont('Roboto', 16))
        layout.addWidget(self.text_display)
        
        message_label = QLabel(message)
        message_label.setFont(QFont('Roboto', 16))
        message_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(message_label)
        self.setLayout(layout)
        
        style = self.open_style(css)
        self.setStyleSheet(style)

    def open_style(self,file_path, style="MSG"):
            """
            Abre un archivo y retorna el contenido de un estilo específico.

            Args:
            - file_path (str): La ruta al archivo a leer.
            - style (str): El estilo a buscar y retornar.

            Returns:
            - str: El contenido del estilo especificado.
            """
            # Define las etiquetas de inicio y fin basadas en el estilo
            start_tag = f"[{style}-INI]"
            end_tag = f"[{style}-END]"

            # Variables para controlar si estamos dentro de la sección correcta
            capture = False
            content = []

            # Abrir y leer el archivo
            with open(file_path, 'r') as file:
                for line in file:
                    if line.strip() == start_tag:
                        # Comienza a capturar el contenido
                        capture = True
                    elif line.strip() == end_tag:
                        # Termina la captura y sale del ciclo
                        capture = False
                        break
                    elif capture:
                        # Añade la línea actual al contenido si está dentro de la sección
                        content.append(line)

            # Retorna el contenido unido como una sola cadena
            return ''.join(content)
    def closeEvent(self, event):
        user_input = self.input_field.text()  # Captura el texto del campo de entrada
        user_text = self.text_display.toPlainText()  # Captura el texto del área de texto
        # Aquí podrías hacer algo con user_input y user_text, como guardarlos o procesarlos
        print("User entered:", user_input)
        print("User wrote in text area:", user_text)
        super().closeEvent(event)

class TimedMessage(CustomMessage):
    def __init__(self, message, css, duration=3000):  #
        super().__init__(message, css, duration)


def show_message(message, css, duration=3000):
    app = QApplication([])
    message = TimedMessage(message, css, duration)
    message.show()
    app.exec_()


# Example usage
#def main():
#    app = QApplication([])
#    message = TimedMessage("This is a test message", 5000)  # Message will last for 5 seconds
#    message.show()
#    app.exec_()

#if __name__ == "__main__":
#    main()

