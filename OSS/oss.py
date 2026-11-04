
import os

from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeCylinder
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse, BRepAlgoAPI_Cut
from OCC.Core.gp import gp_Ax2, gp_Pnt, gp_Dir
from OCC.Core.STEPControl import STEPControl_Writer, STEPControl_AsIs
from OCC.Core.IFSelect import IFSelect_RetDone

# ---------------------------------
# 1. Define dimensions (mm)
# ---------------------------------

shaft_radius = 10
shaft_length = 40

second_radius = 12
second_length = 50

flange_radius = 30
flange_thickness = 10

hole_radius = 4
hole_offset = 15

# ---------------------------------
# 2. Create shaft sections
# ---------------------------------

axis1 = gp_Ax2(gp_Pnt(0, 0, 0), gp_Dir(1, 0, 0))

axis2 = gp_Ax2(
    gp_Pnt(50, 0, 0),
    gp_Dir(1, 0, 0)
)

shaft1 = BRepPrimAPI_MakeCylinder(
    axis1, shaft_radius, shaft_length
).Shape()

shaft2 = BRepPrimAPI_MakeCylinder(
    axis2, second_radius, second_length
).Shape()

# ---------------------------------
# 3. Create mounting flange
# ---------------------------------

flange_axis = gp_Ax2(
    gp_Pnt(40, 0, 0),
    gp_Dir(1, 0, 0)
)

flange = BRepPrimAPI_MakeCylinder(
    flange_axis, flange_radius, flange_thickness
).Shape()

# ---------------------------------
# 4. Fuse all three components
# ---------------------------------

fuse1 = BRepAlgoAPI_Fuse(shaft1, flange)
fuse1.Build()

fuse2 = BRepAlgoAPI_Fuse(fuse1.Shape(), shaft2)
fuse2.Build()

final_shape = fuse2.Shape()

# ---------------------------------
# 5. Create four mounting holes
# ---------------------------------

hole_positions = [
    (hole_offset, hole_offset),
    (-hole_offset, hole_offset),
    (-hole_offset, -hole_offset),
    (hole_offset, -hole_offset)
]

for y, z in hole_positions:

    hole_axis = gp_Ax2(
        gp_Pnt(39, y, z),
        gp_Dir(1, 0, 0)
    )

    hole = BRepPrimAPI_MakeCylinder(
        hole_axis, hole_radius, 12
    ).Shape()

    cut_operation = BRepAlgoAPI_Cut(final_shape, hole)
    cut_operation.Build()

    final_shape = cut_operation.Shape()

# ---------------------------------
# 6. Save STEP file
# ---------------------------------

project_folder = os.path.dirname(os.path.abspath(__file__))

output_folder = os.path.join(project_folder, "output")
os.makedirs(output_folder, exist_ok=True)

output_file = os.path.join(
    output_folder, "complex_flanged_shaft.step"
)

step_writer = STEPControl_Writer()

step_writer.Transfer(final_shape, STEPControl_AsIs)

status = step_writer.Write(output_file)

if status == IFSelect_RetDone:
    print("Model created successfully!")
    print("STEP file saved at:")
    print(output_file)
else:
    print("STEP export failed!")
