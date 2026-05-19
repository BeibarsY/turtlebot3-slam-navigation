# Maps

Occupancy-grid maps produced by SLAM. Each map is a pair:

- `<name>.pgm` — grayscale occupancy grid (dark = wall, white = free, gray = unknown).
- `<name>.yaml` — metadata (resolution, origin, thresholds).

## Maps produced in this project

| File | Source | Notes |
|---|---|---|
| `labyrinth_real.{pgm,yaml}` | Lab 3, physical TurtleBot3 in maze | Noisier; thicker walls due to LiDAR scan misalignment. |
| `labyrinth_sim.{pgm,yaml}` | Lab 4, Gazebo simulation | Cleaner; ground-truth-like walls because the sim has no sensor noise. |

The original `.pgm` files are not committed to the repository because
each lab group produced slightly different maps depending on driving
path and SLAM session.

## How to produce a new map

After running the SLAM pipeline (see `scripts/slam_mapping_sim.sh`),
save the live map from a separate shell:

```bash
cd <repo-root>
ros2 run nav2_map_server map_saver_cli -f maps/labyrinth_sim
```

This writes `labyrinth_sim.pgm` and `labyrinth_sim.yaml` in this
folder. The YAML's `image:` field should be a relative path to the
PGM (it usually is by default).

## YAML format reminder

```yaml
image: labyrinth_sim.pgm
mode: trinary
resolution: 0.050000
origin: [-3.000000, -2.000000, 0.000000]
negate: 0
occupied_thresh: 0.65
free_thresh: 0.25
```

If you copy a map between machines, double-check that `image:` is a
relative path (`labyrinth_sim.pgm`, not `/home/student/...`). The
absolute path is the most common cause of "map_server cannot find the
image" errors.
