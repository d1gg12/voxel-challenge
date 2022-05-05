from scene import Scene; import taichi as ti; from taichi.math import *

scene = Scene(voxel_edges=0, exposure=100)
scene.set_floor(-63/64, (1, 1, 1))
scene.set_background_color((0, 0, 0))
scene.set_directional_light((1, 0.5, 1), 0.1, (0.01, 0.01, 0.01))

@ti.func
def build_cylinder_z(p, r, height, mat, color, symmetric = 0):
    for x, y, z in ti.ndrange((p.x-r, p.x+r+1), (p.y-r, p.y+r+1), (p.z, p.z+height)):
        if (x-p.x)*(x-p.x) + (y-p.y)*(y-p.y) < r * r:
            scene.set_voxel(ivec3(x, y, z), mat, color)
            if symmetric == 1:
                scene.set_voxel(ivec3(-x, y, z), mat, color)

@ti.func
def build_cuboid(p, length_x, length_y, length_z, mat, color, symmetric = 0):
    for x, y, z in ti.ndrange((p.x, p.x+length_x), (p.y, p.y+length_y), (p.z, p.z+length_z)):
        scene.set_voxel(ivec3(x, y, z), mat, color)
        if symmetric == 1:
            scene.set_voxel(ivec3(-x, y, z), mat, color)

@ti.func
def build_line(point, decrease, level, mat, color):
    for i in range(level):
        for j in range(abs(decrease)//1+1):
            scene.set_voxel(vec3(int(point.x + decrease*i)+j, point.y+i, point.z), mat, color)

@ti.kernel
def initialize_voxels():
    knight_pos = vec3(0, -44, 0)
    white = vec3(1, 1, 1); black = vec3(0, 0, 0); green = vec3(0.1, 0.3, 0.1)
    silver = vec3(0.7, 0.7, 0.7)
    xaxis = vec3(1, 0, 0); yaxis = vec3(0, 1, 0); zaxis = vec3(0, 0, 1)
    # build hair
    knight_hair_pos = knight_pos + yaxis * 30
    build_cylinder_z(knight_hair_pos - xaxis * 5 - zaxis * 2, 20, 5, 1, white, 1)
    build_cylinder_z(knight_hair_pos - xaxis * 5 - zaxis * 2, 15, 5, 0, white, 1)
    build_cuboid(knight_hair_pos - xaxis * 7 - yaxis * 10 - zaxis * 2, 15, 31, 5, 0, white)
    build_cuboid(knight_hair_pos - xaxis * 40 + yaxis * 10 - zaxis * 2, 81, 21, 5, 0, white)
    build_cuboid(knight_hair_pos - xaxis * 21 + yaxis * 8 - zaxis * 2, 2, 5, 9, 0, green, 1)
    #build head
    knight_head_pos = knight_pos + yaxis * 10
    build_cylinder_z(knight_head_pos - xaxis * 10 + yaxis * 5 - zaxis * 6, 5, 12, 1, white, 1)
    build_cylinder_z(knight_head_pos - xaxis * 10 - yaxis * 5 - zaxis * 6, 5, 12, 1, white, 1)
    build_cuboid(knight_head_pos - xaxis * 10 - yaxis * 10 - zaxis * 6, 21, 21, 12, 1, white)
    build_cuboid(knight_head_pos - xaxis * 15 - yaxis * 5 - zaxis * 6, 31, 11, 12, 1, white)

    build_cylinder_z(knight_head_pos - xaxis * 8 - yaxis * 2 + zaxis * 4, 4, 2, 1, black, 1)
    build_cylinder_z(knight_head_pos - xaxis * 8 - yaxis * 4 + zaxis * 4, 4, 2, 1, black, 1)
    #build cloth
    knight_body_pos = knight_pos - yaxis * 10
    for i in range(-3, 3):
        build_cuboid(knight_body_pos - xaxis * 5 + yaxis * 6 + zaxis * i, 13, 2, 1, 1, green)
        build_cuboid(knight_body_pos - xaxis * 4 + yaxis * 4 + zaxis * i, 13, 2, 1, 1, green)
        build_cuboid(knight_body_pos - xaxis * 3 + yaxis * 2 + zaxis * i, 13, 2, 1, 1, green)
        build_cuboid(knight_body_pos - xaxis * 2 - yaxis * 0 + zaxis * i, 13, 2, 1, 1, green)
        build_cuboid(knight_body_pos - xaxis * 1 - yaxis * 2 + zaxis * i, 13, 2, 1, 1, green)
        build_cuboid(knight_body_pos + xaxis * 2 - yaxis * 3 + zaxis * i, 11, 1, 1, 1, green)
        build_cuboid(knight_body_pos + xaxis * 3 - yaxis * 4 + zaxis * i, 10, 1, 1, 1, green)
        build_cuboid(knight_body_pos + xaxis * 4 - yaxis * 5 + zaxis * i, 9, 1, 1, 1, green)
        build_cuboid(knight_body_pos + xaxis * 5 - yaxis * 6 + zaxis * i, 9, 1, 1, 1, green)
        build_line(knight_body_pos + xaxis * 11 - yaxis * 6 + zaxis * i, -0.6, 16, 1, black)
        build_line(knight_body_pos + xaxis * 7 - yaxis * 6 + zaxis * i, -0.7, 16, 1, black)

        build_cuboid(knight_body_pos - xaxis * 6 + yaxis * 8 + zaxis * i, 13, 2, 2, 1, green)
        build_cuboid(knight_body_pos - xaxis * 7 + yaxis * 6 + zaxis * i, 13, 2, 2, 1, green)
        build_cuboid(knight_body_pos - xaxis * 8 + yaxis * 4 + zaxis * i, 13, 2, 2, 1, green)
        build_cuboid(knight_body_pos - xaxis * 9 + yaxis * 2 + zaxis * i, 13, 2, 2, 1, green)
        build_cuboid(knight_body_pos - xaxis * 10 - yaxis * 0 + zaxis * i, 13, 2, 2, 1, green)
        build_cuboid(knight_body_pos - xaxis * 11 - yaxis * 2 + zaxis * i, 13, 2, 2, 1, green)
        build_cuboid(knight_body_pos - xaxis * 12 - yaxis * 3 + zaxis * i, 13, 1, 2, 1, green)
        build_cuboid(knight_body_pos - xaxis * 12 - yaxis * 4 + zaxis * i, 12, 1, 2, 1, green)
        build_cuboid(knight_body_pos - xaxis * 13 - yaxis * 5 + zaxis * i, 11, 1, 2, 1, green)
        build_cuboid(knight_body_pos - xaxis * 13 - yaxis * 6 + zaxis * i, 9, 1, 2, 1, green)
        build_line(knight_body_pos - xaxis * 11 - yaxis * 6 + zaxis * (i+1), 0.6, 16, 1, black)
        build_line(knight_body_pos - xaxis * 7 - yaxis * 6 + zaxis * (i+1), 0.7, 16, 1, black)
    #build body
    build_cuboid(knight_body_pos - xaxis * 5 - yaxis * 10 - zaxis * 2, 11, 20, 4, 1, black)
    build_cuboid(knight_body_pos - xaxis * 3 - yaxis * 10 - zaxis * 2, 7, 6, 4, 0, black)
    #build sword
    for i in range(-5, -2):
        build_line(knight_body_pos - xaxis * 5 - yaxis * 5 + zaxis * i, 1.0, 15, 1, silver)
        build_line(knight_body_pos - xaxis * 5 - yaxis * 5 + zaxis * i, 1.3, 13, 1, silver)
        build_line(knight_body_pos - xaxis * 5 - yaxis * 5 + zaxis * i, 1.5, 14, 1, silver)
        build_line(knight_body_pos - xaxis * 5 - yaxis * 5 + zaxis * i, 1.6, 14, 1, silver)
        build_line(knight_body_pos - xaxis * 5 - yaxis * 5 + zaxis * i, 2.0, 9, 1, silver)
        build_line(knight_body_pos - xaxis * 5 - yaxis * 5 + zaxis * i, 2.5, 8, 1, silver)
        build_cuboid(knight_body_pos + xaxis * 7 + yaxis * 2 + zaxis * i, 5, 6, 1, 1, silver)
        build_line(knight_body_pos + xaxis * 14 + yaxis * 2 + zaxis * i, -0.6, 8, 1, silver)
        scene.set_voxel(knight_body_pos + xaxis * 6 + yaxis * 1 + zaxis * i, 1, silver)

initialize_voxels(); scene.finish()
