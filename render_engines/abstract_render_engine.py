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
import pygame as pg

class AbstractRenderEngine(ABC):
    @abstractmethod
    def draw_board(self):
        pass

    @abstractmethod
    def draw_pieces(self):
        pass

    @abstractmethod
    def main_loop(self):
        pass

    def TransformVec3(vecA,mat44):
        vecB = [0, 0, 0, 0]
        for i0 in range(0, 4):
            vecB[i0] = vecA[0] * mat44[0*4+i0] + vecA[1] * mat44[1*4+i0] + vecA[2] * mat44[2*4+i0] + mat44[3*4+i0]
        return [vecB[0]/vecB[3], vecB[1]/vecB[3], vecB[2]/vecB[3]]

    def TestRec(prjMat, mpos, display, zoom, quad):
        ll_ndc = AbstractRenderEngine.TransformVec3(quad[0], prjMat)
        tr_ndc = AbstractRenderEngine.TransformVec3(quad[2], prjMat)
        ndc = [(2.0 * mpos[0]/display[0] - 1.0)*zoom, (2.0 * mpos[1]/display[0] - display[1]/display[0])*zoom]
        inRect = 1 if (ndc[0]>=ll_ndc[0] and ndc[0]<=tr_ndc[0] and ndc[1]>=ll_ndc[1] and ndc[1]<=tr_ndc[1]) else 0
        return inRect

    def is_on_screen(quad, prjMat, zoom):
        on_screen = False
        for vertex in quad:
            projected_vertex = AbstractRenderEngine.TransformVec3(vertex, prjMat)
            if -zoom<=projected_vertex[0]<=zoom and -zoom<=projected_vertex[1]<=zoom:
                on_screen = True
        return on_screen