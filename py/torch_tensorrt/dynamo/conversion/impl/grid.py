from typing import Optional

from torch.fx.node import Target
from torch_tensorrt.dynamo._SourceIR import SourceIR
from torch_tensorrt.dynamo.conversion._ConversionContext import ConversionContext
from torch_tensorrt.fx.converters.converter_utils import set_layer_name
from torch_tensorrt.fx.types import TRTTensor

import tensorrt as trt

# nearest, linear, cubic
GridSamplerInterpolationMode = {
    0: trt.InterpolationMode.NEAREST,
    1: trt.InterpolationMode.LINEAR,
    2: trt.InterpolationMode.CUBIC,
}

# zeros, border, reflection
GridSamplerSampling = {
    0: trt.SampleMode.FILL,
    1: trt.SampleMode.CLAMP,
    2: trt.SampleMode.REFLECT,
}


def grid(
    ctx: ConversionContext,
    target: Target,
    source_ir: Optional[SourceIR],
    name: str,
    input: TRTTensor,
    grid: TRTTensor,
    interpolation_mode: int,
    padding_mode: int,
    align_corners: bool,
) -> TRTTensor:
    grid_layer = ctx.net.add_grid_sample(input, grid)
    assert interpolation_mode in GridSamplerInterpolationMode
    grid_layer.interpolation_mode = GridSamplerInterpolationMode.get(
        interpolation_mode, None
    )
    assert padding_mode in GridSamplerSampling
    grid_layer.sample_mode = GridSamplerSampling.get(padding_mode, None)
    grid_layer.align_corners = align_corners
    set_layer_name(grid_layer, target, name + "_grid_layer", source_ir)
    return grid_layer.get_output(0)
