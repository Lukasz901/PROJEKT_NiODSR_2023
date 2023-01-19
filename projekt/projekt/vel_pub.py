#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Point


#funkcja skalująca predkość dla robota
def velocity_scaling(bounds, point, velocity,inverse = False):
    max = 0
    min = 0
    if(bounds[0] > bounds[1]):
        max = bounds[0]
        min = bounds[1]
    elif(bounds[1] > bounds[0]):
        max = bounds[1]
        min = bounds[0]
    elif(bounds[0] == bounds[1] or velocity <= 0.0):
        return 0
    
    b = (-1* velocity * min)/(max - min)
    a = velocity/(max - min)
    
    wynik = a * point + b
    
    if(inverse):
        wynik = velocity - wynik
    return wynik


#definicja kierunku prędkości w zależności od współrzędnych punktu
def control_algorithm(point_data, velocity):
        msg_data = Twist()
        if(point_data.y < 256 and (point_data.x >= 255 and point_data.x <445) ) :
            msg_data.linear.x = velocity_scaling((255,0),point_data.y, velocity, True)
        elif(point_data.y > 256 and (point_data.x >= 255 and point_data.x <445)):
            msg_data.linear.x = -1*velocity_scaling((257,512),point_data.y, velocity)
        elif((point_data.x>=445)and(point_data.y >=190 and point_data.y <322)):
            msg_data.angular.z = -1*velocity_scaling((445,700),point_data.x, velocity)
        elif((point_data.x <255 and point_data.x >=0) and (point_data.y >=190 and point_data.y <322)):
            msg_data.angular.z = velocity_scaling((255,0), point_data.x, velocity, True)
        elif((point_data.y >=0 and point_data.y <190) and (point_data.x>=0 and point_data.x<255)):
            msg_data.linear.x = velocity_scaling((190,0),point_data.y, velocity ,True)
            msg_data.angular.z = velocity_scaling((255,0),point_data.x, velocity,True)
        elif((point_data.y >=322) and (point_data.x>=0 and point_data.x<255)):
            msg_data.linear.x = -1*velocity_scaling((322,512),point_data.y, velocity)
            msg_data.angular.z = velocity_scaling((255,0),point_data.x, velocity,True)
        elif((point_data.x >=445) and (point_data.y >=0 and point_data.y <190)):
            msg_data.linear.x = velocity_scaling((0,190),point_data.y, velocity,True)
            msg_data.angular.z = -1*velocity_scaling((445,700),point_data.x, velocity)
        elif((point_data.x >=445) and (point_data.y >=322)):
            msg_data.linear.x = -1*velocity_scaling((322,512),point_data.y, velocity)
            msg_data.angular.z = -1*velocity_scaling((445,700),point_data.x, velocity)
        else:
            msg_data.linear.x = 0.0
            msg_data.angular.z = 0.0
        return msg_data


class MinimalPublisher(Node):
    def __init__(self):
        super().__init__('Velocity')
        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)
        self.subscription = self.create_subscription(Point,'point',self.listener_callback,10)
        self.subscription
        self.declare_parameter('velocity_max', 1.0)
        self.my_velocity = self.get_parameter('velocity_max').value 
        timer_period = 0.5  # seconds
        #self.timer = self.create_timer(timer_period, self.timer_callback)
        self.msg = Twist()
        
    def timer_callback(self):
        self.publisher_.publish(self.msg)
        
    def listener_callback(self,point_data):
        self.msg = control_algorithm(point_data, self.my_velocity)
        self.publisher_.publish(self.msg)
        
        
def main(args=None):
    rclpy.init(args=args)
    minimal_publisher = MinimalPublisher()
    minimal_publisher.get_logger().info('Publisher Predkosci Aktywny')
    rclpy.spin(minimal_publisher)
    rclpy.shutdown()

if __name__ == '__main__':
        self.publisher_.publish(self.msg)
