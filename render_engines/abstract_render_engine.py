'''
Copyright 2023 Sam A. Haygood

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

from abc import ABC, abstractmethod
import numpy as np
from PyQt5.QtWidgets import QApplication, QInputDialog


class AbstractRenderEngine(ABC):
    @abstractmethod
    def draw_board(self):
        pass

    @abstractmethod
    def draw_pieces(self):
        pass

    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def main_loop(self):
        pass

    def TransformVec3(vertex, modelview_matrix, projection_matrix):
        # Convert vertex to homogeneous coordinates
        vertex = np.array([*vertex, 1.0])
        
        # Apply ModelView matrix
        camera_space_vertex = np.dot(modelview_matrix, vertex)
        
        # Apply Projection matrix
        ndc_vertex = np.dot(projection_matrix, camera_space_vertex)
        
        # Convert to non-homogeneous coordinates
        ndc_vertex = ndc_vertex / ndc_vertex[3]
        
        return ndc_vertex[:3]

    def TestRec(mvMat, prjMat, mpos, display, zoom, polygon):
        projected_polygon = [AbstractRenderEngine.TransformVec3(vertex, mvMat, prjMat) for vertex in polygon]
        ndc = [(2.0 * mpos[0]/display[0] - 1.0), -(2.0 * mpos[1]/display[1] - 1.0)]
        return AbstractRenderEngine.point_inside_polygon(ndc, projected_polygon)

    def get_save_file_name(default_name):
        app = QApplication([])
        file_name, ok = QInputDialog.getText(None, "Save File Name", "Enter the name of the save file:", text=default_name)
        if ok:
            return file_name or default_name
        return None

    def point_inside_polygon(point, polygon):
            n = len(polygon)
            inside = False
            p1 = polygon[0]
            for i in range(1, n + 1):
                p2 = polygon[i % n]
                if (p1[1] > point[1]) != (p2[1] > point[1]) and \
                        point[0] < (p2[0] - p1[0]) * (point[1] - p1[1]) / (p2[1] - p1[1]) + p1[0]:
                    inside = not inside
                p1 = p2
            return inside

    def is_on_screen(polygon, mvMat, prjMat, zoom):
        def line_segments_intersect(a, b, c, d):
            def ccw(A, B, C):
                return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])

            return ccw(a, c, d) != ccw(b, c, d) and ccw(a, b, c) != ccw(a, b, d)

        screen_bounds = [(-1.0, -1.0), (1.0, -1.0), (1.0, 1.0), (-1.0, 1.0)]
        projected_polygon = [AbstractRenderEngine.TransformVec3(vertex, mvMat, prjMat) for vertex in polygon]

        for vertex in projected_polygon:
            if -1.0 <= vertex[0] <= 1.0 and -1.0 <= vertex[1] <= 1.0:
                return True

        for i in range(len(projected_polygon)):
            p1 = projected_polygon[i]
            p2 = projected_polygon[(i + 1) % len(projected_polygon)]

            for j in range(len(screen_bounds)):
                s1 = screen_bounds[j]
                s2 = screen_bounds[(j + 1) % len(screen_bounds)]

                if line_segments_intersect(p1, p2, s1, s2):
                    return True

        if AbstractRenderEngine.point_inside_polygon((0, 0), projected_polygon):
            return True

        return False

