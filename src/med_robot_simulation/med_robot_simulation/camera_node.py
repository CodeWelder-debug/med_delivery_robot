import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image

class CameraNode(Node):
    def __init__(self):
        super().__init__('camera_node')
        self.subscription = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.image_callback,
            10
        )
        self.get_logger().info('Camera Node has started.')

    def image_callback(self, msg: Image):
        self.get_logger().info(
            f'Received frame: {msg.width}x{msg.height} pixels',
            throttle_duration_sec=2.0
        )

def main(args=None):
    rclpy.init(args=args)
    node = CameraNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()

if __name__ == '__main__':
    main()
