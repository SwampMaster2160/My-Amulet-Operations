import wx

import amulet
from amulet.api.selection import SelectionGroup
from amulet.api.data_types import Dimension, OperationReturnType
from amulet.api.block import Block
from amulet_map_editor.programs.edit.api.operations import SimpleOperationPanel
from amulet.api.level import BaseLevel
from amulet_map_editor.programs.edit.api.canvas import EditCanvas

from itertools import product


def block_equality(a: Block, b: Block) -> bool:
    a_namespace = a.namespace
    if a_namespace == "universal_minecraft":
        a_namespace = "minecraft"
    b_namespace = b.namespace
    if b_namespace == "universal_minecraft":
        b_namespace = "minecraft"
    return a.base_name == b.base_name and a_namespace == b_namespace


def block_in_block_list(a: Block, b) -> bool:
    for block in b:
        if block_equality(a, block):
            return 1
    return 0


# The main class for the operation
class CobblestonePlatform(SimpleOperationPanel):
    # Init method that is called when the user selects the operation form the drop down menu and shows the operation settings.
    def __init__(self, parent: wx.Window, canvas: EditCanvas, world: BaseLevel, options_path: str):
        SimpleOperationPanel.__init__(self, parent, canvas, world, options_path)    # Init the gui panel
        self._add_run_button()                                                      # Add the "Run Operation" button
        self.Layout()                                                               # Finnish gui pannel

    # Method that is called when the user presses the "Run Operation" button.
    def _operation(self, world: BaseLevel, dimension: Dimension, selection: SelectionGroup) -> OperationReturnType:
        cobblestone = world.block_palette.get_add_block(Block("minecraft", "cobblestone"))  # Get a cobblestone block object that we can use to overite a world block.
        replace_list = [Block("minecraft", "air"), Block("minecraft", "water")]
        for chunk, slices, _ in world.get_chunk_slice_box(dimension, selection):
            for slice in range(len(slices) // 3):
                slice_x, slice_y, slice_z = slices[slice * 3], slices[slice * 3 + 1], slices[slice * 3 + 2]
                top = slice_y.stop - 1
                for x, y, z in product(range(slice_x.start, slice_x.stop), range(slice_y.start, slice_y.stop), range(slice_z.start, slice_z.stop)):
                    block_here = chunk.block_palette[chunk.blocks[x, y, z]]
                    if y == top or x % 2 == 0 and z % 2 == 0 and block_in_block_list(block_here, replace_list):
                        chunk.blocks[x, y, z] = cobblestone
            chunk.changed = True


# Some basic info about the operation that amulet needs to know.
export = {
    "name": "Cobblestone Platform",     # Plugin name
    "operation": CobblestonePlatform,   # Main operation class
}
