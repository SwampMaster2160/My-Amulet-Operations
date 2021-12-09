import wx

import amulet
from amulet.api.selection import SelectionGroup
from amulet.api.data_types import Dimension, OperationReturnType
from amulet.api.block import Block
from amulet_map_editor.programs.edit.api.operations import SimpleOperationPanel
from amulet.api.level import BaseLevel
from amulet_map_editor.programs.edit.api.canvas import EditCanvas


# The main class for the operation
class ReplaceWithCobblestone(SimpleOperationPanel):
    # Init method that is called when the user selects the operation form the drop down menu and shows the operation settings.
    def __init__(self, parent: wx.Window, canvas: EditCanvas, world: BaseLevel, options_path: str):
        SimpleOperationPanel.__init__(self, parent, canvas, world, options_path)    # Init the gui panel
        self._add_run_button()                                                      # Add the "Run Operation" button
        self.Layout()                                                               # Finnish gui pannel

    # Method that is called when the user presses the "Run Operation" button.
    def _operation(self, world: BaseLevel, dimension: Dimension, selection: SelectionGroup) -> OperationReturnType:
        cobblestone = world.block_palette.get_add_block(Block("minecraft", "cobblestone"))  # Get a cobblestone block object that we can use to overite a world block.
        # Loop over all the chunks and slices of thoes chunks in the selection.
        for chunk, slices, _ in world.get_chunk_slice_box(dimension, selection):
            chunk.blocks[slices] = cobblestone  # Overite all the blocks in the slice with cobblestone.
            chunk.changed = True                # Tell the editor that we made changes the chunk so it knows to save the chunk.


# Some basic info about the operation that amulet needs to know.
export = {
    "name": "Replace with Cobblestone",     # Plugin name
    "operation": ReplaceWithCobblestone,    # Main operation class
}
