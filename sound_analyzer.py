from pydub import AudioSegment


class Analyzer:
    def __init__(self, files):
        self.files = files
        self.length = len(self.files)
        self.segments = []
        self.raw_data = []
        self.short_parts = []
        self.long_parts = []
        self.copies = set()
        self.selected_copies = set()
        self.copies_numbers = {}
        for file in files:
            segment = AudioSegment.from_mp3(file)
            self.segments.append(segment)
            self.raw_data.append(segment.raw_data)
            self.short_parts.append(segment[:10000].raw_data)
            self.long_parts.append(segment[10000:-10000].raw_data)

    def get_unique(self):
        self.find_copies()
        res = []
        for i in range(0, self.length):
            if i in self.copies_numbers.keys():
                if self.copies_numbers[i] not in self.selected_copies:
                    r = self.choose_one_from_copy(self.copies_numbers[i][0], self.copies_numbers[i][1])
                    self.selected_copies.add(self.copies_numbers[i])
                    res.append(self.files[r])
            else:
                res.append(self.files[i])
        # print(res)
        return res

    def find_copies(self):
        for i in range(0, self.length):
            for j in range(0, self.length):
                if i != j:
                    r = self.raw_data[j].find(self.short_parts[i])
                    if r != -1:
                        r_2 = self.raw_data[j].find(self.long_parts[i])
                        if r_2 != -1:
                            self.copies.add((i, j))
                            self.copies_numbers[i] = (i, j)
                            self.copies_numbers[j] = (i, j)

    def choose_one_from_copy(self, i, j):
        l_1 = len(self.raw_data[i])
        l_2 = len(self.raw_data[j])
        if l_1 > l_2:
            return i
        else:
            return j

