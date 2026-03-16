import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
from rclpy.qos import qos_profile_sensor_data

class CameraViewer(Node):
    def __init__(self):
        super().__init__('camera_viewer')
        
        self.subscription = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.image_callback,
            qos_profile_sensor_data)
        
        self.br = CvBridge()
        self.get_logger().info("Camera Viewer Node Started. Waiting for video...")

    def image_callback(self, data):
        current_frame = self.br.imgmsg_to_cv2(data, desired_encoding='bgr8')
        
        cv2.imshow("Drone Camera Feed", current_frame)
        cv2.waitKey(1)

def main(args=None):
    rclpy.init(args=args)
    node = CameraViewer()
    rclpy.spin(node)
    
    node.destroy_node()
    rclpy.shutdown()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
