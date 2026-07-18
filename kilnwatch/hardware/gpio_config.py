"""
GPIO and SPI pin assignments.
All pin references in the project come from this module.
"""
SPI_BUS = 0
SPI_DEVICE = 0

# BCM GPIO numbers for chip-select lines (one per MAX31856 board)
CS_PINS = {
    1: 8,   # SPI0_CE0 — hardware CS
    2: 7,   # SPI0_CE1 — hardware CS
    3: 25,  # software CS
    4: 24,  # software CS
}
