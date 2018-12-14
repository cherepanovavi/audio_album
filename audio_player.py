import os
import wx
import wx.media
import wx.lib.buttons as buttons
from album_cover import AlbumCover

# unbind?
dirName = os.path.dirname(os.path.abspath(__file__))
bitmapDir = os.path.join(dirName, 'bitmaps')


class PlayerTab(wx.Panel):
    def __init__(self, parent, au_album):
        wx.Panel.__init__(self, parent)
        self.audio_album = au_album
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer_vertical = wx.BoxSizer(wx.VERTICAL)
        self.text = wx.StaticText(self, label="Song is not selected")
        self.sizer_vertical.Add(self.text, 1, wx.LEFT, 0)
        self.sizer_vertical.Add(self.sizer)
        self.SetSizer(self.sizer_vertical)
        self.media_player = wx.media.MediaCtrl(self, style=wx.SIMPLE_BORDER)
        self.play_pause_btn = None
        self.buttons = []
        self.add_controls()
        self.now_playing = None
        self.idx = -1
        self.media_player.Bind(wx.media.EVT_MEDIA_STATECHANGED, self.state_changed)

    def on_song(self, event):
        self.play_pause_btn.Enable(True)
        for btn in self.buttons:
            btn.Enable(True)
        song = self.audio_album.songs_id[event.Id]
        self.change_text(song)
        self.media_player.Load(song.file)
        self.idx = self.now_playing.index(song)
        self.on_play()

    def change_text(self, song):
        label = ('{} - {} - {}'.format(song.artist.title(), song.album.title(), song.title))
        wx.StaticText.SetLabel(self.text, label)

    def add_controls(self):
        self.build_btn({'bitmap': 'player_prev.png', 'handler': self.on_prev,
                        'name': 'prev'})

        img = wx.Bitmap(os.path.join(bitmapDir, "player_play.png"))
        self.play_pause_btn = buttons.GenBitmapToggleButton(self, bitmap=img, name="play")
        self.play_pause_btn.Enable(False)

        img = wx.Bitmap(os.path.join(bitmapDir, "player_pause.png"))
        self.play_pause_btn.SetBitmapSelected(img)

        self.play_pause_btn.Bind(wx.EVT_BUTTON, self.on_play)
        self.sizer.Add(self.play_pause_btn, 0, wx.LEFT, 0)
        self.sizer.SetSizeHints(self)

        btn_data = [
            {'bitmap': 'player_next.png',
             'handler': self.on_next, 'name': 'next'},
            {'bitmap': 'player_add.png',
             'handler': self.on_add, 'name': 'add'},
            {'bitmap': 'player_album.png',
             'handler': self.on_album_cover, 'name': 'album cover'}
        ]
        for btn in btn_data:
            self.build_btn(btn)
        for btn in self.buttons:
            btn.Enable(False)

    def build_btn(self, btn_dict):
        bmp = btn_dict['bitmap']
        handler = btn_dict['handler']
        img = wx.Bitmap(os.path.join(bitmapDir, bmp))
        btn = buttons.GenBitmapButton(self, bitmap=img, name=btn_dict['name'])
        btn.Bind(wx.EVT_BUTTON, handler)
        self.buttons.append(btn)
        self.sizer.Add(btn, 0, wx.RIGHT, 0)

    def on_add(self, event):
        self.PopupMenu(self.now_playing[self.idx].submenu(), self.ScreenToClient(wx.GetMousePosition()))

    def on_play(self, event=None):
        if event is None:
            self.media_player.Play()
        elif event is not None and event.GetIsDown():
            self.media_player.Play()
        else:
            self.media_player.Pause()

    def on_prev(self, event):
        self.idx = (self.idx - 1) % len(self.now_playing)
        song = self.now_playing[self.idx]
        self.media_player.Load(song.file)
        self.change_text(song)

    def on_next(self, event):
        self.idx = (self.idx + 1) % len(self.now_playing)
        self.media_player.Stop()
        song = self.now_playing[self.idx]
        self.media_player.Load(song.file)
        self.change_text(song)

    def on_album_cover(self, event):
        song = self.now_playing[self.idx]
        if song.image_data is None:
            wx.MessageBox('This song hasn\'t album cover')
        else:
            fr = AlbumCover(song)
            fr.Show()

    def state_changed(self, event):
        self.media_player.Play()

    def change_now_playing(self, now_playing):
        self.now_playing = now_playing

    def set_idx(self, idx):
        if idx < len(self.now_playing):
            self.idx = idx
            self.media_player.Load(self.now_playing[idx].file)
