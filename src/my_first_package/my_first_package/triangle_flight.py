import rclpy
from rclpy.node import Node
from px4_msgs.msg import OffboardControlMode, TrajectorySetpoint, VehicleCommand

class TriangleFlightNode(Node):
    def __init__(self):
        super().__init__('triangle_flight')

        # Create Publishers for PX4 Offboard Control
        self.offboard_control_mode_publisher = self.create_publisher(
            OffboardControlMode, '/fmu/in/offboard_control_mode', 10)
        self.trajectory_setpoint_publisher = self.create_publisher(
            TrajectorySetpoint, '/fmu/in/trajectory_setpoint', 10)
        self.vehicle_command_publisher = self.create_publisher(
            VehicleCommand, '/fmu/in/vehicle_command', 10)

        # Timer running at 10 Hz (Required by PX4 for offboard mode)
        self.timer = self.create_timer(0.1, self.timer_callback)

        self.nav_state = 0
        self.counter = 0

        # The Equilateral Triangle Waypoints [X, Y, Z]
        self.waypoints = [
            [0.0, 0.0, -5.0],   # Point 1: Origin
            [5.0, 0.0, -5.0],   # Point 2: 5m North
            [2.5, 4.33, -5.0]   # Point 3: The Apex
        ]
        self.current_wp_index = 0

    def timer_callback(self):
        # 1. Constantly publish the offboard control mode heartbeat
        self.publish_offboard_control_mode()

        # 2. Arm and switch to Offboard mode on the very first loop
        if self.nav_state == 0:
            self.arm()
            self.set_offboard_mode()
            self.nav_state = 1
            self.get_logger().info("Drone Armed. Starting Triangle Trajectory.")

        # 3. Waypoint Navigation Logic
        if self.nav_state == 1:
            target = self.waypoints[self.current_wp_index]
            self.publish_trajectory_setpoint(target[0], target[1], target[2])

            # Wait exactly 10 seconds (100 ticks at 10Hz) at each waypoint
            self.counter += 1
            if self.counter >= 100:
                self.counter = 0
                self.current_wp_index += 1
                self.get_logger().info(f"Moving to Waypoint {self.current_wp_index + 1}")

                # Loop back to Point 1 to close the triangle
                if self.current_wp_index >= len(self.waypoints):
                    self.current_wp_index = 0

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
        msg.position = [x, y, z]
        msg.yaw = 0.0 
        msg.timestamp = int(self.get_clock().now().nanoseconds / 1000)
        self.trajectory_setpoint_publisher.publish(msg)

    def publish_vehicle_command(self, command, **params):
        msg = VehicleCommand()
        msg.command = command
        msg.param1 = params.get("param1", 0.0)
        msg.param2 = params.get("param2", 0.0)
        msg.target_system = 1
        msg.target_component = 1
        msg.source_system = 1
        msg.source_component = 1
        msg.from_external = True
        msg.timestamp = int(self.get_clock().now().nanoseconds / 1000)
        self.vehicle_command_publisher.publish(msg)

    def arm(self):
        self.publish_vehicle_command(VehicleCommand.VEHICLE_CMD_COMPONENT_ARM_DISARM, param1=1.0)

    def set_offboard_mode(self):
        self.publish_vehicle_command(VehicleCommand.VEHICLE_CMD_DO_SET_MODE, param1=1.0, param2=6.0)

def main():
    rclpy.init()
    node = TriangleFlightNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
