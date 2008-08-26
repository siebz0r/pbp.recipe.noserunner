#define GET_COMBO_SIZE(n,k) ((n < 80) ? ((k < 80) ? combo_sizes[n][k] : 0) : 0)
static unsigned int combo_sizes[80][80] = {
    { 1u, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
    { 1u, 1u, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
    { 1u, 2u, 1u, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
    { 1u, 3u, 3u, 1u, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
    { 1u, 4u, 6u, 4u, 1u, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
    { 1u, 5u, 10u, 10u, 5u, 1u, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
    { 1u, 6u, 15u, 20u, 15u, 6u, 1u, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
    { 1u, 7u, 21u, 35u, 35u, 21u, 7u, 1u, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
    { 1u, 8u, 28u, 56u, 70u, 56u, 28u, 8u, 1u, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
    { 1u, 9u, 36u, 84u, 126u, 126u, 84u, 36u, 9u, 1u, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
    { 1u, 10u, 45u, 120u, 210u, 252u, 210u, 120u, 45u, 10u, 1u, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
    { 1u, 11u, 55u, 165u, 330u, 462u, 462u, 330u, 165u, 55u, 11u, 1u, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
    { 1u, 12u, 66u, 220u, 495u, 792u, 924u, 792u, 495u, 220u, 66u, 12u, 1u, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
    { 1u, 13u, 78u, 286u, 715u, 1287u, 1716u, 1716u, 1287u, 715u, 286u, 78u, 13u, 1u, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
    { 1u, 14u, 91u, 364u, 1001u, 2002u, 3003u, 3432u, 3003u, 2002u, 1001u, 364u, 91u, 14u, 1u, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
    { 1u, 15u, 105u, 455u, 1365u, 3003u, 5005u, 6435u, 6435u, 5005u, 3003u, 1365u, 455u, 105u, 15u, 1u, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
    { 1u, 16u, 120u, 560u, 1820u, 4368u, 8008u, 11440u, 12870u, 11440u, 8008u, 4368u, 1820u, 560u, 120u, 16u, 1u, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
    { 1u, 17u, 136u, 680u, 2380u, 6188u, 12376u, 19448u, 24310u, 24310u, 19448u, 12376u, 6188u, 2380u, 680u, 136u, 17u, 1u, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
    { 1u, 18u, 153u, 816u, 3060u, 8568u, 18564u, 31824u, 43758u, 48620u, 43758u, 31824u, 18564u, 8568u, 3060u, 816u, 153u, 18u, 1u, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
    { 1u, 19u, 171u, 969u, 3876u, 11628u, 27132u, 50388u, 75582u, 92378u, 92378u, 75582u, 50388u, 27132u, 11628u, 3876u, 969u, 171u, 19u, 1u, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
    { 1u, 20u, 190u, 1140u, 4845u, 15504u, 38760u, 77520u, 125970u, 167960u, 184756u, 167960u, 125970u, 77520u, 38760u, 15504u, 4845u, 1140u, 190u, 20u, 1u, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
    { 1u, 21u, 210u, 1330u, 5985u, 20349u, 54264u, 116280u, 203490u, 293930u, 352716u, 352716u, 293930u, 203490u, 116280u, 54264u, 20349u, 5985u, 1330u, 210u, 21u, 1u, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
    { 1u, 22u, 231u, 1540u, 7315u, 26334u, 74613u, 170544u, 319770u, 497420u, 646646u, 705432u, 646646u, 497420u, 319770u, 170544u, 74613u, 26334u, 7315u, 1540u, 231u, 22u, 1u, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
    { 1u, 23u, 253u, 1771u, 8855u, 33649u, 100947u, 245157u, 490314u, 817190u, 1144066u, 1352078u, 1352078u, 1144066u, 817190u, 490314u, 245157u, 100947u, 33649u, 8855u, 1771u, 253u, 23u, 1u, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
    { 1u, 24u, 276u, 2024u, 10626u, 42504u, 134596u, 346104u, 735471u, 1307504u, 1961256u, 2496144u, 2704156u, 2496144u, 1961256u, 1307504u, 735471u, 346104u, 134596u, 42504u, 10626u, 2024u, 276u, 24u, 1u, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
    { 1u, 25u, 300u, 2300u, 12650u, 53130u, 177100u, 480700u, 1081575u, 2042975u, 3268760u, 4457400u, 5200300u, 5200300u, 4457400u, 3268760u, 2042975u, 1081575u, 480700u, 177100u, 53130u, 12650u, 2300u, 300u, 25u, 1u, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
    { 1u, 26u, 325u, 2600u, 14950u, 65780u, 230230u, 657800u, 1562275u, 3124550u, 5311735u, 7726160u, 9657700u, 10400600u, 9657700u, 7726160u, 5311735u, 3124550u, 1562275u, 657800u, 230230u, 65780u, 14950u, 2600u, 325u, 26u, 1u, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
    { 1u, 27u, 351u, 2925u, 17550u, 80730u, 296010u, 888030u, 2220075u, 4686825u, 8436285u, 13037895u, 17383860u, 20058300u, 20058300u, 17383860u, 13037895u, 8436285u, 4686825u, 2220075u, 888030u, 296010u, 80730u, 17550u, 2925u, 351u, 27u, 1u, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
    { 1u, 28u, 378u, 3276u, 20475u, 98280u, 376740u, 1184040u, 3108105u, 6906900u, 13123110u, 21474180u, 30421755u, 37442160u, 40116600u, 37442160u, 30421755u, 21474180u, 13123110u, 6906900u, 3108105u, 1184040u, 376740u, 98280u, 20475u, 3276u, 378u, 28u, 1u, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
    { 1u, 29u, 406u, 3654u, 23751u, 118755u, 475020u, 1560780u, 4292145u, 10015005u, 20030010u, 34597290u, 51895935u, 67863915u, 77558760u, 77558760u, 67863915u, 51895935u, 34597290u, 20030010u, 10015005u, 4292145u, 1560780u, 475020u, 118755u, 23751u, 3654u, 406u, 29u, 1u, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
    { 1u, 30u, 435u, 4060u, 27405u, 142506u, 593775u, 2035800u, 5852925u, 14307150u, 30045015u, 54627300u, 86493225u, 119759850u, 145422675u, 155117520u, 145422675u, 119759850u, 86493225u, 54627300u, 30045015u, 14307150u, 5852925u, 2035800u, 593775u, 142506u, 27405u, 4060u, 435u, 30u, 1u, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
    { 1u, 31u, 465u, 4495u, 31465u, 169911u, 736281u, 2629575u, 7888725u, 20160075u, 44352165u, 84672315u, 141120525u, 206253075u, 265182525u, 300540195u, 300540195u, 265182525u, 206253075u, 141120525u, 84672315u, 44352165u, 20160075u, 7888725u, 2629575u, 736281u, 169911u, 31465u, 4495u, 465u, 31u, 1u, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
    { 1u, 32u, 496u, 4960u, 35960u, 201376u, 906192u, 3365856u, 10518300u, 28048800u, 64512240u, 129024480u, 225792840u, 347373600u, 471435600u, 565722720u, 601080390u, 565722720u, 471435600u, 347373600u, 225792840u, 129024480u, 64512240u, 28048800u, 10518300u, 3365856u, 906192u, 201376u, 35960u, 4960u, 496u, 32u, 1u, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
    { 1u, 33u, 528u, 5456u, 40920u, 237336u, 1107568u, 4272048u, 13884156u, 38567100u, 92561040u, 193536720u, 354817320u, 573166440u, 818809200u, 1037158320u, 1166803110u, 1166803110u, 1037158320u, 818809200u, 573166440u, 354817320u, 193536720u, 92561040u, 38567100u, 13884156u, 4272048u, 1107568u, 237336u, 40920u, 5456u, 528u, 33u, 1u, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
    { 1u, 34u, 561u, 5984u, 46376u, 278256u, 1344904u, 5379616u, 18156204u, 52451256u, 131128140u, 286097760u, 548354040u, 927983760u, 1391975640u, 1855967520u, 2203961430u, 2333606220u, 2203961430u, 1855967520u, 1391975640u, 927983760u, 548354040u, 286097760u, 131128140u, 52451256u, 18156204u, 5379616u, 1344904u, 278256u, 46376u, 5984u, 561u, 34u, 1u, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
    { 1u, 35u, 595u, 6545u, 52360u, 324632u, 1623160u, 6724520u, 23535820u, 70607460u, 183579396u, 417225900u, 834451800u, 1476337800u, 2319959400u, 3247943160u, 4059928950u, 0u, 0u, 4059928950u, 3247943160u, 2319959400u, 1476337800u, 834451800u, 417225900u, 183579396u, 70607460u, 23535820u, 6724520u, 1623160u, 324632u, 52360u, 6545u, 595u, 35u, 1u, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
    { 1u, 36u, 630u, 7140u, 58905u, 376992u, 1947792u, 8347680u, 30260340u, 94143280u, 254186856u, 600805296u, 1251677700u, 2310789600u, 3796297200u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 3796297200u, 2310789600u, 1251677700u, 600805296u, 254186856u, 94143280u, 30260340u, 8347680u, 1947792u, 376992u, 58905u, 7140u, 630u, 36u, 1u, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
    { 1u, 37u, 666u, 7770u, 66045u, 435897u, 2324784u, 10295472u, 38608020u, 124403620u, 348330136u, 854992152u, 1852482996u, 3562467300u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 3562467300u, 1852482996u, 854992152u, 348330136u, 124403620u, 38608020u, 10295472u, 2324784u, 435897u, 66045u, 7770u, 666u, 37u, 1u, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
    { 1u, 38u, 703u, 8436u, 73815u, 501942u, 2760681u, 12620256u, 48903492u, 163011640u, 472733756u, 1203322288u, 2707475148u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 2707475148u, 1203322288u, 472733756u, 163011640u, 48903492u, 12620256u, 2760681u, 501942u, 73815u, 8436u, 703u, 38u, 1u, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
    { 1u, 39u, 741u, 9139u, 82251u, 575757u, 3262623u, 15380937u, 61523748u, 211915132u, 635745396u, 1676056044u, 3910797436u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 3910797436u, 1676056044u, 635745396u, 211915132u, 61523748u, 15380937u, 3262623u, 575757u, 82251u, 9139u, 741u, 39u, 1u, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
    { 1u, 40u, 780u, 9880u, 91390u, 658008u, 3838380u, 18643560u, 76904685u, 273438880u, 847660528u, 2311801440u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 2311801440u, 847660528u, 273438880u, 76904685u, 18643560u, 3838380u, 658008u, 91390u, 9880u, 780u, 40u, 1u, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
    { 1u, 41u, 820u, 10660u, 101270u, 749398u, 4496388u, 22481940u, 95548245u, 350343565u, 1121099408u, 3159461968u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 3159461968u, 1121099408u, 350343565u, 95548245u, 22481940u, 4496388u, 749398u, 101270u, 10660u, 820u, 41u, 1u, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
    { 1u, 42u, 861u, 11480u, 111930u, 850668u, 5245786u, 26978328u, 118030185u, 445891810u, 1471442973u, 4280561376u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 4280561376u, 1471442973u, 445891810u, 118030185u, 26978328u, 5245786u, 850668u, 111930u, 11480u, 861u, 42u, 1u, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
    { 1u, 43u, 903u, 12341u, 123410u, 962598u, 6096454u, 32224114u, 145008513u, 563921995u, 1917334783u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 1917334783u, 563921995u, 145008513u, 32224114u, 6096454u, 962598u, 123410u, 12341u, 903u, 43u, 1u, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
    { 1u, 44u, 946u, 13244u, 135751u, 1086008u, 7059052u, 38320568u, 177232627u, 708930508u, 2481256778u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 2481256778u, 708930508u, 177232627u, 38320568u, 7059052u, 1086008u, 135751u, 13244u, 946u, 44u, 1u, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
    { 1u, 45u, 990u, 14190u, 148995u, 1221759u, 8145060u, 45379620u, 215553195u, 886163135u, 3190187286u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 3190187286u, 886163135u, 215553195u, 45379620u, 8145060u, 1221759u, 148995u, 14190u, 990u, 45u, 1u, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
    { 1u, 46u, 1035u, 15180u, 163185u, 1370754u, 9366819u, 53524680u, 260932815u, 1101716330u, 4076350421u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 4076350421u, 1101716330u, 260932815u, 53524680u, 9366819u, 1370754u, 163185u, 15180u, 1035u, 46u, 1u, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
    { 1u, 47u, 1081u, 16215u, 178365u, 1533939u, 10737573u, 62891499u, 314457495u, 1362649145u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 1362649145u, 314457495u, 62891499u, 10737573u, 1533939u, 178365u, 16215u, 1081u, 47u, 1u, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
    { 1u, 48u, 1128u, 17296u, 194580u, 1712304u, 12271512u, 73629072u, 377348994u, 1677106640u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 1677106640u, 377348994u, 73629072u, 12271512u, 1712304u, 194580u, 17296u, 1128u, 48u, 1u, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
    { 1u, 49u, 1176u, 18424u, 211876u, 1906884u, 13983816u, 85900584u, 450978066u, 2054455634u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 2054455634u, 450978066u, 85900584u, 13983816u, 1906884u, 211876u, 18424u, 1176u, 49u, 1u, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
    { 1u, 50u, 1225u, 19600u, 230300u, 2118760u, 15890700u, 99884400u, 536878650u, 2505433700u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 2505433700u, 536878650u, 99884400u, 15890700u, 2118760u, 230300u, 19600u, 1225u, 50u, 1u, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
    { 1u, 51u, 1275u, 20825u, 249900u, 2349060u, 18009460u, 115775100u, 636763050u, 3042312350u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 3042312350u, 636763050u, 115775100u, 18009460u, 2349060u, 249900u, 20825u, 1275u, 51u, 1u, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
    { 1u, 52u, 1326u, 22100u, 270725u, 2598960u, 20358520u, 133784560u, 752538150u, 3679075400u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 3679075400u, 752538150u, 133784560u, 20358520u, 2598960u, 270725u, 22100u, 1326u, 52u, 1u, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
    { 1u, 53u, 1378u, 23426u, 292825u, 2869685u, 22957480u, 154143080u, 886322710u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 886322710u, 154143080u, 22957480u, 2869685u, 292825u, 23426u, 1378u, 53u, 1u, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
    { 1u, 54u, 1431u, 24804u, 316251u, 3162510u, 25827165u, 177100560u, 1040465790u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 1040465790u, 177100560u, 25827165u, 3162510u, 316251u, 24804u, 1431u, 54u, 1u, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
    { 1u, 55u, 1485u, 26235u, 341055u, 3478761u, 28989675u, 202927725u, 1217566350u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 1217566350u, 202927725u, 28989675u, 3478761u, 341055u, 26235u, 1485u, 55u, 1u, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
    { 1u, 56u, 1540u, 27720u, 367290u, 3819816u, 32468436u, 231917400u, 1420494075u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 1420494075u, 231917400u, 32468436u, 3819816u, 367290u, 27720u, 1540u, 56u, 1u, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
    { 1u, 57u, 1596u, 29260u, 395010u, 4187106u, 36288252u, 264385836u, 1652411475u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 1652411475u, 264385836u, 36288252u, 4187106u, 395010u, 29260u, 1596u, 57u, 1u, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
    { 1u, 58u, 1653u, 30856u, 424270u, 4582116u, 40475358u, 300674088u, 1916797311u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 1916797311u, 300674088u, 40475358u, 4582116u, 424270u, 30856u, 1653u, 58u, 1u, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
    { 1u, 59u, 1711u, 32509u, 455126u, 5006386u, 45057474u, 341149446u, 2217471399u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 2217471399u, 341149446u, 45057474u, 5006386u, 455126u, 32509u, 1711u, 59u, 1u, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
    { 1u, 60u, 1770u, 34220u, 487635u, 5461512u, 50063860u, 386206920u, 2558620845u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 2558620845u, 386206920u, 50063860u, 5461512u, 487635u, 34220u, 1770u, 60u, 1u, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
    { 1u, 61u, 1830u, 35990u, 521855u, 5949147u, 55525372u, 436270780u, 2944827765u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 2944827765u, 436270780u, 55525372u, 5949147u, 521855u, 35990u, 1830u, 61u, 1u, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
    { 1u, 62u, 1891u, 37820u, 557845u, 6471002u, 61474519u, 491796152u, 3381098545u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 3381098545u, 491796152u, 61474519u, 6471002u, 557845u, 37820u, 1891u, 62u, 1u, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
    { 1u, 63u, 1953u, 39711u, 595665u, 7028847u, 67945521u, 553270671u, 3872894697u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 3872894697u, 553270671u, 67945521u, 7028847u, 595665u, 39711u, 1953u, 63u, 1u, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
    { 1u, 64u, 2016u, 41664u, 635376u, 7624512u, 74974368u, 621216192u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 621216192u, 74974368u, 7624512u, 635376u, 41664u, 2016u, 64u, 1u, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
    { 1u, 65u, 2080u, 43680u, 677040u, 8259888u, 82598880u, 696190560u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 696190560u, 82598880u, 8259888u, 677040u, 43680u, 2080u, 65u, 1u, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
    { 1u, 66u, 2145u, 45760u, 720720u, 8936928u, 90858768u, 778789440u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 778789440u, 90858768u, 8936928u, 720720u, 45760u, 2145u, 66u, 1u, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
    { 1u, 67u, 2211u, 47905u, 766480u, 9657648u, 99795696u, 869648208u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 869648208u, 99795696u, 9657648u, 766480u, 47905u, 2211u, 67u, 1u, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
    { 1u, 68u, 2278u, 50116u, 814385u, 10424128u, 109453344u, 969443904u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 969443904u, 109453344u, 10424128u, 814385u, 50116u, 2278u, 68u, 1u, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
    { 1u, 69u, 2346u, 52394u, 864501u, 11238513u, 119877472u, 1078897248u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 1078897248u, 119877472u, 11238513u, 864501u, 52394u, 2346u, 69u, 1u, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
    { 1u, 70u, 2415u, 54740u, 916895u, 12103014u, 131115985u, 1198774720u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 1198774720u, 131115985u, 12103014u, 916895u, 54740u, 2415u, 70u, 1u, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
    { 1u, 71u, 2485u, 57155u, 971635u, 13019909u, 143218999u, 1329890705u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 1329890705u, 143218999u, 13019909u, 971635u, 57155u, 2485u, 71u, 1u, 0, 0, 0, 0, 0, 0, 0, 0 },
    { 1u, 72u, 2556u, 59640u, 1028790u, 13991544u, 156238908u, 1473109704u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 1473109704u, 156238908u, 13991544u, 1028790u, 59640u, 2556u, 72u, 1u, 0, 0, 0, 0, 0, 0, 0 },
    { 1u, 73u, 2628u, 62196u, 1088430u, 15020334u, 170230452u, 1629348612u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 1629348612u, 170230452u, 15020334u, 1088430u, 62196u, 2628u, 73u, 1u, 0, 0, 0, 0, 0, 0 },
    { 1u, 74u, 2701u, 64824u, 1150626u, 16108764u, 185250786u, 1799579064u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 1799579064u, 185250786u, 16108764u, 1150626u, 64824u, 2701u, 74u, 1u, 0, 0, 0, 0, 0 },
    { 1u, 75u, 2775u, 67525u, 1215450u, 17259390u, 201359550u, 1984829850u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 1984829850u, 201359550u, 17259390u, 1215450u, 67525u, 2775u, 75u, 1u, 0, 0, 0, 0 },
    { 1u, 76u, 2850u, 70300u, 1282975u, 18474840u, 218618940u, 2186189400u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 2186189400u, 218618940u, 18474840u, 1282975u, 70300u, 2850u, 76u, 1u, 0, 0, 0 },
    { 1u, 77u, 2926u, 73150u, 1353275u, 19757815u, 237093780u, 2404808340u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 2404808340u, 237093780u, 19757815u, 1353275u, 73150u, 2926u, 77u, 1u, 0, 0 },
    { 1u, 78u, 3003u, 76076u, 1426425u, 21111090u, 256851595u, 2641902120u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 2641902120u, 256851595u, 21111090u, 1426425u, 76076u, 3003u, 78u, 1u, 0 },
    { 1u, 79u, 3081u, 79079u, 1502501u, 22537515u, 277962685u, 2898753715u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 2898753715u, 277962685u, 22537515u, 1502501u, 79079u, 3081u, 79u, 1u },
};
