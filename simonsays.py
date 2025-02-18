import sys
import random
import pygame
from PyQt5 import QtWidgets, QtGui, QtCore

class SimonSaysApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simon Says 2025")
        self.setGeometry(100, 100, 400, 400)
        self.setStyleSheet("background-color: #282c34; color: white; font-family: Arial;")

        # Initialize Pygame mixer for sound
        pygame.mixer.init()

        # Load sound effects
        self.sounds = {
            "#ff4c4c": pygame.mixer.Sound("red_sound.wav"),
            "#4cff4c": pygame.mixer.Sound("green_sound.wav"),
            "#4c4cff": pygame.mixer.Sound("blue_sound.wav"),
            "#ffea4c": pygame.mixer.Sound("yellow_sound.wav"),
        }

        self.colors = ["#ff4c4c", "#4cff4c", "#4c4cff", "#ffea4c"]
        self.color_names = ["red", "green", "blue", "yellow"]
        self.sequence = []
        self.user_input = []
        self.level = 0
        self.score = 0
        self.high_score = 0

        # Create layout
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        # Create buttons for each color
        self.buttons = {}
        button_layout = QtWidgets.QGridLayout()
        for color in self.colors:
            button = QtWidgets.QPushButton()
            button.setStyleSheet(f"background-color: {color}; border-radius: 15px;")
            button.setFixedSize(150, 150)
            button.clicked.connect(lambda _, c=color: self.user_click(c))
            button_layout.addWidget(button, self.colors.index(color) // 2, self.colors.index(color) % 2)
            self.buttons[color] = button

        # Add button layout to main layout
        self.layout.addLayout(button_layout)

        # Score display in the center
        self.score_layout = QtWidgets.QVBoxLayout()
        self.score_label = QtWidgets.QLabel("Score: 0")
        self.high_score_label = QtWidgets.QLabel("High Score: 0")
        self.score_layout.addWidget(self.score_label)
        self.score_layout.addWidget(self.high_score_label)
        self.score_layout.setAlignment(QtCore.Qt.AlignCenter)

        # Add score layout to the main layout
        self.layout.addLayout(self.score_layout)

        # Modern Start label
        self.start_label = QtWidgets.QLabel("START")
        self.start_label.setStyleSheet("font-size: 36px; font-weight: bold; color: #61afef;")
        self.start_label.setAlignment(QtCore.Qt.AlignCenter)
        self.start_label.mousePressEvent = self.start_game  # Connect click event
        self.layout.addWidget(self.start_label)

        # Message label
        self.message = QtWidgets.QLabel("")
        self.layout.addWidget(self.message)

    def start_game(self, event=None):
        self.sequence = []
        self.user_input = []
        self.level = 0
        self.score = 0
        self.message.setText("Get Ready!")
        self.score_label.setText("Score: 0")
        self.high_score_label.setText(f"High Score: {self.high_score}")
        self.next_sequence()

    def next_sequence(self):
        self.user_input = []
        self.level += 1
        self.sequence.append(random.choice(self.colors))
        self.show_sequence()

    def show_sequence(self):
        self.message.setText(f"Level {self.level}")
        delay = max(1000 - (self.score * 100), 300)  # Minimum delay of 300ms
        for i, color in enumerate(self.sequence):
            QtCore.QTimer.singleShot(delay * (i + 1), lambda c=color: self.flash_color(c))
            
    def flash_color(self, color):
        button = self.buttons[color]
        button.setStyleSheet(f"background-color: {color}; border-radius: 15px; border: 5px solid white;")
        QtCore.QTimer.singleShot(500, lambda c=color: self.reset_color(c))

    def reset_color(self, color):
        button = self.buttons[color]
        button.setStyleSheet(f"background-color: {color}; border-radius: 15px;")

    def user_click(self, color):
        self.user_input.append(color)
        self.flash_color(color)
        if self.user_input == self.sequence:
            if len(self.user_input) == len(self.sequence):
                self.score += 1
                self.score_label.setText(f"Score: {self.score}")
                if self.score > self.high_score:
                    self.high_score = self.score
                    self.high_score_label.setText(f"High Score: {self.high_score}")
                QtCore.QTimer.singleShot(1000, self.next_sequence)
        elif len(self.user_input) == len(self.sequence):
            self.message.setText("Wrong! Game Over!")
            self.start_button.setEnabled(True)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = SimonSaysApp()
    window.show()
    sys.exit(app.exec_())