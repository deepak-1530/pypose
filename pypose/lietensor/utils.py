import torch
import functools
from .lietensor import  LieTensor
from .lietensor import SE3_type, se3_type
from .lietensor import SO3_type, so3_type
from .lietensor import Sim3_type, sim3_type
from .lietensor import RxSO3_type, rxso3_type


SO3 = functools.partial(LieTensor, ltype=SO3_type)
SO3.__doc__ = r'''
Alias of LieTensor for SO3.
'''

so3 = functools.partial(LieTensor, ltype=so3_type)
so3.__doc__ = r'''
Alias of LieTensor for so3.
'''

SE3 = functools.partial(LieTensor, ltype=SE3_type)
SE3.__doc__ = r'''
Alias of LieTensor for SE3.
'''

se3 = functools.partial(LieTensor, ltype=se3_type)
se3.__doc__ = r'''
Alias of LieTensor for se3.
'''

Sim3 = functools.partial(LieTensor, ltype=Sim3_type)
Sim3.__doc__ = r'''
Alias of LieTensor for Sim3.
'''

sim3 = functools.partial(LieTensor, ltype=sim3_type)
sim3.__doc__ = r'''
Alias of LieTensor for sim3.
'''

RxSO3 = functools.partial(LieTensor, ltype=RxSO3_type)
RxSO3.__doc__ = r'''
Alias of LieTensor for RxSO3.
'''

rxso3 = functools.partial(LieTensor, ltype=rxso3_type)
rxso3.__doc__ = r'''
Alias of LieTensor for rxso3.
'''

def randn_like(input, sigma=[1.0], **kwargs):
    r'''
    Returns a LieTensor with the same size as input that is filled with random
    LieTensor that satisfies the corresponding :obj:`input.ltype`.

    The corresponding random generator can be

    .. list-table:: List of available random LieTensor generator of input :obj:`ltype`.
        :widths: 25 25 30 30 30
        :header-rows: 1

        * - Name
          - ltype
          - randn function
          - Manifold
          - randn function
        * - Orthogonal Group
          - :obj:`SO3_type`
          - :meth:`randn_SO3`
          - :obj:`so3_type`
          - :meth:`randn_so3`
        * - Euclidean Group
          - :obj:`SE3_type`
          - :meth:`randn_SE3`
          - :obj:`se3_type`
          - :meth:`randn_se3`
        * - Similarity Group
          - :obj:`Sim3_type`
          - :meth:`randn_Sim3`
          - :obj:`sim3_type`
          - :meth:`randn_sim3`
        * - Scaling Orthogonal
          - :obj:`RxSO3_type`
          - :meth:`randn_RxSO3`
          - :obj:`rxso3_type`
          - :meth:`randn_rxso3`

    Args:

        input (LieTensor): the size of input will determine size of the output tensor.

        sigma (List, optional): sigma parameter for generating random LieTensors.
            For :obj:`SO3_type` and :obj:`so3_type` input: 1-dimensional list ([:obj:`sigma_d`]).
            For :obj:`SE3_type` and :obj:`se3_type` input: 2-dimensional list ([:obj:`sigma_t`, :obj:`sigma_d`])
            or 4-dimensional list ([:obj:`sigma_t_x`, :obj:`sigma_t_y`, :obj:`sigma_t_z`, :obj:`sigma_d`]).
            For :obj:`Sim3_type` and :obj:`sim3_type` input: 3-dimensional list ([:obj:`sigma_t`, :obj:`sigma_d`, :obj:`sigma_s`])
            or 5-dimensional list ([:obj:`sigma_t_x`, :obj:`sigma_t_y`, :obj:`sigma_t_z`, :obj:`sigma_d`, :obj:`sigma_s`]). 
            For :obj:`RxSO3_type` and :obj:`rxso3_type` input: 2-dimensional list ([:obj:`sigma_d`, :obj:`sigma_s`]).
            Default: 1.0 for all sigma.

        dtype (torch.dtype, optional): the desired data type of returned Tensor.
            Default: if None, defaults to the dtype of input.

        layout (torch.layout, optional): the desired layout of returned tensor.
            Default: if None, defaults to the layout of input.

        device (torch.device, optional): the desired device of returned tensor.
            Default: if None, defaults to the device of input.

        requires_grad (bool, optional): If autograd should record operations on the returned tensor.
            Default: False.

        memory_format (torch.memory_format, optional): the desired memory format of returned Tensor.
            Default: torch.preserve_format.

    Note:
        If we have:

        .. code::

            import pypose as pp
            x = pp.SO3(data)

        Then the following two usages are equivalent:

        .. code::

            pp.randn_like(x)
            pp.randn_SO3(x.lshape, dtype=x.dtype, layout=x.layout, device=x.device)

    Example:
        >>> x = pp.so3(torch.tensor([0, 0, 0]))
        >>> pp.randn_like(x)
            so3Type LieTensor:
            tensor([0.8970, 0.0943, 0.1399])
    '''
    if input.ltype == so3_type or input.ltype == SO3_type:
        assert len(sigma)==1, 'input sigma should be 1-dimensional list ([rotation_sigma]).'
        sigma = sigma[0]
    elif input.ltype == se3_type or input.ltype == SE3_type:
        if len(sigma)==1:
            sigma = [sigma[0], sigma[0]]
        else:
            assert len(sigma)==2 or len(sigma)==4, 'input sigma should be either 2-dimensional list ([transation_sigma, rotation_sigma]) or 4-dimensional list ([transation_sigma_x, transation_sigma_y, transation_sigma_z, rotation_sigma]).'
    elif input.ltype == rxso3_type or input.ltype == RxSO3_type:
        if len(sigma)==1:
            sigma = [sigma[0], sigma[0]]
        else:
            assert len(sigma)==2, 'input sigma should be 2-dimensional list ([transation_sigma, rotation_sigma]).'
    elif input.ltype == sim3_type or input.ltype == Sim3_type:
        if len(sigma)==1:
            sigma = [sigma[0], sigma[0], sigma[0]]
        else:
            assert len(sigma)==3 or len(sigma)==5, 'input sigma should be either 3-dimensional list ([transation_sigma, rotation_sigma, scale_sigma]) or 5-dimensional list ([transation_sigma_x, transation_sigma_y, transation_sigma_z, rotation_sigma, scale_sigma]).'
    return input.ltype.randn_like(*input.lshape, sigma=sigma, **kwargs)


def randn_so3(*size, sigma=1.0, **kwargs):
    r'''
    Returns :obj:`so3_type` LieTensor filled with random numbers satisfying the expected distance (quaternions distance)
    between the generated state and :math:`\mathbf{0}` is :obj:`sigma`.

    The shape of the tensor is defined by the variable argument size.

    Args:
        size (int...): a sequence of integers defining the shape of the output tensor.
            Can be a variable number of arguments or a collection like a list or tuple.

        sigma (float, optional): expected distance between the generated state and zero. Default: 1.

        requires_grad (bool, optional): If autograd should record operations on
            the returned tensor. Default: False.

        generator (torch.Generator, optional): a pseudorandom number generator for sampling

        dtype (torch.dtype, optional): the desired data type of returned tensor.
            Default: if None, uses a global default (see :meth:`torch.set_default_tensor_type()`).

        layout (torch.layout, optional): the desired layout of returned Tensor.
            Default: torch.strided.

        device (torch.device, optional): the desired device of returned tensor.
            Default: if None, uses the current device for the default tensor
            type (see :meth:`torch.set_default_tensor_type()`). device will be the CPU
            for CPU tensor types and the current CUDA device for CUDA tensor types.

    Returns:
        LieTensor: a :obj:`so3_type` LieTensor

    Given the expected distance :obj:`sigma`, we first calculte the standard deviation of the 
    individual components of the tangent perturbation :math:`\sigma_{\mathrm{r}}` as:

    .. math::
        \sigma_{\mathrm{r}} = \frac{2*\sigma}{\sqrt{3}}.

    The factor 2 is due to the way we define distance (see also `Matt Mason's lecture on 
    quaternions <http://www.cs.cmu.edu/afs/cs/academic/class/16741-s07/www/lectures/Lecture8.pdf>`_)
    The :math:`1/\sqrt{3}` factor is necessary because the distribution in the tangent space is 
    a 3-dimensional Gaussian, so that the *length* of a tangent vector needs to be scaled by :math:`1/\sqrt{3}`.

    Then the output can be written as:

    .. math::
        \mathrm{out}_i = \mathcal{N}(\mathbf{0}_{3\times 1}, \mathbf{\sigma_{\mathrm{r}}}_{3\times 1}),

    where :math:`\mathcal{N}` denotes Gaussian distribution.

    Note:
        The detailed explanation of the above implementation can be found in the 
        `OMPL code <https://ompl.kavrakilab.org/SO3StateSpace_8cpp_source.html>`_, line 119.

    Example:
        >>> pp.randn_so3(2, sigma=0.1, requires_grad=True, dtype=torch.float64)
        so3Type LieTensor:
        tensor([[ 0.1918, -0.0804, -0.1110],
        [ 0.0452, -0.1506,  0.2428]], dtype=torch.float64, requires_grad=True)
    '''
    return so3_type.randn(*size, sigma=sigma, **kwargs)


def randn_SO3(*size, sigma=1.0, **kwargs):
    r'''
    Returns :obj:`SO3_type` LieTensor filled with the Exponential map of the random
    :obj:`so3_type` LieTensor, whose expected quaternions distance from :math:`\mathbf{0}` is :obj:`sigma`.

    .. math::
        \mathrm{out}_i = \mathrm{Exp}(\mathcal{N}(\mathbf{0}_{3\times 1}, \mathbf{\sigma_{\mathrm{r}}}_{3\times 1}))

    For the definition and explanation of :math:`\mathbf{\sigma_{\mathrm{r}}}`, please see the documentation of :meth:`randn_so3()`.
    The shape of the tensor is defined by the variable argument size.

    Args:
        size (int...): a sequence of integers defining the shape of the output tensor.
            Can be a variable number of arguments or a collection like a list or tuple.

        sigma (float, optional): expected distance between the generated state and zero. Default: 1.0.

        requires_grad (bool, optional): If autograd should record operations on
            the returned tensor. Default: False.

        generator (torch.Generator, optional): a pseudorandom number generator for sampling

        dtype (torch.dtype, optional): the desired data type of returned tensor.
            Default: if None, uses a global default (see :meth:`torch.set_default_tensor_type()`).

        layout (torch.layout, optional): the desired layout of returned Tensor.
            Default: torch.strided.

        device (torch.device, optional): the desired device of returned tensor.
            Default: if None, uses the current device for the default tensor
            type (see :meth:`torch.set_default_tensor_type()`). device will be the CPU
            for CPU tensor types and the current CUDA device for CUDA tensor types.

    Returns:
        LieTensor: a :obj:`SO3_type` LieTensor

    Example:
        >>> pp.randn_SO3(2, sigma=0.1, requires_grad=True, dtype=torch.float64)
        SO3Type LieTensor:
        tensor([[-0.0494,  0.0226,  0.0243,  0.9982],
                [-0.0701, -0.0723, -0.0199,  0.9947]], dtype=torch.float64,
            requires_grad=True)

    '''
    return SO3_type.randn(*size, sigma=sigma, **kwargs)


def randn_se3(*size, sigma=[1.0,1.0], **kwargs):
    r'''
    Returns :obj:`se3_type` LieTensor, where the transation part :math:`\bm{\tau}_i` is filled with 
    random numbers from a normal distribution with mean 0 and variance :obj:`sigma_t`, the rotation 
    part :math:`\bm{\phi}_i` is filled with random numbers satisfying the expected distance (quaternions distance) 
    between the generated state and :math:`\mathbf{0}` is :obj:`sigma_d`.

    .. math::
        \mathrm{out}_i = [\bm{\tau}_i, \bm{\phi}_i],

    where :math:`\bm{\tau}_i = \mathcal{N}(\mathbf{0}_{3\times 1}, \mathbf{\sigma_{\rm{t}}}_{3\times 1})` and 
    :math:`\bm{\phi}_i = \mathcal{N}(\mathbf{0}_{3\times 1}, \mathbf{\sigma_{\mathrm{r}}}_{3\times 1})`.
    :math:`\mathbf{\sigma_{\mathrm{r}}}` is calculated the same as :meth:`randn_so3()`:

    .. math::
        \sigma_{\mathrm{r}} = \frac{2*\sigma_{\rm{d}}}{\sqrt{3}}.

    The shape of the tensor is defined by the variable argument size.

    Args:
        size (int...): a sequence of integers defining the shape of the output tensor.
            Can be a variable number of arguments or a collection like a list or tuple.

        sigma (List, optional): could be 2-dimensional list ([:obj:`sigma_t`, :obj:`sigma_d`])
        or 4-dimensional list ([:obj:`sigma_t_x`, :obj:`sigma_t_y`, :obj:`sigma_t_z`, :obj:`sigma_d`]). 
        Default: [1.0, 1.0].

        requires_grad (bool, optional): If autograd should record operations on
            the returned tensor. Default: False.

        generator (torch.Generator, optional): a pseudorandom number generator for sampling

        dtype (torch.dtype, optional): the desired data type of returned tensor.
            Default: if None, uses a global default (see :meth:`torch.set_default_tensor_type()`).

        layout (torch.layout, optional): the desired layout of returned Tensor.
            Default: torch.strided.

        device (torch.device, optional): the desired device of returned tensor.
            Default: if None, uses the current device for the default tensor
            type (see :meth:`torch.set_default_tensor_type()`). device will be the CPU
            for CPU tensor types and the current CUDA device for CUDA tensor types.

    Returns:
        LieTensor: a :obj:`se3_type` LieTensor

    Example:
        >>> pp.randn_se3(2, sigma=[1.0,0.5], requires_grad=True, dtype=torch.float64) # sigma = [sigma_t, sigma_d]
            se3Type LieTensor:
            tensor([[-1.2322, -1.4267,  0.6751,  0.8957, -0.0815, -0.8978],
                    [ 0.2730,  0.1029,  0.0180, -0.3064, -1.0914,  1.0258]],
                dtype=torch.float64, requires_grad=True)
        >>> pp.randn_se3(2, sigma=[0.1,0.2,0.3,0.5]) # sigma = [sigma_t_x, sigma_t_y, sigma_t_z, sigma_d]
            se3Type LieTensor:
            tensor([[ 0.0570,  0.1811, -0.0433, -0.3530,  0.8739,  0.3371],
                    [-0.1572,  0.0661, -0.0921, -0.5485,  0.4343, -0.1366]])
    '''
    return se3_type.randn(*size, sigma=sigma, **kwargs)


def randn_SE3(*size, sigma=[1.0,1.0], **kwargs):
    r'''
    Returns :obj:`SE3_type` LieTensor filled with the Exponential map of the random
    :obj:`se3_type` LieTensor generated using :meth:`randn_se3()`.

    .. math::
        \mathrm{out}_i = \mathrm{Exp}([\mathcal{N}(\mathbf{0}_{3\times 1}, \mathbf{\sigma_{\rm{t}}}_{3\times 1}), \mathcal{N}(\mathbf{0}_{3\times 1}, \mathbf{\sigma_{\mathrm{r}}}_{3\times 1})])

    The shape of the tensor is defined by the variable argument size.

    Args:
        size (int...): a sequence of integers defining the shape of the output tensor.
            Can be a variable number of arguments or a collection like a list or tuple.

        sigma (List, optional): could be 2-dimensional list ([:obj:`sigma_t`, :obj:`sigma_d`])
        or 4-dimensional list ([:obj:`sigma_t_x`, :obj:`sigma_t_y`, :obj:`sigma_t_z`, :obj:`sigma_d`]). 
        Default: [1.0, 1.0].

        requires_grad (bool, optional): If autograd should record operations on
            the returned tensor. Default: False.

        generator (torch.Generator, optional): a pseudorandom number generator for sampling

        dtype (torch.dtype, optional): the desired data type of returned tensor.
            Default: if None, uses a global default (see :meth:`torch.set_default_tensor_type()`).

        layout (torch.layout, optional): the desired layout of returned Tensor.
            Default: torch.strided.

        device (torch.device, optional): the desired device of returned tensor.
            Default: if None, uses the current device for the default tensor
            type (see :meth:`torch.set_default_tensor_type()`). device will be the CPU
            for CPU tensor types and the current CUDA device for CUDA tensor types.

    Returns:
        LieTensor: a :obj:`SE3_type` LieTensor

    Example:
        >>> pp.randn_SE3(2, sigma=[1.0,2.0]) # sigma = [sigma_t, sigma_d]
            SE3Type LieTensor:
            tensor([[-0.8355,  0.7782,  0.0338, -0.1641,  0.5466,  0.0998,  0.8151],
                    [ 0.2710, -2.0285, -0.6473, -0.5649, -0.6031,  0.5611,  0.0478]])
        >>> pp.randn_SE3(2, sigma=[1.0,1.5,2.0,2.0]) # sigma = [sigma_t_x, sigma_t_y, sigma_t_z, sigma_d]
            SE3Type LieTensor:
            tensor([[ 0.8922, -0.5284,  0.8733,  0.8678, -0.3748,  0.3049,  0.1164],
                    [-1.3952, -2.8119,  2.5019,  0.2641,  0.2629,  0.0624,  0.9259]])
    '''
    return SE3_type.randn(*size, sigma=sigma, **kwargs)


def randn_sim3(*size, sigma=[1.0,1.0,1.0], **kwargs):
    r'''
    Returns :obj:`sim3_type` LieTensor, where the transation part :math:`\bm{\tau}_i` is filled with random numbers from a normal distribution with mean 0 and variance :obj:`sigma_t`, the rotation part :math:`\bm{\phi}_i` is filled with random numbers satisfying the expected distance (quaternions distance) between the generated state and :math:`\mathbf{0}` is :obj:`sigma_d`, and the scale part :math:`s_i` is a random number from a normal distribution with mean 0 and variance :obj:`sigma_s`.

    .. math::
        \mathrm{out}_i = [\bm{\tau}_i, \bm{\phi}_i, s_i],

    where :math:`[\bm{\tau}_i, \bm{\phi}_i]` is generated using :meth:`randn_se3()` and :math:`s_i = \mathcal{N}(0, \sigma_{\rm{s}}})`.

    The shape of the tensor is defined by the variable argument size.

    Args:
        size (int...): a sequence of integers defining the shape of the output tensor.
            Can be a variable number of arguments or a collection like a list or tuple.

        sigma (List, optional): could be 3-dimensional list ([:obj:`sigma_t`, :obj:`sigma_d`, :obj:`sigma_s`])
        or 5-dimensional list ([:obj:`sigma_t_x`, :obj:`sigma_t_y`, :obj:`sigma_t_z`, :obj:`sigma_d`, :obj:`sigma_s`]). 
        Default: [1.0, 1.0, 1.0].

        requires_grad (bool, optional): If autograd should record operations on
            the returned tensor. Default: False.

        generator (torch.Generator, optional): a pseudorandom number generator for sampling

        dtype (torch.dtype, optional): the desired data type of returned tensor.
            Default: if None, uses a global default (see :meth:`torch.set_default_tensor_type()`).

        layout (torch.layout, optional): the desired layout of returned Tensor.
            Default: torch.strided.

        device (torch.device, optional): the desired device of returned tensor.
            Default: if None, uses the current device for the default tensor
            type (see :meth:`torch.set_default_tensor_type()`). device will be the CPU
            for CPU tensor types and the current CUDA device for CUDA tensor types.

    Returns:
        LieTensor: a :obj:`sim3_type` LieTensor

    Example:
        >>> pp.randn_sim3(2, sigma=[1.0,1.0,2.0]) # sigma = [sigma_t, sigma_d, sigma_s]
            sim3Type LieTensor:
            tensor([[-1.0898, -0.3859, -0.6781, -1.0066,  0.4151,  0.9659, -1.5967],
                    [-1.8039,  0.7329, -0.0616, -1.0538, -0.3579, -1.3305, -0.0532]])
        >>> pp.randn_sim3(2, sigma=[1.0,1.0,2.0,1.0,2.0]) # sigma = [sigma_t_x, sigma_t_y, sigma_t_z, sigma_d, sigma_s]
            sim3Type LieTensor:
            tensor([[-0.4073,  1.0928, -0.4961,  1.2099,  0.6376, -0.8252,  2.4228],
                    [ 0.2881,  1.5011,  0.3938,  1.6231, -0.6546, -0.0889, -0.1773]])
    '''
    return sim3_type.randn(*size, sigma=sigma, **kwargs)


def randn_Sim3(*size, sigma=[1.0,1.0,1.0], **kwargs):
    r'''
    Returns :obj:`Sim3_type` LieTensor filled with the Exponential map of the random
    :obj:`sim3_type` LieTensor generated using :meth:`randn_sim3()`.

    .. math::
        \mathrm{out}_i = \mathrm{Exp}([\mathcal{N}(\mathbf{0}_{3\times 1}, \mathbf{\sigma_{\rm{t}}}_{3\times 1}), \mathcal{N}(\mathbf{0}_{3\times 1}, \mathbf{\sigma_{\mathrm{r}}}_{3\times 1}), \mathcal{N}(0, \sigma_{\rm{s}}})])

    The shape of the tensor is defined by the variable argument size.

    Args:
        size (int...): a sequence of integers defining the shape of the output tensor.
            Can be a variable number of arguments or a collection like a list or tuple.

        sigma (List, optional): could be 3-dimensional list ([:obj:`sigma_t`, :obj:`sigma_d`, :obj:`sigma_s`])
        or 5-dimensional list ([:obj:`sigma_t_x`, :obj:`sigma_t_y`, :obj:`sigma_t_z`, :obj:`sigma_d`, :obj:`sigma_s`]). 
        Default: [1.0, 1.0, 1.0].

        requires_grad (bool, optional): If autograd should record operations on
            the returned tensor. Default: False.

        generator (torch.Generator, optional): a pseudorandom number generator for sampling

        dtype (torch.dtype, optional): the desired data type of returned tensor.
            Default: if None, uses a global default (see :meth:`torch.set_default_tensor_type()`).

        layout (torch.layout, optional): the desired layout of returned Tensor.
            Default: torch.strided.

        device (torch.device, optional): the desired device of returned tensor.
            Default: if None, uses the current device for the default tensor
            type (see :meth:`torch.set_default_tensor_type()`). device will be the CPU
            for CPU tensor types and the current CUDA device for CUDA tensor types.

    Returns:
        LieTensor: a :obj:`Sim_type` LieTensor

    Example:
        >>> pp.randn_Sim3(2, sigma=[1.0,1.0,2.0]) # sigma = [sigma_t, sigma_d, sigma_s]
            Sim3Type LieTensor:
            tensor([[-0.4676, -0.9314, -0.4881,  0.6543, -0.4844, -0.5182,  0.2620,  1.1351],
                    [ 0.7047, -0.8917,  0.4568, -0.1251, -0.4366, -0.3225,  0.8305,  0.2759]])
        >>> pp.randn_Sim3(2, sigma=[1.0,1.0,2.0,1.0,2.0]) # sigma = [sigma_t_x, sigma_t_y, sigma_t_z, sigma_d, sigma_s]
            Sim3Type LieTensor:
            tensor([[ 0.3882,  0.5598,  2.3918, -0.1527,  0.4519,  0.4843,  0.7334,  0.3091],
                    [-1.0396, -2.8683, -0.4880, -0.7121,  0.2236,  0.3979,  0.5334,  3.8714]])
    '''
    return Sim3_type.randn(*size, sigma=sigma, **kwargs)


def randn_rxso3(*size, sigma=[1.0,1.0], **kwargs):
    r'''
    Returns :obj:`rxso3_type` LieTensor, where the rotation part :math:`\bm{\phi}_i` is filled with random numbers satisfying the expected distance (quaternions distance) between the generated state and :math:`\mathbf{0}` is :obj:`sigma_d`, the scale part :math:`s_i` is a random number from a normal distribution with mean 0 and variance :obj:`sigma_s`.

    .. math::
        \mathrm{out}_i = [\bm{\phi}_i, s_i],

    where :math:`\bm{\phi}_i` is generated using :meth:`randn_so3()` and :math:`s_i = \mathcal{N}(0, \sigma_{\rm{s}}})`.

    The shape of the tensor is defined by the variable argument size.

    Args:
        size (int...): a sequence of integers defining the shape of the output tensor.
            Can be a variable number of arguments or a collection like a list or tuple.

        sigma (List, optional): 2-dimensional list ([:obj:`sigma_d`, :obj:`sigma_s`]). 
        Default: [1.0, 1.0].

        requires_grad (bool, optional): If autograd should record operations on
            the returned tensor. Default: False.

        generator (torch.Generator, optional): a pseudorandom number generator for sampling

        dtype (torch.dtype, optional): the desired data type of returned tensor.
            Default: if None, uses a global default (see :meth:`torch.set_default_tensor_type()`).

        layout (torch.layout, optional): the desired layout of returned Tensor.
            Default: torch.strided.

        device (torch.device, optional): the desired device of returned tensor.
            Default: if None, uses the current device for the default tensor
            type (see :meth:`torch.set_default_tensor_type()`). device will be the CPU
            for CPU tensor types and the current CUDA device for CUDA tensor types.

    Returns:
        LieTensor: a :obj:`rxso3_type` LieTensor

    Example:
        >>> pp.randn_rxso3(2, sigma=[1.0,2.0]) # [sigma_d, sigma_s]
            rxso3Type LieTensor:
            tensor([[-0.6014,  0.9899, -2.5600, -1.7157],
                    [-0.5560,  0.3107,  0.8966, -1.5175]])
    '''
    return rxso3_type.randn(*size, sigma=sigma, **kwargs)


def randn_RxSO3(*size, sigma=[1.0,1.0], **kwargs):
    r'''
    Returns :obj:`RxSO3_type` LieTensor filled with the Exponential map of the random
    :obj:`sim3_type` LieTensor generated using :meth:`randn_rxso3()`.

    .. math::
        \mathrm{out}_i = \mathrm{Exp}([\mathcal{N}(\mathbf{0}_{3\times 1}, \mathbf{\sigma_{\mathrm{r}}}_{3\times 1}), \mathcal{N}(0, \sigma_{\rm{s}}})])

    The shape of the tensor is defined by the variable argument size.

    Args:
        size (int...): a sequence of integers defining the shape of the output tensor.
            Can be a variable number of arguments or a collection like a list or tuple.

        sigma (List, optional): 2-dimensional list ([:obj:`sigma_d`, :obj:`sigma_s`]). 
        Default: [1.0, 1.0].

        requires_grad (bool, optional): If autograd should record operations on
            the returned tensor. Default: False.

        generator (torch.Generator, optional): a pseudorandom number generator for sampling

        dtype (torch.dtype, optional): the desired data type of returned tensor.
            Default: if None, uses a global default (see :meth:`torch.set_default_tensor_type()`).

        layout (torch.layout, optional): the desired layout of returned Tensor.
            Default: torch.strided.

        device (torch.device, optional): the desired device of returned tensor.
            Default: if None, uses the current device for the default tensor
            type (see :meth:`torch.set_default_tensor_type()`). device will be the CPU
            for CPU tensor types and the current CUDA device for CUDA tensor types.

    Returns:
        LieTensor: a :obj:`RxSO3_type` LieTensor

    Example:
        >>> pp.randn_RxSO3(2, sigma=[1.0,2.0]) # [sigma_d, sigma_s]
            RxSO3Type LieTensor:
            tensor([[ 0.5917,  0.2337, -0.3464,  0.6894,  0.0237],
                    [-0.3895,  0.2188, -0.4915,  0.7476,  0.2706]])
    '''
    return RxSO3_type.randn(*size, sigma=sigma, **kwargs)


def identity_like(liegroup, **kwargs):
    r'''
     Returns identity LieTensor with the same :obj:`lsize` and :obj:`ltype` as the given LieTensor.

    Args:
        liegroup (LieTensor): the size of liegroup will determine the size of the output tensor. 

    Args:
        requires_grad (bool, optional): If autograd should record operations on
            the returned tensor. Default: False.

        generator (torch.Generator, optional): a pseudorandom number generator for sampling

        dtype (torch.dtype, optional): the desired data type of returned tensor.
            Default: if None, uses a global default (see :meth:`torch.set_default_tensor_type()`).

        layout (torch.layout, optional): the desired layout of returned Tensor.
            Default: torch.strided.

        device (torch.device, optional): the desired device of returned tensor.
            Default: if None, uses the current device for the default tensor
            type (see :meth:`torch.set_default_tensor_type()`). device will be the CPU
            for CPU tensor types and the current CUDA device for CUDA tensor types.
    
    Example:
        >>> x = pp.randn_SO3(3, device="cuda:0", dtype=torch.double, requires_grad=True)
        >>> pp.identity_like(x, device="cpu")
        SO3Type LieTensor:
        tensor([[0., 0., 0., 1.],
                [0., 0., 0., 1.],
                [0., 0., 0., 1.]])
    '''
    return liegroup.ltype.identity_like(*liegroup.lshape, **kwargs)


def identity_SO3(*lsize, **kwargs):
    r'''
    Returns identity :obj:`SO3_type` LieTensor with the given :obj:`lsize`.

    Args:
        lsize (int..., optional): a sequence of integers defining the :obj:`LieTensor.lshape` of
            the output LieTensor. Can be a variable number of arguments or a collection like a
            list or tuple. If not given, a single :obj:`SO3_type` item will be returned.

    Args:
        requires_grad (bool, optional): If autograd should record operations on
            the returned tensor. Default: False.

        generator (torch.Generator, optional): a pseudorandom number generator for sampling

        dtype (torch.dtype, optional): the desired data type of returned tensor.
            Default: if None, uses a global default (see :meth:`torch.set_default_tensor_type()`).

        layout (torch.layout, optional): the desired layout of returned Tensor.
            Default: torch.strided.

        device (torch.device, optional): the desired device of returned tensor.
            Default: if None, uses the current device for the default tensor
            type (see :meth:`torch.set_default_tensor_type()`). device will be the CPU
            for CPU tensor types and the current CUDA device for CUDA tensor types.
    
    Returns:
        LieTensor: a :obj:`SO3_type` LieTensor
    
    Example:
        >>> pp.identity_SO3()
        SO3Type LieTensor:
        tensor([0., 0., 0., 1.])

        >>> pp.identity_SO3(2)
        SO3Type LieTensor:
        tensor([[0., 0., 0., 1.],
                [0., 0., 0., 1.]])

        >>> pp.identity_SO3(2, 1)
        SO3Type LieTensor:
        tensor([[[0., 0., 0., 1.]],
                [[0., 0., 0., 1.]]])
    '''
    return SO3_type.identity(*lsize, **kwargs)


def identity_so3(*lsize, **kwargs):
    r'''
    Returns identity :obj:`so3_type` LieTensor with the given :obj:`lsize`.

    Args:
        lsize (int..., optional): a sequence of integers defining the :obj:`LieTensor.lshape` of
            the output LieTensor. Can be a variable number of arguments or a collection like a
            list or tuple. If not given, a single :obj:`so3_type` item will be returned.

    Args:
        requires_grad (bool, optional): If autograd should record operations on
            the returned tensor. Default: False.

        generator (torch.Generator, optional): a pseudorandom number generator for sampling

        dtype (torch.dtype, optional): the desired data type of returned tensor.
            Default: if None, uses a global default (see :meth:`torch.set_default_tensor_type()`).

        layout (torch.layout, optional): the desired layout of returned Tensor.
            Default: torch.strided.

        device (torch.device, optional): the desired device of returned tensor.
            Default: if None, uses the current device for the default tensor
            type (see :meth:`torch.set_default_tensor_type()`). device will be the CPU
            for CPU tensor types and the current CUDA device for CUDA tensor types.
    
    Returns:
        LieTensor: a :obj:`so3_type` LieTensor
    
    Example:
        >>> pp.identity_so3()
        so3Type LieTensor:
        tensor([0., 0., 0.])

        >>> pp.identity_so3(2)
        so3Type LieTensor:
        tensor([[0., 0., 0.],
                [0., 0., 0.]])

        >>> pp.identity_so3(2,1)
        so3Type LieTensor:
        tensor([[[0., 0., 0.]],
                [[0., 0., 0.]]])
    '''
    return so3_type.identity(*lsize, **kwargs)


def identity_SE3(*lsize, **kwargs):
    r'''
    Returns identity :obj:`SE3_type` LieTensor with the given :obj:`lsize`.

    Args:
        lsize (int..., optional): a sequence of integers defining the :obj:`LieTensor.lshape` of
            the output LieTensor. Can be a variable number of arguments or a collection like a
            list or tuple. If not given, a single :obj:`SE3_type` item will be returned.
    
    Args:

        requires_grad (bool, optional): If autograd should record operations on
            the returned tensor. Default: False.

        generator (torch.Generator, optional): a pseudorandom number generator for sampling

        dtype (torch.dtype, optional): the desired data type of returned tensor.
            Default: if None, uses a global default (see :meth:`torch.set_default_tensor_type()`).

        layout (torch.layout, optional): the desired layout of returned Tensor.
            Default: torch.strided.

        device (torch.device, optional): the desired device of returned tensor.
            Default: if None, uses the current device for the default tensor
            type (see :meth:`torch.set_default_tensor_type()`). device will be the CPU
            for CPU tensor types and the current CUDA device for CUDA tensor types.
    
    Returns:
        LieTensor: a :obj:`SE3_type` LieTensor
    
    Example:
        >>> pp.identity_SE3()
        SE3Type LieTensor:
        tensor([0., 0., 0., 0., 0., 0., 1.])

        >>> pp.identity_SE3(2)
        SE3Type LieTensor:
        tensor([[0., 0., 0., 0., 0., 0., 1.],
                [0., 0., 0., 0., 0., 0., 1.]])

        >>> pp.identity_SE3(2,1)
        SE3Type LieTensor:
        tensor([[[0., 0., 0., 0., 0., 0., 1.]],
                [[0., 0., 0., 0., 0., 0., 1.]]])
    '''
    return SE3_type.identity(*lsize, **kwargs)


def identity_se3(*lsize, **kwargs):
    r'''
    Returns identity :obj:`se3_type` LieTensor with the given :obj:`lsize`.
    
    Args:
        lsize (int..., optional): a sequence of integers defining the :obj:`LieTensor.lshape` of
            the output LieTensor. Can be a variable number of arguments or a collection like a
            list or tuple. If not given, a single :obj:`se3_type` item will be returned.

    Args:
        requires_grad (bool, optional): If autograd should record operations on
            the returned tensor. Default: False.

        generator (torch.Generator, optional): a pseudorandom number generator for sampling

        dtype (torch.dtype, optional): the desired data type of returned tensor.
            Default: if None, uses a global default (see :meth:`torch.set_default_tensor_type()`).

        layout (torch.layout, optional): the desired layout of returned Tensor.
            Default: torch.strided.

        device (torch.device, optional): the desired device of returned tensor.
            Default: if None, uses the current device for the default tensor
            type (see :meth:`torch.set_default_tensor_type()`). device will be the CPU
            for CPU tensor types and the current CUDA device for CUDA tensor types.
    
    Returns:
        LieTensor: a :obj:`se3_type` LieTensor
    
    Example:
        >>> pp.identity_se3()
        se3Type LieTensor:
        tensor([0., 0., 0., 0., 0., 0.])

        >>> pp.identity_se3(2)
        se3Type LieTensor:
        tensor([[0., 0., 0., 0., 0., 0.],
                [0., 0., 0., 0., 0., 0.]])

        >>> pp.identity_se3(2,1)
        se3Type LieTensor:
        tensor([[0., 0., 0., 0., 0., 0.],
                [0., 0., 0., 0., 0., 0.]])
    '''
    return se3_type.identity(*lsize, **kwargs)


def identity_sim3(*lsize, **kwargs):
    r'''
     Returns identity :obj:`sim3_type` LieTensor with the given :obj:`lsize`. 

    Args:
        lsize (int..., optional): a sequence of integers defining the :obj:`LieTensor.lshape` of
            the output LieTensor. Can be a variable number of arguments or a collection like a
            list or tuple. If not given, a single :obj:`sim3_type` item will be returned.

    Args:
        requires_grad (bool, optional): If autograd should record operations on
            the returned tensor. Default: False.

        generator (torch.Generator, optional): a pseudorandom number generator for sampling

        dtype (torch.dtype, optional): the desired data type of returned tensor.
            Default: if None, uses a global default (see :meth:`torch.set_default_tensor_type()`).

        layout (torch.layout, optional): the desired layout of returned Tensor.
            Default: torch.strided.

        device (torch.device, optional): the desired device of returned tensor.
            Default: if None, uses the current device for the default tensor
            type (see :meth:`torch.set_default_tensor_type()`). device will be the CPU
            for CPU tensor types and the current CUDA device for CUDA tensor types.
    
    Returns:
        LieTensor: a :obj:`sim3_type` LieTensor
        
    Example:
        >>> pp.identity_sim3()
        sim3Type LieTensor:
        tensor([0., 0., 0., 0., 0., 0., 0.])

        >>> identity_sim3(2)
        sim3Type LieTensor:
        tensor([[0., 0., 0., 0., 0., 0., 0.],
                [0., 0., 0., 0., 0., 0., 0.]])

        >>> identity_sim3(2,1)
        sim3Type LieTensor:
        tensor([[[0., 0., 0., 0., 0., 0., 0.]],
                [[0., 0., 0., 0., 0., 0., 0.]]])
    '''
    return sim3_type.identity(*lsize, **kwargs)


def identity_Sim3(*lsize, **kwargs):
    r'''
    Returns identity :obj:`Sim3_type` LieTensor with the given :obj:`lsize`.

    Args:
        lsize (int..., optional): a sequence of integers defining the :obj:`LieTensor.lshape` of
            the output LieTensor. Can be a variable number of arguments or a collection like a
            list or tuple. If not given, a single :obj:`Sim3_type` item will be returned.

    Args:
        requires_grad (bool, optional): If autograd should record operations on
            the returned tensor. Default: False.

        generator (torch.Generator, optional): a pseudorandom number generator for sampling

        dtype (torch.dtype, optional): the desired data type of returned tensor.
            Default: if None, uses a global default (see :meth:`torch.set_default_tensor_type()`).

        layout (torch.layout, optional): the desired layout of returned Tensor.
            Default: torch.strided.

        device (torch.device, optional): the desired device of returned tensor.
            Default: if None, uses the current device for the default tensor
            type (see :meth:`torch.set_default_tensor_type()`). device will be the CPU
            for CPU tensor types and the current CUDA device for CUDA tensor types.
    
    Returns:
        LieTensor: a :obj:`Sim3_type` LieTensor
        
    Example:
        >>> pp.identity_Sim3()
        Sim3Type LieTensor:
        tensor([0., 0., 0., 0., 0., 0., 1., 1.])

        >>> identity_Sim3(2)
        Sim3Type LieTensor:
        tensor([[0., 0., 0., 0., 0., 0., 1., 1.],
                [0., 0., 0., 0., 0., 0., 1., 1.]])

        >>> identity_Sim3(2,1)
        Sim3Type LieTensor:
        tensor([[[0., 0., 0., 0., 0., 0., 1., 1.]],
                [[0., 0., 0., 0., 0., 0., 1., 1.]]])
    '''
    return Sim3_type.identity(*lsize, **kwargs)    


def identity_rxso3(*size, **kwargs):
    return rxso3_type.identity(*size, **kwargs)


def identity_RxSO3(*size, **kwargs):
    return RxSO3_type.identity(*size, **kwargs)


def assert_ltype(func):
    @functools.wraps(func)
    def checker(*args, **kwargs):
        assert isinstance(args[0], LieTensor), "Invalid LieTensor Type."
        out = func(*args, **kwargs)
        return out
    return checker


@assert_ltype
def Exp(input):
    r"""The Exponential map for :obj:`LieTensor` (Lie Algebra).

    .. math::
        \mathrm{Exp}: \mathcal{g} \mapsto \mathcal{G}

    Args:
        input (LieTensor): the input LieTensor (Lie Algebra)

    Return:
        LieTensor: the output LieTensor (Lie Group)

    .. list-table:: List of supported :math:`\mathrm{Exp}` map
        :widths: 20 20 8 20 20
        :header-rows: 1

        * - input :obj:`ltype`
          - :math:`\mathcal{g}` (Lie Algebra)
          - :math:`\mapsto`
          - :math:`\mathcal{G}` (Lie Group)
          - output :obj:`ltype`
        * - :obj:`so3_type`
          - :math:`\mathcal{g}\in\mathbb{R}^{*\times3}`
          - :math:`\mapsto`
          - :math:`\mathcal{G}\in\mathbb{R}^{*\times4}`
          - :obj:`SO3_type`
        * - :obj:`se3_type`
          - :math:`\mathcal{g}\in\mathbb{R}^{*\times6}`
          - :math:`\mapsto`
          - :math:`\mathcal{G}\in\mathbb{R}^{*\times7}`
          - :obj:`SE3_type`
        * - :obj:`sim3_type`
          - :math:`\mathcal{g}\in\mathbb{R}^{*\times7}`
          - :math:`\mapsto`
          - :math:`\mathcal{G}\in\mathbb{R}^{*\times8}`
          - :obj:`Sim3_type`
        * - :obj:`rxso3_type`
          - :math:`\mathcal{g}\in\mathbb{R}^{*\times4}`
          - :math:`\mapsto`
          - :math:`\mathcal{G}\in\mathbb{R}^{*\times5}`
          - :obj:`RxSO3_type`

    Warning:
        This function :func:`Exp()` is different from :func:`exp()`, which returns
        a new torch tensor with the exponential of the elements of the input tensor.

    * Input :math:`\mathbf{x}`'s :obj:`ltype` is :obj:`so3_type`
      (input :math:`\mathbf{x}` is an instance of :meth:`so3`):

        If :math:`\|\mathbf{x}_i\| > \text{eps}`:

        .. math::
            \mathbf{y}_i = \left[\mathbf{x}_{i,1}\theta_i,
            \mathbf{x}_{i,2}\theta_i,
            \mathbf{x}_{i,3}\theta_i,
            \cos(\frac{\|\mathbf{x}_i\|}{2})\right],

        where :math:`\theta_i = \frac{1}{\|\mathbf{x}_i\|}\sin(\frac{\|\mathbf{x}_i\|}{2})`,

        otherwise:

        .. math::
            \mathbf{y}_i = \left[\mathbf{x}_{i,1}\theta_i,~
            \mathbf{x}_{i,2}\theta_i,~
            \mathbf{x}_{i,3}\theta_i,~
            1 - \frac{\|\mathbf{x}_i\|^2}{8} + \frac{\|\mathbf{x}_i\|^4}{384} \right],

        where :math:`\theta_i = \frac{1}{2} - \frac{1}{48} \|\mathbf{x}_i\|^2 + \frac{1}{3840} \|\mathbf{x}_i\|^4`.

    * Input :math:`\mathbf{x}`'s :obj:`ltype` is :obj:`se3_type`
      (input :math:`\mathbf{x}` is an instance of :meth:`se3`):

        Let :math:`\bm{\tau}_i`, :math:`\bm{\phi}_i` be the translation and rotation parts
        of :math:`\mathbf{x}_i`, respectively; :math:`\mathbf{y}` be the output.

        .. math::
            \mathbf{y}_i = \left[\mathbf{J}_i\bm{\tau}_i, \mathrm{Exp}(\bm{\phi}_i)\right],
        
        where :math:`\mathrm{Exp}` is the Exponential map for :obj:`so3_type` input and
        :math:`\mathbf{J}_i` is the left Jacobian for :obj:`so3_type` input.

    * Input :math:`\mathbf{x}`'s :obj:`ltype` is :obj:`rxso3_type`
      (input :math:`\mathbf{x}` is an instance of :meth:`rxso3`):

        Let :math:`\bm{\phi}_i`, :math:`\sigma_i` be the rotation and scale parts of
        :math:`\mathbf{x}_i`, respectively; :math:`\mathbf{y}` be the output.

        .. math::
            \mathbf{y}_i = \left[\mathrm{Exp}(\bm{\phi}_i), \mathrm{exp}(\sigma_i)\right],

        where :math:`\mathrm{exp}` is the exponential function.

    * Input :math:`\mathbf{x}`'s :obj:`ltype` is :obj:`sim3_type`
      (input :math:`\mathbf{x}` is an instance of :meth:`sim3`):

        Let :math:`\bm{\tau}_i`, :math:`^{s}\bm{\phi}_i` be the translation and
        :meth:`rxso3` parts of :math:`\mathbf{x}_i`, respectively.
        :math:`\bm{\phi}_i = \theta_i\mathbf{n}_i`, :math:`\sigma_i` be the rotation
        and scale parts of :math:`^{s}\bm{\phi}_i`, :math:`\boldsymbol{\Phi}_i` be the skew matrix
        of :math:`\bm{\phi}_i`; :math:`s_i = e^\sigma_i`, :math:`\mathbf{y}` be the output.

        .. math::
            \mathbf{y}_i = \left[^{s}\mathbf{W}_i\bm{\tau}_i, \mathrm{Exp}(^{s}\bm{\phi}_i)\right],
        
        where

        .. math::
            ^s\mathbf{W}_i = A\boldsymbol{\Phi}_i + B\boldsymbol{\Phi}_i^2 + C\mathbf{I}

        in which if :math:`\|\sigma_i\| \geq \text{eps}`:

        .. math::
            A = \left\{
                    \begin{array}{ll} 
                        \frac{s_i\sin\theta_i\sigma_i + (1-s_i\cos\theta_i)\theta_i}
                        {\theta_i(\sigma_i^2 + \theta_i^2)}, \quad \|\theta_i\| \geq \text{eps}, \\
                        \frac{(\sigma_i-1)s_i+1}{\sigma_i^2}, \quad \|\theta_i\| < \text{eps},
                    \end{array}
                \right.

        .. math::
            B = 
            \left\{
                \begin{array}{ll} 
                    \left( C - \frac{(s_i\cos\theta_i-1)\sigma+ s_i\sin\theta_i\sigma_i}
                    {\theta_i^2+\sigma_i^2}\right)\frac{1}{\theta_i^2}, \quad \|\theta_i\| \geq \text{eps}, \\
                    \frac{s_i\sigma_i^2/2 + s_i-1-\sigma_i s_i}{\sigma_i^3}, \quad \|\theta_i\| < \text{eps},
                \end{array}
            \right.

        .. math::
            C = \frac{e^{\sigma_i} - 1}{\sigma_i}\mathbf{I}

        otherwise:

        .. math::
            A = \left\{
                    \begin{array}{ll} 
                        \frac{1-\cos\theta_i}{\theta_i^2}, \quad \|\theta_i\| \geq \text{eps}, \\
                        \frac{1}{2}, \quad \|\theta_i\| < \text{eps},
                    \end{array}
                \right.

        .. math::
            B = \left\{
                    \begin{array}{ll} 
                        \frac{\theta_i - \sin\theta_i}{\theta_i^3}, \quad \|\theta_i\| \geq \text{eps}, \\
                        \frac{1}{6}, \quad \|\theta_i\| < \text{eps},
                    \end{array}
                \right.

        .. math::
            C = 1
    
    Note:
        The detailed explanation of the above :math:`\mathrm{Exp}`: calculation can be found in the paper:

        * Grassia, F. Sebastian., `Practical Parameterization of Rotations using the
          Exponential Map <https://www.tandfonline.com/doi/pdf/10.1080/10867651.1998.10487493>`_,
          Journal of graphics tools, 1998.

        Assume we have a unit rotation axis :math:`\mathbf{n}~(\|\mathbf{n}\|=1)` and rotation angle
        :math:`\theta~(0\leq\theta<2\pi)`, let :math:`\mathbf{x}=\theta\mathbf{n}`, then the corresponding
        quaternion with unit norm :math:`\mathbf{q}` can be represented as:

            .. math::
                \mathbf{q} = \left[\frac{\sin(\theta/2)}{\theta} \mathbf{x}, \cos(\theta/2) \right].

        Given :math:`\mathbf{x}=\theta\mathbf{n}`, to find its corresponding quaternion
        :math:`\mathbf{q}`, we first calculate the rotation angle :math:`\theta` using:

            .. math::
                \theta = \|\mathbf{x}\|.

        Then, the corresponding quaternion is:
        
            .. math::
                \mathbf{q} = \left[\frac{\sin(\|\mathbf{x}\|/2)}{\|\mathbf{x}\|} \mathbf{x}, \cos(\|\mathbf{x}\|/2) \right].

        If :math:`\|\mathbf{x}\|` is small (:math:`\|\mathbf{x}\|\le \text{eps}`),
        we use the Taylor Expansion form of :math:`\sin(\|\mathbf{x}\|/2)` and :math:`\cos(\|\mathbf{x}\|/2)`.

        More details about :math:`^s\mathbf{W}_i` in :obj:`sim3_type` can be found in Eq. (5.7):

        * H. Strasdat, `Local Accuracy and Global Consistency for Efficient Visual
          SLAM <http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.640.199&rep=rep1&type=pdf>`_,
          Dissertation. Department of Computing, Imperial College London, 2012.

    Example:
    
    * :math:`\mathrm{Exp}`: :meth:`so3` :math:`\mapsto` :meth:`SO3`

        >>> x = pp.randn_so3(2, requires_grad=True)
        so3Type LieTensor:
        tensor([[-0.2547, -0.4478,  0.0783],
                [ 0.7381,  0.2163, -1.8465]], requires_grad=True)
        >>> x.Exp() # equivalent to: pp.Exp(x)
        SO3Type LieTensor:
        tensor([[-0.1259, -0.2214,  0.0387,  0.9662],
                [ 0.3105,  0.0910, -0.7769,  0.5402]], grad_fn=<AliasBackward0>)

    * :math:`\mathrm{Exp}`: :meth:`se3` :math:`\mapsto` :meth:`SE3`

        >>> x = pp.randn_se3(2)
        se3Type LieTensor:
        tensor([[ 1.1912,  1.2425, -0.9696,  0.9540, -0.4061, -0.7204],
                [ 0.5964, -1.1894,  0.6451,  1.1373, -2.6733,  0.4142]])
        >>> x.Exp() # equivalent to: pp.Exp(x)
        SE3Type LieTensor:
        tensor([[ 1.6575,  0.8838, -0.1499,  0.4459, -0.1898, -0.3367,  0.8073],
                [ 0.2654, -1.3860,  0.2852,  0.3855, -0.9061,  0.1404,  0.1034]])

    * :math:`\mathrm{Exp}`: :meth:`rxso3` :math:`\mapsto` :meth:`RxSO3`

        >>> x = pp.randn_rxso3(2)
        rxso3Type LieTensor:
        tensor([[-1.2559, -0.9545,  0.2480, -0.3000],
                [ 1.0867,  0.4305, -0.4303,  0.1563]])
        >>> x.Exp() # equivalent to: pp.Exp(x)
        RxSO3Type LieTensor:
        tensor([[-0.5633, -0.4281,  0.1112,  0.6979,  0.7408],
                [ 0.5089,  0.2016, -0.2015,  0.8122,  1.1692]])

    * :math:`\mathrm{Exp}`: :meth:`sim3` :math:`\mapsto` :meth:`Sim3`

        >>> x = pp.randn_sim3(2)
        sim3Type LieTensor:
        tensor([[-1.2279,  0.0967, -1.1261,  1.2900,  0.2519, -0.7583,  0.8938],
                [ 0.4278, -0.4025, -1.3189, -1.7345, -0.9196,  0.3332,  0.1777]])
        >>> x.Exp() # equivalent to: pp.Exp(x)
        Sim3Type LieTensor:
        tensor([[-1.5811,  1.8128, -0.5835,  0.5849,  0.1142, -0.3438,  0.7257,  2.4443],
                [ 0.9574, -0.9265, -0.2385, -0.7309, -0.3875,  0.1404,  0.5440,  1.1945]])
    """
    return input.Exp()


@assert_ltype
def Log(input):
    r"""The Logarithm map for :obj:`LieTensor` (Lie Group).

    .. math::
        \mathrm{Log}: \mathcal{G} \mapsto \mathcal{g}

    Args:
        input (LieTensor): the input LieTensor (Lie Group)

    Return:
        LieTensor: the output LieTensor (Lie Algebra)

    .. list-table:: List of supported :math:`\mathrm{Log}` map
        :widths: 20 20 8 20 20
        :header-rows: 1

        * - input :obj:`ltype`
          - :math:`\mathcal{G}` (Lie Group)
          - :math:`\mapsto`
          - :math:`\mathcal{g}` (Lie Algebra)
          - output :obj:`ltype`
        * - :obj:`SO3_type`
          - :math:`\mathcal{G}\in\mathbb{R}^{*\times4}`
          - :math:`\mapsto`
          - :math:`\mathcal{g}\in\mathbb{R}^{*\times3}`
          - :obj:`so3_type`
        * - :obj:`SE3_type`
          - :math:`\mathcal{G}\in\mathbb{R}^{*\times7}`
          - :math:`\mapsto`
          - :math:`\mathcal{g}\in\mathbb{R}^{*\times6}`
          - :obj:`se3_type`
        * - :obj:`Sim3_type`
          - :math:`\mathcal{G}\in\mathbb{R}^{*\times8}`
          - :math:`\mapsto`
          - :math:`\mathcal{g}\in\mathbb{R}^{*\times7}`
          - :obj:`sim3_type`
        * - :obj:`RxSO3_type`
          - :math:`\mathcal{G}\in\mathbb{R}^{*\times5}`
          - :math:`\mapsto`
          - :math:`\mathcal{g}\in\mathbb{R}^{*\times4}`
          - :obj:`rxso3_type`
    
    Warning:
        This function :func:`Log()` is different from :func:`log()`, which returns
        a new torch tensor with the logarithm of the elements of the input tensor.

    * If input :math:`\mathbf{x}`'s :obj:`ltype` is :obj:`SO3_type`
      (input :math:`\mathbf{x}` is an instance of :meth:`SO3`):

        Let :math:`w_i`, :math:`\boldsymbol{\nu}_i` be the scalar and vector parts of
        :math:`\mathbf{x}_i`, respectively; :math:`\mathbf{y}` be the output.

        If :math:`\|\boldsymbol{\nu}_i\| > \text{eps}`:

            .. math::
                \mathbf{y}_i = 
                    \left\{
                        \begin{array}{ll} 
                            2\frac{\mathrm{arctan}(\|\boldsymbol{\nu}_i\|/w_i)}{\|
                            \boldsymbol{\nu}_i\|}\boldsymbol{\nu}_i, \quad \|w_i\| > \text{eps}, \\
                            \mathrm{sign}(w_i) \frac{\pi}{\|\boldsymbol{\nu}_i\|}\boldsymbol{\nu}_i,
                            \quad \|w_i\| \leq \text{eps},
                        \end{array}
                    \right.

        otherwise:

        .. math::
            \mathbf{y}_i = 2\left( \frac{1}{w_i} - \frac{\|\boldsymbol{\nu}_i\|^2}{3w_i^3}\right)\boldsymbol{\nu}_i.

    * If input :math:`\mathbf{x}`'s :obj:`ltype` is :obj:`SE3_type`
      (input :math:`\mathbf{x}` is an instance of :meth:`SE3`):

        Let :math:`\mathbf{t}_i`, :math:`\mathbf{q}_i` be the translation and rotation parts of
        :math:`\mathbf{x}_i`, respectively; :math:`\mathbf{y}` be the output.

        .. math::
            \mathbf{y}_i = \left[\mathbf{J}_i^{-1}\mathbf{t}_i, \mathrm{Log}(\mathbf{q}_i) \right],

        where :math:`\mathrm{Log}` is the Logarithm map for :obj:`SO3_type` input and
        :math:`\mathbf{J}_i` is the left Jacobian for :obj:`SO3_type` input.

    * If input :math:`\mathbf{x}`'s :obj:`ltype` is :obj:`RxSO3_type`
      (input :math:`\mathbf{x}` is an instance of :meth:`RxSO3`):

        Let :math:`\mathbf{q}_i`, :math:`s_i` be the rotation and scale parts of :math:`\mathbf{x}_i`, respectively;
        :math:`\mathbf{y}` be the output.

        .. math::
            \mathbf{y}_i = \left[\mathrm{Log}(\mathbf{q}_i), \log(s_i) \right].

    * If input :math:`\mathbf{x}`'s :obj:`ltype` is :obj:`Sim3_type` (input :math:`\mathbf{x}`
      is an instance of :meth:`Sim3`):

        Let :math:`\mathbf{t}_i`, :math:`^s\mathbf{q}_i` be the translation and :obj:`RxSO3` parts
        of :math:`\mathbf{x}_i`, respectively; :math:`\boldsymbol{\phi}_i`, :math:`\sigma_i` be the
        corresponding Lie Algebra of the SO3 and scale part of :math:`^s\mathbf{q}_i`,
        :math:`\boldsymbol{\Phi}_i = \theta_i\mathbf{n}_i` be the skew matrix;
        :math:`s_i = e^\sigma_i`, :math:`\mathbf{y}` be the output.

        .. math::
            \mathbf{y}_i = \left[^s\mathbf{W}_i^{-1}\mathbf{t}_i, \mathrm{Log}(^s\mathbf{q}_i) \right],

        where

            .. math::
               ^s\mathbf{W}_i = A\boldsymbol{\Phi}_i + B\boldsymbol{\Phi}_i^2 + C\mathbf{I}

        in which if :math:`\|\sigma_i\| > \text{eps}`:

        .. math::
            A = \left\{
                    \begin{array}{ll} 
                        \frac{s_i\sin\theta_i\sigma_i + (1-s_i\cos\theta_i)\theta_i}
                        {\theta_i(\sigma_i^2 + \theta_i^2)}, \quad \|\theta_i\| > \text{eps}, \\
                        \frac{(\sigma_i-1)s_i+1}{\sigma_i^2}, \quad \|\theta_i\| \leq \text{eps},
                    \end{array}
                \right.

        .. math::
            B = 
            \left\{
                \begin{array}{ll} 
                    \left( C - \frac{(s_i\cos\theta_i-1)\sigma+ s_i\sin\theta_i\sigma_i}
                    {\theta_i^2+\sigma_i^2}\right)\frac{1}{\theta_i^2}, \quad \|\theta_i\| > \text{eps}, \\
                    \frac{s_i\sigma_i^2/2 + s_i-1-\sigma_i s_i}{\sigma_i^3}, \quad \|\theta_i\| \leq \text{eps},
                \end{array}
            \right.

        .. math::
            C = \frac{e^{\sigma_i} - 1}{\sigma_i}\mathbf{I}

        otherwise:

        .. math::
            A = \left\{
                    \begin{array}{ll} 
                        \frac{1-\cos\theta_i}{\theta_i^2}, \quad \|\theta_i\| > \text{eps}, \\
                        \frac{1}{2}, \quad \|\theta_i\| \leq \text{eps},
                    \end{array}
                \right.

        .. math::
            B = \left\{
                    \begin{array}{ll} 
                        \frac{\theta_i - \sin\theta_i}{\theta_i^3}, \quad \|\theta_i\| > \text{eps}, \\
                        \frac{1}{6}, \quad \|\theta_i\| \leq \text{eps},
                    \end{array}
                \right.

        .. math::
            C = 1

    Note:
        The :math:`\mathrm{arctan}`-based Logarithm map implementation thanks to the paper:

        * C. Hertzberg et al., `Integrating Generic Sensor Fusion Algorithms with Sound State
          Representation through Encapsulation of Manifolds <https://doi.org/10.1016/j.inffus.2011.08.003>`_,
          Information Fusion, 2013.

        Assume we have a unit rotation axis :math:`\mathbf{n}` and rotation angle
        :math:`\theta~(0\leq\theta<2\pi)`, then the corresponding quaternion with
        unit norm :math:`\mathbf{q}` can be represented as

            .. math::
                \mathbf{q} = \left[\sin(\theta/2) \mathbf{n}, \cos(\theta/2) \right]

        Therefore, given a quaternion :math:`\mathbf{q}=[\boldsymbol{\nu}, w]`, where :math:`\boldsymbol{\nu}`
        is the vector part, :math:`w` is the scalar part, to find the corresponding rotation vector ,
        the rotation angle :math:`\theta` can be obtained as 

            .. math::
                \theta = 2\mathrm{arctan}(\|\boldsymbol{\nu}\|/w),~\|\boldsymbol{\nu}\| = \sin(\theta/2), 

        The unit rotation axis :math:`\mathbf{n}` can be obtained as :math:`\mathbf{n} =
        \frac{\boldsymbol{\nu}}{{\|\boldsymbol{\nu}\|}}`. Hence, the corresponding rotation vector is 

            .. math::
                \theta \mathbf{n} = 2\frac{\mathrm{arctan}
                (\|\boldsymbol{\nu}\|/w)}{\|\boldsymbol{\nu}\|}\boldsymbol{\nu}.

        More details about :math:`^s\mathbf{W}_i` in :obj:`Sim3_type` can be found in Eq. (5.7):

        * H. Strasdat, `Local accuracy and global consistency for efficient visual SLAM
          <http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.640.199&rep=rep1&type=pdf>`_, 
          Dissertation. Department of Computing, Imperial College London, 2012.

    Example:

        * :math:`\mathrm{Log}`: :obj:`SO3` :math:`\mapsto` :obj:`so3`

        >>> x = pp.randn_SO3(2)
        >>> x.Log() # equivalent to: pp.Log(x)
        so3Type LieTensor:
        tensor([[-0.3060,  0.2344,  1.2724],
                [ 0.3012, -0.6817,  0.1187]])

        * :math:`\mathrm{Log}`: :obj:`SE3` :math:`\mapsto` :obj:`se3`

        >>> x = pp.randn_SE3(2)
        >>> x.Log() # equivalent to: pp.Log(x)
        se3Type LieTensor:
        tensor([[ 0.2958, -0.0840, -1.4733,  0.7004,  0.4483, -0.9009],
                [ 0.0850, -0.1020, -1.2616, -1.0524, -1.2031,  0.8377]])


        * :math:`\mathrm{Log}`: :obj:`RxSO3` :math:`\mapsto` :obj:`rxso3`

        >>> x = pp.randn_RxSO3(2)
        >>> x.Log() # equivalent to: pp.Log(x)
        rxso3Type LieTensor:
        tensor([[-1.3755,  0.3525, -2.2367,  0.5409],
                [ 0.5929, -0.3250, -0.7394,  1.0965]])

        * :math:`\mathrm{Log}`: :obj:`Sim3` :math:`\mapsto` :obj:`sim3`

        >>> x = pp.randn_Sim3(2)
        >>> x.Log() # equivalent to: pp.Log(x)
        sim3Type LieTensor:
        tensor([[-0.1747, -0.3698,  0.2000,  0.1735,  0.6220,  1.1852, -0.6402],
                [-0.8685, -0.1717,  1.2139, -0.8385, -2.2957, -1.9545,  0.8474]])
    """
    return input.Log()


@assert_ltype
def Inv(x):
    return x.Inv()


@assert_ltype
def Mul(x, y):
    return x * y


@assert_ltype
def Retr(X, a):
    return X.Retr(a)


@assert_ltype
def Act(X, p):
    return X.Act(p)


@assert_ltype
def Adj(X, a):
    return X.Adj(a)


@assert_ltype
def AdjT(X, a):
    return X.AdjT(a)


@assert_ltype
def Jinvp(input, p):
    r"""
    The dot product between left Jacobian inverse at the point given
    by input (Lie Group) and second point (Lie Algebra).

    .. math::
        \mathrm{Jinvp}: (\mathcal{G}, \mathcal{g}) \mapsto \mathcal{g}

    Args:
        input (LieTensor): the input LieTensor (Lie Group)
        p (LieTensor): the second LieTensor (Lie Algebra)

    Return:
        LieTensor: the output LieTensor (Lie Algebra)

    .. list-table:: List of supported :math:`\mathrm{Jinvp}` map
        :widths: 20 20 8 20 20
        :header-rows: 1

        * - input :obj:`ltype`
          - :math:`(\mathcal{G}, \mathcal{g})` (Lie Group, Lie Algebra)
          - :math:`\mapsto`
          - :math:`\mathcal{g}` (Lie Algebra)
          - output :obj:`ltype`
        * - (:obj:`SO3_type`, :obj:`so3_type`)
          - :math:`(\mathcal{G}\in\mathbb{R}^{*\times4}, \mathcal{g}\in\mathbb{R}^{*\times3})`
          - :math:`\mapsto`
          - :math:`\mathcal{g}\in\mathbb{R}^{*\times3}`
          - :obj:`so3_type`
        * - (:obj:`SE3_type`, :obj:`se3_type`)
          - :math:`(\mathcal{G}\in\mathbb{R}^{*\times7}, \mathcal{g}\in\mathbb{R}^{*\times6})`
          - :math:`\mapsto`
          - :math:`\mathcal{g}\in\mathbb{R}^{*\times6}`
          - :obj:`se3_type`
        * - (:obj:`Sim3_type`, :obj:`sim3_type`)
          - :math:`(\mathcal{G}\in\mathbb{R}^{*\times8}, \mathcal{g}\in\mathbb{R}^{*\times7})`
          - :math:`\mapsto`
          - :math:`\mathcal{g}\in\mathbb{R}^{*\times7}`
          - :obj:`sim3_type`
        * - (:obj:`RxSO3_type`, :obj:`rxso3_type`)
          - :math:`(\mathcal{G}\in\mathbb{R}^{*\times5}, \mathcal{g}\in\mathbb{R}^{*\times4})`
          - :math:`\mapsto`
          - :math:`\mathcal{g}\in\mathbb{R}^{*\times4}`
          - :obj:`rxso3_type`

    Let the input be (:math:`\mathbf{x}`, :math:`\mathbf{p}`), :math:`\mathbf{y}` be the output.

        .. math::
            \mathbf{y}_i = \mathbf{J}^{-1}_i(\mathbf{x}_i)\mathbf{p}_i,

        where :math:`\mathbf{J}^{-1}_i(\mathbf{x}_i)` is the inverse of left Jacobian of :math:`\mathbf{x}_i`. 

    * If input (:math:`\mathbf{x}`, :math:`\mathbf{p}`)'s :obj:`ltype` are :obj:`SO3_type` and :obj:`so3_type`
      (input :math:`\mathbf{x}` is an instance of :meth:`SO3`, :math:`\mathbf{p}` is an instance of :meth:`so3`).
      Let :math:`\boldsymbol{\phi}_i = \theta_i\mathbf{n}_i` be the corresponding Lie Algebra of :math:`\mathbf{x}_i`, 
      :math:`\boldsymbol{\Phi}_i` be the skew matrix (:meth:`pypose.vec2skew`) of :math:`\boldsymbol{\phi}_i`:

        .. math::
            \mathbf{J}^{-1}_i(\mathbf{x}_i) = \mathbf{I} - \frac{1}{2}\boldsymbol{\Phi}_i +
            \mathrm{coef}\boldsymbol{\Phi}_i^2

      where :math:`\mathbf{I}` is the identity matrix with the same dimension as :math:`\boldsymbol{\Phi}_i`, and 

        .. math::
            \mathrm{coef} = \left\{
                                \begin{array}{ll} 
                                    \frac{1}{\theta_i^2} - \frac{\cos{\frac{\theta_i}{2}}}{2\theta\sin{\frac{\theta_i}{2}}},
                                    \quad \|\theta_i\| > \text{eps}, \\
                                    \frac{1}{12},
                                    \quad \|\theta_i\| \leq \text{eps}
                                \end{array}
                             \right.

    * If input (:math:`\mathbf{x}`, :math:`\mathbf{p}`)'s :obj:`ltype` are :obj:`SE3_type` and :obj:`se3_type`
      (input :math:`\mathbf{x}` is an instance of :meth:`SE3`, :math:`\mathbf{p}` is an instance of :meth:`se3`).
      Let :math:`\boldsymbol{\phi}_i = \theta_i\mathbf{n}_i` be the corresponding Lie Algebra of the SO3 part of 
      :math:`\mathbf{x}_i`, :math:`\boldsymbol{\tau}_i` be the Lie Algebra of the translation part of :math:`\mathbf{x}_i`; 
      :math:`\boldsymbol{\Phi}_i` and :math:`\boldsymbol{\Tau}_i` be the skew matrices, respectively:

        .. math::
            \mathbf{J}^{-1}_i(\mathbf{x}_i) = \left[
                                \begin{array}{cc} 
                                    \mathbf{J}_i^{-1}(\boldsymbol{\Phi}_i) & -\mathbf{J}_i^{-1}(\boldsymbol{\Phi}_i)
                                    \mathbf{Q}_i(\boldsymbol{\tau}_i, \boldsymbol{\phi}_i)\mathbf{J}_i^{-1}(\boldsymbol{\Phi}_i) \\
                                    \mathbf{0} & \mathbf{J}_i^{-1}(\boldsymbol{\Phi}_i)
                                \end{array}
                             \right]

        where :math:`\mathbf{J}_i^{-1}(\boldsymbol{\Phi}_i)` is the inverse of left Jacobian of the SO3 part of :math:`\mathbf{x}_i`.
        :math:`\mathbf{Q}_i(\boldsymbol{\tau}_i, \boldsymbol{\phi}_i)` is 

        .. math::
            \begin{align*}
                \mathbf{Q}_i(\boldsymbol{\tau}_i, \boldsymbol{\phi}_i) = \frac{1}{2}\boldsymbol{\Tau}_i &+ c_1
                (\boldsymbol{\Phi_i\Tau_i} + \boldsymbol{\Tau_i\Phi_i} + \boldsymbol{\Phi_i\Tau_i\Phi_i}) \\
                 &+ c_2 (\boldsymbol{\Phi_i^2\Tau_i} + \boldsymbol{\Tau_i\Phi_i^2} - 3\boldsymbol{\Phi_i\Tau_i\Phi_i})\\
                 &+ c_3 (\boldsymbol{\Phi_i\Tau_i\Phi_i^2} + \boldsymbol{\Phi_i^2\Tau_i\Phi_i})  
            \end{align*}

        where,

        .. math::
            c_1 = \left\{
                    \begin{array}{ll} 
                        \frac{\theta_i - \sin\theta_i}{\theta_i^3}, \quad \|\theta_i\| > \text{eps}, \\
                        \frac{1}{6}-\frac{1}{120}\theta_i^2,
                        \quad \|\theta_i\| \leq \text{eps}
                    \end{array}
                    \right.

        .. math::
            c_2 = \left\{
                    \begin{array}{ll} 
                        \frac{\theta_i^2 +2\cos\theta_i - 2}{2\theta_i^4}, \quad \|\theta_i\| > \text{eps}, \\
                        \frac{1}{24}-\frac{1}{720}\theta_i^2,
                        \quad \|\theta_i\| \leq \text{eps}
                    \end{array}
                    \right.

        .. math::
            c_3 = \left\{
                    \begin{array}{ll} 
                        \frac{2\theta_i - 3\sin\theta_i + \theta_i\cos\theta_i}{2\theta_i^5}, 
                        \quad \|\theta_i\| > \text{eps}, \\
                        \frac{1}{120}-\frac{1}{2520}\theta_i^2,
                        \quad \|\theta_i\| \leq \text{eps}
                    \end{array}
                    \right.           

    * If input (:math:`\mathbf{x}`, :math:`\mathbf{p}`)'s :obj:`ltype` are :obj:`Sim3_type` and :obj:`sim3_type`
      (input :math:`\mathbf{x}` is an instance of :meth:`Sim3`, :math:`\mathbf{p}` is an instance of :meth:`sim3`).
      The inverse of left Jacobian can be approximated as:

        .. math::
            \mathbf{J}^{-1}_i(\mathbf{x}_i) = \sum_{n=0}(-1)^n\frac{B_n}{n!}(\boldsymbol{\xi}_i^{\curlywedge})^n

        where :math:`B_n` is the Bernoulli number: :math:`B_0 = 1`, :math:`B_1 = -\frac{1}{2}`,
        :math:`B_2 = \frac{1}{6}`, :math:`B_3 = 0`, :math:`B_4 = -\frac{1}{30}`.
        :math:`\boldsymbol{\xi}_i^{\curlywedge} = \mathrm{adj}(\boldsymbol{\xi}_i^{\wedge})` and :math:`\mathrm{adj}` 
        is the adjoint of the Lie algebra :math:`\mathfrak{sim}(3)`, e.g., :math:`\boldsymbol{\xi}_i \in \mathfrak{sim}(3)`.
        Notice that if notate :math:`\boldsymbol{X}_i = \mathrm{Adj}(\mathbf{x}_i)` and :math:`\mathrm{Adj}` 
        is the adjoint of the Lie group :math:`\mathrm{Sim}(3)`, there is a nice property:
        :math:`\mathrm{Adj}(\mathrm{Exp}(\boldsymbol{\xi}_i^{\curlywedge})) = \mathrm{Exp}(\mathrm{adj}(\boldsymbol{\xi}_i^{\wedge}))`, 
        or :math:`\boldsymbol{X}_i = \mathrm{Exp}(\boldsymbol{\xi}_i^{\curlywedge})`.
        

    * If input (:math:`\mathbf{x}`, :math:`\mathbf{p}`)'s :obj:`ltype` are :obj:`RxSO3_type` and :obj:`rxso3_type`
      (input :math:`\mathbf{x}` is an instance of :meth:`RxSO3`, :math:`\mathbf{p}` is an instance of :meth:`rxso3`).
      Let :math:`\boldsymbol{\phi}_i` be the corresponding Lie Algebra of the SO3 part of
      :math:`\mathbf{x}_i`, :math:`\boldsymbol{\Phi}_i` be the skew matrix (:meth:`pypose.vec2skew`),
      The inverse of left Jacobian of :math:`\mathbf{x}_i` is the same as that for the SO3 part of :math:`\mathbf{x}_i`.

        .. math::
            \mathbf{J}^{-1}_i(\mathbf{x}_i) = \left[
                                \begin{array}{cc} 
                                    \mathbf{J}_i^{-1}(\boldsymbol{\Phi}_i) & \mathbf{0} \\
                                    \mathbf{0} & 1
                                \end{array}
                             \right]

        where :math:`\mathbf{J}_i^{-1}(\boldsymbol{\Phi}_i)` is the
        inverse of left Jacobian of the SO3 part of :math:`\mathbf{x}_i`.

    Note:
        :math:`\mathrm{Jinvp}` is usually used in the Baker-Campbell-Hausdorff formula
        (BCH formula) when performing LieTensor multiplication.
        One can refer to this paper for more details:

        * J. Sola et al., `A micro Lie theory for state estimation in
          robotics <https://arxiv.org/abs/1812.01537>`_, arXiv preprint arXiv:1812.01537 (2018).

        In particular, Eq. (146) is the math used in the :obj:`SO3_type`, :obj:`so3_type` scenario; 
        Eq. (179b) and Eq. (180) are the math used in the :obj:`SE3_type`, :obj:`se3_type` scenario.

        For Lie groups such as :obj:`Sim3_type`, :obj:`sim3_type`,
        there is no analytic expression for the left Jacobian and its inverse. 
        Numerical approximation is used based on series expansion.
        One can refer to Eq. (26) of this paper for more details about the approximation:

        * Z. Teed et al., `Tangent Space Backpropagation for 3D Transformation Groups.
          <https://arxiv.org/pdf/2103.12032.pdf>`_, in IEEE/CVF Conference on Computer Vision and
          Pattern Recognition (CVPR) (2021).

        In particular, the Bernoulli numbers can be obtained from Eq. (7.72) of this famous book:

        * T. Barfoot, `State Estimation for Robotics.
          <https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.708.1086&rep=rep1&type=pdf>`_,
          Cambridge University Press (2017).

    Example:

        * :math:`\mathrm{Jinvp}`: (:obj:`SO3`, :obj:`so3`) :math:`\mapsto` :obj:`so3`

        >>> x = pp.randn_SO3(2)
        >>> a = pp.randn_so3(2)
        >>> x.Jinvp(a) # equivalent to: pp.Jinvp(x, a)
            tensor([[-0.1068,  1.6051, -2.0121],
                    [-0.6726, -0.0345,  0.2493]])

        * :math:`\mathrm{Jinvp}`: (:obj:`SE3`, :obj:`se3`) :math:`\mapsto` :obj:`se3`

        >>> x = pp.randn_SE3(2)
        >>> a = pp.randn_se3(2)
        >>> x.Jinvp(a) # equivalent to: pp.Jinvp(x, a)
            tensor([[-1.3803,  0.7891, -0.4268,  0.6917, -0.2167,  0.3333],
                    [-1.4517, -0.8059,  0.9343,  1.7398,  0.6579,  0.4785]])

        * :math:`\mathrm{Jinvp}`: (:obj:`Sim3`, :obj:`sim3`) :math:`\mapsto` :obj:`sim3`

        >>> x = pp.randn_Sim3(2)
        >>> a = pp.randn_sim3(2)
        >>> x.Jinvp(a) # equivalent to: pp.Jinvp(x, a)
            tensor([[ 0.3943, -1.2546,  0.3209,  0.2298, -1.1028, -1.4039,  0.3704],
                    [-0.3591,  0.4190,  0.2833, -0.3121,  1.6293, -0.8617, -0.7911]])

        * :math:`\mathrm{Jinvp}`: (:obj:`RxSO3`, :obj:`rxso3`) :math:`\mapsto` :obj:`rxso3`

        >>> x = pp.randn_RxSO3(2)
        >>> a = pp.randn_rxso3(2)
        >>> x.Jinvp(a) # equivalent to: pp.Jinvp(x, a)
            tensor([[ 0.1730, -1.3778,  0.1657,  0.1820],
                    [-1.0347,  1.6627,  0.3992,  0.1227]])
    """
    return input.Jinvp(p)


@assert_ltype
def Jr(x):
    return x.Jr()
