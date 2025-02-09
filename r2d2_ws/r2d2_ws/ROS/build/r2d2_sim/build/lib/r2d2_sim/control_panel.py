import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel

class ControlPanel(Node, QWidget):
    def __init__(self):
        Node.__init__(self, 'control_panel')
        QWidget.__init__(self)
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Control Panel')
        layout = QVBoxLayout()

        label = QLabel('Move the Robot')
        layout.addWidget(label)
        forward_button = QPushButton('Forward')
        forward_button.clicked.connect(self.move_forward)
        layout.addWidget(forward_button)
        backward_button = QPushButton('Backward')
        backward_button.clicked.connect(self.move_backward)
        layout.addWidget(backward_button)
        left_button = QPushButton('Left')
        left_button.clicked.connect(self.turn_left)
        layout.addWidget(left_button)
        right_button = QPushButton('Right')
        right_button.clicked.connect(self.turn_right)
        layout.addWidget(right_button)
        stop_button = QPushButton('Stop')
        stop_button.clicked.connect(self.stop)
        layout.addWidget(stop_button)

        self.setLayout(layout)

    def move_forward(self):
        msg = Twist()
        msg.linear.x = 1.0
        self.publisher.publish(msg)

    def move_backward(self):
        msg = Twist()
        msg.linear.x = -1.0
        self.publisher.publish(msg)

    def turn_left(self):
        msg = Twist()
        msg.angular.z = 1.0
        self.publisher.publish(msg)

    def turn_right(self):
        msg = Twist()
        msg.angular.z = -1.0
        self.publisher.publish(msg)

    def stop(self):
        msg = Twist()
        self.publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    app = QApplication([])

    node = ControlPanel()
    node.show()

    app.exec_()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
