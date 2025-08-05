import jsonpath_ng.ext

from tomo_mapper.parser.mapping_util import escape_pathelements


class TestMappingUtil:

    def test_escape_dottedpaths(self):
        """
        The test mainly checks for expected usages of functions and unexpected tokens in dotted path.
        In case of extension in functionality of the parsing, this test may need adaption to more test inputs
        :return:
        """
        inputpaths = [
            "some.path.to.list[*]",
            "some.#path.to.list[*]",
            "some.path.to.#list[*]",
            "some.path.to.list[3].`sub(/.*/, replacement)`",
            "some.path.to`split(\",\", *, -1)`",
        ]

        vallist = [1,2,3, "some string"]

        match_dict = {
            "some": {
                "path": {
                    "to": {
                        "list": vallist,
                        "#list": vallist
                    }
                },
                "#path": {
                    "to": {
                        "list": vallist,
                        "#list": vallist
                    }
                }
            }
        }

        for ip in inputpaths:
            escaped = escape_pathelements(ip)
            p = jsonpath_ng.ext.parse(escaped) #if this succeeds, the escaped version does not throw an error about unexpected characters
            values = [m.value for m in p.find(match_dict)]
            if not "`" in ip: #bit harder to check dummy functions, so we are satisfied with getting any result
                assert len(values) == len(vallist)