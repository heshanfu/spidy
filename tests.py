import unittest

from spidy.crawler import (
    crawl,
    check_link,
    check_word,
    check_path,
    make_words,
    make_file_path,
    mime_lookup,
    HeaderError
)


class CrawlerTestCase(unittest.TestCase):

    # Tests for check_link

    def test_check_link_given_valid_url(self):
        url = "http://www.github.com"
        self.assertFalse(check_link(url))

    def test_check_link_given_invalid_url(self):
        url = "www.blah.com"
        self.assertTrue(check_link(url))

    def test_check_link_given_invalid_url2(self):
        url = "github.com"
        self.assertTrue(check_link(url))

    def test_check_link_given_short_url(self):
        url = "http://a"
        self.assertTrue(check_link(url))

    # Tests for check_word

    def test_check_word_given_valid_word(self):
        word = "crawler"
        self.assertFalse(check_word(word))

    def test_check_word_given_invalid_word(self):
        word = "supercalifragilistic"
        self.assertTrue(check_word(word))

    # Test check_paths

    def test_check_path_given_valid_path(self):
        path = "C:\\useraccount\\documents\\pictures\\picture1.jpg"
        self.assertTrue(check_path(path))

    def test_check_path_given_invalid_path(self):
        path = "C:\\useraccount\\documents\\pictures\\subdirectory\\subdirectory\\subdirectory\\" \
            "subdirectory\\subdirectory\\subdirectory\\subdirectory\\subdirectory\\subdirectory\\" \
            "subdirectory\\subdirectory\\subdirectory\\subdirectory\\subdirectory\\subdirectory\\" \
            "subdirectory\\subdirectory\\subdirectory\\subdirectory\\subdirectory\\subdirectory\\.jpg"
        self.assertFalse(check_path(path))

    # Test make_words

    def test_make_words_given_string(self):
        from requests.models import Response
        input_string = Response()
        input_string._content = bytes("This is a supercalifragilistic test string!", 'utf-8')
        expected_result = "This is a test string!".split()
        self.assertEqual(make_words(input_string).sort(), expected_result.sort(), "woo")

    # Test mime_lookup

    def test_mime_lookup_given_blank_value(self):
        value = ""
        expected_result = ".html"
        self.assertEqual(mime_lookup(value), expected_result)

    def test_mime_lookup_given_correct_value(self):
        value = "application/atom+xml"
        expected_result = ".atom"
        self.assertEqual(mime_lookup(value), expected_result)

    def test_mime_lookup_given_unknown_type(self):
        value = "this_mime_doesn't_exist"
        with self.assertRaises(HeaderError):
            mime_lookup(value)

    # Check make_file_path

    def test_make_file_path_given_url_without_extension(self):
        value = "https://github.com"
        extension = ".html"
        expected_result = "https--github.com.html"
        self.assertEqual(make_file_path(value, extension), expected_result)

    def test_make_file_path_given_url_with_extension(self):
        value = "http://www.test-site.com/index.html"
        extension = ".html"
        expected_result = "http--www.test-site.com-index.html"
        self.assertEqual(make_file_path(value, extension), expected_result)

    def test_make_file_path_given_too_long_url(self):
        value = "http://reallylongurlreallylongurlreallylongurlreallylongurlreallylongurlreallylongurlreallylongurlreallylongurlreallylongurlreallylongurlreallylongurlreallylongurlreallylongurlreallylongurlreallylongurlreallylongurlreallylongurlreallylongurlreallylongurlend.php"
        extension = ".php"
        expected_result = "http--reallylongurlreallylongurlreallylongurlreallylongurlreallylongurlreallylongurlreallylongurlreallylongurlreallylongurlreallylongurlreallylongurlreallylongurlreallylongurlreallylongurlreallylongurlreallylongurlreallylongurlreallylongurlreallylongurlen.php"
        self.assertEqual(make_file_path(value, extension), expected_result)

    # Test crawl

    def test_crawl_given_valid_url(self):
        value = "https://github.com"
        raised = False
        try:
            crawl(value)
        except Exception:
            raised = True
        self.assertFalse(raised)

    def test_crawl_given_invalid_url(self):
        value = "https://example.reee"
        raised = False
        try:
            crawl(value)
        except Exception:
            raised = True
        self.assertTrue(raised)

    def test_crawl_given_invalid_schema(self):
        value = "foo://github.com"
        raised = False
        try:
            crawl(value)
        except Exception:
            raised = True
        self.assertTrue(raised)


if __name__ == '__main__':
    unittest.main()
