import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Bool

class AutonomousMover(Node):
    def __init__(self):
        super().__init__('autonomous_mover')
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        self.obstacle_sub = self.create_subscription(
            Bool, '/lidar_obstacle_detected', self.obstacle_callback, 10
        )
        
        self.obstacle_detected = False
        self.timer = self.create_timer(0.1, self.timer_callback)
        self.get_logger().info('Autonomous Robot Mover Node has started.')

    def obstacle_callback(self, msg: Bool):
        self.obstacle_detected = msg.data

    def timer_callback(self):
        msg = Twist()
        
        if self.obstacle_detected:
            msg.linear.x = 0.0
            msg.angular.z = 0.5
        else:
            msg.linear.x = 0.2
            msg.angular.z = 0.1
            
        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    autonomous_mover = AutonomousMover()
    
    try:
        rclpy.spin(autonomous_mover)
    except KeyboardInterrupt:
        pass
    finally:
        autonomous_mover.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()

if __name__ == '__main__':
    main()
