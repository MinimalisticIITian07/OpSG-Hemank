import rclpy
from rclpy.node import Node
from std_srvs.srv import SetBool 

class ArmingService(Node):
    def __init__(self):
        super().__init__('arming_service')
        self.srv = self.create_service(SetBool, 'arm_drone', self.arm_callback)
        self.get_logger().info('Arm Drone Service is ready.')

    def arm_callback(self, request, response):
        if request.data == True:
            response.success = True
            response.message = 'Drone successfully armed!'
            self.get_logger().info('Received request: Arming sequence initiated.')
        else:
            response.success = True
            response.message = 'Drone disarmed.'
            self.get_logger().info('Received request: Disarming sequence initiated.')
        
        return response

def main(args=None):
    rclpy.init(args=args)
    node = ArmingService()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
