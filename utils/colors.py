import catppuccin
cpcn = catppuccin.PALETTE.mocha.colors
class Colors:
#
#    CELL_COLOR_A = '#99e600'
#    CELL_COLOR_B = '#77b300'
#
#    CELL_COLOR_A_OPEN = '#d9aa75'
#    CELL_COLOR_B_OPEN = '#f2c48f'
#
#    BACKGROUND = "#000000"
#    TEXT = "#705129" 
#    BIGTEXT = "#e0e0e0"

    CELL_COLOR_A = cpcn.surface0.hex
    CELL_COLOR_B = cpcn.surface1.hex

    CELL_COLOR_A_OPEN = cpcn.crust.hex
    CELL_COLOR_B_OPEN = cpcn.mantle.hex

    BACKGROUND = cpcn.base.hex

    TEXT = {
        -1: cpcn.red.hex,
        0 : cpcn.crust.hex,
        1 : cpcn.mauve.hex, 
        2 : cpcn.peach.hex,
        3 : cpcn.green.hex,
        4 : cpcn.teal.hex,
        5 : cpcn.lavender.hex,
        6 : cpcn.pink.hex,
        7 : cpcn.sapphire.hex,
        8 : cpcn.rosewater.hex,
    }

    WON = cpcn.blue.hex
    LOST = cpcn.red.hex

    BANNER = cpcn.surface2.hex
