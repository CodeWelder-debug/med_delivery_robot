import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from nav2_msgs.action import NavigateToPose
import time

class HospitalDispatchServer(Node):
    def __init__(self):
        super().__init__('hospital_dispatch_server')
        
        self._nav_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')
        
        self.room_database = {
            "storage_room": {"x": 1.0, "y": 3.5},
            "room_a":       {"x": 3.0, "y": 3.5},
            "room_b":       {"x": 5.0, "y": 3.5},
            "room_c":       {"x": 7.0, "y": 3.5},
            "room_d":       {"x": 3.0, "y": -3.5},
            "room_e":       {"x": 5.0, "y": -3.5},
            "room_f":       {"x": 7.0, "y": -3.5}
        }
        
        self.get_logger().info('Hospital Named-Room Dispatch & Verification Server is online.')

    def dispatch_to_room(self, room_key):
        key = room_key.lower().replace(" ", "_")
        
        if key not in self.room_database:
            self.get_logger().error(f'Unknown room name: "{room_key}". Available rooms: {list(self.room_database.keys())}')
            return False

        coords = self.room_database[key]
        room_x = coords["x"]
        room_y = coords["y"]
        
        self.get_logger().info(f'Dispatching robot to [{room_key.upper()}] at coordinates ({room_x}, {room_y})...')
        
        if not self._nav_client.wait_for_server(timeout_sec=5.0):
            self.get_logger().error('Nav2 action server not available!')
            return False

        goal_msg = NavigateToPose.Goal()
        goal_msg.pose.header.frame_id = 'map'
        goal_msg.pose.header.stamp = self.get_clock().now().to_msg()
        goal_msg.pose.pose.position.x = room_x
        goal_msg.pose.pose.position.y = room_y
        goal_msg.pose.pose.orientation.w = 1.0

        self._send_goal_future = self._nav_client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback
        )
        self._send_goal_future.add_done_callback(self.goal_response_callback)
        return True

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().warn('Mission goal rejected by Nav2!')
            return

        self.get_logger().info('Mission goal accepted. Robot en route...')

    def feedback_callback(self, feedback_msg):
        pass

def main(args=None):
    rclpy.init(args=args)
    server = HospitalDispatchServer()
    server.dispatch_to_room("storage_room")
    
    try:
        rclpy.spin(server)
    except KeyboardInterrupt:
        pass
    finally:
        server.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()

if __name__ == '__main__':
    main()
