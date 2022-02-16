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

//std_msgs::Float64 mydata;

Servo servo1;
Servo servo2;

//---------------------------------------------------------------------

void messageCb(const std_msgs::Float32MultiArray& cmd_msg)
{
  servo1.write(cmd_msg.data[0]); //set servo angle, should be from 0-180
  servo2.write(cmd_msg.data[1]);
  digitalWrite(13, HIGH - digitalRead(13)); //toggle led
}
 
ros::Subscriber<std_msgs::Float32MultiArray> sub("/joint_servo_topic", &messageCb);

//----------------------------------------------------------------------

//ros::Publisher chatter("chatter", &mydata);

void setup()
{
  nh.getHardware()->setBaud(115200);
  nh.initNode();
  nh.subscribe(sub);
//  nh.advertise(chatter);
//  ros::init(argc, argv, "listener");
//  ros::NodeHandle n;
//  ros::Subscriber sub = n.subscribe("chatter", 1000, chatterCallback);
//  ros::spin();
  servo1.attach(9); //attach it to pin 9
  servo2.attach(10);//attach it to pin10
}

void loop()
{
//  mydata.data = angle[1];
//  chatter.publish( &mydata );
  nh.spinOnce();
  delay(1);
}
