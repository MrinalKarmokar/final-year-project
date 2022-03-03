#include <kdl/tree.hpp>
#include <ros/ros.h>
#include "robot_state_publisher/robot_state_publisher.h"
#include "robot_state_publisher/joint_state_listener.h"
#include <kdl_parser/kdl_parser.hpp>
using namespace std;
using namespace ros;
using namespace KDL;
using namespace robot_state_publisher;
JointStateListener::JointStateListener(const KDL::Tree& tree)
  : n_tilde_("~"), publish_rate_(0.0), state_publisher_(tree)
{
      // set publish frequency
  double publish_freq;
  n_tilde_.param("publish_frequency", publish_freq, 50.0);
  publish_rate_ = Rate(publish_freq);

  if (tree.getNrOfJoints() == 0){
        boost::shared_ptr<sensor_msgs::JointState> empty_state(new sensor_msgs::JointState);
    while (ros::ok()){
          empty_state->header.stamp = ros::Time::now();
      this->callbackJointState(empty_state);
      publish_rate_.sleep();
    }
  }
  else{
        // subscribe to mechanism state
    joint_state_sub_ = n_.subscribe("joint_states", 1, &JointStateListener::callbackJointState, this);
  }
};
JointStateListener::~JointStateListener()
{};
void JointStateListener::callbackJointState(const JointStateConstPtr& state)
{
      if (state->name.size() != state->position.size()){
        ROS_ERROR("Robot state publisher received an invalid joint state vector");
    return;
  }
  // get joint positions from state message
  map<string, double> joint_positions;
  for (unsigned int i=0; i<state->name.size(); i++)
    joint_positions.insert(make_pair(state->name[i], state->position[i]));
  state_publisher_.publishTransforms(joint_positions, state->header.stamp);
  publish_rate_.sleep();
}
// ----------------------------------
// ----- MAIN -----------------------
// ----------------------------------
int main(int argc, char** argv)
{
      // Initialize ros
  ros::init(argc, argv, "robot_state_publisher");
  NodeHandle node;
  // gets the location of the robot description on the parameter server
  KDL::Tree tree;
  if (!kdl_parser::treeFromParam("robot_description", tree)){
        ROS_ERROR("Failed to extract kdl tree from xml robot description");
    return -1;
  }
  if (tree.getNrOfSegments() == 0){
        ROS_WARN("Robot state publisher got an empty tree and cannot publish any state to tf");
    ros::spin();
  }
  else{
        JointStateListener state_publisher(tree);
    ros::spin();
  }
  return 0;
}