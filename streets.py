import overpy
import sys 
import time

api = overpy.Overpass(url="https://overpass.kumi.systems/api/interpreter")

def get_postal_codes_by_area_id(area_id):
    print(f"Getting postal codes for id={area_id}...", file=sys.stderr)
    start_time = time.time()
    result = api.query(
        f"""
        area({area_id});
        relation["boundary"="postal_code"](area);
        out;
        """)

    postalcodes = []
    for relation in result.relations:
        postalcode = relation.tags.get("postal_code", "UNKNOWN")
        postalcodes.append(postalcode)
    end_time = time.time()
    print(f"Got {len(postalcodes)} postal codes, took {end_time-start_time}", file=sys.stderr)
    return postalcodes

# does not work as expected somehow
def get_postal_codes_by_area_name(area_name):
    print(f"Getting postal codes for name={area_name}...", file=sys.stderr)
    start_time = time.time()
    result = api.query(
        f"""
        area[name="{area_name}"];
        relation["boundary"="postal_code"](area);
        out;
        """)

    postalcodes = []
    for relation in result.relations:
        postalcode = relation.tags.get("postal_code", "UNKNOWN")
        postalcodes.append(postalcode)
    end_time = time.time()
    print(f"Got {len(postalcodes)} postal codes, took {end_time-start_time}", file=sys.stderr)
    return postalcodes

def get_streets(area_id, postalcode):
    print(f"Getting streets for postcal code={postalcode} in area id={area_id}...", file=sys.stderr)
    start_time = time.time()
    result = api.query(
        f"""
        area({area_id});
        rel["boundary"="postal_code"]["postal_code"="{postalcode}"](area);
        map_to_area;
        way(area)[highway][name];
        out;
        """)

    streets = []
    for way in result.ways:
        street = way.tags.get("name", "UNKNOWN")
        streets.append(street)
    end_time = time.time()
    print(f"Got {len(streets)} streets, took {end_time-start_time}", file=sys.stderr)
    return streets

area_id=3600051477
#postalcodes = get_postal_codes_by_area_name("Bamberg")
#postalcodes = get_postal_codes_by_area_name("Deutschland")
postalcodes = get_postal_codes_by_area_id(area_id) # Germany

postalcodes.sort()
for index, postalcode in enumerate(postalcodes):
    print(f"Processing {postalcode} ({index+1}/{len(postalcodes)})...", file=sys.stderr)
    streets = get_streets(area_id, postalcode)
    streets = list(set(streets)) # only unique results
    streets.sort()
    print(f"Retrieved {len(streets)} unique streets...", file=sys.stderr)
    for street in streets:
        print(f"{postalcode}\t{street}")
