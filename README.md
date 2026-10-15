# Medical Delivery Robot (ROS 2 & Gazebo Sim)

A ROS 2-based autonomous mobile robot simulation project designed for navigating hospital environments, avoiding obstacles, and managing delivery tasks. This simulation utilizes **Gazebo Sim (Ignition Gazebo)** and custom SDF worlds to test path planning, LIDAR sensor integration, and robot localization.

---

## Features
- **Custom Hospital World:** Features a 3D hospital building mesh (`hospital_obj` / `hospital_stl`) complete with inline obstacles (barriers, pillars, partitions) for rigorous navigation testing.
- **Differential/Omni Drive Integration:** Configured with `ros_gz_bridge` to seamlessly bridge ROS 2 topics (`/cmd_vel`, `/odom`, `/scan`) with Gazebo physics and sensors.
- **Robot State Publisher:** Publishes robot transforms and URDF descriptions (`med_robot_simulation`).
- **Autonomous Navigation Ready:** Integrated sensor suites (LIDAR, odometry) suited for SLAM, costmaps, and navigation stacks (Nav2).

---

## Repository Structure

```text
med_delivery_robot/
├── build/                 # Colcon build artifacts
├── install/               # Colcon installation space
├── log/                   # Build and execution logs
└── src/
    └── med_robot_simulation/
        ├── config/        # Configuration files (Nav2, controllers, bridges)
        ├── launch/        # ROS 2 launch files (simulation.launch.py)
        ├── meshes/        # 3D hospital models (.obj, .stl)
        ├── resource/      # Package resource markers
        ├── urdf/          # Robot description files and xacros
        ├── worlds/        # Gazebo world files (hospital_world.sdf)
        ├── package.xml    # Package dependencies
        └── setup.py       # Python package setup file
```

---

## Prerequisites & Dependencies

Ensure your system meets the following requirements before building:
- **OS:** Ubuntu 22.04 LTS (Jammy Jellyfish) or compatible Linux distribution
- **ROS 2:** Humble Hawksbill (or Iron/Jazzy depending on your local setup)
- **Gazebo Sim:** Fortress / Garden (compatible with `gz-sim` packages)
- **Colcon:** ROS 2 build tool

---

## Installation & Setup

1. **Clone or open your workspace directory:**
   ```bash
   cd ~/med_delivery_robot
   ```

2. **Install missing dependencies (if any):**
   ```bash
   rosdep install --from-paths src --ignore-src -r -y
   ```

3. **Build the workspace:**
   ```bash
   colcon build --packages-select med_robot_simulation
   ```

4. **Source the workspace overlay:**
   ```bash
   source install/setup.bash
   ```

---

## Running the Simulation

To launch the hospital world, spawn the medical delivery robot, and activate the ROS 2-Gazebo bridge, execute:

```bash
ros2 launch med_robot_simulation simulation.launch.py
```

### Key Topics Published/Subscribed:
- **Control Command:** `/cmd_vel` (`geometry_msgs/msg/Twist`)
- **Odometry:** `/odom` (`nav_msgs/msg/Odometry`)
- **LIDAR Scan:** `/scan` (`sensor_msgs/msg/LaserScan`)
- **Clock:** `/clock` (`rosgraph_msgs/msg/Clock`)

---

## Customizing Obstacles
Obstacles are embedded directly as inline models within the world file to ensure an offline, error-free simulation load. You can modify, add, or reposition obstacles by editing the world configuration:
```bash
nano src/med_robot_simulation/worlds/hospital_world.sdf
```
After making changes, remember to rebuild your workspace:
```bash
colcon build --packages-select med_robot_simulation && source install/setup.bash
```

---

## License
This project is developed for educational and research purposes under standard academic/open-source guidelines.
