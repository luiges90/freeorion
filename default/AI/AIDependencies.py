import freeOrionAIInterface as fo  # interface used to interact with FreeOrion AI client  # pylint: disable=import-error

#
#  Miscellaneous
#

# TODO look into (enabling) simply retrieving the below values via UserString
INDUSTRY_PER_POP = 0.2

RESEARCH_PER_POP = 0.2

TROOPS_PER_POP = 0.2

TECH_COST_MULTIPLIER = 2.0


#
# Specials details (some specials are instead covered in the section they most directly affect
#
metabolismBoostMap = {"ORGANIC": ["FRUIT_SPECIAL", "PROBIOTIC_SPECIAL", "SPICE_SPECIAL"],
                      "LITHIC": ["CRYSTALS_SPECIAL", "ELERIUM_SPECIAL", "MINERALS_SPECIAL"],
                      "ROBOTIC": ["MONOPOLE_SPECIAL", "POSITRONIUM_SPECIAL", "SUPERCONDUCTOR_SPECIAL"],
                      "SELF_SUSTAINING": []
                      }

metabolismBoosts = {}
for metab, boosts in metabolismBoostMap.items():
    for boost in boosts:
        metabolismBoosts[boost] = metab

HONEYCOMB_IND_MULTIPLIER = 2.5
COMPUTRONIUM_RES_MULTIPLIER = 1.0

#
# Colonization details
#
COLONY_POD_COST = 120
COLONY_POD_UPKEEP = 0.06
OUTPOST_POD_COST = 50
SHIP_UPKEEP = 0.01

OUTPOSTING_TECH = "SHP_GAL_EXPLO"

#
#  Supply details
#
supply_range_techs = {"CON_ORBITAL_CON": 1, "CON_CONTGRAV_ARCH": 1, "CON_GAL_INFRA": 1}
supply_by_size = {fo.planetSize.tiny: 2,
                  fo.planetSize.small: 1,
                  fo.planetSize.large: -1,
                  fo.planetSize.huge: -2,
                  fo.planetSize.gasGiant: -1
                  }

SUPPLY_MOD_SPECIALS = {'WORLDTREE_SPECIAL': {-1: 1}}

# building supply bonuses are keyed by planet size; key -1 stands for any planet size
building_supply = {"BLD_IMPERIAL_PALACE": {-1: 2},
                   "BLD_MEGALITH": {-1: 2},
                   "BLD_SPACE_ELEVATOR": {fo.planetSize.tiny: 1,
                                          fo.planetSize.small: 2,
                                          fo.planetSize.medium: 3,
                                          fo.planetSize.large: 4,
                                          fo.planetSize.huge: 5,
                                          fo.planetSize.gasGiant: 4,
                                          },
                   }

#
# tech names etc.
PRO_ORBITAL_GEN = "PRO_ORBITAL_GEN"
PRO_SOL_ORB_GEN = "PRO_SOL_ORB_GEN"
PRO_MICROGRAV_MAN = "PRO_MICROGRAV_MAN"
PRO_SINGULAR_GEN = "PRO_SINGULAR_GEN"
PROD_AUTO_NAME = "PRO_SENTIENT_AUTOMATION"
NEST_DOMESTICATION_TECH = "SHP_DOMESTIC_MONSTER"

ART_MINDS = "LRN_ARTIF_MINDS"
LRN_ALGO_ELEGANCE = "LRN_ALGO_ELEGANCE"
LRN_QUANT_NET = "LRN_QUANT_NET"
LRN_XENOARCH = "LRN_XENOARCH"
LRN_ART_BLACK_HOLE = "LRN_ART_BLACK_HOLE"

GRO_XENO_GENETICS = "GRO_XENO_GENETICS"
GRO_GENOME_BANK = "GRO_GENETIC_MED"

CON_CONC_CAMP = "CON_CONC_CAMP"

TECH_EXCLUSION_MAP_1 = {"LRN_TRANSCEND": fo.aggression.typical}  # (k,v) exclude tech k if aggression is less than v
TECH_EXCLUSION_MAP_2 = {}  # (k,v) exclude tech k if aggression is greater than v

FIRST_PLANET_SHIELDS_TECH = "LRN_FORCE_FIELD"
PLANET_BARRIER_I_TECH = "DEF_PLAN_BARRIER_SHLD_1"
DEFENSE_REGEN_1_TECH = "DEF_DEFENSE_NET_REGEN_1"

PROT_FOCUS_MULTIPLIER = 2.0

# TODO obtain this information from techs.txt
UNRESEARCHABLE_TECHS = ["SHP_KRILL_SPAWN", "DEF_PLANET_CLOAK"]

UNUSED_TECHS = ["LRN_SPATIAL_DISTORT_GEN", "LRN_GATEWAY_VOID", "LRN_PSY_DOM",
                "GRO_TERRAFORM", "GRO_BIOTERROR", "GRO_GAIA_TRANS",
                "PRO_NDIM_ASSMB",
                "CON_ORGANIC_STRC", "CON_PLANET_DRIVE", "CON_STARGATE",
                "CON_ART_HEAVENLY", "CON_ART_PLANET",
                "SHP_NOVA_BOMB", "SHP_DEATH_SPORE", "SHP_BIOTERM"]

THEORY_TECHS = ["LRN_PHYS_BRAIN", "LRN_TRANSLING_THT", "LRN_PSIONICS", "LRN_GRAVITONICS", "LRN_EVERYTHING", "LRN_MIND_VOID", "LRN_NDIM_SUBSPACE", "LRN_TIME_MECH",
                "GRO_PLANET_ECOL", "GRO_GENETIC_ENG", "GRO_ADV_ECOMAN", "GRO_NANOTECH_MED", "GRO_TRANSORG_SENT",
                "PRO_NANOTECH_PROD", "PRO_ZERO_GEN",
                "CON_ASYMP_MATS", "CON_ARCH_PSYCH",
                "SHP_GAL_EXPLO"]

DEFENSE_TECHS_PREFIX = "DEF"

PRODUCTION_BOOST_TECHS = ["PRO_ROBOTIC_PROD", "PRO_FUSION_GEN", "PRO_SENTIENT_AUTOMATION",
                          "PRO_INDUSTRY_CENTER_I", "PRO_INDUSTRY_CENTER_II", "PRO_INDUSTRY_CENTER_III",
                          "PRO_SOL_ORB_GEN"]

RESEARCH_BOOST_TECHS = ["LRN_ALGO_ELEGANCE", "LRN_ARTIF_MINDS", "LRN_DISTRIB_THOUGHT", "LRN_QUANT_NET", "LRN_STELLAR_TOMOGRAPHY",
                        "LRN_ENCLAVE_VOID"]

PRODUCTION_AND_RESEARCH_BOOST_TECHS = ["LRN_UNIF_CONC", "GRO_ENERGY_META"]

POPULATION_BOOST_TECHS = ["GRO_SYMBIOTIC_BIO", "GRO_XENO_HYBRIDS", "GRO_CYBORG", "GRO_SUBTER_HAB",
                          "CON_ORBITAL_HAB", "CON_NDIM_STRC"]

SUPPLY_BOOST_TECHS = ["CON_ARCH_MONOFILS", "CON_GAL_INFRA", "CON_CONTGRAV_ARCH", "CON_ORBITAL_CON"]

METER_CHANGE_BOOST_TECHS = ["CON_FRC_ENRG_STRC", "CON_TRANS_ARCH"]

DETECTION_TECHS = ["SPY_DETECT_1", "SPY_DETECT_2", "SPY_DETECT_3", "SPY_DETECT_4", "SPY_DETECT_5", "SPY_DIST_MOD", "SPY_LIGHTHOUSE"]
STEALTH_TECHS = ["SPY_STEALTH_1", "SPY_STEALTH_2", "SPY_STEALTH_3", "SPY_STEALTH_4", "CON_FRC_ENRG_CAMO"]

COLONY_UPGRADE_TECHS = ["GRO_LIFECYCLE_MAN"]
TROOP_UPGRADE_TECHS = ["GRO_NANO_CYBERNET"]

SHIP_TECHS_REQUIRING_BLACK_HOLE = ["SHP_SOLAR_CONT"]

# ship facilities info, dict keyed by building name, value is (min_aggression, prereq_bldg, base_cost, time)
# not currently determined dynamically because it is initially used in a location-independent fashion
# note that BLD_SHIPYARD_BASE is not an absolute prereq for BLD_NEUTRONIUM_FORGE, but is a practical one
SHIP_FACILITIES = {
    "BLD_SHIPYARD_BASE": (0, "", 10, 4),
    "BLD_SHIPYARD_ORBITAL_DRYDOCK": (0, "BLD_SHIPYARD_BASE", 20, 5),
    "BLD_SHIPYARD_CON_NANOROBO": (fo.aggression.aggressive, "BLD_SHIPYARD_ORBITAL_DRYDOCK", 250, 5),
    "BLD_SHIPYARD_CON_GEOINT": (fo.aggression.aggressive, "BLD_SHIPYARD_ORBITAL_DRYDOCK", 750, 5),
    "BLD_SHIPYARD_CON_ADV_ENGINE": (0, "BLD_SHIPYARD_ORBITAL_DRYDOCK", 500, 5),
    "BLD_SHIPYARD_AST": (fo.aggression.typical, "", 75, 5),
    "BLD_SHIPYARD_AST_REF": (fo.aggression.maniacal, "BLD_SHIPYARD_AST", 500, 5),
    "BLD_SHIPYARD_ORG_ORB_INC": (0, "BLD_SHIPYARD_BASE", 40, 8),
    "BLD_SHIPYARD_ORG_CELL_GRO_CHAMB": (fo.aggression.aggressive, "BLD_SHIPYARD_ORG_ORB_INC", 64, 8),
    "BLD_SHIPYARD_ORG_XENO_FAC": (fo.aggression.aggressive, "BLD_SHIPYARD_ORG_ORB_INC", 120, 8),
    "BLD_SHIPYARD_ENRG_COMP": (fo.aggression.aggressive, "BLD_SHIPYARD_BASE", 200, 5),
    "BLD_SHIPYARD_ENRG_SOLAR": (fo.aggression.maniacal, "BLD_SHIPYARD_ENRG_COMP", 1200, 5),
    "BLD_NEUTRONIUM_FORGE": (fo.aggression.cautious, "BLD_SHIPYARD_BASE", 100, 3),
}

# those facilities that need merely be in-system
SYSTEM_SHIP_FACILITIES = {
    "BLD_SHIPYARD_AST",
    "BLD_SHIPYARD_AST_REF",
}

FULL_REPAIR = 1e6  # arbitrary large number higher than any structure.
FULL_FUEL = 1e6
BASE_DETECTION = 25


PART_KRILL_SPAWNER = "SP_KRILL_SPAWNER"

# known tokens the AI can handle
REPAIR_PER_TURN = "REPAIR_PER_TURN"
FUEL_PER_TURN = "FUEL_PER_TURN"
STEALTH_MODIFIER = "STEALTH_MODIFIER"
ASTEROID_STEALTH = "ASTEROID_STEALTH"
SOLAR_STEALTH = "SOLAR_STEALTH"
SHIELDS = "SHIELDS"
DETECTION = "DETECTION"                 # do only specify if irregular detection
ORGANIC_GROWTH = "ORGANIC_GROWTH"       # structure for value is (per_turn, maximum)
STACKING_RULES = "STACKING_RULES"       # expects a list of stacking rules
# stacking rules
NO_EFFECT_WITH_CLOAKS = "NO_EFFECT_WITH_CLOAKS"

HULL_EFFECTS = {
    # Robotic line
    "SH_ROBOTIC": {REPAIR_PER_TURN: 2},
    "SH_SPATIAL_FLUX": {STEALTH_MODIFIER: -30},
    "SH_NANOROBOTIC": {REPAIR_PER_TURN: FULL_REPAIR},
    "SH_LOGISTICS_FACILITATOR": {REPAIR_PER_TURN: FULL_REPAIR},
    # Asteroid line
    "SH_SMALL_ASTEROID": {ASTEROID_STEALTH: 20},
    "SH_ASTEROID": {ASTEROID_STEALTH: 20},
    "SH_HEAVY_ASTEROID": {ASTEROID_STEALTH: 20},
    "SH_SMALL_CAMOUFLAGE_ASTEROID": {ASTEROID_STEALTH: 20},
    "SH_CAMOUFLAGE_ASTEROID": {ASTEROID_STEALTH: 40},
    "SH_CRYSTALLIZED_ASTEROID": {ASTEROID_STEALTH: 20},
    "SH_MINIASTEROID_SWARM": {ASTEROID_STEALTH: 20, SHIELDS: 5},
    "SH_SCATTERED_ASTEROID": {ASTEROID_STEALTH: 40, SHIELDS: 3},
    # Organic line
    "SH_ORGANIC": {REPAIR_PER_TURN: 2, FUEL_PER_TURN: 0.2, DETECTION: 10, ORGANIC_GROWTH: (0.2, 5)},
    "SH_ENDOMORPHIC": {DETECTION: 50, ORGANIC_GROWTH: (0.5, 15)},
    "SH_SYMBIOTIC": {REPAIR_PER_TURN: 2, FUEL_PER_TURN: 0.2, DETECTION: 50, ORGANIC_GROWTH: (0.2, 10)},
    "SH_PROTOPLASMIC": {REPAIR_PER_TURN: 2, FUEL_PER_TURN: 0.2, DETECTION: 50, ORGANIC_GROWTH: (0.5, 25)},
    "SH_ENDOSYMBIOTIC": {REPAIR_PER_TURN: 2, FUEL_PER_TURN: 0.2, DETECTION: 50, ORGANIC_GROWTH: (0.5, 15)},
    "SH_RAVENOUS": {DETECTION: 75, ORGANIC_GROWTH: (0.5, 20)},
    "SH_BIOADAPTIVE": {REPAIR_PER_TURN: FULL_REPAIR, FUEL_PER_TURN: 0.2,
                       DETECTION: 75, ORGANIC_GROWTH: (0.5, 25)},
    "SH_SENTIENT": {REPAIR_PER_TURN: 2, FUEL_PER_TURN: 0.2, DETECTION: 70,
                    ORGANIC_GROWTH: (1, 45), STEALTH_MODIFIER: 20},
    # Energy Line
    "SH_SOLAR": {SOLAR_STEALTH: 120, FUEL_PER_TURN: FULL_FUEL}
}

PART_EFFECTS = {
    "SH_MULTISPEC": {SOLAR_STEALTH: 60},
    "FU_TRANSPATIAL_DRIVE": {},  # not supported yet
    "FU_RAMSCOOP": {FUEL_PER_TURN: 0.1},
    "FU_ZERO_FUEL": {FUEL_PER_TURN: FULL_FUEL},
    "SP_DISTORTION_MODULATOR": {},  # not supported yet
    "SH_ROBOTIC_INTERFACE_SHIELDS": {},  # not supported yet
    PART_KRILL_SPAWNER: {STEALTH_MODIFIER: 40, STACKING_RULES: [NO_EFFECT_WITH_CLOAKS]}
}

