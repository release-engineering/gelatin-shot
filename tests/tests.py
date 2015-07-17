import requests
import simplejson as json
import unittest

def getChecksumTypes():
    response = requests.get("http://localhost:5000/api/checksumtypes")
    return json.loads(response.text)
def postChecksumTypes(payload):
    response = requests.post("http://localhost:5000/api/checksumtypes", headers={'content-type':'application/json'}, data=json.dumps(payload))
def deleteChecksumTypes():
    response = requests.delete("http://localhost:5000/api/checksumtypes")


def geturis():
    response = requests.get("http://localhost:5000/api/uris")
    return json.loads(response.text)
def puturis(payload):
    response = requests.put("http://localhost:5000/api/uris", headers={'content-type':'application/json'}, data=json.dumps(payload))
def deleteuris():
    response = requests.delete("http://localhost:5000/api/uris")

def convertchecksums(payload, target):
    response = requests.get("http://localhost:5000/api/checksums/convert/"+target, headers={'content-type':'application/json'}, data=json.dumps(payload))
    return response.text


class TestChecksumTypesEmpty(unittest.TestCase):
    #DELETE should always return empty
    def test_delete(self):
        deleteChecksumTypes()
        self.assertEqual(getChecksumTypes(), {})
    #GET on empty should return empty
    def test_get(self):
        self.assertEqual(getChecksumTypes(), {})

class TestChecksumTypesEmptyPOST1(unittest.TestCase):
    def setUp(self):
        payload = {
            "SHA256": 1,
            "MD5": 2
            }
        postChecksumTypes(payload)
        self.results = getChecksumTypes()
        self.sha256 = self.results["SHA256"]
        self.md5 = self.results["MD5"]
    def tearDown(self):
        deleteChecksumTypes()

    def test_postIsDictionary(self):
        self.assertIsInstance(self.results, dict)
    def test_postHasSHA256(self):
        self.assertIsNotNone(self.sha256)
    def test_SHA256Is1(self):
        self.assertEqual(self.sha256["size"], 1)
    def test_postHasMD5(self):
        self.assertIsNotNone(self.md5)
    def test_MD5Is2(self):
        self.assertEqual(self.md5["size"], 2)

class TestChecksumTypesEmptyPOST2(unittest.TestCase):
    def setUp(self):
        payload = {
            "sha256": 1,
            "md5": 2
            }
        postChecksumTypes(payload)
        self.results = getChecksumTypes()
    def tearDown(self):
        deleteChecksumTypes()

    def test_postIsDictionary(self):
        self.assertIsInstance(self.results, dict)

    def test_postHasSHA256(self):
        self.sha256 = self.results["SHA256"]
        self.assertIsNotNone(self.sha256)
    def test_SHA256Is1(self):
        self.sha256 = self.results["SHA256"]
        self.assertEqual(self.sha256["size"], 1)

    def test_postHasMD5(self):
        self.md5 = self.results["MD5"]
        self.assertIsNotNone(self.md5)
    def test_MD5Is2(self):
        self.md5 = self.results["MD5"]
        self.assertEqual(self.md5["size"], 2)


class TestChecksumTypesNotEmpty(unittest.TestCase):
    def setUp(self):
        payload = {
            "SHA256": 1,
            "MD5": 2
            }
        postChecksumTypes(payload)
    def tearDown(self):
        deleteChecksumTypes()

    def test_delete(self):
        deleteChecksumTypes()
        self.assertEqual(getChecksumTypes(), {})
    def test_get(self):
        self.assertIsInstance(getChecksumTypes(), dict)
        self.assertIsNotNone(getChecksumTypes()["SHA256"])
        self.assertEqual(getChecksumTypes()["SHA256"]["size"], 1)
        self.assertIsNotNone(getChecksumTypes()["MD5"])
        self.assertEqual(getChecksumTypes()["MD5"]["size"], 2)

class TestChecksumTypesNotEmptyPOST(unittest.TestCase):
    def setUp(self):
        payload = {
            "SHA256": 1,
            "MD5": 2
            }
        postChecksumTypes(payload)
        payload = {
            "sha256": 1,
            "SHA512": 3
            }
        postChecksumTypes(payload)
        self.results = getChecksumTypes()
    def tearDown(self):
        deleteChecksumTypes()

    def test_postIsDictionary(self):
        self.assertIsInstance(self.results, dict)

    def test_postHasSHA256(self):
        self.sha256 = self.results["SHA256"]
        self.assertIsNotNone(self.sha256)
    def test_SHA256Is1(self):
        self.sha256 = self.results["SHA256"]
        self.assertEqual(self.sha256["size"], 1)

    def test_postHasMD5(self):
        self.md5 = self.results["MD5"]
        self.assertIsNotNone(self.md5)
    def test_MD5Is2(self):
        self.md5 = self.results["MD5"]
        self.assertEqual(self.md5["size"], 2)

    def test_postHasSHA512(self):
        self.sha512 = self.results["SHA512"]
        self.assertIsNotNone(self.sha512)
    def test_SHA512Is3(self):
        self.sha512 = self.results["SHA512"]
        self.assertEqual(self.sha512["size"], 3)

class TestUrisEmpty(unittest.TestCase):
    #DELETE should always return empty
    def test_delete(self):
        deleteuris()
        self.assertEqual(geturis(), {})
    #GET on empty should return empty
    def test_get(self):
        self.assertEqual(geturis(), {})

class TestUrisEmptyPostNoValid(unittest.TestCase):
    def setUp(self):
        payload = {
            "URI1": {
                "SHA256": "ASHA256CHECKSUM",
                "MD5": "ANMD5CHECKSUM4"
            },
            "URI5": {
                "SHA256": "ASHA256CHECKSUM",
                "MD5": "ANMD5CHECKSUM"
            },
            "URI2": {
                "SHA256": "ASHA256CHECKSUM",
                "MD5": "ANMD5CHECKSUM"
            },
            "URI2": {
                "SHA256": "ASHA256CHECKSUM1",
                "MD5": "ANMD5CHECKSUM2"
            }
        }
        puturis(payload)
        self.results = geturis()
    def tearDown(self):
        deleteuris()

    def test_postIsDictionary(self):
        self.assertIsInstance(self.results, dict)
    def test_postIsEmpty(self):
        self.assertEqual(self.results, {})

class TestUrisEmptyPostValid(unittest.TestCase):
    def setUp(self):
        payload = {
            "sha256": 1,
            "md5": 2
            }
        postChecksumTypes(payload)
        payload = {
            "URI1": { #URI 1 should have SHA256 and MD5
                "SHA256": "A",
                "MD5": "AN"
            },
            "URI5": { #URI 5 should not be present
                "sha256": "AS",
                "md5": "ANM"
            },
            "URI2": { # URI 2 should have MD5
                "SHA512": "ASHA512CHECKSUM",
                "MD5": "AM"
            },
            "URI3": { # URI 3 should have MD5
                "SHA512": "ASHA512CHECKSUA",
                "md5": "AO"
            }
        }
        puturis(payload)
        self.results = geturis()
    def tearDown(self):
        deleteuris()
        deleteChecksumTypes()

    def test_postIsDictionary(self):
        self.assertIsInstance(self.results, dict)
    def test_postIsNotEmpty(self):
        self.assertNotEqual(self.results, {})

    def test_postHasURI1(self):
        self.assertIsNotNone(self.results["URI1"])
    def test_postURI1HasSHA256(self):
        self.assertIsNotNone(self.results["URI1"]["SHA256"])
    def test_postURI1SHA256IsA(self):
        self.assertEqual(self.results["URI1"]["SHA256"]["checksum"], "A")
    def test_postURI1MD5IsAN(self):
        self.assertEqual(self.results["URI1"]["MD5"]["checksum"], "AN")

    def test_postHasURI2(self):
        self.assertIsNotNone(self.results["URI2"])
    def test_postURI2HasMD5(self):
        self.assertIsNotNone(self.results["URI2"]["MD5"])
    def test_postURI2MD5IsAN(self):
        self.assertEqual(self.results["URI2"]["MD5"]["checksum"], "AM")
    
    def test_postHasURI3(self):
        self.assertIsNotNone(self.results["URI3"])
    def test_postURI3HasMD5(self):
        self.assertIsNotNone(self.results["URI3"]["MD5"])
    def test_postURI3MD5IsAN(self):
        self.assertEqual(self.results["URI3"]["MD5"]["checksum"], "AO")

class TestUris(unittest.TestCase):
    def setUp(self):
        payload = {
            "sha256": 1,
            "md5": 2
            }
        postChecksumTypes(payload)
        payload = {
            "URI1": { #URI 1 should have SHA256 and MD5
                "SHA256": "A",
                "MD5": "AN"
            },
            "URI5": { #URI 5 should not be present
                "sha256": "AS",
                "md5": "ANM"
            },
            "URI2": { # URI 2 should have MD5
                "SHA512": "ASHA512CHECKSUM",
                "MD5": "A2"
            },
            "URI3": { # URI 3 should have MD5
                "SHA512": "ASHA512CHECKSUM",
                "md5": "A3"
            }
        }
        puturis(payload)
        self.results = geturis()
    def tearDown(self):
        deleteuris()
        deleteChecksumTypes()

    #DELETE should always return empty
    def test_delete(self):
        deleteuris()
        self.assertEqual(geturis(), {})
    def test_get(self):
        self.assertNotEqual(geturis(), {})
        self.assertIsNotNone(self.results["URI1"])
        self.assertIsNotNone(self.results["URI1"]["SHA256"])

class TestConvert(unittest.TestCase):
    def setUp(self):
        payload = {
            "sha256": 1,
            "md5": 2,
            "sha512": 3
            }
        postChecksumTypes(payload)
        payload = {
            "URI1": { #URI 1 should have SHA256 and MD5
                "SHA256": "A",
                "MD5": "AN",
                "sha512": "ASH"
            },
            "URI2": { # URI 2 should have MD5
                "SHA512": "ASQ",
                "MD5": "AQ",
                "sha256": "A"
            }
        }
        puturis(payload)
        print geturis()
	payload = {
	    "md5": [
	        "AN"
	    ],
	    "sha512": [
	        "ASQ"
	    ]
	}
        self.result = convertchecksums(payload, "sha256")
    def tearDown(self):
        deleteuris()
        deleteChecksumTypes()
    
    def test_convert(self):
        print geturis()
        print self.result
#TODO: IMPLEMENT CHECKSUM UNIQUENESS
if __name__ == '__main__':
    unittest.main()




