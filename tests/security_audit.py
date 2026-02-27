import os
import sys
import unittest

# Add parent directory to path to import servers
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestMCPSecurity(unittest.TestCase):
    def setUp(self):
        self.traversal_payload = "../sensitive/credentials.env"

    def test_secure_server_path_anchoring(self):
        """Verify that the secure server blocks path traversal."""
        from secure_server import read_report
        result = read_report(self.traversal_payload)
        self.assertIn("Denied", result)
        self.assertIn("Security Alert", result)

    def test_vulnerable_server_vulnerability(self):
        """demonstrate that the vulnerable server is susceptible to traversal."""
        from vulnerable_server import read_report
        result = read_report(self.traversal_payload)
        self.assertIn("SECRET_API_KEY", result)

if __name__ == "__main__":
    unittest.main()
