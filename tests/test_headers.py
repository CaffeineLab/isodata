import unittest
from isodata.src.isodata.utils import get_filename_from_headers


class TestHeaderMethods(unittest.TestCase):

    def test_empty_headers(self):
        self.assertIsNone(get_filename_from_headers(None))
        self.assertIsNone(get_filename_from_headers(""))
        self.assertIsNone(get_filename_from_headers({}))
        self.assertIsNone(get_filename_from_headers({"content-disposition": ""}))
        self.assertIsNone(get_filename_from_headers({"content-disposition": "x"}))
        self.assertIsNone(get_filename_from_headers({"Content-Disposition": ""}))
        self.assertIsNone(get_filename_from_headers({"CONTENT-DISPOSITION": "x"}))

    def test_headers(self):
        headers = {'Content-Length': '710', 'Content-Type': 'application/zip', 'Content-Disposition': 'attachment; filename=759030830.cdr.00012302.0000000000000000.20210216.220501761.SCEDBTCNP686_csv.zip', 'Access-Control-Allow-Origin': '*', 'Date': 'Wed, 14 Aug 2024 13:28:12 GMT'}
        expectation = '759030830.cdr.00012302.0000000000000000.20210216.220501761.SCEDBTCNP686_csv.zip'
        self.assertEqual(get_filename_from_headers(headers), expectation)

        headers = {'Content-Length': '710', 'Content-Type': 'application/zip', 'content-disposition': 'attachment; filename=759030830.cdr.00012302.0000000000000000.20210216.220501761.SCEDBTCNP686_csv.zip', 'Access-Control-Allow-Origin': '*', 'Date': 'Wed, 14 Aug 2024 13:28:12 GMT'}
        expectation = '759030830.cdr.00012302.0000000000000000.20210216.220501761.SCEDBTCNP686_csv.zip'
        self.assertEqual(get_filename_from_headers(headers), expectation)


if __name__ == '__main__':
    unittest.main()
