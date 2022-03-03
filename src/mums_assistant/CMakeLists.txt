cmake_minimum_required(VERSION 2.8.3)

project(mums_assistant)

find_package(catkin REQUIRED
	joint_state_publisher
	robot_state_publisher
	roslaunch
	rviz
	xacro
	roscpp
	urdf
	geometry_msgs
	roscpp
	rospy
	std_msgs
	sensor_msgs
	message_generation
)

add_message_files(
   FILES
   Dofs.msg
 )

generate_messages(
   DEPENDENCIES
   geometry_msgs
   sensor_msgs
   std_msgs
 )

catkin_package(
	CATKIN_DEPENDS geometry_msgs roscpp rospy std_msgs message_runtime
)

 include_directories(
# include
  ${catkin_INCLUDE_DIRS}
)

if(CATKIN_ENABLE_TESTING)
	find_package(roslaunch)
  roslaunch_add_file_check(launch)
endif()

foreach(dir config launch meshes urdf)
	install(DIRECTORY ${dir}/
		DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/${dir})
endforeach(dir)
