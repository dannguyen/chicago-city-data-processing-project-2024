#!/usr/bin/env python3
import click
import csv
import io
from datetime import datetime
from pathlib import Path
import re
from typing import List, Dict, Union

SCHEMA_READ_PATH = Path('meta/incident-schema.csv')

RX_ADDRESS = re.compile(r"""
        (?P<street_number>\d{1,5}X{1,})\s
        (?:(?P<street_direction>[NSEW])\s)?
        (?P<street_name>[A-Z0-9. ']+?)
        (?:\s(?P<street_suffix>[A-Z]{2,4}))?$
        """, re.VERBOSE)

    # match = re.match(r"""(\d{1,5}X{1,})\s([NSEW])\s([A-Z0-9 ']+)(?:\s([A-Z]{2,4}))?$""", addr)


def read_schema(infile:io.TextIOWrapper) -> Dict[str, Dict[str, str]]:
    schema = {}
    for d in csv.DictReader(infile):
        schema[d['field_name']] = {
            'original_name': d.get('original_name'),
            'datatype': d['datatype']
        }
    return schema

def extract_incident_datetime_components(txt:str) -> Dict[str, Union[int, str]]:
    # Parse the datetime string into a datetime object
    dt = datetime.fromisoformat(txt)

    # Create the dictionary with the required fields
    result = {
        # 'datetime': dt.isoformat(),
        'day_of_week': dt.weekday(),  # Monday is 0 and Sunday is 6
        'month': dt.month,
        'quarter': (dt.month - 1) // 3 + 1,
        'hour': dt.hour
    }

    return result



def extract_street_components(address:str) -> Dict[str, str]:
    """Regular expression to match components in the address string"""

    """Uncaught patterns:
        'XX  UNKNOWN', cleaned: 'XX UNKNOWN'
        '005XX N FAIRBANKS CT (PARK N', cleaned: '005XX N FAIRBANKS CT (PARK N'
        '068XX S ST. LAWRENCE AV', cleaned: '068XX S ST. LAWRENCE AV'
        '021XX N ST. LOUIS  AVE', cleaned: '021XX N ST. LOUIS AVE'
    """
    def cleanaddr(txt:str) -> str:
        t = re.sub(r'\s+', ' ', txt.upper())
        return re.sub(r'[.,`!?+\-]$', '', t).strip()

    addr = cleanaddr(address)

    d = {
            'street_name': None,
            'street_direction': None,
            'street_number': None,
            'street_suffix': None,
    }

    # match = re.match(r"""(\d{1,5}X{1,})\s([NSEW])\s([A-Z0-9 ']+)(?:\s([A-Z]{2,4}))?$""", addr)
    match = RX_ADDRESS.match(addr)
    if match:
        #standard match
        d['street_number'] = match.group('street_number').replace('X', '0')
        d['street_direction'] = match.group('street_direction') if match.group('street_direction') else None
        d['street_name'] = match.group('street_name')
        d['street_suffix'] = match.group('street_suffix') if match.group('street_suffix') else None
    else:
        errtxt = f"""Unexpected address pattern: '{address}', cleaned: '{addr}'"""
        # click.echo(errtxt, err=True)
        # raise ValueError(errtxt)
    return d

def clean_record(record:dict, schema:Dict[str, Dict[str, str]]) -> dict:
    def cleanval(value:str, datatype:str) -> Union[str, bool, int, float, datetime]:
        v = value.strip()
        if v:
            if datatype == 'boolean':
                v = bool(v)
            elif datatype == 'datetime':
                dx = datetime.strptime(v, "%m/%d/%Y %I:%M:%S %p")
                v = dx.isoformat()
            elif datatype == 'float':
                v = float(v)
            elif datatype == 'integer':
                v = int(v)
            else:
                v = str(v)
        else:
            v = None

        return v


    d = {}

    # typecast each field where there's an original value
    for fieldname, s in schema.items():
        if oname := s['original_name']:
            d[fieldname] = cleanval(record[oname], datatype=s['datatype'])
        else:
            d[fieldname] = None

    # handle the extra fields separately
    d.update(extract_incident_datetime_components(d['datetime']))
    d.update(extract_street_components(d['block_address']))
    return d

@click.command()
@click.option('--input-path', '-i', type=click.File('r'), default='-', help="Input file containing JSON. Reads from stdin if not provided.")
@click.option('--output-path', '-o', type=click.File('w'), default='-', help="Output file to write prettified JSON. Defaults to stdout.")
@click.option('--schema-path', '-s', type=click.File('r'), required=True, help="CSV file with mapped headers and datatypes")
def clean_data(input_path, output_path, schema_path):
    schema = read_schema(schema_path)

    outcsv = csv.DictWriter(output_path, fieldnames=schema.keys())
    outcsv.writeheader()

    for ix in csv.DictReader(input_path):
        ox = clean_record(ix, schema)
        outcsv.writerow(ox)





if __name__ == '__main__':
    clean_data()
