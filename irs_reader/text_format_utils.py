import json
import sys

### Thanks to github.com/jsvine/pdfplumber see cli.py#L11 
class DecimalEncoder(json.JSONEncoder):
    """ 
    Helper to deal with decimal encoding, think it's not needed here now(?)
    """
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o.quantize(Decimal('.0001'), rounding=ROUND_HALF_UP))
        return super(DecimalEncoder, self).default(o)
### ibid.
def to_json(data, encoding=None):
    if hasattr(sys.stdout, "buffer"):
        sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer, "strict")
        json.dump(data, sys.stdout)
    else:
        json.dump(data, sys.stdout)


def print_documented_vars(vardata):
    var_array = []
    for this_key in vardata.keys():
        if this_key=='name':
            continue
        this_var = vardata[this_key]
        this_var['name'] = this_key
        var_array.append(this_var)
    sorted_vars = sorted(var_array, key=lambda k: int(k['ordering'])) 

    for this_vardata in sorted_vars:
        print("\n\t*%s*: value=%s \n\tLine Number '%s' Description: '%s' Type: %s" % (this_vardata['name'], this_vardata['value'], this_vardata.get('line_number') or '', this_vardata.get('description') or '' , this_vardata.get('db_type') or ''))

def print_part_start(part_name):
    print("\n%s\n" % part_name)

def write_ordered_documentation(data, standardizer):

    for schedule in data:
        print("\nSchedule: %s\n" % schedule['schedule_name'])

        schedule_parts = []
        for key in schedule['data']['schedule_parts'].keys():
            this_part = schedule['data']['schedule_parts'][key]
            this_part['name']=key

            schedule_parts.append(this_part)

        schedule_parts_sorted = sorted(schedule_parts, key=lambda k: standardizer.part_ordering(k['name']))
        for part in schedule_parts_sorted:
            print_part_start(part['name'])
            print_documented_vars(part)
        
        for grpkey in schedule['data']['groups'].keys():
            for grp in schedule['data']['groups'][grpkey]:
                print ("\nRepeating Group: %s\n" % grpkey)

                print_documented_vars(grp)


def format_for_text(data, standardizer=None, documentation=False):
    """ If we're not showing documentation, just pretty print the json
        But if we're showing the documentation, reorder it.
    """
    if documentation:
        if not standardizer:
            raise Exception("standardizer must be included to order documentation")
        write_ordered_documentation(data, standardizer)

    else:    
        if hasattr(sys.stdout, "buffer"):
            sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer, "strict")
            json.dump(data, sys.stdout, indent=4)
        else:
            json.dump(data, sys.stdout, indent=4)
    
    print("\n\n")