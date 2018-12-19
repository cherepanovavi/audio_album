import wx
from wx.lib.scrolledpanel import ScrolledPanel


class TagDialog(wx.Dialog):
    def __init__(self, parent, song, audio_album):
        wx.Dialog.__init__(self, parent, wx.ID_ANY, "Tag Input", size=(650, 240))
        self.text_controls_v1 = {}
        self.text_controls_v2 = {}
        self.song = song
        self.audio_album = audio_album
        self.panel = ScrolledPanel(self, wx.ID_ANY)
        self.panel.SetupScrolling()
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        t1 = wx.StaticText(self.panel, label='ID3v1')
        self.sizer.Add(t1)
        for key in self.song.tags_v1.keys():
            if key == 'Genre':
                control = self.add_choice('Genre', self.song.tags_v1[key], GENRES)
            elif type(self.song.tags_v1[key]) == str:
                control = self.add_text_control(key, self.song.tags_v1[key])
            elif type(self.song.tags_v1[key]) == list:
                control = self.add_int_controls(key, self.song.tags_v1[key])
            self.text_controls_v1[key] = control
        t2 = wx.StaticText(self.panel, label='ID3v2')
        self.sizer.Add(t2)
        for key in self.song.tags_v2.keys():
            if key == 'Genre':
                control = self.add_choice('Genre', self.song.tags_v2[key], GENRES)
            elif type(self.song.tags_v2[key]) == str:
                control = self.add_text_control(key, self.song.tags_v2[key])
            elif type(self.song.tags_v2[key]) == list:
                control = self.add_int_controls(key, self.song.tags_v2[key])
            self.text_controls_v2[key] = control
        self.saveButton = wx.Button(self.panel, label="Save")
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_sizer.Add(self.saveButton)
        self.closeButton = wx.Button(self.panel, label="Cancel")
        btn_sizer.Add(self.closeButton)
        self.sizer.Add(btn_sizer)
        self.saveButton.Bind(wx.EVT_BUTTON, self.save)
        self.closeButton.Bind(wx.EVT_BUTTON, self.on_quit)
        self.Bind(wx.EVT_CLOSE, self.on_quit)
        self.panel.SetSizer(self.sizer)
        self.Show()

    def add_text_control(self, label_text, value_text=''):
        if value_text is None:
            return self.add_control(label_text, lambda: wx.TextCtrl(self.panel))
        return self.add_control(label_text, lambda: wx.TextCtrl(self.panel, value=str(value_text)))

    def add_int_controls(self, label_text, values):
        controls = []
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        contols_sizer = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self.panel, label=label_text)
        sizer.Add(label, 1, wx.EXPAND | wx.ALL, 3)
        for value in values:
            controls.append(self.add_int_control(value[0], value[1], value[2], contols_sizer))
        sizer.Add(contols_sizer, 3, wx.EXPAND | wx.LEFT, 8)
        self.sizer.Add(sizer, 1, wx.BOTTOM | wx.EXPAND, 3)
        return controls

    def add_int_control(self, value, min, max, sizer):
        if value is None:
            control = wx.SpinCtrl(self.panel, min=min, max=max)
        else:
            control = wx.SpinCtrl(self.panel,  min=min, max=max, initial=value)
        sizer.Add(control, 1, wx.EXPAND | wx.LEFT, 0)
        return control

    def add_choice(self, label_text, value, choices):
        if value is None:
            return self.add_control(label_text, lambda: wx.Choice(self.panel, choices = choices))
        return self.add_control(label_text, lambda: self.create_choice_with_selection(choices, value))

    def create_choice_with_selection(self, choices, value):
        ch = wx.Choice(self.panel, choices=choices)
        ch.SetSelection(value)
        return ch

    def add_control(self, label_text, control_creating):
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self.panel, label=label_text)
        control = control_creating()
        sizer.Add(label, 1, wx.EXPAND | wx.ALL, 3)
        sizer.Add(control, 3, wx.EXPAND | wx.LEFT, 8)
        self.sizer.Add(sizer, 1, wx.BOTTOM | wx.EXPAND, 3)
        return control

    def on_quit(self, event):
        self.Destroy()

    def save(self, event):
        ch_1 = get_version_changes(self.text_controls_v1, self.song.tags_v1)
        ch_2 = get_version_changes(self.text_controls_v2, self.song.tags_v2)
        if ch_1[0] or ch_2[0]:
            self.song.change_id3_tags(ch_1[1], ch_2[1])
            update_song(self.audio_album, self.song)
        self.Destroy()


def update_song(audio_album, song, song_file=None):
    pls = audio_album.song_playlists[song]
    audio_album.delete_song(song)
    if song_file is None:
        s = audio_album.add_song(song.file, song.file_name)
    else:
        s = audio_album.add_song(song_file['file'], song_file['name'])
    for pl in pls:
        if not audio_album.add_song_to_playlist(s, pl):
            wx.MessageBox('This playlist already contains this song')


def get_version_changes(text_controls, prev_values):
    changed = False
    new_values = {}
    for control in text_controls.keys():
        if type(text_controls[control]) == list:
            new_values[control] = []
            for i in text_controls[control]:
                new_values[control].append(i.GetValue())
                if new_values[control] != prev_values[control][0]:
                    changed = True
        else:
            if type(text_controls[control]) == wx.Choice:
                new_values[control] = text_controls[control].GetCurrentSelection()
            else:
                new_values[control] = text_controls[control].GetValue()
            if new_values[control] != prev_values[control]:
                changed = True
    return changed, new_values

GENRES = [
    u'Blues',
    u'Classic Rock',
    u'Country',
    u'Dance',
    u'Disco',
    u'Funk',
    u'Grunge',
    u'Hip-Hop',
    u'Jazz',
    u'Metal',
    u'New Age',
    u'Oldies',
    u'Other',
    u'Pop',
    u'R&B',
    u'Rap',
    u'Reggae',
    u'Rock',
    u'Techno',
    u'Industrial',
    u'Alternative',
    u'Ska',
    u'Death Metal',
    u'Pranks',
    u'Soundtrack',
    u'Euro-Techno',
    u'Ambient',
    u'Trip-Hop',
    u'Vocal',
    u'Jazz+Funk',
    u'Fusion',
    u'Trance',
    u'Classical',
    u'Instrumental',
    u'Acid',
    u'House',
    u'Game',
    u'Sound Clip',
    u'Gospel',
    u'Noise',
    u'AlternRock',
    u'Bass',
    u'Soul',
    u'Punk',
    u'Space',
    u'Meditative',
    u'Instrumental Pop',
    u'Instrumental Rock',
    u'Ethnic',
    u'Gothic',
    u'Darkwave',
    u'Techno-Industrial',
    u'Electronic',
    u'Pop-Folk',
    u'Eurodance',
    u'Dream',
    u'Southern Rock',
    u'Comedy',
    u'Cult',
    u'Gangsta Rap',
    u'Top 40',
    u'Christian Rap',
    u'Pop / Funk',
    u'Jungle',
    u'Native American',
    u'Cabaret',
    u'New Wave',
    u'Psychedelic',
    u'Rave',
    u'Showtunes',
    u'Trailer',
    u'Lo-Fi',
    u'Tribal',
    u'Acid Punk',
    u'Acid Jazz',
    u'Polka',
    u'Retro',
    u'Musical',
    u'Rock & Roll',
    u'Hard Rock',
    u'Folk',
    u'Folk-Rock',
    u'National Folk',
    u'Swing',
    u'Fast Fusion',
    u'Bebob',
    u'Latin',
    u'Revival',
    u'Celtic',
    u'Bluegrass',
    u'Avantgarde',
    u'Gothic Rock',
    u'Progressive Rock',
    u'Psychedelic Rock',
    u'Symphonic Rock',
    u'Slow Rock',
    u'Big Band',
    u'Chorus',
    u'Easy Listening',
    u'Acoustic',
    u'Humour',
    u'Speech',
    u'Chanson',
    u'Opera',
    u'Chamber Music',
    u'Sonata',
    u'Symphony',
    u'Booty Bass',
    u'Primus',
    u'Porn Groove',
    u'Satire',
    u'Slow Jam',
    u'Club',
    u'Tango',
    u'Samba',
    u'Folklore',
    u'Ballad',
    u'Power Ballad',
    u'Rhythmic Soul',
    u'Freestyle',
    u'Duet',
    u'Punk Rock',
    u'Drum Solo',
    u'A Cappella',
    u'Euro-House',
    u'Dance Hall',
    u'Goa',
    u'Drum & Bass',
    u'Club-House',
    u'Hardcore',
    u'Terror',
    u'Indie',
    u'BritPop',
    u'Negerpunk',
    u'Polsk Punk',
    u'Beat',
    u'Christian Gangsta Rap',
    u'Heavy Metal',
    u'Black Metal',
    u'Crossover',
    u'Contemporary Christian',
    u'Christian Rock',
    u'Merengue',
    u'Salsa',
    u'Thrash Metal',
    u'Anime',
    u'JPop',
    u'Synthpop',
    u'Abstract',
    u'Art Rock',
    u'Baroque',
    u'Bhangra',
    u'Big Beat',
    u'Breakbeat',
    u'Chillout',
    u'Downtempo',
    u'Dub',
    u'EBM',
    u'Eclectic',
    u'Electro',
    u'Electroclash',
    u'Emo',
    u'Experimental',
    u'Garage',
    u'Global',
    u'IDM',
    u'Illbient',
    u'Industro-Goth',
    u'Jam Band',
    u'Krautrock',
    u'Leftfield',
    u'Lounge',
    u'Math Rock',
    u'New Romantic',
    u'Nu-Breakz',
    u'Post-Punk',
    u'Post-Rock',
    u'Psytrance',
    u'Shoegaze',
    u'Space Rock',
    u'Trop Rock',
    u'World Music',
    u'Neoclassical',
    u'Audiobook',
    u'Audio Theatre',
    u'Neue Deutsche Welle',
    u'Podcast',
    u'Indie Rock',
    u'G-Funk',
    u'Dubstep',
    u'Garage Rock',
    u'Psybient',
]
