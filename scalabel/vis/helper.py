"""Helper functions used by the visualizer."""
import copy
import colorsys
import io
import os
import urllib.request
from typing import List, Optional, Tuple

import matplotlib.patches as mpatches
import numpy as np
from matplotlib.path import Path
from PIL import Image

from ..common.logger import logger
from ..common.typing import NDArrayF64, NDArrayU8
from ..label.typing import Edge, Frame, Intrinsics, Label, Node
from ..label.utils import get_matrix_from_intrinsics
from .geometry import Label3d


def generate_colors(length: int) -> List[Tuple[int]]:
    """Generate a color palette of [length] colors."""
    brightness = 0.7
    hsv = [(i / length, 1, brightness) for i in range(length)]
    colors = list(map(lambda c: colorsys.hsv_to_rgb(*c), hsv))
    s = np.random.get_state()
    np.random.seed(0)
    result = [tuple(colors[i]) for i in np.random.permutation(len(colors))]
    np.random.set_state(s)
    return result


NUM_COLORS = 50
COLOR_PALETTE = generate_colors(NUM_COLORS)


def random_color(track_id: str) -> NDArrayF64:
    """Generate a random color (RGB)."""
    return COLOR_PALETTE[int(track_id) % NUM_COLORS]


# Function to fetch images
def fetch_image(inputs: Tuple[Frame, str]) -> NDArrayU8:
    """Fetch the image given image information."""
    frame, image_dir = inputs
    logger.info("Loading image: %s", frame.name)

    # Fetch image
    if frame.url is not None and len(frame.url) > 0:
        with urllib.request.urlopen(frame.url, timeout=300) as req:
            image_data = req.read()
        im: NDArrayU8 = np.asarray(
            Image.open(io.BytesIO(image_data)), dtype=np.uint8
        )
    else:
        if frame.videoName is not None:
            image_path = os.path.join(image_dir, frame.videoName, frame.name)
        else:
            image_path = os.path.join(image_dir, frame.name)
        print("Local path:", image_path)
        img = Image.open(image_path)
        im = np.array(img, dtype=np.uint8)

    return im


def gen_2d_rect(
    label: Label, color: List[float], linewidth: int
) -> List[mpatches.Rectangle]:
    """Generate individual bounding box from 2d label."""
    assert label.box2d is not None
    box2d = label.box2d
    x1 = box2d.x1
    y1 = box2d.y1
    x2 = box2d.x2
    y2 = box2d.y2

    # Draw and add one box to the figure
    return [
        mpatches.Rectangle(
            (x1, y1),
            x2 - x1,
            y2 - y1,
            linewidth=linewidth,
            edgecolor=color + [0.75],
            facecolor=color + [0.25],
            fill=True,
        )
    ]


def check_edge_visibility(
    edge: List[List[float]], img_w: int, img_h: int
) -> bool:
    """Check whether both ends of the edges is inside the picture."""
    return (
        (0 >= edge[0][0] or edge[0][0] >= img_w)
        or (0 >= edge[0][1] or edge[0][1] >= img_h)
    ) and (
        (0 >= edge[1][0] or edge[1][0] >= img_w)
        or (0 >= edge[1][1] or edge[1][1] >= img_h)
    )


def gen_3d_cube(
    label: Label,
    color: List[float],
    linewidth: int,
    intrinsics: Intrinsics,
    img_w: int,
    img_h: int,
    alpha: float,
) -> Tuple[Label3d, List[mpatches.Polygon]]:
    """Generate individual bounding box from 3d label.

    Assumes the following format:
    * location: 3D center of the box, stored as 3D point in camera coordinates,
     meaning the axes (x,y,z) point right, down, and forward.
    * orientation: 3D orientation of the bounding box, stored as axis angles in
     the same coordinate frame as the location.
    * dimension: 3D box size, with length in x direction, height in y direction
     and width in z direction
    """
    assert label.box3d is not None
    box3d = label.box3d
    label3d = Label3d.from_box3d(box3d)
    edges = label3d.get_edges_with_visibility(
        get_matrix_from_intrinsics(intrinsics)
    )

    lines = []
    for edge in edges["dashed"]:
        if check_edge_visibility(edge, img_w, img_h):
            continue
        lines.append(
            mpatches.Polygon(
                edge,
                linewidth=linewidth,
                linestyle=(0, (2, 2)),
                edgecolor=color,
                facecolor="none",
                fill=False,
                alpha=alpha,
            )
        )
    for edge in edges["solid"]:
        if check_edge_visibility(edge, img_w, img_h):
            continue
        lines.append(
            mpatches.Polygon(
                edge,
                linewidth=linewidth,
                edgecolor=color,
                facecolor="none",
                fill=False,
                alpha=alpha,
            )
        )

    return label3d, lines


def poly2patch(
    vertices: List[Tuple[float, float]],
    types: str,
    color: Optional[NDArrayF64] = None,
    linewidth: int = 2,
    alpha: float = 1.0,
    closed: bool = False,
) -> mpatches.PathPatch:
    """Convert 2D polygon vertices into patch."""
    moves = {"L": Path.LINETO, "C": Path.CURVE4}
    points = copy.deepcopy(vertices)
    codes = [moves[t] for t in types]
    codes[0] = Path.MOVETO

    if closed:
        points.append(points[0])
        codes.append(Path.LINETO)

    if color is None:
        color = random_color()

    return mpatches.PathPatch(
        Path(points, codes),
        facecolor=color if closed else "none",
        edgecolor=color,  # if not closed else 'none'
        lw=1 if closed else linewidth,
        alpha=alpha,
        antialiased=False,
        snap=True,
    )


def gen_graph_point(
    node: Node, color: List[float], radius: int, alpha: float
) -> List[mpatches.Circle]:
    """Generate graph point from node."""
    assert node is not None

    # Draw and add graph node to the figure
    return [
        mpatches.Circle(node.location, radius=radius, color=color, alpha=alpha)
    ]


def gen_graph_edge(
    edge: Edge, label: Label, color: List[float], linewidth: int, alpha: float
) -> List[mpatches.ConnectionPatch]:
    """Generate graph edges from graph label."""
    assert edge is not None
    assert label.graph is not None
    nodes = {node.id: node for node in label.graph.nodes}

    # Draw and add graph edges to the figure
    return [
        mpatches.ConnectionPatch(
            nodes[edge.source].location,
            nodes[edge.target].location,
            "data",
            color=color,
            linewidth=linewidth,
            alpha=alpha,
        )
    ]
