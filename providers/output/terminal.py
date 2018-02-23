import operator
import re
import textwrap
from decimal import Decimal

from providers.output.provider import OutputProvider

IDENTIFIER = "Terminal"

class Provider(OutputProvider):
    def process_data(self, movie_data, filters):
        movie_data = self.apply_filters(movie_data, filters)
        movie_data = filter(lambda data: data.get("filmtipset_my_grade_type", "none") != "seen", movie_data)
        movie_data = sorted(movie_data, key=self._get_ratings, reverse=True)
        return movie_data

    def _get_ratings(self, data):
        filmtipset_my_grade = self._get_filmtipset_my_grade(data)
        imdb_rating = data.get("imdb_rating", 0)
        return (str(filmtipset_my_grade), str(imdb_rating))

    def _get_filmtipset_my_grade(self, data):
        rating = 0
        if "filmtipset_my_grade_type" not in data:
            return rating

        if data["filmtipset_my_grade_type"] != "none" and data["filmtipset_my_grade"]:
            rating = data["filmtipset_my_grade"]
        elif data["filmtipset_avg_grade"]:
            rating = data["filmtipset_avg_grade"]

        return rating

    @staticmethod
    def _get_sort_key(data):
        # NOTE: filmtipset_my_grade and imdb_rating are stored as strings as JSON has no decimal impl.
        return (
            Decimal(data.get("filmtipset_my_grade", "0") or "0"),
            Decimal(data.get("imdb_rating", "0") or "0")
        )

    @staticmethod
    def _equals_or_contains(val1, val2):
        if isinstance(val1, list):
            return val2.lower() in [v.lower() for v in val1]

        return operator.eq(val1.lower(), val2.lower())

    @staticmethod
    def _notequals_or_notcontains(val1, val2):
        if isinstance(val1, list):
            return val2.lower() not in [v.lower() for v in val1]

        return operator.ne(val1.lower(), val2.lower())

    def apply_filters(self, movie_data, filters):
        OPERATORS = {
            "==": self._equals_or_contains,
            "!=": self._notequals_or_notcontains,
            ">": operator.gt,
            ">=": operator.ge,
            "<": operator.lt,
            "<=": operator.le,
        }

        if not filters:
            return movie_data

        filtered_data = list(movie_data)
        for _filter in filters.split(","):
            if len(filtered_data) == 0:
                return filtered_data

            # NOTE: Need to look for "<=" before "<" to avoid splitting x<=6 into (x, <, =6)
            operator_keys = sorted(OPERATORS.keys(), reverse=True)
            result = re.split(r"(%s)" % "|".join(operator_keys), _filter)
            if len(result) != 3:
                raise Exception("Filter '%s' is not a valid filter specification.\n\n A valid filter looks like %s" % (
                    result[0],
                    "imdb_rating>=4",
                ))

            field, op, value = result

            if field not in filtered_data[0]:
                raise Exception("Field '%s' is not a valid field name. \n\nValid field names are: %s" % (
                    field,
                    ", ".join(filtered_data[0].keys()),
                ))

            keep = []
            for data in filtered_data:
                if data.get(field) and OPERATORS[op](data.get(field), value):
                    keep.append(data)

            filtered_data = keep

        return filtered_data

    def output(self, movie_data, limit, filters):
        movie_data = self.process_data(movie_data, filters)

        print()
        for data in movie_data[:limit]:
            print("%s (Filmtipset: %s, IMDB: %s)" % (
                data["title"],
                data.get("filmtipset_my_grade", "-"),
                data.get("imdb_rating", "-"),
            ))

            print("  [Genre: %s, Country: %s, Year: %s]" % (
                ", ".join(data.get("genre", ["-"])),
                ", ".join(data.get("country", ["-"])),
                data.get("year", "-"),
            ))

            plot = data.get("plot", None)
            if plot:
                text = textwrap.wrap('Plot: "' + data.get("plot", "-") + '"', width=80, initial_indent="  ", subsequent_indent="  ")
                print("\n".join(text))
            print()
