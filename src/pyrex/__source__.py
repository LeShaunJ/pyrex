#!/usr/bin/env python3
"""Simple `xterm` color usage & management.

```python
from pyhues import *
```
```python
from pyhues import (
  Red,   Orange,    Yellow,  Lime,
  Green, Turquoise, Teal,    Cyan,
  Blue,  Purple,    Magenta, Rose,
  Grey,  White,     Black
)
```

Every color is grouped into one of twelves tones within the color wheel. A `Hue` represents a tone and every possible brightness/saturation variations (_aka `Color`_) it provides. By itself, a `Hue` can be used with `f-strings` to colorize text with its deepest features; or, with **brightness** and **saturation** specified for further customization.

All shades fall under `Grey`, and it works the same way, with the `Black` and `White` symbols serving as shortcuts to grey's most darkest/saturated and brightess/desaturated values, respectively.

Examples:
  Colorize strings with a hue's default features:
  >>> print(f'{Red:hello, world}')
  \033[38;5;196mhello, world\033[0m
  >>> print(f'{Orange:hello, world}')
  \033[38;5;202mhello, world\033[0m
  >>> print(f'{Yellow:hello, world}')
  \033[38;5;190mhello, world\033[0m
  >>> print(f'{Lime:hello, world}')
  \033[38;5;82mhello, world\033[0m
  >>> print(f'{Green:hello, world}')
  \033[38;5;46mhello, world\033[0m
  >>> print(f'{Turquoise:hello, world}')
  \033[38;5;47mhello, world\033[0m
  >>> print(f'{Teal:hello, world}')
  \033[38;5;45mhello, world\033[0m
  >>> print(f'{Cyan:hello, world}')
  \033[38;5;27mhello, world\033[0m
  >>> print(f'{Blue:hello, world}')
  \033[38;5;21mhello, world\033[0m
  >>> print(f'{Purple:hello, world}')
  \033[38;5;57mhello, world\033[0m
  >>> print(f'{Magenta:hello, world}')
  \033[38;5;165mhello, world\033[0m
  >>> print(f'{Rose:hello, world}')
  \033[38;5;197mhello, world\033[0m

  Specify the brigthness and saturation a hue:
  >>> print(f'{Red(2,7):hello, world}')
  \033[38;5;95mhello, world\033[0m
  >>> print(f'{Orange(1,7):hello, world}')
  \033[38;5;94mhello, world\033[0m
  >>> print(f'{Yellow(3,5):hello, world}')
  \033[38;5;144mhello, world\033[0m
  >>> print(f'{Lime(5,6):hello, world}')
  \033[38;5;155mhello, world\033[0m
  >>> print(f'{Green(3,5):hello, world}')
  \033[38;5;108mhello, world\033[0m
  >>> print(f'{Turquoise(1,9):hello, world}')
  \033[38;5;29mhello, world\033[0m
  >>> print(f'{Teal(1,9):hello, world}')
  \033[38;5;23mhello, world\033[0m
  >>> print(f'{Cyan(5,6):hello, world}')
  \033[38;5;75mhello, world\033[0m
  >>> print(f'{Blue(5,6):hello, world}')
  \033[38;5;99mhello, world\033[0m
  >>> print(f'{Purple(5,6,True):hello, world}')
  \033[48;5;135mhello, world\033[0m
  >>> print(f'{Magenta(5,6):hello, world}')
  \033[38;5;171mhello, world\033[0m
  >>> print(f'{Rose(5,6):hello, world}')
  \033[38;5;205mhello, world\033[0m

  Shade with greyscale:
  >>> print(f'{Grey:hello, world}')
  \033[38;5;249mhello, world\033[0m
  >>> print(f'{Grey(3,6):hello, world}')
  \033[38;5;244mhello, world\033[0m
  >>> print(f'{White:hello, world}')
  \033[38;5;231mhello, world\033[0m
  >>> print(f'{Black:hello, world}')
  \033[38;5;16mhello, world\033[0m

  Fill the background:
  >>> print(f'{Rose(bg=True):hello, world}')
  \033[48;5;197mhello, world\033[0m
"""
##########################################################################################################################################################
# IMPORTS

import sys as _sys, typing as _t
from functools import lru_cache
from .__meta__ import __title__

##########################################################################################################################################################
# GLOBALS

__version__ = '0.1.0'
__author__  = "Arian Johnson"
__contact__ = "arian.johnson@rcgtconsulting.com"

__all__ = [
  'Red',
  'Orange',
  'Yellow',
  'Lime',
  'Green',
  'Turquoise',
  'Teal',
  'Cyan',
  'Blue',
  'Purple',
  'Magenta',
  'Rose',
  'Grey',
  'White',
  'Black',
]

##########################################################################################################################################################
# TYPES

_T = _t.TypeVar('_T')

HueName  : _t.TypeAlias = _t.Literal['Red','Orange','Yellow','Lime','Green','Turquoise','Teal','Cyan','Blue','Purple','Magenta','Rose']
"""```python
  'Red'|'Orange'|'Yellow'|'Lime'|'Green'|'Turquoise'|'Teal'|'Cyan'|'Blue'|'Purple'|'Magenta'|'Rose'
  ```
  A valid name of a hue.
"""
HueLevel : _t.TypeAlias = _t.Literal[0, 1, 2, 3, 4, 5]
"""```python
  0|1|2|3|4|5
  ```
  An amount of color a hue can have.
"""
SatLevel : _t.TypeAlias = _t.Literal[1, 2, 3, 4, 5, 6, 7, 8, 9]
"""```python
  1|2|3|4|5|6|7|8|9
  ```
  An amount of saturation a hue can have.
"""

class _LVL:
  min: _t.ClassVar[_t.Literal[1]] = 1
  max: _t.ClassVar[_t.Literal[5]] = 5

class _SAT:
  min: _t.ClassVar[_t.Literal[1]] = 1
  max: _t.ClassVar[_t.Literal[9]] = 9

class Bit8(int):
  """A type-guard for an 8-bit number value between `0` and `255`.

    Examples:
    >>> Bit8(128)
    128
    >>> ~Bit8(4)
    251
  """

  __slots__ = ()

  _: _t.ClassVar[int] = 255

  def __new__(cls, value: str | int):
    """
      Args:
        value (str | int): A valid 8-bit number between `0` and `255`.

      Raises:
        ValueError: If `num` is not between `0` and `255`.
        ValueError: If `num` is not convertible to `int`.
    """
    try:
      if isinstance(value, cls):
        return value
      value = int(value)
      assert value >= 0 and value <= 255
      return super().__new__(cls, value)
    except AssertionError:
      raise ValueError('Bit8 value must be between 0-255')
    except:
      raise ValueError(f'Bit8 value must be convertible to int (got {repr(value)})')

  @lru_cache
  def __invert__(self) -> int:
    return Bit8(self._ - int(self))

  @lru_cache
  def __add__(self, other: int):
    result = int(super().__add__(other))
    return Bit8(self._ if result > self._ else result)

  @lru_cache
  def __radd__(self, other: int):
    return self.__add__(other)

  @lru_cache
  def __sub__(self, other: int):
    result = int(super().__sub__(other))
    return Bit8(0 if result < 0 else result)

  @lru_cache
  def __rsub__(self, other: int):
    return self.__sub__(other)

  @lru_cache
  def __mul__(self, other: int):
    result = int(super().__mul__(other))
    return Bit8(self._ if result > self._ else result)

  @lru_cache
  def __rmul__(self, other: int):
    return self.__mul__(other)

  @lru_cache
  def __truediv__(self, other: int):
    result = int(super().__truediv__(other))
    return Bit8(0 if result < 0 else result)

  @lru_cache
  def __rtruediv__(self, other: int):
    return self.__truediv__(other)

class DegUnit(int):
  """A type-guard representing degrees (`°`) from `0` and `360`.

    Examples:
      >>> DegUnit(270)
      270
      >>> str(DegUnit(270))
      '270°'
  """

  __slots__ = ()

  _: _t.ClassVar[int] = 360

  @lru_cache
  def __new__(cls, value: str | int = 0):
    """
      Args:
        value (str | int): A valid 8-bit number between `0` and `360`.

      Raises:
        ValueError: If `num` is not between `0` and `360`.
        ValueError: If `num` is not convertible to `int`.
    """
    try:
      value = int(value)
      assert value >= 0 and value <= 360
      return super().__new__(cls, value)
    except AssertionError:
      raise ValueError('Degree value must be between 0-360')
    except:
      raise ValueError('Degree value must be convertible to int')

  @lru_cache
  def __str__(self) -> str:
    return f'{repr(self)}°'

  @lru_cache
  def __add__(self, other: int):
    result = super().__add__(other)
    return result % self._ if result > self._ else result

  @lru_cache
  def __radd__(self, other: int):
    return self.__add__(other)

  @lru_cache
  def __sub__(self, other: int):
    result = super().__sub__(other)
    return result % self._ if result < 0 else result

  @lru_cache
  def __rsub__(self, other: int):
    return self.__sub__(other)

class Percent(float):
  """Represents the fractional value of a percentage, yielding it's percentile value when inverted.

    Examples:
      >>> Percent(0.75)
      0.75
      >>> ~Percent(0.2594)
      25.94
      >>> str(Percent(0.681))
      '68.1%'
  """

  __slots__ = ()

  @lru_cache
  def __new__(cls, value: str | int | float):
    """
      Args:
        value (str | int | float): A percentage.

      Raises:
        ValueError: If `num` is not convertible to `float`.
    """
    try:
      value = float(value)
      assert value >= 0 and value <= 1
      return super().__new__(cls, value)
    except AssertionError:
      raise ValueError('Percent value must be between 0 and 1')
    except ValueError:
      raise ValueError('Percent value must be convertible to float')

  @lru_cache
  def __invert__(self) -> float:
    return self * 100.0

  @lru_cache
  def __str__(self) -> str:
    return f'{~self:.1F}%'

class Color:
  """Repesents a color and its specific features.

    Examples:
      Pick a color using its ANSI code:
      >>> clr = Color(196)

      Format text using the color:
      >>> print(f'{clr:hello, world}')
      \033[38;5;196mhello, world\033[0m

      Set the color as a background:
      >>> clr.Background = True
      >>> print(f'{clr:hello, world}')
      \033[48;5;196mhello, world\033[0m
      >>> clr.Background = False

      Shift the color to the next hue in the color wheel:
      >>> clr >>= 1
      >>> print(f'{clr:hello, world}')
      \033[38;5;202mhello, world\033[0m

      Shift the color two hues back in the color wheel:
      >>> clr <<= 2
      >>> print(f'{clr:hello, world}')
      \033[38;5;197mhello, world\033[0m

      Darken the color by 3 (_out of 5_) levels:
      >>> clr -= 3
      >>> print(f'{clr:hello, world}')
      \033[38;5;89mhello, world\033[0m

      Brighten the color by 2 (_out of 5_) levels:
      >>> clr += 2
      >>> print(f'{clr:hello, world}')
      \033[38;5;161mhello, world\033[0m

      Desaturate the color by 4 (_out of 9_) levels:
      >>> clr /= 4
      >>> print(f'{clr:hello, world}')
      \033[38;5;175mhello, world\033[0m

      Saturate the color by 2 (_out of 9_) levels:
      >>> clr *= 2
      >>> print(f'{clr:hello, world}')
      \033[38;5;168mhello, world\033[0m
  """

  class RGBModel(tuple[Bit8, Bit8, Bit8]):
    """Represents an RGB color model.
    """

    __slots__ = ()

    @property
    @lru_cache
    def R(self) -> Bit8:
      """The the amount of red (`0-255`) in the color."""
      return self[0]

    @property
    @lru_cache
    def G(self) -> Bit8:
      """The the amount of green (`0-255`) in the color."""
      return self[1]

    @property
    @lru_cache
    def B(self) -> Bit8:
      """The the amount of blue (`0-255`) in the color."""
      return self[2]

    def __new__(cls, R: Bit8 = 0, G: Bit8 = 0, B: Bit8 = 0):
      """
        Args:
          R (Bit8, optional): The the amount of red (`0-255`) in the color.. Defaults to 0.
          G (Bit8, optional): The the amount of green (`0-255`) in the color.. Defaults to 0.
          B (Bit8, optional): The the amount of blue (`0-255`) in the color.. Defaults to 0.
      """
      return super().__new__(cls, (Bit8(R), Bit8(G), Bit8(B)))

    def __getnewargs__(self) -> _t.Tuple[Bit8, Bit8, Bit8]:
      return self

    def __str__(self) -> str:
      R, G, B = self
      return f'rgb({R:>3}, {G:>3}, {B:>3})'

    def __hash__(self):
      R, G, B = self
      return hash((
        ('R',R), ('G',G), ('B',B)
      ))

  class HSVModel(tuple[Bit8, Bit8, Bit8]):
    """Represents an HSV color model.
    """

    __slots__ = ()

    @property
    @lru_cache
    def H(self) -> DegUnit:
      """The point in which the color's hue falls on the color wheel (`0°-360°`)."""
      return self[0]

    @property
    @lru_cache
    def S(self) -> Percent:
      """The percentage of saturation (intensity/vividness) the color has."""
      return self[1]

    @property
    @lru_cache
    def V(self) -> Bit8:
      """The maximum brightness (`0-255`) the color has."""
      return self[2]

    def __new__(cls, H: DegUnit = 0, S: Percent = 0, V: Bit8 = 0):
      """
        Args:
          H (DegUnit, optional): The point in which the color's hue falls on the color wheel (`0°-360°`).. Defaults to 0.
          S (Percent, optional): The percentage of saturation (intensity/vividness) the color has.. Defaults to 0.
          V (Bit8, optional): The maximum brightness (`0-255`) the color has.. Defaults to 0.
      """
      return super().__new__(cls, (DegUnit(H), Percent(S), Bit8(V)))

    def __getnewargs__(self) -> _t.Tuple[DegUnit, Percent, Bit8]:
      return self

    def __str__(self) -> str:
      H, S, V = self
      return f'hsv({str(H):>4}, {str(S):>4}, {V:>3})'

    def __hash__(self):
      H, S, V = self
      return hash((
        ('H',H), ('S',S), ('V',V)
      ))

  #################################################

  @property
  def ANSI(self) -> Bit8:
    """The ANSI code (`0-255`) the color corresponds tp."""
    return self._ansi

  @property
  def RGB(self) -> RGBModel:
    """The red-green-blue values as a `tuple`."""
    return self._rgb

  @property
  def HSV(self) -> HSVModel:
    """The hue-saturation-brightness values as a `tuple`."""
    return self._hsv

  @property
  def Hue(self) -> str:
    """The name of the hue the color belongs to."""
    return _NAMES[self.HSV.H]

  @property
  def Background(self) -> bool:
    """Marks the color for background coloring purposes."""
    return getattr(self,'_bg')
  @Background.setter
  def Background(self, value: bool):
    setattr(self, '_bg', bool(value))

  #################################################

  # def __new__(cls, *args, **_):
  #   if args and isinstance(args[0], cls):
  #     return args[0]
  #   return super().__new__(cls)

  @_t.overload
  def __init__(self, ansi: Bit8):
    """Create a `Color` instance from its correspnding ANSI code.

      Args:
        ansi (int): A valid ASNI color code.
    """
  @_t.overload
  def __init__(self, color: 'Color'):
    """Duplicate a `Color` instance from an existing `Color`.

      Args:
        ansi (Color): An existing `Color` instance.
    """
  def __init__(self, value):
    # ...
    if isinstance(value, self.__class__):
      setattr(self, '_ansi', value.ANSI)
      setattr(self,  '_rgb', value.RGB)
      setattr(self,  '_hsv', value.HSV)
      setattr(self,   '_bg', value.Background)
      return
    # ...
    r,g,b = 0, 0, 0
    ansi  = Bit8(value)
    # ...
    if ansi < 0 or ansi > 255:
      raise ValueError(f"ANSI value is invalid; must be 0-255. Got {ansi}")
    # ...
    elif ansi < 16:
      r,g,b = [
        (  0,   0,   0),
        (128,   0,   0),
        (  0, 128,   0),
        (128, 128,   0),
        (  0,   0, 128),
        (128,   0, 128),
        (  0, 128, 128),
        (192, 192, 192),
        (128, 128, 128),
        (255,   0,   0),
        (  0, 255,   0),
        (255, 255,   0),
        (  0,   0, 255),
        (255,   0, 255),
        (  0, 255, 255),
        (255, 255, 255),
      ][ansi]
    # ...
    elif ansi > 231:
      s = (ansi - 232) * 10 + 8
      r,g,b = s,s,s
    # ...
    else:
      n = ansi - 16
      # ...
      b = n % 6
      g = (n - b) / 6 % 6
      r = (n - b - g * 6) / 36 % 6
      # ...
      r, g, b = [
        int(v * 40 + 55 if v else 0)
        for v in (r, g, b)
      ]
    # ...
    import colorsys
    # ...
    shade = r == g == b
    base  = 30
    h,s,v = colorsys.rgb_to_hsv(r, g, b)
    h     = base * int(round((360 * h) / base))
    h     = 30 if h > 360 else h
    h     = 360 if not shade and not h else h
    # ...
    rgb = Color.RGBModel(r,g,b)
    hsv = Color.HSVModel(h,s,v)
    # ...
    setattr(self, '_ansi', ansi)
    setattr(self,  '_rgb', rgb)
    setattr(self,  '_hsv', hsv)
    setattr(self,   '_bg', False)

  def __point__(self) -> _t.Tuple[HueLevel, int]:
    H, V = self.HSV.H, self.HSV.V
    A = _SPECTRUM[H][V]
    return (_LEVELS[V], A.index(self))

  #################################################

  def __str__(self) -> str:
    ansi, rgb, hsv = self.ANSI, self.RGB, self.HSV
    return f'{self:{ansi:>3} | {rgb} | {hsv}}'

  def __format__(self, __format_spec: str) -> str:
    text = str(__format_spec)
    ansi = self.ANSI
    modi = 48 if self.Background else 38
    return f'\033[{modi};5;{ansi}m{text}\033[0m'

  def __getstate__(self):
    return self.__dict__.copy()

  def __setstate__(self, dict):
    self.__dict__.update(dict)

  #################################################

  def __hash__(self):
    return hash((self.ANSI, self.RGB, self.HSV, self.Background))

  def __eq__(self, __o: object) -> bool:
    if isinstance(__o, Color):
      return self.__hash__() == __o.__hash__()
    else:
      return __o.__eq__(self)

  def __ne__(self, __o: object) -> bool:
    return not self.__eq__(__o)

  #################################################

  def __rshift__(self, other: int):
    H = self.HSV.H + (Bit8(30) * other)
    H = 30 if H == 0 else H
    V, S = self.__point__()
    return _SPECTRUM[H][_AMOUNTS[V]][S]

  def __rrshift__(self, other: int):
    return self.__rshift__(other)

  def __lshift__(self, other: int):
    H = self.HSV.H - (30 * other)
    H = 30 if H == 0 else H
    V, S = self.__point__()
    return _SPECTRUM[H][_AMOUNTS[V]][S]

  def __rlshift__(self, other: int):
    return self.__lshift__(other)


  def __add__(self, other: int):
    H, (V, S) = self.HSV.H, self.__point__()
    V = V + other
    V = _LVL.max if V > _LVL.max else V
    return _SPECTRUM[H][_AMOUNTS[V]][S]

  def __radd__(self, other: int):
    return self.__add__(other)

  def __sub__(self, other: int):
    H, (V, S) = self.HSV.H, self.__point__()
    V = V - other
    V = _LVL.min if V < _LVL.min else V
    Q = _SPECTRUM[H]
    A = _AMOUNTS[V]
    while A not in Q and A <= 255:
      V += 1
      A = _AMOUNTS[V]
    return Q[A][S]

  def __rsub__(self, other: int):
    return self.__sub__(other)


  def __mul__(self, other: int):
    M = _SAT.min - 1
    H, (V, S) = self.HSV.H, self.__point__()
    S = S - other
    S = M if S < M else S
    return _SPECTRUM[H][_AMOUNTS[V]][S]

  def __rmul__(self, other: int):
    return self.__mul__(other)

  def __truediv__(self, other: int):
    M = _SAT.max - 1
    H, (V, S) = self.HSV.H, self.__point__()
    S = S + other
    S = M if S > M else S
    return _SPECTRUM[H][_AMOUNTS[V]][S]

  def __rtruediv__(self, other: int):
    return self.__truediv__(other)

##########################################################################################################################################################
# CONSTANTS

_AMOUNTS: _t.Dict[HueLevel, Bit8] = {
  0: Bit8(0),
  1: Bit8(95),
  2: Bit8(135),
  3: Bit8(175),
  4: Bit8(215),
  5: Bit8(255),
}
_LEVELS: _t.Dict[Bit8, HueLevel] = {
  a: l for l,a in _AMOUNTS.items()
}
_NAMES: _t.Dict[DegUnit, HueName] = {
  DegUnit(  0): 'Grey',
  DegUnit( 30): 'Orange',
  DegUnit( 60): 'Yellow',
  DegUnit( 90): 'Lime',
  DegUnit(120): 'Green',
  DegUnit(150): 'Turquoise',
  DegUnit(180): 'Teal',
  DegUnit(210): 'Cyan',
  DegUnit(240): 'Blue',
  DegUnit(270): 'Purple',
  DegUnit(300): 'Magenta',
  DegUnit(330): 'Rose',
  DegUnit(360): 'Red',
}
_DEGREES: _t.Dict[HueName, DegUnit] = {
  n: d for d,n in _NAMES.items()
}
_SPECTRUM: _t.Dict[DegUnit, _t.Dict[Bit8, _t.List[Color]]] = {}

##########################################################################################################################################################
# CLASSES

# The common bound-memebers a `Hue` shares as a type-instance.
class _HueInterface:

  _level: HueLevel = _LVL.max
  _saturation: SatLevel = _SAT.max

  @property
  def Name(self) -> str:
    """The name of the hue."""
    return self._name

  @property
  def Degree(self) -> DegUnit:
    """The degree the hue falls within the color-wheel."""
    return self._degree
  @Degree.setter
  def Degree(self, value: DegUnit) -> DegUnit:
    try:
      self._degree = value
      self._amounts: _t.Dict[Bit8, _t.List[Color]] = _SPECTRUM[value]
      self._name = _NAMES[value]
    except:
      pass

  @property
  def Level(self) -> HueLevel:
    """The current default pigment level."""
    return self._level

  @property
  def Saturation(self) -> SatLevel:
    """The current default saturation."""
    return self._saturation

  def SetDefault(self, level: HueLevel = _LVL.max, saturation: SatLevel = _SAT.max):
    """Set the featured color for a `Hue`. Direct references to the `Hue` in `f-strings` will default to the color specified.

      Examples:
        >>> print(f'{Green:hello, world}')
        \033[38;5;46mhello, world\033[0m
        >>> Green.SetDefault(3)
        >>> print(f'{Green:hello, world}')
        \033[38;5;34mhello, world\033[0m

      Args:
        level (HueLevel, optional): The amount of pigment in the color, from `1` (darkest) to `5` (brightest). Defaults to 5.
        saturation (SatLevel, optional): The intensity of the color, from `1` (dull) to `9` (vivid). Defaults to 9.
    """
    self._level = level
    self._saturation = saturation

  #################################################

  def __call__(self, level: HueLevel = _LVL.max, saturation: SatLevel = _SAT.max, bg: bool = False) -> Color:
    """Retrieve a color of specified features within a hue.

      Args:
        level (HueLevel, optional): The brightness level. Defaults to 5.
        saturation (SatLevel, optional): The level of saturation. Defaults to 9.
        bg (bool, optional): If `True`, colorizations occur on the background instead of the foreground. Defaults to False.

      Returns:
        Color: The specified color.
    """
    amount = _AMOUNTS[level]
    # ...
    while amount not in self._amounts:
      level += 1;
      amount = _AMOUNTS[level]
    # ...
    color = Color(self._amounts[amount][_SAT.max-saturation])
    color.Background = bg
    # ...
    return color

  def __default__(self) -> Color:
    V, S = self._level, (_SAT.max - self._saturation)
    return self._amounts[_AMOUNTS[V]][S]

  def __str__(self) -> str:
    amounts = self._amounts
    purest  = amounts[255][0]
    result  = [f'{purest:{self.Name}(y=level,x=saturation)}','\n\n']
    # ...
    result.append(f'{"":4}')
    for sat in range(_SAT.max, _SAT.min-1, -1):
      level = f'({sat})'
      result.append(f'{purest:{level:<4}}')
    result.append('\n')
    # ...
    for amount, colors in sorted(amounts.items(), key=lambda r: r[0], reverse=True):
      level = f'({_LEVELS[amount]})'
      result.append(f'{purest:{level:<4}}')
      for color in colors:
        result.append(f'{color:{color.ANSI:>3}} ')
      result.append('\n')
    # ...
    return ''.join(result)

  def __format__(self, __format_spec: object) -> str:
    return f'{self.__default__():{__format_spec}}'

  #################################################

  def __rshift__(self, other: int):
    return self.__default__().__rshift__(other)

  def __rrshift__(self, other: int):
    return self.__rshift__(other)

  def __lshift__(self, other: int):
    return self.__default__().__lshift__(other)

  def __rlshift__(self, other: int):
    return self.__lshift__(other)

  def __add__(self, other: int):
    return self.__default__().__add__(other)

  def __radd__(self, other: int):
    return self.__add__(other)

  def __sub__(self, other: int):
    return self.__default__().__sub__(other)

  def __rsub__(self, other: int):
    return self.__sub__(other)

  def __mul__(self, other: int):
    return self.__default__().__mul__(other)

  def __rmul__(self, other: int):
    return self.__mul__(other)

  def __truediv__(self, other: int):
    return self.__default__().__truediv__(other)

  def __rtruediv__(self, other: int):
    return self.__truediv__(other)

# The meta-type that allows a `Hue` to be called as a `function` and work as a type-instance.
class _HueType(_HueInterface, type):

  def __new__(typ, name: HueName, bases: tuple, dct: dict):
    cls = super().__new__(typ, name, bases, dct)
    cls.Degree = _DEGREES[name]
    return cls

# A ghost-protocol (lol) that triggers intellisense and (hopefully) pydoc.
class _HueProtocol:

  def __new__(self, level: HueLevel = 5, saturation: SatLevel = 9, bg: bool = False) -> Color:
    """Retrieve a color of specified features within a hue.

      Args:
        level (HueLevel, optional): The amount of pigment in the color, from `1` (darkest) to `5` (brightest). Defaults to 5.
        saturation (SatLevel, optional): The intensity of the color, from `1` (dull) to `9` (vivid). Defaults to 9.
        bg (bool, optional): If `True`, colorizations occur on the background instead of the foreground. Defaults to False.

      Returns:
        Color: The specific color.
    """
    ...

# The meta-type that ensures `Spectrum` is a static singleton.
class _Spectrum(type):

  @staticmethod
  def __setup__():
    """Initializes the color database.
    """
    global _SPECTRUM
    # Run once.
    if _SPECTRUM: return
    # ...
    import os.path as _path, sys as _sys, pickle
    from pathlib import Path
    from functools import reduce
    if getattr(_sys, 'frozen', False):
      app_path = _sys._MEIPASS
    else:
      app_path = _path.dirname(_path.realpath(__file__))
    # Determine cache version
    tag = 'main' if __name__ == "__main__" else 'sub'
    # Generate cache path.
    dirc = Path(f'{app_path}/.store')
    dirc.mkdir(parents=True, exist_ok=True)
    path = dirc / f'spectrum.{tag}.p'
    # Attempt to pull from the cache.
    if path.exists() and _path.getmtime(path) > _path.getmtime(__file__):
      try:
        _SPECTRUM = pickle.load(open(path, 'rb'))
        return
      except:
        pass
    # Otherwise, create colors and update the cache, if needed.
    _shades: list[Color] = []
    _colors: list[Color] = [
      color for color in
      [Color(ansi) for ansi in range(16, 255)]
    ]
    # Organize the spectrum by hue > brightness > saturation.
    for _color in _colors:
      _H, _S, _V = _color.HSV
      # ...
      if _V and _V in _LEVELS:
        if _H not in _SPECTRUM: _SPECTRUM[_H] = {}
        if _V not in _SPECTRUM[_H]: _SPECTRUM[_H][_V] = []
        # ...
        _SPECTRUM[_H][_V].append(_color)
      else:
        _shades.append(_color)
    # Handle Shades.
    def reducer(a: Bit8, b: Bit8) -> Bit8:
      def filterer(c: Color) -> bool:
        C = c.HSV.V + 40
        return C < a and C > b
      S = list(filter(filterer, _shades))
      S = sorted(S, key=lambda c: c.HSV.V, reverse=True)
      _SPECTRUM[0][a] += S
      _SPECTRUM[0][a] = list(reversed(_SPECTRUM[0][a]))
      return b
    reduce(reducer, sorted(_LEVELS.keys(), reverse=True))
    # Fill in empty saturations.
    for _H, _rankings in _SPECTRUM.items():
      for _V, _colors in _rankings.items():
        # ...
        _colors = sorted(_colors, key=lambda c: c.HSV.S, reverse=True)
        # ...
        _SPECTRUM[_H][_V] = _colors + (_colors[-1:]*(_SAT.max-len(_colors)))
    # Save to cache
    pickle.dump(_SPECTRUM, open(path, 'wb'))
  # Initialize each hue.
  __setup__()

  def __call__(cls, *__args, **__kwargs):
    raise SyntaxError(f'{cls.__name__} is a static object and cannot be instantiated.')

  def __setattr__(cls, __name: str, __value: _t.Any) -> None:
    raise AttributeError(f'{cls.__name__} is a static object and cannot be assigned attributes.')

  def __str__(cls) -> str:
    result = ['']
    hues = [_t.cast(_HueInterface, getattr(cls, hue)) for hue in _NAMES.values() if hasattr(cls, hue)]
    for hue in sorted(hues, key=lambda h: h.Degree, reverse=True): result.append(str(hue))
    result.append('')
    return '\n'.join(result)

# The stars of the show.
class Red(_HueProtocol, metaclass=_HueType): ...
class Orange(_HueProtocol, metaclass=_HueType): ...
class Yellow(_HueProtocol, metaclass=_HueType): ...
class Lime(_HueProtocol, metaclass=_HueType): ...
class Green(_HueProtocol, metaclass=_HueType): ...
class Turquoise(_HueProtocol, metaclass=_HueType): ...
class Teal(_HueProtocol, metaclass=_HueType): ...
class Cyan(_HueProtocol, metaclass=_HueType): ...
class Blue(_HueProtocol, metaclass=_HueType): ...
class Purple(_HueProtocol, metaclass=_HueType): ...
class Magenta(_HueProtocol, metaclass=_HueType): ...
class Rose(_HueProtocol, metaclass=_HueType): ...
class Grey(_HueProtocol, metaclass=_HueType): ...

White = Grey(5,1)
Black = Grey(1,9)

# Just a static collection of hues.
class Spectrum(metaclass=_Spectrum):
  """The entire palette of hues.
  """

  Red = Red
  """Red and its variations (_see [**Red**](#pyhues.Red) for details_)."""
  Orange = Orange
  """Orange and its variations (_see [**Orange**](#pyhues.Orange) for details_)."""
  Yellow = Yellow
  """Yellow and its variations (_see [**Yellow**](#pyhues.Yellow) for details_)."""
  Lime = Lime
  """Lime and its variations (_see [**Lime**](#pyhues.Lime) for details_)."""
  Green = Green
  """Green and its variations (_see [**Green**](#pyhues.Green) for details_)."""
  Turquoise = Turquoise
  """Turquoise and its variations (_see [**Turquoise**](#pyhues.Turquoise) for details_)."""
  Teal = Teal
  """Teal and its variations (_see [**Teal**](#pyhues.Teal) for details_)."""
  Cyan = Cyan
  """Cyan and its variations (_see [**Cyan**](#pyhues.Cyan) for details_)."""
  Blue = Blue
  """Blue and its variations (_see [**Blue**](#pyhues.Blue) for details_)."""
  Purple = Purple
  """Purple and its variations (_see [**Purple**](#pyhues.Purple) for details_)."""
  Magenta = Magenta
  """Magenta and its variations (_see [**Magenta**](#pyhues.Magenta) for details_)."""
  Rose = Rose
  """Rose and its variations (_see [**Rose**](#pyhues.Rose) for details_)."""
  Grey = Grey
  """Grey and its variations (_see [**Grey**](#pyhues.Grey) for details_)."""

  def Kaleidoscope():
    """Have some fun with hues. Displays a looping marquee of a color spectrum:
      - Use <kbd>ctrl</kbd> + <kbd>c</kbd> to change the spectrum.
      - Use <kbd>ctrl</kbd> + <kbd>\\</kbd> (<kbd>ctrl</kbd> + <kbd>x</kbd>) to quit.
    """
    from signal import signal, SIGQUIT, SIGINT
    from random import randint as _randint, choice
    from time import sleep as _sleep
    global C
    # ...
    def change():
      global C
      try:
        V = choice([v for v in LVL if v != C.HSV.V])
        S = choice([s for s in SAT if s != C.HSV.S])
        C = _SPECTRUM[C.HSV.H][V][S]
      except KeyError:
        change()
    def quit(*_args):
      _sys.exit(0)
    def refresh(*_args):
      print('\033[1000000000D', end='')
      change()
    # ...
    signal(SIGQUIT, quit)
    signal(SIGINT, refresh)
    # ...
    LVL = [ l for l in _LEVELS.keys() if l ]
    SAT = [ *range(_SAT.max) ]
    C = Color(_randint(17,230))
    # ...

    # ...
    mn, mx = 1, 12
    while True:
      try:
        C >>= 1
        _sleep(.025)
        print(C)
      except KeyError:
        change()

##########################################################################################################################################################

if __name__ == "__main__":
    print(f"{__title__} - {__doc__}")  # pragma: no cover
