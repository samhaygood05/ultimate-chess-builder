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

    def TransformVec3(vecA,mat44):
        vecB = [0, 0, 0, 0]
        for i0 in range(0, 4):
            vecB[i0] = vecA[0] * mat44[0*4+i0] + vecA[1] * mat44[1*4+i0] + vecA[2] * mat44[2*4+i0] + mat44[3*4+i0]
        return [vecB[0]/vecB[3], vecB[1]/vecB[3], vecB[2]/vecB[3]]

    def TestRec(prjMat, mpos, display, zoom, polygon):
        projected_polygon = [AbstractRenderEngine.TransformVec3(vertex, prjMat) for vertex in polygon]
        ndc = [(2.0 * mpos[0]/display[0] - 1.0)*zoom, (2.0 * mpos[1]/display[0] - display[1]/display[0])*zoom]
        return AbstractRenderEngine.point_inside_polygon(ndc, projected_polygon)
    
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

    def is_on_screen(polygon, prjMat, zoom):
        def line_segments_intersect(a, b, c, d):
            def ccw(A, B, C):
                return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])

            return ccw(a, c, d) != ccw(b, c, d) and ccw(a, b, c) != ccw(a, b, d)

        screen_bounds = [(-zoom, -zoom), (zoom, -zoom), (zoom, zoom), (-zoom, zoom)]
        projected_polygon = [AbstractRenderEngine.TransformVec3(vertex, prjMat) for vertex in polygon]

        for vertex in projected_polygon:
            if -zoom <= vertex[0] <= zoom and -zoom <= vertex[1] <= zoom:
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

