import wx
from audio_objects import Song


class Panel(wx.Panel):
    def __init__(self, parent, text, start_pos=(0, 25)):
        wx.Panel.__init__(self, parent, size=(200, 600), style=wx.BORDER_SUNKEN)
        self.start_pos = start_pos
        self.parent = parent
        self.objects_list = None
        self.buttons = []
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        t = wx.StaticText(self, -1, text)
        self.sizer.Add(t)
        self.SetSizer(self.sizer)

    def add_buttons(self, objects_list):
        self.objects_list = objects_list
        i = 0
        for au_obj in objects_list:
            obj_id = i
            if type(au_obj) == Song:
                obj_id = au_obj.id
            button = wx.Button(self, obj_id, label=au_obj.title, size=(200, 25),
                               pos=(self.start_pos[0], self.start_pos[1] + i * 25), style=wx.BU_LEFT)
            self.buttons.append(button)
            self.sizer.Add(button)
            button.Bind(wx.EVT_BUTTON, self.on_button)
            i += 1

    def delete_buttons(self):
        for button in self.buttons:
            button.Destroy()
        self.buttons = []
        self.objects_list = None

    # default logic for album, genre and playlist panels
    def on_button(self, event):
        self.parent.song_panel.delete_buttons()
        self.parent.song_panel.add_buttons(self.objects_list[event.Id].songs)


class SongPanel(Panel):
    def __init__(self, parent, player, text="Choose a song to listen"):
        Panel.__init__(self, parent, text)
        self.player = player

    def on_button(self, event):
        self.player.change_now_playing(self.objects_list)
        self.player.on_song(event)

    def add_buttons(self, objects_list):
        super().add_buttons(objects_list)
        for btn in self.buttons:
            btn.Bind(wx.EVT_RIGHT_DOWN, self.show_menu)

    def show_menu(self, event):
        menu = self.player.audio_album.songs_id[event.Id].menu()
        self.PopupMenu(menu, self.ScreenToClient(wx.GetMousePosition()))


class SongTab(wx.SplitterWindow):
    def __init__(self, parent, song_list, player):
        wx.SplitterWindow.__init__(self, parent)
        self.panel = SongPanel(self, player)
        self.panel.add_buttons(song_list)


class HalfSplittedTab(wx.SplitterWindow):
    def __init__(self, parent, objects_list, player, text, start_pos=(0, 25)):
        wx.SplitterWindow.__init__(self, parent)
        self.panel = Panel(self, text, start_pos)
        self.panel.add_buttons(objects_list)
        self.song_panel = SongPanel(self, player)
        self.SplitVertically(self.panel, self.song_panel)
        self.SetSashGravity(0.5)


class PlaylistTab(HalfSplittedTab):
    def __init__(self, parent, objects_list, player, text, au_album):
        HalfSplittedTab.__init__(self, parent, objects_list, player, text, start_pos=(0, 60))
        self.audio_album = au_album
        button = wx.Button(self.panel, size=(100, 40), pos=(0, 25), label="Create a playlist")
        button.SetBackgroundColour('light blue')
        button.Bind(wx.EVT_BUTTON, self.create_playlist)
        self.panel.sizer.Add(button)

    def create_playlist(self, event):
        dlg = wx.TextEntryDialog(self.panel, 'Enter playlist title', 'Playlist title')
        title = 'New playlist'
        dlg.SetValue(title)
        if dlg.ShowModal() == wx.ID_OK:
            title = dlg.GetValue()
        dlg.Destroy()
        playlist = self.audio_album.add_playlist(title)
        l = list(self.audio_album.songs_titles.keys())
        ch = wx.MultiChoiceDialog(self, 'Choose songs to add to your playlist', 'Choosing songs', l)
        songs = []
        if ch.ShowModal() == wx.ID_OK:
            selections = ch.GetSelections()
            songs = [self.audio_album.songs_titles[l[i]] for i in selections]
        ch.Destroy()
        playlist.add_songs(songs)
        self.panel.add_buttons(self.audio_album.playlists)
