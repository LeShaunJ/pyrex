# `pyrex`

[![Build Status][build_status_badge]][build_status_link]
[![Coverage][coverage_badge]][coverage_link]
[![PyPI version][pypi_badge]][pypi_link]

Simplified `xterm` color usage and management.

## Contents

* [Installation](#installation)
* [Usage](#usage)
* [Classes](#classes)
  * [Color](#color)
  * [Spectrum](#spectrum)
* [Types](#types)
  * [Bit8](#bit8)
  * [DegUnit](#degunit)
  * [Percent](#percent)
* [Additional](#additional)
  * [HueName](#hueshuename)
  * [HueLevel](#hueshuelevel)
  * [SatLevel](#huessatlevel)

## Installation

```bash
# In your virtual environment
pip install pyrex
```

## Usage

Every color is grouped into one of twelves tones within the color wheel. A `Hue` represents a tone and every possible brightness/saturation variations (_aka `Color`_) it provides. By itself, a `Hue` can be used with `f-strings` to colorize text with its deepest features; or, with **brightness** and **saturation** specified for further customization.

All shades fall under `Grey`, and it works the same way, with the `Black` and `White` symbols serving as shortcuts to grey's most darkest/saturated and brightess/desaturated values, respectively.

```python
from pyrex import *
```
```python
from pyrex import (
    Red,   Orange,    Yellow,  Lime,
    Green, Turquoise, Teal,    Cyan,
    Blue,  Purple,    Magenta, Rose,
    Grey,  White,     Black
)
```

**Examples**:

Colorize strings with a hue's default features:
```python
>>> print(f'{Red:hello, world}')
\033[38;5;196mhello, world\033[0m
```
```python
>>> print(f'{Orange:hello, world}')
\033[38;5;202mhello, world\033[0m
```
```python
>>> print(f'{Yellow:hello, world}')
\033[38;5;190mhello, world\033[0m
```
```python
>>> print(f'{Lime:hello, world}')
\033[38;5;82mhello, world\033[0m
```
```python
>>> print(f'{Green:hello, world}')
\033[38;5;46mhello, world\033[0m
```
```python
>>> print(f'{Turquoise:hello, world}')
\033[38;5;47mhello, world\033[0m
```
```python
>>> print(f'{Teal:hello, world}')
\033[38;5;45mhello, world\033[0m
```
```python
>>> print(f'{Cyan:hello, world}')
\033[38;5;27mhello, world\033[0m
```
```python
>>> print(f'{Blue:hello, world}')
\033[38;5;21mhello, world\033[0m
```
```python
>>> print(f'{Purple:hello, world}')
\033[38;5;57mhello, world\033[0m
```
```python
>>> print(f'{Magenta:hello, world}')
\033[38;5;165mhello, world\033[0m
```
```python
>>> print(f'{Rose:hello, world}')
\033[38;5;197mhello, world\033[0m
```

  Specify the brigthness and saturation a hue:
```python
>>> print(f'{Red(2,7):hello, world}')
\033[38;5;95mhello, world\033[0m
```
```python
>>> print(f'{Orange(1,7):hello, world}')
\033[38;5;94mhello, world\033[0m
```
```python
>>> print(f'{Yellow(3,5):hello, world}')
\033[38;5;144mhello, world\033[0m
```
```python
>>> print(f'{Lime(5,6):hello, world}')
\033[38;5;155mhello, world\033[0m
```
```python
>>> print(f'{Green(3,5):hello, world}')
\033[38;5;108mhello, world\033[0m
```
```python
>>> print(f'{Turquoise(1,9):hello, world}')
\033[38;5;29mhello, world\033[0m
```
```python
>>> print(f'{Teal(1,9):hello, world}')
\033[38;5;23mhello, world\033[0m
```
```python
>>> print(f'{Cyan(5,6):hello, world}')
\033[38;5;75mhello, world\033[0m
```
```python
>>> print(f'{Blue(5,6):hello, world}')
\033[38;5;99mhello, world\033[0m
```
```python
>>> print(f'{Purple(5,6,True):hello, world}')
\033[48;5;135mhello, world\033[0m
```
```python
>>> print(f'{Magenta(5,6):hello, world}')
\033[38;5;171mhello, world\033[0m
```
```python
>>> print(f'{Rose(5,6):hello, world}')
\033[38;5;205mhello, world\033[0m
```

  Shade with greyscale:
```python
>>> print(f'{Grey:hello, world}')
\033[38;5;249mhello, world\033[0m
```
```python
>>> print(f'{Grey(3,6):hello, world}')
\033[38;5;244mhello, world\033[0m
```
```python
>>> print(f'{White:hello, world}')
\033[38;5;231mhello, world\033[0m
```
```python
>>> print(f'{Black:hello, world}')
\033[38;5;16mhello, world\033[0m
```

  Fill the background:
```python
>>> print(f'{Rose(bg=True):hello, world}')
\033[48;5;197mhello, world\033[0m
```

## Classes

## `Color`

```python
Color(ansi: Bit8)
Color(color: "Color")
```

Repesents a color and its specific features.

**Examples**:

  Pick a color using its ANSI code:
```python
>>> clr = Color(196)
```

  Format text using the color:
```python
>>> print(f'{clr:hello, world}')
\033[38;5;196mhello, world\033[0m
```

  Set the color as a background:
```python
>>> clr.Background = True
>>> print(f'{clr:hello, world}')
\033[48;5;196mhello, world\033[0m
```

  Shift the color to the next hue in the color wheel:
```python
>>> clr >>= 1
>>> print(f'{clr:hello, world}')
\033[38;5;202mhello, world\033[0m
```

  Shift the color two hues back in the color wheel:
```python
>>> clr <<= 2
>>> print(f'{clr:hello, world}')
\033[38;5;197mhello, world\033[0m
```

  Darken the color by 3 (_out of 5_) levels:
```python
>>> clr -= 3
>>> print(f'{clr:hello, world}')
\033[38;5;89mhello, world\033[0m
```

  Brighten the color by 2 (_out of 5_) levels:
```python
>>> clr += 2
>>> print(f'{clr:hello, world}')
\033[38;5;161mhello, world\033[0m
```

  Desaturate the color by 4 (_out of 9_) levels:
```python
>>> clr /= 4
>>> print(f'{clr:hello, world}')
\033[38;5;175mhello, world\033[0m
```

  Saturate the color by 2 (_out of 9_) levels:
```python
>>> clr *= 2
>>> print(f'{clr:hello, world}')
\033[38;5;168mhello, world\033[0m
```

Create a `Color` instance from its correspnding ANSI code.

**Arguments**:

| Keyword | Type | Required | Description | Defaault |
| :-- | :--: | :--: | :-- | :--: |
| **ansi** | `int\|str` | ✓ | A valid ASNI color code. |  |

Duplicate a `Color` instance from an existing `Color`.

**Arguments**:

| Keyword | Type | Required | Description | Defaault |
| :-- | :--: | :--: | :-- | :--: |
| **ansi** | `Color` | ✓ | An existing `Color` instance. |  |

### `Color.ANSI`

```python
instance.ANSI: Bit8
```

The ANSI code (`0-255`) the color corresponds tp.

### `Color.RGB`

```python
instance.RGB: RGBModel
```

The red-green-blue values as a `tuple`.

### `Color.HSV`

```python
instance.HSV: HSVModel
```

The hue-saturation-brightness values as a `tuple`.

### `Color.Hue`

```python
instance.Hue: str
```

The name of the hue the color belongs to.

### `Color.Background`

```python
instance.Background: bool
```

Marks the color for background coloring purposes.

## `Color.RGBModel`

```python
Color.RGBModel(R: Bit8 = 0, G: Bit8 = 0, B: Bit8 = 0)
```

Represents an RGB color model.

**Arguments**:

| Keyword | Type | Required | Description | Defaault |
| :-- | :--: | :--: | :-- | :--: |
| **R** | `Bit8` |  | The the amount of red (`0-255`) in the color.. | `0` |
| **G** | `Bit8` |  | The the amount of green (`0-255`) in the color.. | `0` |
| **B** | `Bit8` |  | The the amount of blue (`0-255`) in the color.. | `0` |

### `Color.RGBModel.R`

```python
instance.R: Bit8
```

The the amount of red (`0-255`) in the color.

### `Color.RGBModel.G`

```python
instance.G: Bit8
```

The the amount of green (`0-255`) in the color.

### `Color.RGBModel.B`

```python
instance.B: Bit8
```

The the amount of blue (`0-255`) in the color.

## `Color.HSVModel`

```python
Color.HSVModel(H: DegUnit = 0, S: Percent = 0, V: Bit8 = 0)
```

Represents an HSV color model.

**Arguments**:

| Keyword | Type | Required | Description | Defaault |
| :-- | :--: | :--: | :-- | :--: |
| **H** | `DegUnit` |  | The point in which the color's hue falls on the color wheel (`0°-360°`).. | `0` |
| **S** | `Percent` |  | The percentage of saturation (intensity/vividness) the color has.. | `0` |
| **V** | `Bit8` |  | The maximum brightness (`0-255`) the color has.. | `0` |

### `Color.HSVModel.H`

```python
instance.H: DegUnit
```

The point in which the color's hue falls on the color wheel (`0°-360°`).

### `Color.HSVModel.S`

```python
instance.S: Percent
```

The percentage of saturation (intensity/vividness) the color has.

### `Color.HSVModel.V`

```python
instance.V: Bit8
```

The maximum brightness (`0-255`) the color has.

## `Spectrum`

```python
Spectrum(metaclass=_Spectrum)
```

The entire palette of hues.

### `Spectrum.Kaleidoscope`

```python
Kaleidoscope()
```

Have some fun with hues. Displays a looping marquee of a color spectrum:
- Use <kbd>ctrl</kbd> + <kbd>c</kbd> to change the spectrum.
- Use <kbd>ctrl</kbd> + <kbd>\</kbd> (<kbd>ctrl</kbd> + <kbd>x</kbd>) to quit.

#### `Spectrum.Red`

Red and its variations.

#### `Spectrum.Orange`

Orange and its variations.

#### `Spectrum.Yellow`

Yellow and its variations.

#### `Spectrum.Lime`

Lime and its variations.

#### `Spectrum.Green`

Green and its variations.

#### `Spectrum.Turquoise`

Turquoise and its variations.

#### `Spectrum.Teal`

Teal and its variations.

#### `Spectrum.Cyan`

Cyan and its variations.

#### `Spectrum.Blue`

Blue and its variations.

#### `Spectrum.Purple`

Purple and its variations.

#### `Spectrum.Magenta`

Magenta and its variations.

#### `Spectrum.Rose`

Rose and its variations.

#### `Spectrum.Grey`

Grey and its variations.

## `Bit8`

```python
Bit8(value: str | int)
```

A type-guard for an 8-bit number value between `0` and `255`.

**Examples**:

```python
>>> Bit8(128)
128
```
```python
>>> ~Bit8(4)
251
```

**Arguments**:

| Keyword | Type | Required | Description | Defaault |
| :-- | :--: | :--: | :-- | :--: |
| **value** | `str\|int` | ✓ | A valid 8-bit number between `0` and `255`. |  |


**Raises**:

| Type | Description |
| :--: | :-- |
| `ValueError` | If `num` is not between `0` and `255`. |
| `ValueError` | If `num` is not convertible to `int`. |

## `DegUnit`

```python
DegUnit(value: str | int = 0)
```

A type-guard representing degrees (`°`) from `0` and `360`.

**Examples**:

```python
>>> DegUnit(270)
270
```
```python
>>> str(DegUnit(270))
'270°'
```

**Arguments**:

| Keyword | Type | Required | Description | Defaault |
| :-- | :--: | :--: | :-- | :--: |
| **value** | `str\|int` | ✓ | A valid 8-bit number between `0` and `360`. |  |


**Raises**:

| Type | Description |
| :--: | :-- |
| `ValueError` | If `num` is not between `0` and `360`. |
| `ValueError` | If `num` is not convertible to `int`. |

## `Percent`

```python
Percent(value: str | int | float)
```

Represents a percentage, yielding it's fractional value when inverted.

**Examples**:

```python
>>> Percent(75)
75.0
```
```python
>>> ~Percent(25.94)
0.2594
```
```python
>>> str(Percent(68.1))
'68.1%'
```

**Arguments**:

| Keyword | Type | Required | Description | Defaault |
| :-- | :--: | :--: | :-- | :--: |
| **value** | `str\|int\|float` | ✓ | A percentage. |  |


**Raises**:

| Type | Description |
| :--: | :-- |
| `ValueError` | If `num` is not convertible to `float`. |

### `Percent.FromFraction`

```python
FromFraction(value: str | float)
```

Create a Percent instance from a fractional value.

**Arguments**:

| Keyword | Type | Required | Description | Defaault |
| :-- | :--: | :--: | :-- | :--: |
| **value** | `str\|float` | ✓ | The fractional representation of the Percent value. |  |


**Returns**:

| Type | Description |
| :--: | :-- |
| `Percent` | A new Percent instance. |

## Additional

#### `HueName`

```python
'Red'|'Orange'|'Yellow'|'Lime'|'Green'|'Turquoise'|'Teal'|'Cyan'|'Blue'|'Purple'|'Magenta'|'Rose'
```
A valid name of a hue.

#### `HueLevel`

```python
0|1|2|3|4|5
```
An amount of color a hue can have.

#### `SatLevel`

```python
1|2|3|4|5|6|7|8|9
```
An amount of saturation a hue can have.

[build_status_badge]: https://github.com/LeShaunJ/pyrex/actions/workflows/test.yml/badge.svg
[build_status_link]: https://github.com/LeShaunJ/pyrex/actions/workflows/test.yml
[coverage_badge]: https://raw.githubusercontent.com/LeShaunJ/pyrex/main/docs/coverage.svg
[coverage_link]: https://raw.githubusercontent.com/LeShaunJ/pyrex/main/docs/coverage.svg
[pypi_badge]: https://badge.fury.io/py/pyrex.svg
[pypi_link]: https://badge.fury.io/py/pyrex
