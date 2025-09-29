questions = {
    'Overall Population' : 'B01001_001E',
    'White, non-Hispanic population' : 'B01001H_001E',
    'Black alone population' : 'B01001B_001E',
    'Native American alone population' : 'B01001C_001E',
    'Asian population' : 'B01001D_001E',
    'Hispanic population' : 'B01001I_001E',
    
    'Overall population in labor force' : 'DP03_0002E',
    'White, non-Hispanic labor force' : 'S2301_C02_020E',
    'Native American alone labor force' : 'S2301_C02_014E',
    'Black alone labor force' : 'S2301_C02_013E',
    'Asian labor force' : 'S2301_C02_015E',
    'Hispanic labor force' : 'S2301_C02_019E',
    'Ratio of Native American participation to white participation' : 'S2301_C02_014E / S2301_C02_020E',
    'Ratio of Black, Asian, and Hispanic participation to white participation' : ' ( S2301_C02_013E + S2301_C02_015E + S2301_C02_019E ) / ( S2301_C02_020E ) ',
    
    'Overall managerial' : 'B08124_002E',
    'White, non-Hispanic managerial' : ' ( C24010A_003E + C24010H_009E ) / ( S2301_C01_020E / B01001H_001E )',
    'Native American alone managerial' : '( C24010C_003E + C24010C_009E ) / ( S2301_C01_014E / B01001C_001E )',
    'Black alone managerial' : '( C24010B_003E + C24010B_003E ) / ( S2301_C01_013E / B01001B_001E )',
    'Asian managerial' : '( C24010D_003E + C24010D_009E ) / ( S2301_C01_015E / B01001D_001E )',
    'Hispanic managerial' : '( C24010I_002E + C24010I_002E ) / ( S2301_C01_019E / B01001I_001E )',
    'Ratio of Native American rates to white rates' : '( C24010C_003E + C24010C_009E ) / ( C24010A_003E + C24010H_009E )',
    'Ratio of Black, Asian and Hispanic rates to white rates' : '( C24010B_003E + C24010B_003E + C24010D_003E + C24010D_009E + C24010I_002E + C24010I_002E ) / ( C24010A_003E + C24010H_009E )',

    'Overall median earnings' : 'S2001_C01_002E',
    'White, non-Hispanic median earnings' : 'B20017H_001E',
    'Black alone median earnings' : 'B20017B_001E',
    'Native American alone median earnings' : 'B20017C_001E',
    'Asian median earnings' : 'B20017D_001E',
    'Hispanic median earnings' : 'B20017I_001E',
    'Ratio of Native American earnings to white earnings': 'B20017C_001E / B20017H_001E',
    
    'Overall population with BA or better' : 'B06009_005E + B06009_006E',
    'White, non-Hispanic with BA or better' : 'S1501_C02_033E',
    'Black alone with BA or better' : 'S1501_C02_036E',
    'Native American alone with BA or better' : 'S1501_C02_039E',
    'Asian with BA or better' : 'S1501_C02_042E',
    'Hispanic with BA or better' : 'S1501_C02_054E',
    'Ratio of Native Americans to whites with BA or more education' : 'S1501_C02_039E / S1501_C02_033E',

    'Overall percentage below the poverty level' : 'S1701_C03_001E',
    'White, non-Hispanic below poverty level' : 'S1701_C03_021E',
    'Black alone below poverty level' : 'S1701_C03_014E',
    'Native American alone below poverty level' : 'S1701_C03_015E',
    'Asian below poverty level' : 'S1701_C03_016E',
    'Hispanic below poverty level' : 'S1701_C03_020E',
    'Ratio of Native Americans to whites below poverty level' : 'S1701_C03_015E / S1701_C03_021E',

    'Overall percentage with health insurance' : 'S2701_C03_001E',
    'White, non-Hispanic with health insurance' : 'S2701_C03_024E',
    'Black alone with health insurance' : 'S2701_C03_017E',
    'Native American alone with health insurance' : 'S2701_C03_018E',
    'Asian with health insurance' : 'S2701_C03_019E',
    'Hispanic with health insurance' : 'S2701_C03_023E',
    'Ratio of Native Americans to whites with health insurance' : 'S2701_C03_018E / S2701_C03_024E'
}

products = {
    'B' : '',
    'S' : '/subject',
    'C' : '',
    'D' : '/profile'
}

positions = [149, 151, 152, 153, 154, 155, 158, 160, 161, 162, 163, 164, 165, 166, 169, 170, 171, 172, 173, 174, 175, 176, 179, 181, 182, 183, 184, 185, 186, 189, 191, 192, 193, 194, 195, 196, 199, 201, 202, 203, 204, 205, 206, 209, 211, 212, 213, 214, 215, 216]

# for i in range(0, len(positions)):
#     positions[i] = positions[i] - 2

# print(positions)


# White, non-Hispanic managerial                                   72       ( C24010A_003E + C24010H_009E ) / ( S2301_C01_020EA / B01001H_001E )
# Asian managerial                                                  1       ( C24010D_003E + C24010D_009E ) / ( S2301_C01_015E / B01001D_001E )
# White, non-Hispanic with BA or better                            72       x S1501_C02_033EA -> S1501_C02_033E
# Ratio of Native Americans to whites with BA or more education    72       x S1501_C02_039E / S1501_C02_033EA -> S1501_C02_039E / S1501_C02_033E
# Overall percentage below the poverty level                       45       x S1703_C03_001E -> S1701_C03_001E



