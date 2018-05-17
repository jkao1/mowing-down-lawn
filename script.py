import mdl
from display import *
from matrix import *
from draw import *

def run(filename):
    """
    This function runs an mdl script
    """
    view = [0,
            0,
            1];
    ambient = [50,
               50,
               50]
    light = [[0.5,
              0.75,
              1],
             [236,
              120,
              59]]
    areflect = [0.1,
                0.1,
                0.1]
    dreflect = [0.5,
                0.5,
                0.5]
    sreflect = [0.5,
                0.5,
                0.5]

    color = [0, 0, 0]
    tmp = new_matrix()
    ident( tmp )

    stack = [ [x[:] for x in tmp] ]
    screen = new_screen()
    zbuffer = new_zbuffer()
    tmp = []
    polygons = []
    step_3d = 20

    p = mdl.parseFile(filename)

    if not p:
        print "Parsing failed."
        return

    (commands, symbols) = p
    for cmd in commands:
        name = cmd[0]
        if name == "push":
            stack.append([ x[:] for x in stack[-1] ])
        elif name == "pop":
            stack.pop()
        elif name == "display":
            display( screen )
        elif name == "save":
            save_extension( screen, cmd[1] + cmd[2] )

        elif name in "sphere|torus|box|triangle":
            if name == "sphere":
                add_sphere(
                    polygons,
                    float(cmd[1]), float(cmd[2]), float(cmd[3]),
                    float(cmd[4]),
                    step_3d,
                )
            elif name == "torus":
                add_torus(
                    polygons,
                    float(cmd[1]), float(cmd[2]), float(cmd[3]),
                    float(cmd[4]), float(cmd[5]),
                    step_3d,
                )
            elif name == "box":
                add_box(
                    polygons,
                    float(cmd[1]), float(cmd[2]), float(cmd[3]),
                    float(cmd[4]), float(cmd[5]), float(cmd[6]),
                )
            elif name == "triangle":
                add_polygon(
                    polygons,
                    float(cmd[1]), float(cmd[2]), float(cmd[3]),
                    float(cmd[4]), float(cmd[5]), float(cmd[6]),
                    float(cmd[7]), float(cmd[8]), float(cmd[9]),
                )
            matrix_mult( stack[-1], polygons )
            draw_polygons(
                polygons,
                screen,
                zbuffer,
                view, ambient, light,
                areflect, dreflect, sreflect
            )
            polygons = []

        elif name == "line":
            add_edge(
                edges,
                float(cmd[1]), float(cmd[2]), float(cmd[3]),
                float(cmd[4]), float(cmd[5]), float(cmd[6]),
            )
            matrix_mult( stack[-1], edges )
            draw_lines( edges, screen, zbuffer, color )
            edges = []

        elif name in "movescalerotate":
            if name == "move":
                transformer = make_translate(
                    float(cmd[1]), float(cmd[2]), float(cmd[3])
                )
            elif name == "scale":
                transformer = make_scale(
                    float(cmd[1]), float(cmd[2]), float(cmd[3])
                )
            elif name == "rotate":
                theta = float(cmd[2]) * math.pi / 180
                if cmd[1] == "x":
                    transformer = make_rotX(theta)
                elif cmd[1] == "y":
                    transformer = make_rotY(theta)
                elif cmd[1] == "z":
                    transformer = make_rotZ(theta)
            matrix_mult( stack[-1], transformer )
            stack[-1] = [ x[:] for x in transformer ]
