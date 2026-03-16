import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32 

class DronePublisher(Node):
    def __init__(self):
        super().__init__('drone_publisher')
        self.publisher_ = self.create_publisher(Float32, 'drone_altitude', 10)
        
        timer_period = 1.0  
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.altitude = 0.0

    def timer_callback(self):
        msg = Float32()
        msg.data = self.altitude
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing Drone Altitude: "%f"' % msg.data)
        self.altitude += 0.5 

def main(args=None):
    rclpy.init(args=args)
    drone_publisher = DronePublisher()
    rclpy.spin(drone_publisher)
    drone_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
