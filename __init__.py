# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
# Copyright (C) 2020 Juan Fran Matheu G.
# Contact: jfmatheug@gmail.com

bl_info = {
    "name" : "PoseGizmos",
    "author" : "JFranMatheu", # add your name/nick here if you modify and distribute your modified version
    "description" : "New gizmos to control bone rotation in pose mode by selecting",
    "blender" : (2, 82, 0),
    "version" : (0, 0, 1),
    "location" : "'N' Panel > UI > Gizmos",
    "warning" : "",
    "category" : "Generic"
}

import bpy
from bpy.types import AddonPreferences
from bpy.props import BoolProperty

class PoseGizmos_AddonPreferences(AddonPreferences):
    bl_idname = "PoseGizmos"
    isRegistered_PoseGG : BoolProperty()

from bpy.types import (
    GizmoGroup,
    Operator,
    Panel
)
from mathutils import Vector
from bpy_extras.view3d_utils import location_3d_to_region_2d as toScreenPos
from bpy.utils import register_class, unregister_class

class POSE_GG_Transform_Bone(GizmoGroup):
    bl_idname = "Transform_Bone_Gizmo"
    bl_label = "Transform Bone Gizmo"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_options = {'PERSISTENT', 'SCALE'}

    @classmethod
    def poll(cls, context):
        return (context.mode == 'POSE' and context.selected_pose_bones)

    def draw_prepare(self, context):
        pos = toScreenPos(context.region, context.space_data.region_3d, context.selected_pose_bones[0].head, default = None)
        self.gizmo_x.matrix_basis[0][3], self.gizmo_x.matrix_basis[1][3] = pos + Vector((-40, 16))
        self.gizmo_y.matrix_basis[0][3], self.gizmo_y.matrix_basis[1][3] = pos + Vector((0, 46))
        self.gizmo_z.matrix_basis[0][3], self.gizmo_z.matrix_basis[1][3] = pos + Vector((40, 16))

    def setup(self, context):
        # X ARROW
        #mpr = self.gizmos.new("GIZMO_GT_arrow_3d")
        #mpr.target_set_prop("offset", context.selected_pose_bones[0], "translate") 
        #mpr.matrix_basis = context.selected_pose_bones[0].matrix_local.normalized()
        #mpr.draw_style = 'BOX'
        #mpr.color = 1.0, 0.0, 0.0
        #mpr.alpha = 0.4
        #mpr.color_highlight = 0.5, 0.0, 0.0
        #mpr.alpha_highlight = 0.2
        #self.gizmo_x_arrow = mpr
        
        # GIZMO X
        mpr = self.gizmos.new("GIZMO_GT_button_2d")
        mpr.icon = 'EVENT_X'
        mpr.draw_options = {'BACKDROP', 'OUTLINE'}
        mpr.use_draw_value = True

        mpr.color = .5, 0.0, 0.0 
        mpr.alpha = 0.4
        mpr.color_highlight = 1, 0.0, 0.0
        mpr.alpha_highlight = 0.5
        
        props = mpr.target_set_operator("transform.rotate")
        props.orient_axis = 'X'
        props.orient_type = 'LOCAL'
        props.constraint_axis = (True, False, False)

        mpr.scale_basis = 14 #(80 * 0.35) / 2
        self.gizmo_x = mpr
        
        # GIZMO Y
        mpr = self.gizmos.new("GIZMO_GT_button_2d")
        mpr.icon = 'EVENT_Y'
        mpr.draw_options = {'BACKDROP', 'OUTLINE'}
        mpr.use_draw_value = True

        mpr.color = 0.0, .5, 0.0 
        mpr.alpha = 0.4
        mpr.color_highlight = 0.0, 1, 0.0
        mpr.alpha_highlight = 0.5
        
        props = mpr.target_set_operator("transform.rotate")
        props.orient_axis = 'Y'
        props.orient_type = 'LOCAL'
        props.constraint_axis = (False, True, False)

        mpr.scale_basis = 14 #(80 * 0.35) / 2
        self.gizmo_y = mpr
        
        # GIZMO Z
        mpr = self.gizmos.new("GIZMO_GT_button_2d")
        mpr.icon = 'EVENT_Z'
        mpr.draw_options = {'BACKDROP', 'OUTLINE'}
        #mpr.use_draw_value = True

        mpr.color = 0.0, 0.0, .5 
        mpr.alpha = 0.4
        mpr.color_highlight = 0.0, 0.0, 1
        mpr.alpha_highlight = 0.5
        
        props = mpr.target_set_operator("transform.rotate")
        props.orient_axis = 'Z'
        props.orient_type = 'LOCAL'
        props.constraint_axis = (False, False, True)

        mpr.scale_basis = 14 #(80 * 0.35) / 2
        self.gizmo_z = mpr

class PG_PT_Gizmos(Panel):
    bl_label = "Gizmos"
    bl_category = 'UI'
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    #bl_context = "NONE"
    bl_options = {'DEFAULT_CLOSED'}
    #bl_ui_units_x = 14
    bl_order = 7

    def draw_header(self, context):
        self.layout.label(text="", icon='GIZMO')
        self.layout.separator()

    def draw(self, context):
        wm = context.window_manager
        scn = context.scene
        prefs = context.preferences.addons["PoseGizmos"].preferences

        layout = self.layout
        #box = layout.box()
        col = layout.column(align=True)

        dpress = prefs.isRegistered_PoseGG
        col.operator('pg.register_pose_gg', text="Pose Gizmo", depress=dpress).registration = not dpress

class PG_OT_Register_Pose_GG(Operator):
    bl_idname = "pg.register_pose_gg"
    bl_label = ""
    bl_description = "Register Pose Gizmos"
    registration : BoolProperty()
    def execute(self, context):
        if self.registration:
            register_class(POSE_GG_Transform_Bone)
        else:
            try:
                unregister_class(POSE_GG_Transform_Bone)
            except:
                pass
        context.preferences.addons["PoseGizmos"].preferences.isRegistered_PoseGG = self.registration
        return {'FINISHED'}

def register():
    register_class(PoseGizmos_AddonPreferences)
    register_class(PG_OT_Register_Pose_GG)
    register_class(PG_PT_Gizmos)

def unregister():
    unregister_class(PG_OT_Register_Pose_GG)
    unregister_class(PG_PT_Gizmos)
    try:
        if bpy.context.preferences.addons["PoseGizmos"].preferences.isRegistered_PoseGG:
            unregister_class(POSE_GG_Transform_Bone)
    except:
        pass
    unregister_class(PoseGizmos_AddonPreferences)