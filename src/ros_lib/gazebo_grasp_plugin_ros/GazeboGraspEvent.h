#ifndef _ROS_gazebo_grasp_plugin_ros_GazeboGraspEvent_h
#define _ROS_gazebo_grasp_plugin_ros_GazeboGraspEvent_h

#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include "ros/msg.h"

namespace gazebo_grasp_plugin_ros
{

  class GazeboGraspEvent : public ros::Msg
  {
    public:
      typedef const char* _arm_type;
      _arm_type arm;
      typedef const char* _object_type;
      _object_type object;
      typedef bool _attached_type;
      _attached_type attached;

    GazeboGraspEvent():
      arm(""),
      object(""),
      attached(0)
    {
    }

    virtual int serialize(unsigned char *outbuffer) const override
    {
      int offset = 0;
      uint32_t length_arm = strlen(this->arm);
      varToArr(outbuffer + offset, length_arm);
      offset += 4;
      memcpy(outbuffer + offset, this->arm, length_arm);
      offset += length_arm;
      uint32_t length_object = strlen(this->object);
      varToArr(outbuffer + offset, length_object);
      offset += 4;
      memcpy(outbuffer + offset, this->object, length_object);
      offset += length_object;
      union {
        bool real;
        uint8_t base;
      } u_attached;
      u_attached.real = this->attached;
      *(outbuffer + offset + 0) = (u_attached.base >> (8 * 0)) & 0xFF;
      offset += sizeof(this->attached);
      return offset;
    }

    virtual int deserialize(unsigned char *inbuffer) override
    {
      int offset = 0;
      uint32_t length_arm;
      arrToVar(length_arm, (inbuffer + offset));
      offset += 4;
      for(unsigned int k= offset; k< offset+length_arm; ++k){
          inbuffer[k-1]=inbuffer[k];
      }
      inbuffer[offset+length_arm-1]=0;
      this->arm = (char *)(inbuffer + offset-1);
      offset += length_arm;
      uint32_t length_object;
      arrToVar(length_object, (inbuffer + offset));
      offset += 4;
      for(unsigned int k= offset; k< offset+length_object; ++k){
          inbuffer[k-1]=inbuffer[k];
      }
      inbuffer[offset+length_object-1]=0;
      this->object = (char *)(inbuffer + offset-1);
      offset += length_object;
      union {
        bool real;
        uint8_t base;
      } u_attached;
      u_attached.base = 0;
      u_attached.base |= ((uint8_t) (*(inbuffer + offset + 0))) << (8 * 0);
      this->attached = u_attached.real;
      offset += sizeof(this->attached);
     return offset;
    }

    virtual const char * getType() override { return "gazebo_grasp_plugin_ros/GazeboGraspEvent"; };
    virtual const char * getMD5() override { return "a5b6c6f554465c6bcbcad9409a41137a"; };

  };

}
#endif
