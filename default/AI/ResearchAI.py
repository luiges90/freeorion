import freeOrionAIInterface as fo  # pylint: disable=import-error
import FreeOrionAI as foAI
import AIDependencies
import AIstate
import traceback
import ColonisationAI
import ShipDesignAI
import random

from ProductionAI import get_design_cost
from freeorion_tools import tech_is_complete, get_ai_tag_grade

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

def get_max_stealth_species():
    stealth_grades = {'BAD': -15, 'GOOD': 15, 'GREAT': 40, 'ULTIMATE': 60}
    stealth = -999
    stealth_species = ""
    for specName in ColonisationAI.empire_colonizers:
        this_spec = fo.getSpecies(specName)
        if not this_spec:
            continue
        this_stealth = stealth_grades.get(get_ai_tag_grade(list(this_spec.tags), "STEALTH"), 0)
        if this_stealth > stealth:
            stealth_species = specName
            stealth = this_stealth
    result = (stealth_species, stealth)
    return result

def get_ship_tech_usefulness(tech, ship_designer):
    this_tech = fo.getTech(tech)
    if not this_tech:
        print "Invalid Tech specified"
        return 0
    unlocked_items = this_tech.unlockedItems
    unlocked_hulls = []
    unlocked_parts = []
    for item in unlocked_items:
        if item.type == fo.unlockableItemType.shipPart:
            unlocked_parts.append(item.name)
        elif item.type == fo.unlockableItemType.shipHull:
            unlocked_hulls.append(item.name)
    if not (unlocked_parts or unlocked_hulls):
        return 0
    old_designs = ship_designer.optimize_design(consider_fleet_count=False)
    new_designs = ship_designer.optimize_design(additional_hulls=unlocked_hulls, additional_parts=unlocked_parts, consider_fleet_count=False)
    if not (old_designs and new_designs):
        # AI is likely defeated; don't bother with logging error message
        return 0
    old_rating, old_pid, old_design_id, old_cost = old_designs[0]
    old_design = fo.getShipDesign(old_design_id)
    old_rating = old_rating
    new_rating, new_pid, new_design_id, new_cost = new_designs[0]
    new_design = fo.getShipDesign(new_design_id)
    new_rating = new_rating
    if new_rating > old_rating:
        ratio = (new_rating - old_rating) / (new_rating + old_rating)
        return ratio * 1.5 + 0.5
    else:
        return 0

def get_defense_priority(rng):
    if foAI.foAIstate.aggression <= fo.aggression.cautious:
        print "AI is cautious. Increasing priority for defense techs."
        return 2
    if foAI.foAIstate.misc.get('enemies_sighted', {}):
        return 1
    else:
        return 0.2

def get_production_boost_priority(rng):
    return 1.5

def get_research_boost_priority(rng):
    return 2

def get_production_and_research_boost_priority(rng):
    return 2.5

def get_population_boost_priority(rng):
    return 2

def get_supply_boost_priority(rng):
    # TODO consider starlane density and planet density
    return 1

def get_meter_change_boost_priority(rng):
    return 1

def get_detection_priority(rng):
    # TODO consider stealth of enemies
    return 1

def get_weapon_priority(rng):
    if foAI.foAIstate.misc.get('enemies_sighted', {}):
        return 1
    else:
        return 0.1

def get_armor_priority(rng):
    if foAI.foAIstate.misc.get('enemies_sighted', {}):
        return 1
    else:
        return 0.1

def get_shield_priority(rng):
    if foAI.foAIstate.misc.get('enemies_sighted', {}):
        return 1
    else:
        return 0.1

def get_engine_priority(rng):
    return 1 if rng.random() < 0.7 else 0

def get_fuel_priority(rng):
    return 1 if rng.random() < 0.7 else 0

def get_troop_pod_priority(rng):
    if foAI.foAIstate.misc.get('enemies_sighted', {}):
        return 1
    else:
        return 0

def get_colony_pod_priority(rng):
    return 1

def get_stealth_priority(rng):
    max_stealth_species = get_max_stealth_species()
    if max_stealth_species[1] > 0:
        print "Has a stealthy species %s. Increase stealth tech priority" % max_stealth_species[0]
        return 2.5
    else:
        return 0

def get_genome_bank_priority(rng):
    # TODO boost genome bank if enemy is using bioterror
    return 1

def get_xeno_genetics_priority(rng):
    if foAI.foAIstate.aggression < fo.aggression.cautious:
        return get_population_boost_priority(rng)
    if has_only_bad_colonizers():
        # Empire only have lousy colonisers, xeno-genetics are really important for them
        print "Empire has only lousy colonizers, increase priority to xeno_genetics"
        return get_population_boost_priority(rng) * 3
    else:
        return get_population_boost_priority(rng)

def get_xenoarch_priority(rng):
    if foAI.foAIstate.aggression < fo.aggression.typical:
        return 1
    if ColonisationAI.gotRuins:
        print "Empire has ruins, increase priority to xenoarch"
        return 5
    else:
        return 0

def get_artificial_black_hole_priority(rng):
    if has_star(fo.starType.blackHole) or not has_star(fo.starType.red):
        print "Already have black hole, or does not have a red star to turn to black hole. Skipping ART_BLACK_HOLE"
        return 0
    for tech in AIDependencies.SHIP_TECHS_REQUIRING_BLACK_HOLE:
        if tech_is_complete(tech):
            print "Solar hull is researched, needs a black hole to produce it. Research ART_BLACK_HOLE now!"
            return 999
    return 1

def get_nest_domestication_priority(rng):
    if foAI.foAIstate.aggression < fo.aggression.typical:
        return 0
    if ColonisationAI.got_nest:
        print "Monster nest found. Increase priority to nest domestication"
        return 3
    else:
        return 0

def get_damage_control_priority(rng):
    if foAI.foAIstate.misc.get('enemies_sighted', {}):
        return 0.5
    else:
        return 0.1

def get_hull_priority(rng, tech_name):
    hull = 1
    offtrack_hull = 0.05

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
        asteroid = 0
    if has_star(fo.starType.blue) or has_star(fo.starType.blackHole):
        extra = rng.random() < 0.05
        energy = hull if chosen_hull == 3 or extra else offtrack_hull
        if energy == hull and not extra:
            org = offtrack_hull
            robotic = offtrack_hull
            asteroid = offtrack_hull
    else:
        energy = 0

    useful = max(
        get_ship_tech_usefulness(tech_name, ShipDesignAI.MilitaryShipDesigner()),
        get_ship_tech_usefulness(tech_name, ShipDesignAI.StandardTroopShipDesigner()),
        get_ship_tech_usefulness(tech_name, ShipDesignAI.StandardColonisationShipDesigner()))
    
    if foAI.foAIstate.misc.get('enemies_sighted', {}):
        aggression = 1
    else:
        aggression = 0.1
    
    if tech_name in AIDependencies.ROBOTIC_HULL_TECHS:
        return robotic * useful * aggression
    elif tech_name in AIDependencies.ORGANIC_HULL_TECHS:
        return org * useful * aggression
    elif tech_name in AIDependencies.ASTEROID_HULL_TECHS:
        return asteroid * useful * aggression
    elif tech_name in AIDependencies.ENERGY_HULL_TECHS:
        return energy * useful * aggression
    else:
        return useful * aggression

def get_priority(rng, tech_name):
    """
    Get tech priority. 1 is default. 0 if not useful (but doesn't hurt to research),
    < 0 to prevent AI to research it
    """

    if tech_name in AIDependencies.UNRESEARCHABLE_TECHS:
        return -1

    if tech_name in AIDependencies.UNUSED_TECHS:
        return 0

    if tech_name in AIDependencies.THEORY_TECHS:
        return 0

    # defense
    if tech_name.startswith(AIDependencies.DEFENSE_TECHS_PREFIX):
        return get_defense_priority(rng)

    # production
    if tech_name in AIDependencies.PRODUCTION_BOOST_TECHS:
        return get_production_boost_priority(rng)

    if tech_name == AIDependencies.PRO_MICROGRAV_MAN:
        return get_production_boost_priority(rng) if ColonisationAI.got_ast else 0

    if tech_name == AIDependencies.PRO_ORBITAL_GEN:
        return get_production_boost_priority(rng) if ColonisationAI.got_gg else 0

    if tech_name == AIDependencies.PRO_SINGULAR_GEN:
        return get_production_boost_priority(rng) if has_star(fo.starType.blackHole) else 0

    # research
    if tech_name in AIDependencies.RESEARCH_BOOST_TECHS:
        return get_research_boost_priority(rng)

    if tech_name in AIDependencies.PRODUCTION_AND_RESEARCH_BOOST_TECHS:
        return get_production_and_research_boost_priority(rng)

    # growth
    if tech_name in AIDependencies.POPULATION_BOOST_TECHS:
        return get_population_boost_priority(rng)

    if tech_name == AIDependencies.GRO_XENO_GENETICS:
        return get_xeno_genetics_priority(rng)

    # supply
    if tech_name in AIDependencies.SUPPLY_BOOST_TECHS:
        return get_supply_boost_priority(rng)

    # meter change
    if tech_name in AIDependencies.METER_CHANGE_BOOST_TECHS:
        return get_meter_change_boost_priority(rng)

    # detection
    if tech_name in AIDependencies.DETECTION_TECHS:
        return get_detection_priority(rng)

    # Stealth
    if tech_name in AIDependencies.STEALTH_TECHS:
        return get_stealth_priority(rng)

    # xenoarcheology
    if tech_name == AIDependencies.LRN_XENOARCH:
        return get_xenoarch_priority(rng)

    # artificial black hole
    if tech_name == AIDependencies.LRN_ART_BLACK_HOLE:
        return get_artificial_black_hole_priority(rng)

    # genome bank (its tech)
    if tech_name == AIDependencies.GRO_GENOME_BANK:
        return get_genome_bank_priority(rng)

    # concentration camp
    if tech_name == AIDependencies.CON_CONC_CAMP:
        return 0  # TODO Concentration camps are now disabled

    # tames space monsters
    if tech_name == AIDependencies.NEST_DOMESTICATION_TECH:
        return get_nest_domestication_priority(rng)

    # damage control
    if tech_name in AIDependencies.DAMAGE_CONTROL_TECHS:
        return get_damage_control_priority(rng)

    # ship hulls
    if tech_name in AIDependencies.HULL_TECHS:
        return get_hull_priority(rng, tech_name)

    # ship weapons
    if tech_name in AIDependencies.WEAPON_TECHS:
        useful = get_ship_tech_usefulness(tech_name, ShipDesignAI.MilitaryShipDesigner())
        return useful * get_weapon_priority(rng)

    # ship armors
    if tech_name in AIDependencies.ARMOR_TECHS:
        useful = get_ship_tech_usefulness(tech_name, ShipDesignAI.MilitaryShipDesigner())
        return useful * get_armor_priority(rng)

    # ship engines
    if tech_name in AIDependencies.ENGINE_TECHS:
        useful = max(
                get_ship_tech_usefulness(tech_name, ShipDesignAI.MilitaryShipDesigner()),
                get_ship_tech_usefulness(tech_name, ShipDesignAI.StandardTroopShipDesigner()),
                get_ship_tech_usefulness(tech_name, ShipDesignAI.StandardColonisationShipDesigner()))
        return useful * get_engine_priority(rng)

    # ship fuels
    if tech_name in AIDependencies.FUEL_TECHS:
        useful = max(
                get_ship_tech_usefulness(tech_name, ShipDesignAI.MilitaryShipDesigner()),
                get_ship_tech_usefulness(tech_name, ShipDesignAI.StandardTroopShipDesigner()),
                get_ship_tech_usefulness(tech_name, ShipDesignAI.StandardColonisationShipDesigner()))
        return useful * get_fuel_priority(rng)

    # ship shields
    if tech_name in AIDependencies.SHIELD_TECHS:
        useful = get_ship_tech_usefulness(tech_name, ShipDesignAI.MilitaryShipDesigner())
        return useful * get_shield_priority(rng)

    # troop pod parts
    if tech_name in AIDependencies.TROOP_POD_TECHS:
        useful = get_ship_tech_usefulness(tech_name, ShipDesignAI.StandardTroopShipDesigner())
        return useful * get_troop_pod_priority(rng)

    # colony pod parts
    if tech_name in AIDependencies.COLONY_POD_TECHS:
        useful = get_ship_tech_usefulness(tech_name, ShipDesignAI.StandardColonisationShipDesigner())
        return useful * get_colony_pod_priority(rng)

    # default priority for unseen techs
    print "Tech %s does not have a priority, falling back to default." % tech_name

    return 1


def calculate_research_requirements(empire):
    """calculate RPs and prerequisties of every tech, in (prereqs, cost)"""
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
    rng = random.Random()
    rng.seed(fo.getEmpire().name + fo.getGalaxySetupData().seed)

    research_reqs = calculate_research_requirements(empire)
    total_rp = empire.resourceProduction(fo.resourceType.research)
    priorities = {}
    for tech_name in fo.techs():
        priority = get_priority(rng, tech_name)
        if not tech_is_complete(tech_name) and priority >= 0:
            turn_needed = research_reqs[tech_name][1] / total_rp
            priorities[tech_name] = float(priority) / turn_needed

    #
    # put in highest priority techs until all RP spent
    #
    possible = sorted(priorities.keys(), key=priorities.__getitem__)

    print "Research priorities"
    print "    %25s %8s %8s %s" % ("Name", "Priority", "Cost","Missing Prerequisties")
    for tech_name in possible[-10:]:
        print "    %25s %8.6f %8.2f %s" % (tech_name, priorities[tech_name], research_reqs[tech_name][1],research_reqs[tech_name][0])
    print

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
