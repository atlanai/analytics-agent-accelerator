"""The workbook's fee tile and its tour agree with the demo's actual ticket population."""
import csv
import json
from pathlib import Path
import re
import sqlite3
import unittest
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


class BoxOfficeFees(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.workbook = ET.parse(ROOT / 'box-office/tableau/box-office-pulse.twb').getroot()
        cls.source = cls.workbook.find("./datasources/datasource[@caption='Box Office']")
        cls.sql = cls.source.find("./connection/relation[@type='text']").text
        cls.formulas = {c.get('caption'): c.find('calculation').get('formula')
                        for c in cls.source.findall('column') if c.find('calculation') is not None}
        cls.db = sqlite3.connect(':memory:')
        cls.addClassCleanup(cls.db.close)
        cls.db.execute("ATTACH DATABASE ':memory:' AS tix")
        for name in ('tickets', 'orders', 'events', 'venues'):
            with (ROOT / 'box-office/data' / (name + '.csv')).open(newline='') as stream:
                header, *rows = csv.reader(stream)
            columns = ', '.join('"' + c.replace('"', '""') + '" TEXT' for c in header)
            cls.db.execute(f'CREATE TABLE tix.{name} ({columns})')
            cls.db.executemany(f'INSERT INTO tix.{name} VALUES ({", ".join("?" for _ in header)})', rows)
        cls.db.execute('PRAGMA query_only=ON')

    def calculate(self, formula):
        sql = re.sub(r'\[([a-z_]+)\]', r'"\1"', formula)
        return self.db.execute('SELECT ' + sql + ' FROM (' + self.sql + ')').fetchone()[0]

    def test_fee_tile_uses_fan_spending_while_take_rate_keeps_face_value(self):
        fees = self.calculate(self.formulas['Total Fees'])
        spending = self.calculate(self.formulas['Gross Sales'])
        share = self.calculate(self.formulas['Fee Share'])
        take = self.calculate(self.formulas['Fee Take Rate'])
        self.assertAlmostEqual(share, fees / spending)
        self.assertAlmostEqual(take, fees / (spending - fees))
        self.assertEqual((f'{share:.1%}', f'{take:.1%}'), ('21.3%', '27.1%'))
        sheet = self.workbook.find("./worksheets/worksheet[@name='Fee Share']")
        self.assertEqual(sheet.find('./layout-options/title/formatted-text/run').text,
                         'Fees as % of what fans paid')
        column = sheet.find("./table/view/datasource-dependencies/column[@caption='Fee Share']")
        self.assertEqual(column.find('calculation').get('formula'), self.formulas['Fee Share'])
        encoded = sheet.find('./table/panes/pane/encodings/text').get('column')
        self.assertIn(column.get('name').strip('[]'), encoded)
        self.assertIsNotNone(self.workbook.find("./dashboards/dashboard/zones//zone[@name='Fee Share']"))

    def test_tour_value_formula_and_tile_match_the_workbook(self):
        tour = (ROOT / 'docs/box-office-tour/index.html').read_text()
        data = json.loads(re.search(r'^var D=(.*);$', tour, re.M).group(1))
        self.assertAlmostEqual(data['tiles']['share'], self.calculate(self.formulas['Fee Share']))
        formula = re.search(r"'Fee Share':\{ds:'Box Office',f:'([^']+)'", tour).group(1)
        self.assertEqual(formula, self.formulas['Fee Share'])
        self.assertIn("['share','Fee Share','Fees as % of what fans paid',pct(D.tiles.share)]", tour)
        self.assertNotIn('Title and measure disagree', tour)


if __name__ == '__main__':
    unittest.main()
