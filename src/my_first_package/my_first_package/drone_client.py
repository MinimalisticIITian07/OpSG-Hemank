import rclpy
from rclpy.node import Node
from std_srvs.srv import SetBool

class ArmingClient(Node):
    def __init__(self):
        super().__init__('arming_client')
        self.cli = self.create_client(SetBool, 'arm_drone')
        
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Service not available, waiting again...')
        
        self.req = SetBool.Request()

    def send_request(self, arm_command):
        self.req.data = arm_command
        
        self.future = self.cli.call_async(self.req)
        rclpy.spin_until_future_complete(self, self.future)
        return self.future.result()

def main(args=None):
    rclpy.init(args=args)
    
    client = ArmingClient()
    
    client.get_logger().info('Sending request to arm drone...')
    response = client.send_request(True) 
    
    client.get_logger().info('Result from server: success=%s, message="%s"' % (response.success, response.message))
    
    client.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
