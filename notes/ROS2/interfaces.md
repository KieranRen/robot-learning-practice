# ROS 2 Interfaces and a Dual-Arm Driver

[English](interfaces.md) | [中文](interfaces_zh.md)

## Overview

Study notes for 20–21 November 2026. I used the Tianji dual-arm driver to understand how an application connects to a robot, sends motion targets, and observes the measured state. The driver conventions below come from the interface material reviewed during these sessions. The examples were worked through on paper.

## 1. Nodes, names, and types

A ROS 2 node is a unit of computation. A node can offer several interfaces at once. The node name identifies who does the work, the interface name identifies where the interaction happens, and the interface type specifies the fields exchanged.

| Mechanism | Interaction | Definition | Typical use |
|---|---|---|---|
| Topic | Publishers send messages and subscribers receive them | `.msg` defines one message | State streams and continuously updated setpoints |
| Service | A client sends a request and receives a response | `.srv` has Request and Response sections separated by `---` | Connect, configure, select a mode, or submit a one-shot command |
| Action | A client submits a goal, can receive feedback and request cancellation, and gets a result | `.action` is written in Goal, Result, Feedback order | Move an arm to a pose or run a calibration |

For this case, `/tianji_driver` is the node, `/tianji/feedback` is an interface name, and `ArmFeedbacks` is the outer message type. A nested message is like a C struct used inside another struct. The same type can appear inside a Topic message or inside a Service request or Action goal. Think of the MuJoCo distinction between writing a control input and reading back `qpos`: ROS 2 carries those kinds of data between nodes.

## 2. Services and what the response confirms

| Service | Request | Meaning of success |
|---|---|---|
| `Command` | Connect or disconnect the shared link with an empty arm selector. Clear a fault or request a stop for a named arm. | The request was accepted. A stop response can arrive while the arm is still settling. |
| `SetMotionProfile` | Select one or more parameter groups: speed and acceleration limit ratios, joint impedance, Cartesian impedance, or impedance axes. The speed and acceleration ratios update together. | Feedback confirmed the selected parameters took effect and the mode stayed the same. An invalid selected value rejects the request. |
| `SetMode` | Select a mode for one arm, plus a drag direction when applicable. | Fresh feedback confirmed the requested mode and direction. |
| `SetToolTransform` | Set the fixed pose of the tool center point (TCP) in flange coordinates. Translation is in metres and rotation uses quaternion order `xyzw`. | The transform was updated and saved. |
| `set_gripper_enabled` | Use a Boolean to enable or disable one gripper. | Fresh gripper motor feedback confirmed the requested state. Disabling clears pending targets. |
| `SetGripperMIT` | Send one command to an enabled gripper. | One command frame was sent. Read the feedback stream to check actual motion. |

Motion-profile updates require a connected, stationary, fault-free arm with valid feedback. To select a nonzero mode, the arm must have valid feedback, be stationary and fault-free, and have no active motion source. Mode 0 disables the arm. Modes 1, 2, and 3 select joint position, joint impedance, and Cartesian impedance. Modes 4 and 5 select joint and Cartesian hand-guided drag; mode 5 uses direction 1/2/3/4 for X/Y/Z/rotation, while other modes use 0. When changing drag type or direction, release the hand-guiding button and wait for the arm to settle.

## 3. Actions and completion criteria

| Action | Goal and setup | Feedback and completion |
|---|---|---|
| `MoveJointPosition` | One seven-axis target for a single arm in mode 1. The arm in the goal matches the path. The driver interpolates from the measured starting position. | Progress uses measured aggregate joint displacement. It reaches 1 only when the measured joints are within tolerance and stationary. The documented default tolerance is 0.1° per joint. |
| `MoveJointImpedance` | One seven-axis equilibrium target for a single arm in mode 2. The driver interpolates from the measured starting position. | Progress tracks interpolation of the equilibrium target. Success confirms that the final equilibrium target was submitted. Actual joint angles may differ under load. |
| `CalibrateToolDynamics` | Select one arm, a file base name, and capture mode. The motion input must be closed and the arm stationary. Only one arm is sampled at a time. | Feedback reports the current stage and progress. Capture results point to a CSV. When tool parameters are applied, the result points to the parameter file and the mass, centre of mass, and inertia are valid. |

The motion Actions use the configured speed and acceleration ratios and require the appropriate mode before submission. Consider an illustrative joint goal from 10° to 40°. With position control, a measured angle of 25° is about half of the requested displacement. With impedance, the equilibrium reference may reach 40° while an external load holds the joint at 35°. The Action reports on its task; the feedback Topic reports the measured angle in both cases.

Calibration uses `"empty"` for a standalone unloaded capture and `"loaded"` for a standalone loaded capture. Sending the empty string starts the two-stage workflow. The first goal yields `BASELINE_READY`; after the tool is fitted, a second goal with the empty string runs identification and writeback, ending at `TOOL_APPLIED`. The model stores mass in kg, the centre of mass in the flange frame in m, and six inertia components about the flange origin in kg·m².

## 4. Topics and nested messages

| Topic | Direction from the application | Contents |
|---|---|---|
| `/tianji/feedback` | Subscribe | One `ArmFeedbacks` message contains two `ArmFeedback` elements, A first and B second. |
| `/tianji/target/joint_position` | Publish | A and B joint-position targets, plus matching gripper commands. |
| `/tianji/target/joint_impedance` | Publish | A and B joint-equilibrium targets, optional impedance updates, and matching gripper commands. |
| `/tianji/target/cartesian_impedance` | Publish | A and B Cartesian impedance targets and matching gripper commands. |
| `/tianji/control_cycle_hz` | Subscribe | A report of the measured control-loop frequency, published around once per second. |

On feedback, check the selected arm’s `valid` flag before using its joint state. `sample_time` is the receipt time of its latest valid sample. The stream also reports mode, enable state, faults, motion-profile readbacks, joint velocity, TCP pose and wrench, tool configuration, and gripper angle and torque. The two arms can differ in feedback validity. Some status fields use 255 for unknown or inapplicable values. Gripper angle and torque become NaN after more than one second without fresh gripper feedback.

Feedback order is fixed. Target array order is flexible, but each frame must contain one target for A and one for B. The command at `gripper_targets[i]` belongs to the arm named in `targets[i].arm`. Both arms must be in the required mode and ready to accept targets; one invalid side rejects the pair.

The nominal feedback and target rate is 500 Hz, about 2 ms per frame. A stream's nominal rate and the separately reported control-loop frequency describe different things. The driver uses ROS domain 66. Its feedback QoS is Reliable / Volatile / Keep Last 10, and the target streams use depth 1 with the same reliability and durability. QoS describes communication behavior such as delivery policy and retained history.

The singular `JointPositionTarget` is reused as a single-arm Action goal field and as each element of a dual-arm Topic target array. `JointImpedanceTarget` follows the same pattern and contains an `Impedance` value with seven stiffnesses and seven damping ratios. `GripperCommandValues` is reused in the single-shot gripper Service and in the target arrays. Its five fields specify motor angle, motor speed, position gain, damping gain, and signed feedforward torque. The application decides when to open, close, detect contact, and hold.

## 5. Impedance, frames, and units

Joint impedance behaves like a virtual spring and damper at each joint. Its correction is expressed as joint torque along that joint's axis. Cartesian impedance defines the response in tool-motion directions. For a sponge wiping a surface, the application can choose greater stiffness along the surface and lower stiffness normal to it. The corresponding joint motions depend on the arm configuration.

In this driver, the Cartesian message gives a seven-angle baseline equilibrium and a six-component target wrench. A zero wrench uses the baseline. With a nonzero wrench, the requested wrench and stiffness determine the equilibrium offset. A zero-stiffness axis requires zero target force or torque along that axis. The impedance axes are rotated from the arm base axes about fixed body axes. Use the identity rotation to retain the base directions. Impedance arrays are ordered J1–J7 in joint space and X/Y/Z/Rx/Ry/Rz/null space in Cartesian space. Damping ratio is dimensionless, from 0 to 1; gripper `kd` is a damping gain with units.

| Value | Convention in this driver |
|---|---|
| Arm joint angle / angular velocity | deg / deg/s |
| Gripper target angle / angular velocity | rad / rad/s |
| Gripper measured angle / torque | deg / N·m |
| Joint stiffness | N·m/deg |
| Cartesian translation stiffness / rotation and null-space stiffness | N/m / N·m/rad |
| TCP pose / commanded TCP wrench | Body frame; position in m, rotation in quaternion order `xyzw`, wrench in N and N·m |
| Measured TCP wrench | Current TCP frame, with moment taken about the TCP origin |
| Tool transform and tool dynamics | Flange frame |

## 6. Putting the interfaces together

For a one-off move, the application connects through a Service, subscribes to feedback and checks validity, configures parameters if needed, selects the mode, and sends an Action goal. It can read measured state during the action. For continuous dual-arm control, the application follows the same preparation and then publishes new dual-arm targets. Feedback still comes from the same subscription.

Each arm has one motion source at a time. An active motion goal blocks a new goal. For a handoff between a continuous target Topic and an Action, the documented sequence is to request a stop, confirm that the arm has settled, and select the mode again. Ceasing publication leaves Topic control ownership in place. A Service acknowledgment, an Action result, and a measured joint state each answer a different question.

## References

- [ROS 2 interface concepts](https://docs.ros.org/en/jazzy/Concepts/Basic/About-Interfaces.html)
- [ROS 2 topics, services, and actions](https://docs.ros.org/en/jazzy/How-To-Guides/Topics-Services-Actions.html)
