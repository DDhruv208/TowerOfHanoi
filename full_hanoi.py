from manim import *
import numpy as np

config.frame_rate = 12


class CubeofHanoi(ThreeDScene):
    def construct(self):
        num_cubes = 5  # Number of blocks

        # Set up the camera angle
        self.set_camera_orientation(
            phi=345 * DEGREES,
            theta=270 * DEGREES,
            distance=12,
            zoom=0.7,
        )

        # Define rod positions
        rod_positions = [-3, 0, 3]
        rods = VGroup(
            *[
                Cylinder(radius=0.1, height=3, direction=X_AXIS)
                .shift(RIGHT * pos + DOWN * 1.5)
                .set_color(RED_D)
                .set_stroke(color=BLACK, opacity=0.5)
                for pos in rod_positions
            ]
        )

        # Draw base platform
        base = (
            Prism(dimensions=[8, 0.5, 3])
            .set_fill(color=BLUE, opacity=0.5)
            .move_to(DOWN * 2.3)
            .set_stroke(color=BLACK, opacity=0.5)
        ).joint_type
        self.play(Create(base))

        self.play(
            base.animate.scale(1.2).set_fill(YELLOW, opacity=0.8),
            run_time=1,
        )
        self.play(
            base.animate.scale(1 / 1.2).set_fill(BLUE, opacity=0.7),
            run_time=1,
        )
        self.wait(1)
        self.play(SpiralIn(rods))

        # Define cube sizes (blocks)
        cube_sizes = [0.8 + 0.2 * i for i in range(num_cubes - 1, -1, -1)]
        colors = [WHITE, BLUE, GREEN, YELLOW, ORANGE, PURPLE]

        # Function to create a fading trail effect
        def create_trail(radius, start_angle, angle_factor, color, cube):
            num_points = 30  # Increased smoothness
            trail = VGroup()
            for i in range(num_points):
                t = np.linspace(start_angle, 0, num_points)[i]
                x = radius * np.cos(angle_factor * t)
                y = 0  # Keeping the trails in the same plane as the cube
                z = radius * np.sin(t)
                segment = Dot(
                    point=cube.get_center() + np.array([x, y, z]),
                    color=color,
                    radius=0.03,
                )
                segment.set_opacity(1 - i / num_points)  # Fading effect
                trail.add(segment)
            return trail

        # Introducing cubes one by one with scaling effect and trails
        cubes = []
        for i in range(num_cubes):
            cube = (
                Prism(dimensions=[cube_sizes[i], cube_sizes[i], cube_sizes[i]])
                .set_fill(colors[i % len(colors)], opacity=0.9)
                .set_stroke(BLACK, width=0.8)
                .set_shade_in_3d(True)  # Enable smooth shading
            )
            cube.move_to(
                rod_positions[0] * RIGHT
                + DOWN * (2 - sum(cube_sizes[: i + 1]) + cube_sizes[i] / 2)
            )

            number_label = Text(str(i + 1), font_size=32, color=BLACK)
            number_label.move_to(cube.get_center()).scale(1.2)

            trail1 = create_trail(
                radius=1.2,
                start_angle=PI / 2,
                angle_factor=PI / 3,
                color=YELLOW_C,
                cube=cube,
            )

            trail2 = create_trail(
                radius=1.1,
                start_angle=PI,
                angle_factor=PI / 3,
                color=PURE_RED,
                cube=cube,
            )

            trail3 = create_trail(
                radius=1.3,
                start_angle=3 * PI / 2,
                angle_factor=PI / 3,
                color=PURE_GREEN,
                cube=cube,
            )

            self.play(
                ShowIncreasingSubsets(cube),
                Create(trail1),
                Create(trail2),
                Create(trail3),
                FadeIn(number_label),
            )

            self.play(
                Rotate(
                    trail1,
                    angle=TAU,
                    axis=UP,
                    about_point=cube.get_center(),
                    run_time=3.5,
                ),
                Rotate(
                    trail2,
                    angle=TAU,
                    axis=DOWN,
                    about_point=cube.get_center(),
                    run_time=2,
                ),
                Rotate(
                    trail3,
                    angle=TAU,
                    axis=UP,
                    about_point=cube.get_center(),
                    run_time=3,
                ),
                cube.animate.scale(1.3).set_fill(RED, opacity=0.9),
                run_time=1,
            )
            # self.play(cube.animate.scale(1.3).set_fill(RED, opacity=0.9), run_time=1)
            self.play(
                cube.animate.scale(1 / 1.3).set_fill(
                    colors[i % len(colors)], opacity=0.9
                ),
                FadeOut(trail1, trail2, trail3, number_label),
                run_time=1,
            )
            self.wait(0.7)
            # self.play(FadeOut(trail1, trail2, trail3))
            cubes.append(cube)

        self.wait(1)

        banner = ManimBanner()
        title = Title(f"Tower Of Hanoi")
        self.play(banner.create(title))
        self.play(banner.expand())
        self.add(banner.expand())
        
        # Tower of Hanoi Animation
        rods_stack = [list(cubes), [], []]

        def move_cube(source, target):
            cube = rods_stack[source].pop()
            target_height = sum(c.width for c in rods_stack[target])
            rods_stack[target].append(cube)

            lift_height = 2.5  # Height to lift before moving horizontally

            path = VMobject()
            path.set_points_as_corners(
                [
                    cube.get_center(),
                    cube.get_center() + UP * lift_height,
                    RIGHT * rod_positions[target] + UP * lift_height,
                    RIGHT * rod_positions[target]
                    + DOWN * (2 - target_height - cube.width / 2),
                ]
            )



            self.play(MoveAlongPath(cube, path), run_time=1.5)
            self.wait(0.4)

        def hanoi(n, source, auxiliary, target):
            if n == 1:
                move_cube(source, target)
            else:
                hanoi(n - 1, source, target, auxiliary)
                move_cube(source, target)
                hanoi(n - 1, auxiliary, source, target)

        hanoi(num_cubes, 0, 1, 2)
        self.wait(2)

#created by dhruv