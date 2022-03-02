
#include "Arduino.h"
#include <Servo.h>
#include <ros.h>
#include "mums_assistant/Dofs.h"

using namespace ros;

NodeHandle nh;


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

//write data to servos, from the variable Dofs subscribed from topic arm_dofs
  servo1.write((msg.joint1)-90);
  servo2.write((msg.joint2)-90);
  servo3.write((msg.joint3)-90);
  servo4.write((msg.joint4)-90);
  servo5.write((msg.joint5)-90);
  servo6.write((msg.joint6)-90);
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