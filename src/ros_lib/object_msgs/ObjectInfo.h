#ifndef _ROS_SERVICE_ObjectInfo_h
#define _ROS_SERVICE_ObjectInfo_h
#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include "ros/msg.h"
#include "object_msgs/Object.h"

namespace object_msgs
{

static const char OBJECTINFO[] = "object_msgs/ObjectInfo";

  class ObjectInfoRequest : public ros::Msg
  {
    public:
      typedef const char* _name_type;
      _name_type name;
      typedef bool _get_geometry_type;
      _get_geometry_type get_geometry;

    ObjectInfoRequest():
      name(""),
      get_geometry(0)
    {
    }

    virtual int serialize(unsigned char *outbuffer) const override
    {
      int offset = 0;
      uint32_t length_name = strlen(this->name);
      varToArr(outbuffer + offset, length_name);
      offset += 4;
      memcpy(outbuffer + offset, this->name, length_name);
      offset += length_name;
      union {
        bool real;
        uint8_t base;
      } u_get_geometry;
      u_get_geometry.real = this->get_geometry;
      *(outbuffer + offset + 0) = (u_get_geometry.base >> (8 * 0)) & 0xFF;
      offset += sizeof(this->get_geometry);
      return offset;
    }

    virtual int deserialize(unsigned char *inbuffer) override
    {
      int offset = 0;
      uint32_t length_name;
      arrToVar(length_name, (inbuffer + offset));
      offset += 4;
      for(unsigned int k= offset; k< offset+length_name; ++k){
          inbuffer[k-1]=inbuffer[k];
      }
      inbuffer[offset+length_name-1]=0;
      this->name = (char *)(inbuffer + offset-1);
      offset += length_name;
      union {
        bool real;
        uint8_t base;
      } u_get_geometry;
      u_get_geometry.base = 0;
      u_get_geometry.base |= ((uint8_t) (*(inbuffer + offset + 0))) << (8 * 0);
      this->get_geometry = u_get_geometry.real;
      offset += sizeof(this->get_geometry);
     return offset;
    }

    virtual const char * getType() override { return OBJECTINFO; };
    virtual const char * getMD5() override { return "1e9343217518c31b3fdbfdafad9f786b"; };

  };

  class ObjectInfoResponse : public ros::Msg
  {
    public:
      typedef bool _success_type;
      _success_type success;
      typedef object_msgs::Object _object_type;
      _object_type object;
      typedef int8_t _error_code_type;
      _error_code_type error_code;
      enum { NO_ERROR = 0 };
      enum { OBJECT_NOT_FOUND = 1 };
      enum { OTHER_ERROR = 2 };

    ObjectInfoResponse():
      success(0),
      object(),
      error_code(0)
    {
    }

    virtual int serialize(unsigned char *outbuffer) const override
    {
      int offset = 0;
      union {
        bool real;
        uint8_t base;
      } u_success;
      u_success.real = this->success;
      *(outbuffer + offset + 0) = (u_success.base >> (8 * 0)) & 0xFF;
      offset += sizeof(this->success);
      offset += this->object.serialize(outbuffer + offset);
      union {
        int8_t real;
        uint8_t base;
      } u_error_code;
      u_error_code.real = this->error_code;
      *(outbuffer + offset + 0) = (u_error_code.base >> (8 * 0)) & 0xFF;
      offset += sizeof(this->error_code);
      return offset;
    }

    virtual int deserialize(unsigned char *inbuffer) override
    {
      int offset = 0;
      union {
        bool real;
        uint8_t base;
      } u_success;
      u_success.base = 0;
      u_success.base |= ((uint8_t) (*(inbuffer + offset + 0))) << (8 * 0);
      this->success = u_success.real;
      offset += sizeof(this->success);
      offset += this->object.deserialize(inbuffer + offset);
      union {
        int8_t real;
        uint8_t base;
      } u_error_code;
      u_error_code.base = 0;
      u_error_code.base |= ((uint8_t) (*(inbuffer + offset + 0))) << (8 * 0);
      this->error_code = u_error_code.real;
      offset += sizeof(this->error_code);
     return offset;
    }

    virtual const char * getType() override { return OBJECTINFO; };
    virtual const char * getMD5() override { return "a9fe6ed8f44295e2c52c2814c09b1b79"; };

  };

  class ObjectInfo {
    public:
    typedef ObjectInfoRequest Request;
    typedef ObjectInfoResponse Response;
  };

}
#endif
