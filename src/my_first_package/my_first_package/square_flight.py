import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy, DurabilityPolicy
from px4_msgs.msg import OffboardControlMode, TrajectorySetpoint, VehicleCommand

class SquareFlight(Node):
    def __init__(self):
        super().__init__('square_flight')
        
        qos_profile = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            durability=DurabilityPolicy.TRANSIENT_LOCAL,
            history=HistoryPolicy.KEEP_LAST,
            depth=1
        )

        self.offboard_control_mode_publisher = self.create_publisher(
            OffboardControlMode, '/fmu/in/offboard_control_mode', qos_profile)
        self.trajectory_setpoint_publisher = self.create_publisher(
            TrajectorySetpoint, '/fmu/in/trajectory_setpoint', qos_profile)
        self.vehicle_command_publisher = self.create_publisher(
            VehicleCommand, '/fmu/in/vehicle_command', qos_profile)

        self.timer = self.create_timer(0.1, self.timer_callback)
        self.timer_count = 0
        self.phase = "STARTING"

    def timer_callback(self):
        self.publish_offboard_control_mode()
        
        if self.timer_count == 10: 
            self.publish_vehicle_command(VehicleCommand.VEHICLE_CMD_DO_SET_MODE, 1.0, 6.0)
            self.arm()
            self.phase = "TAKEOFF"
            self.get_logger().info("Taking off...")

        elif self.timer_count == 100: 
            self.phase = "WP1"
            self.get_logger().info("Moving to Waypoint 1 (North 5m)...")
            
        elif self.timer_count == 200: 
            self.phase = "WP2"
            self.get_logger().info("Moving to Waypoint 2 (East 5m)...")
            
        elif self.timer_count == 300:
            self.phase = "WP3"
            self.get_logger().info("Moving to Waypoint 3 (South 5m)...")
            
        elif self.timer_count == 400: 
            self.phase = "WP4"
            self.get_logger().info("Moving to Waypoint 4 (Back to start)...")
            
        elif self.timer_count == 500: 
            self.land()
            self.phase = "LANDING"
            self.get_logger().info("Landing...")

        if self.phase == "TAKEOFF" or self.phase == "STARTING":
            self.publish_trajectory_setpoint(0.0, 0.0, -5.0)
        elif self.phase == "WP1":
            self.publish_trajectory_setpoint(5.0, 0.0, -5.0)
        elif self.phase == "WP2":
            self.publish_trajectory_setpoint(5.0, 5.0, -5.0)
        elif self.phase == "WP3":
            self.publish_trajectory_setpoint(0.0, 5.0, -5.0)
        elif self.phase == "WP4":
            self.publish_trajectory_setpoint(0.0, 0.0, -5.0)

        self.timer_count += 1

    def arm(self):
        self.publish_vehicle_command(VehicleCommand.VEHICLE_CMD_COMPONENT_ARM_DISARM, 1.0)

    def land(self):
        self.publish_vehicle_command(VehicleCommand.VEHICLE_CMD_NAV_LAND)

    def publish_offboard_control_mode(self):
        msg = OffboardControlMode()
        msg.position = True
        msg.velocity = False
        msg.acceleration = False
        msg.attitude = False
        msg.body_rate = False
        msg.timestamp = int(self.get_clock().now().nanoseconds / 1000)
        self.offboard_control_mode_publisher.publish(msg)

    def publish_trajectory_setpoint(self, x, y, z):
        msg = TrajectorySetpoint()
        msg.position = [float(x), float(y), float(z)]
        msg.yaw = 0.0
        msg.timestamp = int(self.get_clock().now().nanoseconds / 1000)
        self.trajectory_setpoint_publisher.publish(msg)

    def publish_vehicle_command(self, command, param1=0.0, param2=0.0):
        msg = VehicleCommand()
        msg.command = command
        msg.param1 = float(param1)
        msg.param2 = float(param2)
        msg.target_system = 1
        msg.target_component = 1
        msg.source_system = 1
        msg.source_component = 1
        msg.from_external = True
        msg.timestamp = int(self.get_clock().now().nanoseconds / 1000)
        self.vehicle_command_publisher.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = SquareFlight()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
