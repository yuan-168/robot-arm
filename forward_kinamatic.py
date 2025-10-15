# Importing necessary libraries from ROS2 Python client library
import rclpy
from rclpy.node import Node
from std_msgs.msg import String  # Import the String message type from standard ROS2 message library


# Defining the SimpleSubscriber class which inherits from Node
class SimpleSubscriber(Node):

    def __init__(self):
        super().__init__('simple_subscriber')  # Initialize the node with the name 'simple_subscriber'
        # Create a subscription object that listens to messages of type String
        # on the topic 'topic'. The 'listener_callback' function is called
        # when a new message is received. '10' is the queue size.
        self.subscription = self.create_subscription(
            Float32MultiArray,
            '/joint_state',
            self.listener_callback,
            10)
        self.subscription  # Dummy expression to avoid unused variable warning

    def listener_callback(self, msg):
        # Callback function that is invoked when a new message is received
        self.get_logger().info('I heard: "%s"' % msg.data)  # Log the received message
        num_joints = 3  # change to match your robot
        pos = msg.data[0:num_joints]
        vel = msg.data[num_joints:2*num_joints]
        cur = msg.data[2*num_joints:3*num_joints]
        
        x, y = self.kinamatic(pos)
        J = self.jacobian(pos)


    def kinamatic(self, pos):
        # callback function that calculate the 2d location
        joint1, joint2, joint3 = pos
        x = cos(joint1)*10+cos(joint1+joint2)*10+cos(joint3+joint2+joint1)*10
        y = sin(joint1)*10+sin(joint1+joint2)*10+sin(joint3+joint2+joint1)*10

        self.get_logger().info(f"End effector position: x={x:.2f}, y={y:.2f}")
        return x, y

    def jacobian(self, pos):
        joint1, joint2, joint3 = pos
        L1 = L2 = L3 = 10.0  # link lengths

        J = np.array([
        [
            -L1*sin(joint1) - L2*sin(joint1 + joint2) - L3*sin(joint1 + joint2 + joint3),
            -L2*sin(joint1 + joint2) - L3*sin(joint1 + joint2 + joint3),
            -L3*sin(joint1 + joint2 + joint3)
        ],
        [
             L1*cos(joint1) + L2*cos(joint1 + joint2) + L3*cos(joint1 + joint2 + joint3),
             L2*cos(joint1 + joint2) + L3*cos(joint1 + joint2 + joint3),
             L3*cos(joint1 + joint2 + joint3)
        ]
        ])
        return J


# The main function which serves as the entry point for the program
def main(args=None):
    rclpy.init(args=args)  # Initialize the ROS2 Python client library
    simple_subscriber = SimpleSubscriber()  # Create an instance of the SimpleSubscriber

    try:
        rclpy.spin(simple_subscriber)  # Keep the node alive and listening for messages
    except KeyboardInterrupt:  # Allow the program to exit on a keyboard interrupt (Ctrl+C)
        pass

    simple_subscriber.destroy_node()  # Properly destroy the node
    rclpy.shutdown()  # Shutdown the ROS2 Python client library

# This condition checks if the script is executed directly (not imported)
if __name__ == '__main__':
    main()  # Execute the main function
