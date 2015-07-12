import freeOrionAIInterface as fo  # pylint: disable=import-error
import FreeOrionAI as foAI
import AIDependencies
import AIstate
import traceback
import ColonisationAI
import ShipDesignAI
import random

from freeorion_tools import tech_is_complete

priorities = {}
empire_stars = {}

# TODO research AI no longer use this method, rename and move this method elsewhere
def get_research_index():
    empire_id = fo.empireID()
    research_index = empire_id % 2
    if foAI.foAIstate.aggression >= fo.aggression.aggressive:  # maniacal
        research_index = 2 + (empire_id % 3)  # so indices [2,3,4]
    elif foAI.foAIstate.aggression >= fo.aggression.typical:
        research_index += 1
    return research_index

def has_star(star_type):
    if star_type not in empire_stars:
        empire_stars[star_type] = len(AIstate.empireStars.get(star_type, [])) != 0
    return empire_stars[star_type]

def has_only_bad_colonizers():
    most_adequate = 0
    for specName in ColonisationAI.empire_colonizers:
        environs = {}
        this_spec = fo.getSpecies(specName)
        if not this_spec:
            continue
        for ptype in [fo.planetType.swamp, fo.planetType.radiated, fo.planetType.toxic, fo.planetType.inferno, fo.planetType.barren, fo.planetType.tundra, fo.planetType.desert, fo.planetType.terran, fo.planetType.ocean, fo.planetType.asteroids]:
            environ = this_spec.getPlanetEnvironment(ptype)
            environs.setdefault(environ, []).append(ptype)
        most_adequate = max(most_adequate, len(environs.get(fo.planetEnvironment.adequate, [])))
    return most_adequate == 0

def get_defense_priority():
    # TODO reduce priority at very early stage for defense techs, until enemies seen
    if 'defense' not in priorities:
        priorities['defense'] = 2 if foAI.foAIstate.aggression <= fo.aggression.cautious else 1
    return priorities['defense']

def get_production_boost_priority():
    return 1.5

def get_research_boost_priority():
    return 2

def get_production_and_research_boost_priority():
    return 3

def get_population_boost_priority():
    return 2

def get_supply_boost_priority():
    # TODO consider starlane density and planet density instead
    if 'supply' not in priorities:
        priorities['supply'] = 2 if ColonisationAI.galaxy_is_sparse() else 0.5
    return priorities['supply']

def get_meter_change_boost_priority():
    return 1

def get_detection_priority():
    return 1  # TODO consider stealth of enemies

def get_stealth_priority():
    return 0  # TODO stealthy species want more stealth techs

def get_genome_bank_priority():
    # TODO boost genome bank if enemy is using bioterror
    return 1

def get_xeno_genetics_priority():
    if foAI.foAIstate.aggression < fo.aggression.cautious:
        return get_population_boost_priority()
    if has_only_bad_colonizers():
        # Empire only have lousy colonisers, xeno-genetics are really important for them
        return get_population_boost_priority() * 3
    else:
        return get_population_boost_priority()

def get_xenoarch_priority():
    if foAI.foAIstate.aggression < fo.aggression.typical:
        return 1
    return 5 if ColonisationAI.gotRuins else 0 # get xenoarcheology when we have ruins, otherwise it is useless

def get_artificial_black_hole_priority():
    if has_star(fo.starType.blackHole) or not has_star(fo.starType.red):
        return 0
    for tech in AIDependencies.SHIP_TECHS_REQUIRING_BLACK_HOLE:
        if tech_is_complete(tech):
            return 999
    return 1

def get_nest_domestication_priority():
    if foAI.foAIstate.aggression < fo.aggression.typical:
        return 1
    return 3 if ColonisationAI.got_nest else 0

def get_priority(tech_name):
    """
    Get tech priority. 1 is default. 0 if not useful (but doesn't hurt to research),
    < 0 to prevent AI to research it
    """

    rng = random.Random()
    rng.seed(fo.getEmpire().name + fo.getGalaxySetupData().seed)

    shield = 1.25 # shields are more powerful than armors or weapons
    hull = 1
    offtrack_hull = 0.05
    offtrack_subhull = 0.25
    # select one hull and specialize it, but some AI may want to have more hulls, by random
    chosen_hull = rng.randrange(4)
    org = hull if chosen_hull % 2 == 0 or rng.random() < 0.05 else offtrack_hull
    robotic = hull if chosen_hull % 2 == 1 or rng.random() < 0.05 else offtrack_hull
    if ColonisationAI.got_ast:
        extra = rng.random() < 0.05
        asteroid = hull if chosen_hull == 2 or extra else offtrack_hull
        if asteroid == hull and not extra:
            org = offtrack_hull
            robotic = offtrack_hull
    else:
        asteroid = offtrack_hull
    if has_star(fo.starType.blue) or has_star(fo.starType.blackHole):
        extra = rng.random() < 0.05
        energy = hull if chosen_hull == 3 or extra else offtrack_hull
        if energy == hull and not extra:
            org = offtrack_hull
            robotic = offtrack_hull
            asteroid = offtrack_hull
    else:
        energy = offtrack_hull

    # TODO consider subhulls, weapons, armors, engines and fuels by estimating their strengths
    # https://github.com/freeorion/freeorion/pull/178
    # further specialization for robotic hulls
    chosen_subhull = rng.randrange(2)
    contgrav = hull if robotic == hull and chosen_subhull == 0 else offtrack_subhull
    nanorobo = hull if robotic == hull and chosen_subhull == 1 else offtrack_subhull
    flux = hull if robotic == hull and rng.random() < 0.5 else offtrack_subhull
    # further specialization for asteroid hulls
    chosen_subhull = rng.randrange(3)
    astheavy = hull if asteroid == hull and chosen_subhull == 0 else offtrack_subhull
    astswarm = hull if asteroid == hull and chosen_subhull == 1 else offtrack_subhull
    astcamo = hull if asteroid == hull and chosen_subhull == 2 else offtrack_subhull
    # further specialization for organic hulls
    chosen_subhull = rng.randrange(2)
    orgneural = hull if org == hull and chosen_subhull == 0 else offtrack_subhull
    orgraven = hull if org == hull and chosen_subhull == 1 else offtrack_subhull
    orgendosym = hull if org == hull and rng.random() < 0.5 else offtrack_subhull
    # further specialization for energy hulls
    chosen_subhull = rng.randrange(2)
    energyfrac = hull if energy == hull and chosen_subhull == 0 else offtrack_subhull
    energymag = hull if energy == hull and chosen_subhull == 1 else offtrack_subhull
    # repair techs may be skipped if AI decides to go for nanorobotic hull which full-repairs
    repair = 1 if not nanorobo == hull or rng.random() < 0.75 else 0.3

    # (Disabled) AI may skip weapon lines
    weapon = 1
    # massdriver = weapon if rng.random() < 0.75 else 0
    # laser = weapon if (rng.random() < 0.4 if massdriver == weapon else rng.random() < 0.75) else 0
    # plasmacannon = weapon if (rng.random() < 0.4 if laser == weapon else rng.random() < 0.75) else 0
    massdriver = weapon
    laser = weapon
    plasmacannon = weapon
    deathray = weapon

    armor = 1

    engine = 1 if (rng.random() < 0.8 if ColonisationAI.galaxy_is_sparse() else rng.random() < 0.4) else 0
    fuel = 1 if (rng.random() < 0.8 if ColonisationAI.galaxy_is_sparse() else rng.random() < 0.4) else 0

    if tech_name in AIDependencies.UNRESEARCHABLE_TECHS:
        return -1

    if tech_name in AIDependencies.UNUSED_TECHS:
        return 0

    if tech_name in AIDependencies.THEORY_TECHS:
        return 0

    # defense
    if tech_name.startswith(AIDependencies.DEFENSE_TECHS_PREFIX):
        return get_defense_priority()

    # production
    if tech_name in AIDependencies.PRODUCTION_BOOST_TECHS:
        return get_production_boost_priority()

    if tech_name == AIDependencies.PRO_MICROGRAV_MAN:
        return get_production_boost_priority() if ColonisationAI.got_ast else 0

    if tech_name == AIDependencies.PRO_ORBITAL_GEN:
        return get_production_boost_priority if ColonisationAI.got_gg else 0

    if tech_name == AIDependencies.PRO_SINGULAR_GEN:
        return get_production_boost_priority if has_star(fo.starType.blackHole) else 0

    # research
    if tech_name in AIDependencies.RESEARCH_BOOST_TECHS:
        return get_research_boost_priority()

    if tech_name in AIDependencies.PRODUCTION_AND_RESEARCH_BOOST_TECHS:
        return get_production_and_research_boost_priority()

    # growth
    if tech_name in AIDependencies.POPULATION_BOOST_TECHS:
        return get_population_boost_priority()

    if tech_name == AIDependencies.GRO_XENO_GENETICS:
        return get_xeno_genetics_priority()

    # supply
    if tech_name in AIDependencies.SUPPLY_BOOST_TECHS:
        return get_supply_boost_priority()

    # meter change
    if tech_name in AIDependencies.METER_CHANGE_BOOST_TECHS:
        return get_meter_change_boost_priority()

    # detection
    if tech_name in AIDependencies.DETECTION_TECHS:
        return get_detection_priority()

    # Stealth
    if tech_name in AIDependencies.STEALTH_TECHS:
        return get_stealth_priority()

    # xenoarcheology
    if tech_name == AIDependencies.LRN_XENOARCH:
        return get_xenoarch_priority()

    # artificial black hole
    if tech_name == AIDependencies.LRN_ART_BLACK_HOLE:
        return get_artificial_black_hole_priority()

    # genome bank (its tech)
    if tech_name == AIDependencies.GRO_GENOME_BANK:
        return get_genome_bank_priority()

    # concentration camp
    if tech_name == AIDependencies.CON_CONC_CAMP:
        return 0  # TODO Concentration camps are now disabled

    # tames space monsters
    if tech_name == AIDependencies.NEST_DOMESTICATION_TECH:
        return get_nest_domestication_priority()

    # Production
    if tech_name in ["PRO_NEUTRONIUM_EXTRACTION"]:
        return armor if has_star(fo.starType.neutron) else 0 # application of neutronium extraction is armor only for now

    # Robotic hulls
    if tech_name in ["SHP_MIL_ROBO_CONT", "SHP_MIDCOMB_LOG"]:
        return robotic
    if tech_name in ["SHP_SPACE_FLUX_DRIVE", "SHP_TRANSSPACE_DRIVE"]:
        return min(robotic, flux)
    if tech_name in ["SHP_CONTGRAV_MAINT", "SHP_MASSPROP_SPEC"]:
        return min(robotic, contgrav)
    if tech_name in ["SHP_NANOROBO_MAINT"]:
        return min(robotic, nanorobo)
    if tech_name in ["SHP_XENTRONIUM_HULL"]:
        return 1 # this is not a robotic hull!

    # Asteroid hulls
    if tech_name in ["SHP_ASTEROID_HULLS", "SHP_ASTEROID_REFORM", "SHP_MONOMOLEC_LATTICE", "SHP_SCAT_AST_HULL"]:
        return asteroid
    if tech_name in ["SHP_HEAVY_AST_HULL"]:
        return min(asteroid, astheavy)
    if tech_name in ["SHP_CAMO_AST_HULL"]:
        return min(asteroid, astcamo)
    if tech_name in ["SHP_MINIAST_SWARM"]:
        return min(asteroid, astswarm)

    # Organic hulls
    if tech_name in ["SHP_ORG_HULL", "SHP_SENT_HULL"]:
        return org
    if tech_name in ["SHP_MULTICELL_CAST", "SHP_ENDOCRINE_SYSTEMS", "SHP_CONT_BIOADAPT"]:
        return min(org, orgraven)
    if tech_name in ["SHP_MONOCELL_EXP", "SHP_CONT_SYMB", "SHP_BIOADAPTIVE_SPEC"]:
        return min(org, orgneural)
    if tech_name in ["SHP_ENDOSYMB_HULL"]:
        return min(org, orgendosym)

    # energy hulls
    if tech_name in ["SHP_FRC_ENRG_COMP"]:
        return energy
    if tech_name in ["SHP_QUANT_ENRG_MAG"]:
        return min(energy, energymag, 999 if has_star(fo.starType.blue) or has_star(fo.starType.blackHole) else 0)
    if tech_name in ["SHP_ENRG_BOUND_MAN"]:
        return min(energy, energyfrac, 999 if has_star(fo.starType.blue) or has_star(fo.starType.blackHole) else 0)
    if tech_name in ["SHP_SOLAR_CONT"]:
        return min(energy, 999 if has_star(fo.starType.red) or has_star(fo.starType.blackHole) else 0) # red star can be turned into has_black_hole by Artificial black hole

    # damage control
    if tech_name in ["SHP_REINFORCED_HULL"]:
        return armor
    if tech_name in ["SHP_BASIC_DAM_CONT", "SHP_FLEET_REPAIR", "SHP_ADV_DAM_CONT"]:
        return repair

    # ship parts
    if tech_name in ["SHP_IMPROVED_ENGINE_COUPLINGS", "SHP_N_DIMENSIONAL_ENGINE_MATRIX", "SHP_SINGULARITY_ENGINE_CORE"]:
        return engine
    if tech_name in ["SHP_DEUTERIUM_TANK", "SHP_ANTIMATTER_TANK", "SHP_ZERO_POINT"]:
        return fuel

    # ship shields
    if tech_name in ["SHP_DEFLECTOR_SHIELD", "SHP_PLASMA_SHIELD", "SHP_BLACKSHIELD"]:
        return shield
    if tech_name in ["SHP_MULTISPEC_SHIELD"]:
        return max(shield, get_stealth_priority())

    # ship armor TODO include these branches into ship-design calculation
    if tech_name in ["SHP_ROOT_ARMOR", "SHP_ZORTRIUM_PLATE"]:
        return armor
    if tech_name in ["SHP_DIAMOND_PLATE", "SHP_XENTRONIUM_PLATE"]:
        return 0 if asteroid == hull or has_star(fo.starType.neutron) else armor # asteroid hull line and neutronium extraction includes better armors

    # weapons TODO include these branches into ship-design calculation
    if tech_name in ["SHP_ROOT_AGGRESSION", "SHP_WEAPON_1_2", "SHP_WEAPON_1_3", "SHP_WEAPON_1_4"]:
        return massdriver if not tech_is_complete("SHP_WEAPON_4_1") else 0 # don't research obsolete weapons if get deathray from ruins
    if tech_name in ["SHP_WEAPON_2_1", "SHP_WEAPON_2_2", "SHP_WEAPON_2_3", "SHP_WEAPON_2_4"]:
        return laser if not tech_is_complete("SHP_WEAPON_4_1") else 0
    if tech_name in ["SHP_WEAPON_3_1", "SHP_WEAPON_3_2", "SHP_WEAPON_3_3", "SHP_WEAPON_3_4"]:
        return plasmacannon if not tech_is_complete("SHP_WEAPON_4_1") else 0
    if tech_name in ["SHP_WEAPON_4_1", "SHP_WEAPON_4_2", "SHP_WEAPON_4_3", "SHP_WEAPON_4_4"]:
        return deathray

    # default priority for unseen techs
    return 1


def calculate_research_requirements(empire):
    """calculate RPs and prerequisties of every tech"""
    result = {}

    # TODO subtract already spent RPs from research projects
    completed_techs = get_completed_techs()
    for tech_name in fo.techs():
        this_tech = fo.getTech(tech_name)
        prereqs = [preReq for preReq in this_tech.recursivePrerequisites(empire.empireID) if preReq not in completed_techs]
        cost = this_tech.researchCost(empire.empireID)
        for prereq in prereqs:
            cost += fo.getTech(prereq).researchCost(empire.empireID)
        result[tech_name] = (prereqs, cost)

    return result

def generate_research_orders():
    """generate research orders"""
    report_adjustments = False
    empire = fo.getEmpire()
    empire_id = empire.empireID
    enemies_sighted = foAI.foAIstate.misc.get('enemies_sighted', {})
    galaxy_is_sparse = ColonisationAI.galaxy_is_sparse()
    print "Research Queue Management:"
    resource_production = empire.resourceProduction(fo.resourceType.research)
    print "\nTotal Current Research Points: %.2f\n" % resource_production
    print "Techs researched and available for use:"
    completed_techs = sorted(list(get_completed_techs()))
    tlist = completed_techs+3*[" "]
    tlines = zip(tlist[0::3], tlist[1::3], tlist[2::3])
    for tline in tlines:
        print "%25s %25s %25s" % tline
    print

    #
    # report techs currently at head of research queue
    #
    research_queue = empire.researchQueue
    research_queue_list = get_research_queue_techs()
    tech_turns_left = {}
    if research_queue_list:
        print "Techs currently at head of Research Queue:"
        for element in list(research_queue)[:10]:
            tech_turns_left[element.tech] = element.turnsLeft
            this_tech = fo.getTech(element.tech)
            if not this_tech:
                print "Error: can't retrieve tech ", element.tech
                continue
            missing_prereqs = [preReq for preReq in this_tech.recursivePrerequisites(empire_id) if preReq not in completed_techs]
            # unlocked_items = [(uli.name, uli.type) for uli in this_tech.unlocked_items]
            unlocked_items = [uli.name for uli in this_tech.unlockedItems]
            if not missing_prereqs:
                print "    %25s allocated %6.2f RP -- unlockable items: %s " % (element.tech, element.allocation, unlocked_items)
            else:
                print "    %25s allocated %6.2f RP -- missing preReqs: %s -- unlockable items: %s " % (element.tech, element.allocation, missing_prereqs, unlocked_items)
        print

    #
    # calculate all research priorities, as in get_priority(tech) / total cost of tech (including prereqs)
    #
    research_reqs = calculate_research_requirements(empire)
    priorities = {}
    for tech_name in fo.techs():
        priority = get_priority(tech_name)
        if not tech_is_complete(tech_name) and priority >= 0:
            priorities[tech_name] = float(priority) / research_reqs[tech_name][1]

    #
    # put in highest priority techs until all RP spent
    #
    possible = sorted(priorities.keys(), key=priorities.__getitem__)

    print "Research priorities"
    print "    %25s %8s %8s %s" % ("Name", "Priority", "Cost", "Missing Prerequisties")
    for tech_name in possible[-10:]:
        print "    %25s %8.6f %8.2f %s" % (tech_name, priorities[tech_name], research_reqs[tech_name][1], research_reqs[tech_name][0])
    print

    # TODO: Remove the following example code
    # Example/Test code for the new ShipDesigner functionality
    techs = ["SHP_WEAPON_4_2", "SHP_TRANSSPACE_DRIVE", "SHP_INTSTEL_LOG", "SHP_ASTEROID_HULLS", ""]
    for tech in techs:
        this_tech = fo.getTech(tech)
        if not this_tech:
            print "Invalid Tech specified"
            continue
        unlocked_items = this_tech.unlockedItems
        unlocked_hulls = []
        unlocked_parts = []
        for item in unlocked_items:
            if item.type == fo.unlockableItemType.shipPart:
                print "Tech %s unlocks a ShipPart: %s" % (tech, item.name)
                unlocked_parts.append(item.name)
            elif item.type == fo.unlockableItemType.shipHull:
                print "Tech %s unlocks a ShipHull: %s" % (tech, item.name)
                unlocked_hulls.append(item.name)
        if not (unlocked_parts or unlocked_hulls):
            print "No new ship parts/hulls unlocked by tech %s" % tech
            continue
        old_designs = ShipDesignAI.MilitaryShipDesigner().optimize_design(consider_fleet_count=False)
        new_designs = ShipDesignAI.MilitaryShipDesigner().optimize_design(additional_hulls=unlocked_hulls, additional_parts=unlocked_parts, consider_fleet_count=False)
        if not (old_designs and new_designs):
            # AI is likely defeated; don't bother with logging error message
            continue
        old_rating, old_pid, old_design_id, old_cost = old_designs[0]
        old_design = fo.getShipDesign(old_design_id)
        new_rating, new_pid, new_design_id, new_cost = new_designs[0]
        new_design = fo.getShipDesign(new_design_id)
        if new_rating > old_rating:
            print "Tech %s gives access to a better design!" % tech
            print "old best design: Rating %.5f" % old_rating
            print "old design specs: %s - " % old_design.hull, list(old_design.parts)
            print "new best design: Rating %.5f" % new_rating
            print "new design specs: %s - " % new_design.hull, list(new_design.parts)
        else:
            print "Tech %s gives access to new parts or hulls but there seems to be no military advantage." % tech

    total_rp = empire.resourceProduction(fo.resourceType.research)
    print "enqueuing techs. already spent RP: %s total RP: %s" % (fo.getEmpire().researchQueue.totalSpent, total_rp)

    if fo.currentTurn() == 1:
        fo.issueEnqueueTechOrder("LRN_ALGO_ELEGANCE", -1)
    else:
        # some floating point issues can cause AI to enqueue every tech......
        while empire.resourceProduction(fo.resourceType.research) - empire.researchQueue.totalSpent > 0.001 and possible:
            queued_techs = get_research_queue_techs()

            to_research = possible.pop()  # get tech with highest priority
            prereqs, cost = research_reqs[to_research]
            prereqs += [to_research]

            for prereq in prereqs:
                if prereq not in queued_techs:
                    fo.issueEnqueueTechOrder(prereq, -1)
                    print "    enqueued tech " + prereq + "  : cost: " + str(fo.getTech(prereq).researchCost(empire.empireID)) + "RP"

            fo.updateResearchQueue()
        print


def get_completed_techs():
    """get completed and available for use techs"""
    return [tech for tech in fo.techs() if tech_is_complete(tech)]

def get_research_queue_techs():
    """ Get list of techs in research queue."""
    return [element.tech for element in fo.getEmpire().researchQueue]
