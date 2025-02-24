# D. Kaputa
# Ravvenlabs

import bpy
import numpy as np
import socket
import struct
from mathutils import Euler
import math

counter = 1
conn = []
s = []
connected = False

# switch on nodes
bpy.context.scene.use_nodes = True
tree = bpy.context.scene.node_tree
links = tree.links
  
# clear default nodes
for n in tree.nodes:
    tree.nodes.remove(n)
  
# create input render layer node
rl = tree.nodes.new('CompositorNodeRLayers')      
rl.location = 185,285
 
# create output node
v = tree.nodes.new('CompositorNodeViewer')   
v.location = 750,210
v.use_alpha = False
 
# Links
links.new(rl.outputs[0], v.inputs[0])  # link Image output to Viewer input

def xform_object_by_name(object_name,x,y,z,pitch,roll,yaw):
    if object_name in bpy.data.objects:
        obj = bpy.data.objects[object_name]
        obj.location = (x, y, z)
        pitchRad = math.radians(pitch)
        rollRad = math.radians(roll)
        yawRad = math.radians(yaw)
        obj.rotation_euler = Euler((pitchRad, rollRad, yawRad), 'XYZ')
    else:
        print(f"Object '{object_name}' not found.")

def linear_to_gamma(rgb, gamma=2.4):
    """Convert linear RGB values to gamma-corrected RGB values."""
    return np.power(rgb, 1.0 / gamma) * 255.0

def from_linear(linear):
    srgb = linear.copy()
    less = linear <= 0.0031308
    srgb[less] = linear[less] * 12.92
    srgb[~less] = 1.055 * np.power(linear[~less], 1.0 / 2.4) - 0.055
    return srgb * 255.0
    
def handle_data():
    interval = .1
    data = None

    # receive floats
    try:
        data = conn.recv(32)
    except:
        pass
    
    floats = struct.unpack('f' * 8, data)
    
    
    bpy.context.scene.render.resolution_x = int(floats[0])
    bpy.context.scene.render.resolution_y = int(floats[1])
    
    # receive text
    try:
        data = conn.recv(1024)
    except:
        pass
    
    text = data.decode("utf-8")
    
    # xform object
    xform_object_by_name(text,floats[2],floats[3],floats[4],floats[5],floats[6],floats[7]) 
    
    # render
    bpy.ops.render.render()
 
    # get viewer pixels
    pixels = bpy.data.images['Viewer Node'].pixels

    # copy buffer to numpy array for faster manipulation
    arr = np.array(pixels[:])
        
    pixels = np.uint8(from_linear(arr))

    if not data:
        pass
    else:
        conn.sendall(pixels)

    return interval

class TEST_OT_stopServer(bpy.types.Operator):
    bl_idname = "scene.stop_server"
    bl_label = "Stop Server"

    def execute(self, context):
        global conn
        global s
        global connected
        print("stopping server")
        if connected:
            conn.close()
            s.close()
        bpy.app.timers.unregister(handle_data)
        return {'FINISHED'}

class TEST_OT_startServer(bpy.types.Operator):
    bl_idname = "scene.start_server"
    bl_label = "Start Server"

    def execute(self, context):
        global s
        global conn
        global connected
        print("starting server")
        HOST = '127.0.0.1'
        PORT = 55001
    
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        conn.settimeout(5)
        connected = True
        bpy.app.timers.register(handle_data)
        return {'FINISHED'}

class MatlabPanel(bpy.types.Panel):
    bl_label = "Matlab Server"
    bl_idname = "PT_MatlabPanel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Matlab Server"
    
    def draw(self,context):
        layout = self.layout
        row1 = layout.row()
        row1.operator("scene.start_server", text="Start Server")
        row2 = layout.row()
        row2.operator("scene.stop_server", text="Stop Server")

def register():
    bpy.utils.register_class(MatlabPanel)
    bpy.utils.register_class(TEST_OT_stopServer)
    bpy.utils.register_class(TEST_OT_startServer)

def unregister():
    bpy.utils.unregister_class(MatlabPanel)
    bpy.utils.unregister_class(TEST_OT_stopServer)
    bpy.utils.unregister_class(TEST_OT_startServer)
    
if __name__ == "__main__":
    register()