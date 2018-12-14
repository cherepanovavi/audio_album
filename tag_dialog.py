import wx
from wx.lib.scrolledpanel import ScrolledPanel


class TagDialog(wx.Dialog):
    def __init__(self, parent, song, audio_album):
        wx.Dialog.__init__(self, parent, wx.ID_ANY, "Tag Input", size=(650, 240))
        self.text_controls_v1 = {}
        self.text_controls_v2 = {}
        self.prev_values_v1 = {}
        self.prev_values_v2 = {}
        self.song = song
        self.tags_v1 = self.song.tags['ID3TagV1'] if 'ID3TagV1' in self.song.tags.keys() else {}
        self.tags_v2 = self.song.tags['ID3TagV2'] if 'ID3TagV2' in self.song.tags.keys() else {}
        self.audio_album = audio_album
        self.panel = ScrolledPanel(self, wx.ID_ANY)
        self.panel.SetupScrolling()
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        t1 = wx.StaticText(self.panel, label='ID3v1')
        self.sizer.Add(t1)
        keys_v1 = [('Track number', 'track'), ('Title', 'song'), ('Artist', 'artist'), ('Album', 'album'),
                   ('Genre', 'genre'), ('Date', 'year'), ('Comments', 'comment')]
        for key in keys_v1:
            if key[1] in self.tags_v1.keys():
                control = self.add_text_control(key[0], self.tags_v1[key[1]])
                self.prev_values_v1[key[0]] = self.tags_v1[key[1]]
            else:
                control = self.add_text_control(key[0])
                self.prev_values_v1[key[0]] = ""
            self.text_controls_v1[key[0]] = control
        t2 = wx.StaticText(self.panel, label='ID3v2')
        self.sizer.Add(t2)
        keys_v2 = [('Track number', 'track'), ('Title', 'song'), ('Artist', 'artist'), ('Album', 'album'),
                   ('Genre', 'genre'), ('Date', 'year'), ('Comments', 'comment'),
                   ('URL', 'url'), ('Copyright', 'copyright'), ('Publisher', 'publisher'),
                   ('Composer', 'composer')]
        for key in keys_v2:
            if key[1] in self.tags_v2.keys():
                control = self.add_text_control(key[0], self.tags_v2[key[1]])
                self.prev_values_v2[key[0]] = self.tags_v2[key[1]]
            else:
                control = self.add_text_control(key[0])
                self.prev_values_v2[key[0]] = ""
            self.text_controls_v2[key[0]] = control
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
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self.panel, label=label_text)
        if value_text is None:
            control = wx.TextCtrl(self.panel)
        else:
            control = wx.TextCtrl(self.panel, value=str(value_text))
        sizer.Add(label, 1, wx.EXPAND | wx.ALL, 3)
        sizer.Add(control, 3, wx.EXPAND | wx.LEFT, 8)
        self.sizer.Add(sizer, 1, wx.BOTTOM | wx.EXPAND, 3)
        return control

    def on_quit(self, event):
        self.Destroy()

    def save(self, event):
        ch_1 = get_version_changes(self.text_controls_v1, self.prev_values_v1)
        if ch_1[0]:
            self.song.change_id3_tags(ch_1[1], 1)
            update_song(self.audio_album, self.song)
        ch_2 = get_version_changes(self.text_controls_v2, self.prev_values_v2)
        if ch_2[0]:
            self.song.change_id3_tags(ch_2[1], 2)
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
        new_values[control] = text_controls[control].GetValue()
        if new_values[control] != prev_values[control]:
            changed = True
    return changed, new_values
