# Labyrinth STL

Place your `labyrinth.stl` mesh here.

This file is intentionally **not** committed to the repository because:

- STL files are binary blobs that bloat repo size and don't diff usefully.
- Each lab group used a different physical labyrinth geometry, so the
  mesh is environment-specific.
- The original labyrinth dimensioned drawing is preserved in
  `docs/02_physical_labyrinth_drawing.jpg` for reference if anyone wants
  to reconstruct the geometry.

## Producing the mesh

Two practical paths:

1. **CAD → STL.** Build the maze in Fusion 360 / FreeCAD / SolidWorks
   from the dimensioned drawing in `docs/`, then export as `.stl` and
   save here as `labyrinth.stl`.

2. **Blender from a 2D plan.** Trace the wall layout from the technical
   drawing, extrude the walls to the configured height, and export STL.

The `model.sdf` expects the file at this exact path:
`gazebo/models/labyrinth/meshes/labyrinth.stl`.
