#if (ARDUINO >= 100)
#include <Arduino.h>
#else
#include <WProgram.h>
#endif
#include <ros.h>
#include <std_msgs/Float64.h>
#include <sensor_msgs/JointState.h>
#include <stdlib.h>
#include "std_msgs/Float32MultiArray.h"
#include <Servo.h>

ros::NodeHandle nh;

Servo servo1;
Servo servo2;
Servo servo3;
Servo servo4;
Servo servo5;
Servo servo6;

//---------------------------------------------------------------------

void arm_messageCb(const std_msgs::Float32MultiArray& cmd_msg)
{
  servo1.write(90+(cmd_msg.data[0])); //set servo angle, should be from 0-180
  servo2.write(90+(cmd_msg.data[1]));
  servo3.write(90+(cmd_msg.data[2]));
  servo4.write(90+(cmd_msg.data[3]));
  servo5.write(90+(cmd_msg.data[4]));
//  digitalWrite(13, HIGH - digitalRead(13)); //toggle led
}
 
ros::Subscriber<std_msgs::Float32MultiArray> sub_code_arm("/joint_servo_arm_topic", &arm_messageCb);


//---------------------------------------------------------------------

void gripper_messageCb(const std_msgs::Float32MultiArray& cmd_msg)
{
  servo6.write(90+(cmd_msg.data[0]));
//  digitalWrite(13, HIGH - digitalRead(13)); //toggle led
}
 
ros::Subscriber<std_msgs::Float32MultiArray> sub_code_gripper("/joint_servo_gripper_topic", &gripper_messageCb);


//----------------------------------------------------------------------

void arm_rviz_msgCb(const std_msgs::Float32MultiArray& cmd_msg)
{
  servo1.write(90+(180*cmd_msg.data[0]/3.14)); //set servo angle, should be from 0-180
  servo2.write(90+(180*cmd_msg.data[1]/3.14));
  servo3.write(90+(180*cmd_msg.data[2]/3.14));
  servo4.write(90+(180*cmd_msg.data[3]/3.14));
  servo5.write(90+(180*cmd_msg.data[4]/3.14));
}
 
ros::Subscriber<std_msgs::Float32MultiArray> sub_arm_rviz("/joint_servo_arm_rviz_topic", &arm_rviz_msgCb);

//----------------------------------------------------------------------


void gripper_rviz_msgCb(const std_msgs::Float32MultiArray& cmd_msg)
{
  servo6.write(180*cmd_msg.data[0]/3.14);
}
 
ros::Subscriber<std_msgs::Float32MultiArray> sub_gripper_rviz("/joint_servo_gripper_rviz_topic", &gripper_rviz_msgCb);

//----------------------------------------------------------------------


void setup()
{
  nh.getHardware()->setBaud(115200);
  nh.initNode();
  nh.subscribe(sub_code_arm);
  nh.subscribe(sub_code_gripper);
  nh.subscribe(sub_arm_rviz);
  nh.subscribe(sub_gripper_rviz);
  servo1.attach(2); //attach it to pin 2
  servo2.attach(3); //attach it to pin 3
  servo3.attach(4);
  servo4.attach(5);
  servo5.attach(6);
  servo6.attach(7);
}

void loop()
{
  nh.spinOnce();
  delay(1);
}
