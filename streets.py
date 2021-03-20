import overpy
import sys 

api = overpy.Overpass(url="https://overpass.kumi.systems/api/interpreter")

def get_postal_codes_by_area_id(area_id):
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
    return postalcodes

# does not work as expected somehow
def get_postal_codes_by_area_name(area_name):
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
    return postalcodes

def get_streets(area_id, postalcodes):
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
    return streets

#postalcodes = get_postal_codes_by_area_name("Bamberg")
#postalcodes = get_postal_codes_by_area_name("Deutschland")
postalcodes = get_postal_codes_by_area_id(3600051477) # Germany

postalcodes.sort()
for index, postalcode in enumerate(postalcodes):
    print(f"Processing {postalcode} ({index+1}/{len(postalcodes)})...", file=sys.stderr)
    streets = get_streets(postalcode)
    streets = list(set(streets)) # only unique results
    streets.sort()
    print(f"Retrieved {len(streets)} unique streets...", file=sys.stderr)
    for street in streets:
        print(f"{postalcode}\t{street}")
