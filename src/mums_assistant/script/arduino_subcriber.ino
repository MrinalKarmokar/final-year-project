#if (ARDUINO >= 100)
  #include <Arduino.h>
#else
  #include <WProgram.h>
#endif
#include <Servo.h>
#include <ros.h>
#include "mums_assistant/Dofs.h"

using namespace ros;

ros::NodeHandle nh;

Servo servo1;
Servo servo2;
Servo servo3;
Servo servo4;
Servo servo5;
Servo servo6;

//---------------------------------------------------------------------

void init_servo(void){
  servo1.attach(3);
  servo2.attach(5);
  servo3.attach(6);
  servo4.attach(9);
  servo5.attach(10);
  servo6.attach(11);
}

void cb( const mums_assistant::Dofs& msg){

//write data to servo!s, from the variable Dofs subscribed from topic arm_dofs
  if (msg.joint1 != 0){
    servo1.write((msg.joint1)+90);
  }
  if (msg.joint2 != 0){
    servo2.write((msg.joint2)+90);
  }
  if (msg.joint3 != 0){
    servo3.write((msg.joint3)+90);
  }
  if (msg.joint4 != 0){
    servo4.write((msg.joint4)+90);
  }
  if (msg.joint5 != 0){
    servo5.write((msg.joint5)+90);
  }
  if (msg.joint6 != 0){
    servo6.write(-(msg.joint6));
  }
}

Subscriber<mums_assistant::Dofs>sub("arm_dofs", cb);

void setup(){

  nh.getHardware()->setBaud(115200);
  nh.initNode();
  nh.subscribe(sub);
  init_servo();

}

void loop(){
  nh.spinOnce();
  delay(100);
  //nh.loginfo("Ready to go");
}