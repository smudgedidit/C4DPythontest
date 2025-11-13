"""Cinema 4D Python script to create a cube in the currently selected layer.

Run this script from the Script Manager. It will create a new cube primitive
and assign it to the first selected layer in the Layer Manager. If no layer is
selected, the user is notified and the script exits without creating anything.
"""

import c4d


def get_active_layer(doc):
    """Return the first active layer in the Layer Manager.

    The Layer Manager can have multiple selections. Cinema 4D flags selected
    layers with the BIT_ACTIVE bit. This helper walks through the layer tree to
    find the first such layer.
    """
    if doc is None:
        return None

    layer_root = doc.GetLayerObjectRoot()
    if layer_root is None:
        return None

    layer = layer_root.GetDown()
    while layer:
        if layer.GetBit(c4d.BIT_ACTIVE):
            return layer
        layer = layer.GetNext()
    return None


def main():
    doc = c4d.documents.GetActiveDocument()
    if doc is None:
        return

    active_layer = get_active_layer(doc)
    if active_layer is None:
        c4d.gui.MessageDialog("Please select a layer before running the script.")
        return

    cube = c4d.BaseObject(c4d.Ocube)
    if cube is None:
        c4d.gui.MessageDialog("Failed to create cube primitive.")
        return

    cube.SetLayerObject(doc, active_layer)
    doc.InsertObject(cube)
    c4d.EventAdd()


if __name__ == "__main__":
    main()
