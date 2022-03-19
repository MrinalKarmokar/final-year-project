
#if (ARDUINO >= 100)
  #include <Arduino.h>
#else
  #include <WProgram.h>
#endif
#include "HCPCA9685.h"
#include <ros.h>
#include "mums_assistant/Dofs.h"

using namespace ros;

ros::NodeHandle nh;

/* I2C slave address for the device/module. For the HCMODU0097 the default I2C address
   is 0x40 */
#define  I2CAdd 0x40

/* Create an instance of the library */
HCPCA9685 HCPCA9685(I2CAdd);

void cb( const mums_assistant::Dofs& msg){

//write data to servo!s, from the variable Dofs subscribed from topic arm_dofs
  HCPCA9685.Servo(0, angleToPulse(msg.joint1)+90);
  HCPCA9685.Servo(2, angleToPulse(msg.joint2)+90);
  HCPCA9685.Servo(4, angleToPulse(msg.joint3)+90);
  HCPCA9685.Servo(6, angleToPulse(msg.joint4)+90);
  HCPCA9685.Servo(8, angleToPulse(msg.joint5)+90);
  HCPCA9685.Servo(10, -angleToPulse(msg.joint6));
}

Subscriber<mums_assistant::Dofs>sub("arm_dofs", cb);

int angleToPulse(int ang){
   int pulse = map(ang,0, 180, 50,440);// map angle of 0 to 180 to Servo min and Servo max
   return pulse;
}

void setup()
{
  /* Initialise the library and set it to 'servo mode' */
  HCPCA9685.Init(SERVO_MODE);

  /* Wake the device up */
  HCPCA9685.Sleep(false);

  nh.getHardware()->setBaud(115200);
  nh.initNode();
  nh.subscribe(sub);
//  init_servo();
}


void loop()
{

  nh.spinOnce();
  delay(100);

}