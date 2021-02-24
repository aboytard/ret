## ret:
<!--For the RET project, this package provides the ROS driver testing device. It must be running while the Button Pressing Detection is running on a Raspberry Pi.-->

## Prerequirement:

Having the right workspace  
In your workspace, create a repository for the RET:  
`$ mkdir -p workspace/ret/src `  
go into the folder :  
`$ cd workspace/ret/src`  
init the workspace:  
`$ catkin_init_worskspace`  
create the ROS configuration  
`$ cd .. `  
`$ catkin_make`  

## Requirement:
/!\ pilz_ws and ret_ws are in the same global workspace but do not belong to the same repositories
Step 1) Get the pilz robot driver  
In your workspace:  
`$ git clone -b melodic-devel https://github.com/PilzDE/pilz_robots.git`  
and follow the instruction of the readme file https://github.com/PilzDE/pilz_robots.  
/!\ pilz_utils and pilz_testutils has been moved from the former package  
add pilz_test_utils and pilz_utils  to the pilz_robots package:  
`$ git clone -b melodic-devel https://github.com/PilzDE/pilz_common.git`  

Tips: Try `rosdep install --from-paths src -r-y --ignore-src`

Once the configuration is setup, you need to make some changes inside this repository:  
Manually add the ready position to :  
`$ cd workspaces/pilz_ws/src/pilz_robots/prbt_moveit_config/config`

Ensure the first arg is defaulted to false like so - <arg name="iso10218_support" default="false" /> in robot.launch : look into pilz_robots/prbt_support/launch   

Add the ready position to the pilz_robot/prbt_moveit_config/config/prbt.srdf.xacro  
<group_state name="ready" group="manipulator">  
        <joint name="prbt_joint_1" value="-1.5245" />  
        <joint name="prbt_joint_2" value="-0.26" />  
        <joint name="prbt_joint_3" value="1.26" />  
        <joint name="prbt_joint_4" value="1.60" />  
        <joint name="prbt_joint_5" value="0" />  
        <joint name="prbt_joint_6" value="0" />  
    </group_state>  

/!\ This is in the global workspace, but in the ret repository
Step 2) Get the pilz_manipulation package in your repository  
`$ git clone https://github.com/aboytard/pilz_manipulation.git`  

You should check if these commands have been made:  
`$ sudo apt install ros-melodic-pilz-robots`  
`$ sudo apt update`  
`$ sudo apt install ros-melodic-pilz-industrial-motion`  

step 3) Get the ret package inside its own repository in the workspace  
`git clone https://github.com/aboytard/ret.git`
/!\ bInsure that you overlay the ret workspace with the pilz_ws:  
To do so, source the pilz_ws before catkin_make  

You should install InfluxDB on your machine. You can follow these command:  
`$ wget https://dl.influxdata.com/influxdb/releases/influxdb-1.8.4_linux_amd64.tar.gz`  
`$ tar xvfz influxdb-1.8.4_linux_amd64.tar.gz`  
`$ wget -qO- https://repos.influxdata.com/influxdb.key | sudo apt-key add -`  
`$ source /etc/lsb-release`  
`$ echo "deb https://repos.influxdata.com/${DISTRIB_ID,,} ${DISTRIB_CODENAME} stable" | sudo tee /etc/apt/sources.list.d/influxdb.list`  
`$ sudo apt-get update && sudo apt-get install influxdb`  

Step 4) Get the Raspeberri Pi set up  
To have your Raspberry Pi set up, you should follow the instructions in:  
`https://github.com/aboytard/Buttons_Pressing_Detection`

## Setup the communication between the computer and the RPi:
Step 1) Connect the computer to the pilz_robot  
The robot is currently configured on : `169.254.60.100`  
Step 2) Connect the computer and the RPi to the rooter on the same IP Net ID  
The socket communication is currently configured on : `10.4.11.132`  
If needed, create two static IP adress on the RPi and on your computer corresponding with the Net ID adress of the rooter (make sure that you are not already using these IP address)  

## Real robot + Raspberry Pi 
Spep 0) Setup the can:  
`$ sudo ip link set can0 up type can bitrate 1000000`  

Step 1) Launch the moveit driver + the /tool_pose_publisher:  
`roslaunch pilz_manipulation ret_pilz_ROS.launch sim:=false pipeline:=pilz_command_planner`  

Step 2) Make sure that the Button Pressing Detection is running on the RPi, and that the socket's client and servers are connecting on the same IP adress.  

Step 3) Run the RET node :  
`cd workspace/ret/src/ret/scripts` : You must run this node from the folder where you have put the scripts to use a relative path instead of a global path.
` rosrun ret RET_main.py `

Step 4) Run the Button Masher Application node:  
`rosrun pilz_manipulation Button_Masher_Application.py`


## Visualize the data
# In InfluxDB:
Step 1) Start InfluxDB  
`sudo service influxdb start`
Step 2) Visualize the data  
`show databases`  
`use <databases name>` (you may have to add those "" if you get into a parse error)  
`show measurement`  
`select <field keys> from <measurement name>`  
# In csv:  
`cd /workspaces/ret/src/ret/scripts/RET_csv_logfile`  




