############################################################################

target_name = "deform_rig"
control_name = "control_rig"

############################################################################

import bpy

C = bpy.context
D = bpy.data
O = bpy.ops

Armature = D.objects[target_name].data

#sym_names = ["hand", "arm_lower_2", "arm_lower_1", "arm_upper_2", "arm_upper_1"]

arm_origin_names = ["arm_upper", "arm_lower"]
arm_end_origin_names = ["shoulder", "hand"]

leg_origin_names = ["leg_upper", "leg_lower"]
foot_name = "foot"
hip_name = "hip"


def deselect_all():
    for obj in bpy.data.objects:
        obj.select_set(False)
    bpy.context.view_layer.objects.active = None
            

def default_start_pos():
    current_mode = bpy.context.object.mode
    match current_mode:
        case "POSE":
            bpy.ops.object.mode_set(mode="OBJECT")
            deselect_all()
        case "EDIT":
            bpy.ops.object.mode_set(mode="OBJECT")
            deselect_all()
        case "OBJECT":
            deselect_all()

            
def select_target():
    target = bpy.data.objects[target_name]
    target.select_set(True)
    bpy.context.view_layer.objects.active = target

    
def deselect_all_edit_bones():
    C.object.data.edit_bones.active = None
    O.armature.select_all(action='DESELECT')

    
def deselect_all_pose_bones():
    C.object.data.bones.active = None
    O.pose.select_all(action='DESELECT')


def create_limb_bb(origins, side):
    seg_count = 12
    
    for b in origins:
        o_bone = Armature.edit_bones[b+"."+side]
        
        bb1 = Armature.edit_bones.new(b+"_bb_1."+side)
        bb1.head = o_bone.head
        bb1.tail = o_bone.tail
        bb1.roll = o_bone.roll
        bb1.length = 0.1
        bb1.parent = o_bone
        bb1.use_deform = False
        
        bb2 = Armature.edit_bones.new(b+"_bb_2."+side)
        bb2.head = o_bone.head
        bb2.tail = o_bone.tail
        bb2.roll = o_bone.roll
        bb2.length = o_bone.length + 0.1
        bb2.head = o_bone.tail
        bb2.parent = o_bone
        bb2.use_deform = False
        
        bb = Armature.edit_bones.new(b+"_bb."+side)
        bb.head = o_bone.head
        bb.tail = o_bone.tail
        bb.roll = o_bone.roll
        bb.bbone_x = 0.05
        bb.bbone_z = 0.05
        bb.bbone_segments = seg_count
        bb.bbone_handle_type_start = "TANGENT"
        bb.bbone_custom_handle_start = bb1
        bb.bbone_handle_use_ease_start = True
        bb.bbone_handle_type_end = "TANGENT"
        bb.bbone_custom_handle_end = bb2
        bb.bbone_handle_use_ease_end = True
        bb.use_deform = True
        
        bb_tar = Armature.edit_bones.new(b+"_bb_twist_tar."+side)
        bb_tar.head = o_bone.tail + o_bone.z_axis * 0.2
        bb_tar.tail = o_bone.tail + o_bone.z_axis * 0.2 + o_bone.y_axis * 0.2
        bb_tar.roll = o_bone.roll
        bb_tar.bbone_x = 0.03
        bb_tar.bbone_z = 0.03
        bb_tar.parent = bb2
        bb_tar.use_deform = False
        
        
def create_wrist_twist_helper(side):
    o_bone = Armature.edit_bones[arm_end_origin_names[1]+"."+side]
    o_bone2 = Armature.edit_bones[arm_origin_names[1]+"."+side]
    
    twist_helper = Armature.edit_bones.new(arm_end_origin_names[1]+"_twist_helper."+side)
    twist_helper.head = o_bone2.tail + o_bone2.z_axis * 0.4
    twist_helper.tail = o_bone2.tail + o_bone2.z_axis * 0.4 + o_bone2.y_axis * 0.2
    twist_helper.roll = o_bone2.roll
    twist_helper.bbone_x = 0.03
    twist_helper.bbone_z = 0.03
    twist_helper.parent = o_bone
    twist_helper.use_deform = False
    
    
def create_shoulder_twist_helper(side):
    o_bone = Armature.edit_bones[arm_end_origin_names[0]+"."+side]
    o_bone2 = Armature.edit_bones[arm_origin_names[0]+"."+side]
    sign = o_bone2.head[0] / abs(o_bone2.head[0])
    
    twist_helper = Armature.edit_bones.new(arm_end_origin_names[0]+"_twist_helper."+side)
    twist_helper.head = o_bone2.head + o_bone2.x_axis * sign*0.4 + o_bone2.y_axis * 0.4
    twist_helper.tail = o_bone2.head + o_bone2.x_axis * sign*0.4 + o_bone2.y_axis * (0.4 + 0.2)
    twist_helper.roll = o_bone2.roll
    twist_helper.bbone_x = 0.03
    twist_helper.bbone_z = 0.03
    twist_helper.parent = o_bone
    twist_helper.use_deform = False
    
def create_ankle_twist_helper(side):
    foot_bone = Armature.edit_bones[foot_name+"."+side]
    lo_leg_b = Armature.edit_bones[leg_origin_names[1]+"."+side]
    
    twist_helper = Armature.edit_bones.new(foot_name+"_twist_helper."+side)
    twist_helper.head = lo_leg_b.tail + lo_leg_b.z_axis * 0.4
    twist_helper.tail = lo_leg_b.tail + lo_leg_b.z_axis * 0.4 + lo_leg_b.y_axis * 0.2
    twist_helper.roll = lo_leg_b.roll
    twist_helper.bbone_x = 0.03
    twist_helper.bbone_z = 0.03
    twist_helper.parent = foot_bone
    twist_helper.use_deform = False
    
def create_hip_twist_helper(side):
    hip_bone = Armature.edit_bones[hip_name]
    up_leg_b = Armature.edit_bones[leg_origin_names[0]+"."+side]
    sign = up_leg_b.head[0] / abs(up_leg_b.head[0])
    
    twist_helper = Armature.edit_bones.new(leg_origin_names[0]+"_twist_helper."+side)
    twist_helper.head = up_leg_b.head + up_leg_b.x_axis * sign*0.4 + up_leg_b.y_axis * -0.3
    twist_helper.tail = up_leg_b.head + up_leg_b.x_axis * sign*0.4 + up_leg_b.y_axis * (-0.3 + 0.2)
    twist_helper.roll = up_leg_b.roll
    twist_helper.bbone_x = 0.03
    twist_helper.bbone_z = 0.03
    twist_helper.parent = hip_bone
    twist_helper.use_deform = False


def constrain_limb_bb(origin, side):
    for b in origin:
        bb1_name = b+"_bb_1."+side
        bb2_name = b+"_bb_2."+side
        bb_tar_name = b+"_bb_twist_tar."+side
        bb_name = b+"_bb."+side
        bb = Armature.bones[bb_name]
        
        bb.select = True
        bpy.context.object.data.bones.active = bb
        
        O.pose.constraint_add(type="COPY_LOCATION")
        C.object.pose.bones[bb_name].constraints["Copy Location"].target = D.objects[target_name]
        C.object.pose.bones[bb_name].constraints["Copy Location"].subtarget = bb1_name
        
        O.pose.constraint_add(type="DAMPED_TRACK")
        C.object.pose.bones[bb_name].constraints["Damped Track"].target = D.objects[target_name]
        C.object.pose.bones[bb_name].constraints["Damped Track"].subtarget = bb2_name
        
        O.pose.constraint_add(type="LOCKED_TRACK")
        C.object.pose.bones[bb_name].constraints["Locked Track"].target = D.objects[target_name]
        C.object.pose.bones[bb_name].constraints["Locked Track"].subtarget = bb_tar_name
        C.object.pose.bones[bb_name].constraints["Locked Track"].track_axis = "TRACK_Z"
        C.object.pose.bones[bb_name].constraints["Locked Track"].lock_axis = "LOCK_Y"
        
        
def constrain_wrist_twist_helper(side):
    bb2_name = arm_origin_names[1]+"_bb_2."+side
    helper_name = arm_end_origin_names[1]+"_twist_helper."+side
    bb2 = Armature.bones[bb2_name]
    
    bb2.select = True
    bpy.context.object.data.bones.active = bb2
    
    O.pose.constraint_add(type="LOCKED_TRACK")
    C.object.pose.bones[bb2_name].constraints["Locked Track"].target = D.objects[target_name]
    C.object.pose.bones[bb2_name].constraints["Locked Track"].subtarget = helper_name
    C.object.pose.bones[bb2_name].constraints["Locked Track"].track_axis = "TRACK_Z"
    C.object.pose.bones[bb2_name].constraints["Locked Track"].lock_axis = "LOCK_Y"
    
    
def constrain_shoulder_twist_helper(side):
    bb1_name = arm_origin_names[0]+"_bb_1."+side
    helper_name = arm_end_origin_names[0]+"_twist_helper."+side
    bb1 = Armature.bones[bb1_name]
    
    sign = bb1.head[0] / abs(bb1.head[0])
    
    bb1.select = True
    bpy.context.object.data.bones.active = bb1
    
    O.pose.constraint_add(type="LOCKED_TRACK")
    C.object.pose.bones[bb1_name].constraints["Locked Track"].target = D.objects[target_name]
    C.object.pose.bones[bb1_name].constraints["Locked Track"].subtarget = helper_name
    if sign == 1:
        C.object.pose.bones[bb1_name].constraints["Locked Track"].track_axis = "TRACK_X"
    elif sign == -1:
        C.object.pose.bones[bb1_name].constraints["Locked Track"].track_axis = "TRACK_NEGATIVE_X"
    C.object.pose.bones[bb1_name].constraints["Locked Track"].lock_axis = "LOCK_Y"
    

def constrain_ankle_twist_helper(side):
    bb2_name = leg_origin_names[1]+"_bb_2."+side
    helper_name = foot_name+"_twist_helper."+side
    bb2 = Armature.bones[bb2_name]
    
    bb2.select = True
    bpy.context.object.data.bones.active = bb2
    
    O.pose.constraint_add(type="LOCKED_TRACK")
    C.object.pose.bones[bb2_name].constraints["Locked Track"].target = D.objects[target_name]
    C.object.pose.bones[bb2_name].constraints["Locked Track"].subtarget = helper_name
    C.object.pose.bones[bb2_name].constraints["Locked Track"].track_axis = "TRACK_Z"
    C.object.pose.bones[bb2_name].constraints["Locked Track"].lock_axis = "LOCK_Y"
    
def constrain_hip_twist_helper(side):
    bb1_name = leg_origin_names[0]+"_bb_1."+side
    helper_name = leg_origin_names[0]+"_twist_helper."+side
    bb1 = Armature.bones[bb1_name]
    
    sign = bb1.head[0] / abs(bb1.head[0])
    
    bb1.select = True
    bpy.context.object.data.bones.active = bb1
    
    O.pose.constraint_add(type="LOCKED_TRACK")
    C.object.pose.bones[bb1_name].constraints["Locked Track"].target = D.objects[target_name]
    C.object.pose.bones[bb1_name].constraints["Locked Track"].subtarget = helper_name
    if sign == 1:
        C.object.pose.bones[bb1_name].constraints["Locked Track"].track_axis = "TRACK_X"
    elif sign == -1:
        C.object.pose.bones[bb1_name].constraints["Locked Track"].track_axis = "TRACK_NEGATIVE_X"
    C.object.pose.bones[bb1_name].constraints["Locked Track"].lock_axis = "LOCK_Y"
        
############################################################################

if True:
    default_start_pos()
    select_target()
    
    O.object.mode_set(mode="EDIT")
    deselect_all_edit_bones()
    create_limb_bb(arm_origin_names, "L")
    create_wrist_twist_helper("L")
    create_shoulder_twist_helper("L")
    create_limb_bb(arm_origin_names, "R")
    create_wrist_twist_helper("R")
    create_shoulder_twist_helper("R")
    
    deselect_all_edit_bones()
    create_limb_bb(leg_origin_names, "L")
    create_ankle_twist_helper("L")
    create_hip_twist_helper("L")
    create_limb_bb(leg_origin_names, "R")
    create_ankle_twist_helper("R")
    create_hip_twist_helper("R")
    
    O.object.mode_set(mode="POSE")
    deselect_all_pose_bones()
    constrain_limb_bb(arm_origin_names, "L")
    constrain_wrist_twist_helper("L")
    constrain_shoulder_twist_helper("L")
    constrain_limb_bb(arm_origin_names, "R")
    constrain_wrist_twist_helper("R")
    constrain_shoulder_twist_helper("R")
    
    deselect_all_pose_bones()
    constrain_limb_bb(leg_origin_names, "L")
    constrain_ankle_twist_helper("L")
    constrain_hip_twist_helper("L")
    constrain_limb_bb(leg_origin_names, "R")
    constrain_ankle_twist_helper("R")
    constrain_hip_twist_helper("R")
    
    
else:
    pass
