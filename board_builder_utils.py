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

from typing import Callable, Tuple, Any

class BoardBuilderUtils:
    
    def sumt(a, b):
            return tuple(map(sum, zip(a, b)))
        
    def scalet(a, s):
        return tuple(x*s for x in a)

    def linear_transform(X, y, x):
        shift_x = (X[0] + 1/2)
        shift_y = (X[1] - 1/2)
        tuple = BoardBuilderUtils.sumt(BoardBuilderUtils.scalet(x, shift_x), BoardBuilderUtils.scalet(y, -shift_y))
        return (tuple[0], tuple[1], X[2])

    def functional_transform(
        X: Tuple[Any, Any, Any], 
        y: Callable[[Tuple[Any, Any, Any]], Tuple[Any, Any, Any]], 
        x: Callable[[Tuple[Any, Any, Any]], Tuple[Any, Any, Any]]) -> Tuple[Any, Any, Any]:

        local_x = x(X)
        local_y = y(X)
        return BoardBuilderUtils.linear_transform(X, local_y, local_x)