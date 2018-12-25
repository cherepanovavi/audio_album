import acoustid

API_KEY = 'cSpUJKpD'


class Analyzer:
    def __init__(self, files):
        self.files = list(files)
        self.length = len(self.files)
        self.ids = []
        self.copies = set()
        self.selected_copies = set()
        self.copies_numbers = {}

        for file in files:
            self.ids.append(aidmatch(file))
        self.find_copies()

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
        return res

    def find_copies(self):
        for i in range(0, self.length):
            for j in range(0, self.length):
                if i != j and self.ids[i] == self.ids[j]:
                    self.copies.add((i, j))
                    self.copies_numbers[i] = (i, j)
                    self.copies_numbers[j] = (i, j)

    def choose_one_from_copy(self, i, j):
        l_1 = self.ids[i][0]
        l_2 = self.ids[j][0]
        if l_1 > l_2:
            return i
        else:
            return j


def aidmatch(filename):
    try:
        results = acoustid.match(API_KEY, filename)
    except acoustid.NoBackendError:
        print("chromaprint library/tool not found")
    except acoustid.FingerprintGenerationError:
        print("fingerprint could not be calculated")
    except acoustid.WebServiceError as exc:
        print("web service request failed:", exc.message)
    else:
        for score, rid, title, artist in results:
            return rid
