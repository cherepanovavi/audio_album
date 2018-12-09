import os
import wx
import wx.media
import wx.lib.buttons as buttons
import audio_album

# unbind?
dirName = os.path.dirname(os.path.abspath(__file__))
bitmapDir = os.path.join(dirName, 'bitmaps')


class PlayerTab(wx.Panel):
    def __init__(self, parent, au_album):
        wx.Panel.__init__(self, parent)
        self.audio_album = au_album
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.media_player = wx.media.MediaCtrl(self, style=wx.SIMPLE_BORDER)
        self.play_pause_btn = None
        self.buttons = []
        self.add_controls()
        self.now_playing = None
        self.idx = -1
        self.text = wx.StaticText(self, label="Song is not selected", pos=(60, 80), style=wx.ALIGN_CENTER)
        self.sizer.Add(self.text)
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
                        'name': 'prev', 'size': (200, 200), 'pos': (60, 10)})

        img = wx.Bitmap(os.path.join(bitmapDir, "player_play.png"))
        self.play_pause_btn = buttons.GenBitmapToggleButton(self, bitmap=img, name="play", size=wx.DefaultSize,
                                                            pos=(158, 10))
        self.play_pause_btn.Enable(False)

        img = wx.Bitmap(os.path.join(bitmapDir, "player_pause.png"))
        self.play_pause_btn.SetBitmapSelected(img)
        self.play_pause_btn.SetInitialSize()

        self.play_pause_btn.Bind(wx.EVT_BUTTON, self.on_play)
        self.sizer.Add(self.play_pause_btn, 0, wx.LEFT, 3)

        btn_data = [
            {'bitmap': 'player_next.png',
             'handler': self.on_next, 'name': 'next',
             'size': (50, 50), 'pos': (220, 10)},
            {'bitmap': 'player_add.png',
             'handler': self.on_add, 'name': 'add',
             'size': (50, 50), 'pos': (320, 10)}
        ]
        for btn in btn_data:
            self.build_btn(btn)
        for btn in self.buttons:
            btn.Enable(False)

    def build_btn(self, btn_dict):
        bmp = btn_dict['bitmap']
        handler = btn_dict['handler']
        img = wx.Bitmap(os.path.join(bitmapDir, bmp))
        btn = buttons.GenBitmapButton(self, bitmap=img, name=btn_dict['name'], pos=btn_dict['pos'])
        btn.SetInitialSize()
        btn.Bind(wx.EVT_BUTTON, handler)
        self.buttons.append(btn)
        self.sizer.Add(btn, 0, wx.LEFT, 3)

    def on_add(self, event):
        self.PopupMenu(self.now_playing[self.idx].submenu, pos=(320, 10))

    def on_play(self, event=None):
        print("!")
        print(self.media_player.GetState())
        if event is None:
            self.media_player.Play()
        elif event is not None and event.GetIsDown():
            self.media_player.Play()
        else:
            self.media_player.Pause()

    def on_prev(self, event):
        # self.idx = self.now_playing.index[]
        song = self.now_playing[(self.idx - 1) % len(self.now_playing)]
        self.media_player.Load(self.now_playing[(self.idx - 1) % len(self.now_playing)].file)
        self.idx = self.idx - 1

    def on_next(self, event):
        self.media_player.Stop()
        song = self.now_playing[(self.idx + 1) % len(self.now_playing)]
        self.media_player.Load(song.file)
        self.idx = self.idx + 1
        self.change_text(song)
        # self.on_play()

    def state_changed(self, event):
        self.media_player.Play()

    def change_now_playing(self, now_playing):
        self.now_playing = now_playing
