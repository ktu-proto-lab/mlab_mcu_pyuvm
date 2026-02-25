# Software
## Structure
```
.
├── driver
├── hal
├── soc
└── test
```
*Meanings:*

1. `soc` - bare-metal hardware definitions:
    - register maps
    - base addresses
    - bit masks

2. `hal` - hardware abstraction layer:
    - safe initialization
    - read/write functions

3. `driver` - peripheral modules built on HAL:
    - LED
    - display
    - keyboard

4. `test` - verify functionality