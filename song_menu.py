import wx


class SongMenu(wx.Menu):
    def __init__(self, audio_album, song):
        wx.Menu.__init__(self)
        self.audio_album = audio_album
        self.song = song
        self.submenu = SongSubMenu(audio_album, song)
        text = 'Add "{}" to playlist'.format(song.title)
        self.AppendSubMenu(self.submenu, text, 'Click here to add this song to some playlist')
        tag_item = self.Append(-1, item='Change id3 tags', kind=wx.ITEM_NORMAL)
        self.Bind(wx.EVT_MENU, self.change_id3_tags, tag_item)

    def change_id3_tags(self, event):
        d = GetData(None, self.song)
       # self.audio_album.update()


class GetData(wx.Dialog):
    def __init__(self, parent, song):
        wx.Dialog.__init__(self, parent, wx.ID_ANY, "Tag Input", size=(650, 240))
        self.song = song
        self.panel = wx.Panel(self, wx.ID_ANY)
        self.lbl_artist = wx.StaticText(self.panel, label="Artist", pos=(20, 20))
        self.artist = wx.TextCtrl(self.panel, value=song.artist.title(), pos=(110, 20), size=(500, -1))
        self.lbl_alb = wx.StaticText(self.panel, label="Album", pos=(20, 60))
        self.album = wx.TextCtrl(self.panel, value=song.album.title(), pos=(110, 60), size=(500, -1))
        self.lbl_ttl = wx.StaticText(self.panel, label="Song name", pos=(20, 100))
        self.title = wx.TextCtrl(self.panel, value=song.title, pos=(110, 100), size=(500, -1))
        self.saveButton = wx.Button(self.panel, label="Save", pos=(110, 160))
        self.closeButton = wx.Button(self.panel, label="Cancel", pos=(210, 160))
        self.saveButton.Bind(wx.EVT_BUTTON, self.save)
        self.closeButton.Bind(wx.EVT_BUTTON, self.on_quit)
        self.Bind(wx.EVT_CLOSE, self.on_quit)
        self.Show()

    def on_quit(self, event):
        self.Destroy()

    def save(self, event):
        self.song.change_id3_tags({'title': self.title.GetValue(), 'artist': self.artist.GetValue(),
                                   'album': self.album.GetValue()})
        self.Destroy()


class SongSubMenu(wx.Menu):
    def __init__(self, audio_album, song):
        wx.Menu.__init__(self)
        self.audio_album = audio_album
        self.song = song
        for pl in audio_album.playlists:
            item = self.Append(-1, item=pl.title, kind=wx.ITEM_NORMAL)
            self.Bind(wx.EVT_MENU, self.on_popup_item_selected, item)
        cr_pl = self.Append(-1, item='Create a playlist', kind=wx.ITEM_NORMAL)
        self.Bind(wx.EVT_MENU, self.create_playlist, cr_pl)

    def on_popup_item_selected(self, event):
        item = self.FindItemById(event.Id)
        self.audio_album.playlists_titles[item.GetText()].add_song(self.song)

    def create_playlist(self, event):
        dlg = wx.TextEntryDialog(None, 'Enter playlist title', 'Playlist title')
        title = 'New playlist'
        dlg.SetValue(title)
        if dlg.ShowModal() == wx.ID_OK:
            title = dlg.GetValue()
        dlg.Destroy()
        playlist = self.audio_album.add_playlist(title)
        playlist.add_song(self.song)