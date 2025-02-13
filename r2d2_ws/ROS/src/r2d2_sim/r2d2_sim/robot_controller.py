import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TwistStamped

class RobotController(Node):
    def __init__(self):
        super().__init__('robot_controller')
        self.declare_parameter('frame_id', 'body')
        self.publisher = self.create_publisher(
            TwistStamped,
            '/diff_drive_controller/cmd_vel',
            10
        )
        self.get_logger().info("RobotController node started.")

    def send_command(self, linear_x, angular_z):
        msg = TwistStamped()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = self.get_parameter('frame_id').get_parameter_value().string_value
        msg.twist.linear.x = linear_x
        msg.twist.angular.z = angular_z

        self.publisher.publish(msg)
        self.get_logger().info(
            f"Sending command: linear_x={linear_x}, angular_z={angular_z}, frame_id={msg.header.frame_id}"
        )

def main(args=None):
    rclpy.init(args=args)
    node = RobotController()
    try:
        while rclpy.ok():
            node.send_command(0.1, 0.1)
            rclpy.spin_once(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

