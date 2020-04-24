

class Units(int):
    @property
    def seconds(self) -> float:
        return self.__int__() / 1000

    @property
    def minutes(self) -> float:
        return self.seconds / 60

    @property
    def hours(self) -> float:
        return self.minutes / 60


class Line:
    def __init__(self, data):
        try:
            int(data[-1])
            data = data[:-1]
        except ValueError:
            pass
        self._raw = data
        self.timestamp = data[0]
        self.line = self._sanitize(" ".join(data[1:]))

    @staticmethod
    def _sanitize(text: str):
        """
        Some of the text in these particular subtitle files include italics
        words which are included in the <i></i> html tags. These were
        creating problems in tagging. Hence we will just remove them here.
        :param text:
        :return:
        """
        return text.replace("<i>", "").replace("</i>", "").replace("-", " ")

    @staticmethod
    def _time_convert(time: str):
        other, mil = time.split(",")
        hour, minute, seconds = other.split(":")

        total = int(mil)
        total += int(seconds) * 1000
        total += int(minute) * 1000 * 60
        total += int(hour) * 1000 * 60 * 60

        return total

    @property
    def start_time(self) -> Units:
        return Units(self._time_convert(self.timestamp.split("-->")[0]))

    @property
    def end_time(self) -> Units:
        return Units(self._time_convert(self.timestamp.split("-->")[1]))


class Subtitle:
    """
    Simple class to hold the subtitle data
    """

    def __init__(self, lines):
        self.lines = lines

    @property
    def text(self) -> str:
        """Returns all the subtitle lines joined by space
        """
        return " ".join([x.line for x in self.lines])

    @staticmethod
    def _convert_units(ms: Units, unit: str):
        if unit == "ms":
            return ms.__int__()
        elif unit == "s":
            return ms.seconds
        elif unit == "min":
            return ms.minutes
        elif unit == "h":
            return ms.hours
        else:
            raise ValueError(f"Unknown unit '{unit}'. Currently only "
                             f"following units are supported: ms, s, min, h")

    def start_times(self, unit: str = "ms") -> list:
        """
        Start time of all of the subtitles (in milliseconds)
        :param unit: In which unit you want (ms, s, min, h)
        :return: List of times
        """
        return [self._convert_units(x.start_time, unit) for x in self.lines]

    def end_times(self, unit: str = "ms") -> list:
        """
        End time of all of the subtitles (in milliseconds)
        :param unit: In which unit you want (ms, s, min, h)
        :return: List of times
        """
        return [self._convert_units(x.end_time, unit) for x in self.lines]