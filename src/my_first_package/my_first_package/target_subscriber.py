import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32

class TargetSubscriber(Node):
    def __init__(self):
        super().__init__('target_subscriber')
        # Create a subscriber listening to the 'drone_altitude' topic
        self.subscription = self.create_subscription(
            Float32,
            'drone_altitude', 
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info('Received Target Altitude Data: "%f"' % msg.data)

def main(args=None):
    rclpy.init(args=args)
    target_subscriber = TargetSubscriber()
    rclpy.spin(target_subscriber)
    target_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
