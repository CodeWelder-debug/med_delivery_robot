import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Bool
import math

class LidarProcessor(Node):
    def __init__(self):
        super().__init__('lidar_processor')
        
        self.subscription = self.create_subscription(
            LaserScan,
            '/scan',
            self.scan_callback,
            10
        )
        self.obstacle_publisher = self.create_publisher(Bool, '/lidar_obstacle_detected', 10)
        self.get_logger().info('LiDAR Processor Node has started.')

    def scan_callback(self, msg: LaserScan):
        if not msg.ranges:
            return

        num_ranges = len(msg.ranges)
        center_idx = num_ranges // 2
        span = int(num_ranges * 0.08)
        
        front_ranges = []
        for i in range(center_idx - span, center_idx + span):
            idx = i % num_ranges
            r = msg.ranges[idx]
            if not math.isinf(r) and not math.isnan(r) and r >= msg.range_min:
                front_ranges.append(r)

        min_front_distance = min(front_ranges) if front_ranges else msg.range_max

        obstacle_msg = Bool()
        if min_front_distance < 0.7:
            obstacle_msg.data = True
            self.get_logger().warn(f'Obstacle detected ahead! Distance: {min_front_distance:.2f} m', throttle_duration_sec=1.0)
        else:
            obstacle_msg.data = False

        self.obstacle_publisher.publish(obstacle_msg)

def main(args=None):
    rclpy.init(args=args)
    node = LidarProcessor()
    
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
