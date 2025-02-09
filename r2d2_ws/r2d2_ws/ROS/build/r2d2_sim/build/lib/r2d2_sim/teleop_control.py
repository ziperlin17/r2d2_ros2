import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from rclpy.node import Node
from rclpy.qos import QoSProfile
import rclpy
from geometry_msgs.msg import Twist

class TeleopControl(Node):
    def __init__(self):
        super().__init__('teleop_control')
        qos = QoSProfile(depth=10)
        self.publisher = self.create_publisher(Twist, '/cmd_vel', qos)
        self.twist = Twist()

    def send_command(self, linear_x, angular_z):
        self.twist.linear.x = linear_x
        self.twist.angular.z = angular_z
        self.publisher.publish(self.twist)
        self.get_logger().info(f'Sent command: linear={linear_x}, angular={angular_z}')

class TeleopWidget(QWidget):
    def __init__(self, teleop_node):
        super().__init__()
        self.teleop_node = teleop_node

        self.setWindowTitle('Robot Teleop Control')
        layout = QVBoxLayout()

        # Forward Button
        forward_btn = QPushButton('Move Forward')
        forward_btn.clicked.connect(lambda: self.teleop_node.send_command(1.0, 0.0))
        layout.addWidget(forward_btn)

        # Backward Button
        backward_btn = QPushButton('Move Backward')
        backward_btn.clicked.connect(lambda: self.teleop_node.send_command(-1.0, 0.0))
        layout.addWidget(backward_btn)

        # Turn Left Button
        left_btn = QPushButton('Turn Left')
        left_btn.clicked.connect(lambda: self.teleop_node.send_command(0.0, 1.0))
        layout.addWidget(left_btn)

        # Turn Right Button
        right_btn = QPushButton('Turn Right')
        right_btn.clicked.connect(lambda: self.teleop_node.send_command(0.0, -1.0))
        layout.addWidget(right_btn)

        # Stop Button
        stop_btn = QPushButton('Stop')
        stop_btn.clicked.connect(lambda: self.teleop_node.send_command(0.0, 0.0))
        layout.addWidget(stop_btn)

        self.setLayout(layout)

def main():
    rclpy.init()
    teleop_node = TeleopControl()

    app = QApplication(sys.argv)
    teleop_widget = TeleopWidget(teleop_node)
    teleop_widget.show()

    app.exec_()
    teleop_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
