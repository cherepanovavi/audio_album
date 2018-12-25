import wx
import os
import shutil
from album_cover import AlbumCover
from tag_dialog import TagDialog, update_song

class SongMenu(wx.Menu):
    def __init__(self, audio_album, song):
        wx.Menu.__init__(self)
        self.audio_album = audio_album
        self.song = song
        # self.submenu = song.submenu()
        # text = 'Add "{}" to playlist'.format(song.title)
        # self.AppendSubMenu(self.submenu, text, 'Click here to add this song to some playlist')
        items = ['Change tags', 'Rename file', 'Change directory', 'Delete file', 'Show album cover',
                 'Delete song from playlist']
        helps = ['Press here to view and change id3 tags', 'Press here to change file name of this song',
                 'Press here to change song file directory', 'Press here to delete song file from your computer',
                 'Press here to see album cover if it exists', 'Press here to delete this song from some playlist']
        handlers = [self.change_id3_tags, self.rename_file, self.change_dir, self.delete_file, self.show_album,
                    self.delete_from_playlist]
        for i in range(0, 6):
            item = self.Append(-1, item=items[i], kind=wx.ITEM_NORMAL, helpString=helps[i])
            self.Bind(wx.EVT_MENU, handlers[i], item)

    def change_id3_tags(self, event):
        TagDialog(None, self.song, self.audio_album)
        warning()

    def delete_from_playlist(self, event):
        l = [p.title for p in self.audio_album.song_playlists[self.song]]
        ch = wx.SingleChoiceDialog(None, 'Choose a playlist to delete song from', 'Choosing playlist', l)
        if ch.ShowModal() == wx.ID_OK:
            selection = ch.GetSelection()
            self.audio_album.delete_song_from_playlist(self.song, self.audio_album.playlists_titles[l[selection]])
        ch.Destroy()

    def rename_file(self, event):
        dlg = wx.TextEntryDialog(None, 'Enter new file name', 'Rename file')
        dlg.SetValue(self.song.file_name)
        if dlg.ShowModal() == wx.ID_OK:
            file_name = dlg.GetValue()
            try:
                os.rename(self.song.file, self.get_song_dir() + file_name)
                update_song(self.audio_album, self.song, {'file': self.get_song_dir() + file_name,
                                                          'name': file_name})
            except FileExistsError as e:
                wx.MessageBox(e.strerror, 'Error', wx.ICON_ERROR)
        dlg.Destroy()
        warning()

    def delete_file(self, event):
        result = wx.MessageBox('Are you sure you want to delete this file?', 'Delete file', wx.YES_NO)
        if result == wx.YES:
            try:
                os.remove(self.song.file)
                self.audio_album.delete_song(self.song)
            except OSError as e:
                wx.MessageBox(e, 'Error', wx.ICON_ERROR)
        warning()

    def change_dir(self, event):
        dir_path = wx.DirSelector('Choose a new folder for file')
        if dir_path != '':
            file = dir_path + os.sep + self.song.file_name
            shutil.move(self.song.file, file)
            update_song(self.audio_album, self.song, {'file': file, 'name': self.song.file_name})
        warning()

    def show_album(self, event):
        if self.song.image_data is None:
            wx.MessageBox('This song haven\'t album cover')
        else:
            fr = AlbumCover(self.song)
            fr.Show()

    def get_song_dir(self):
        return self.song.file[0:self.song.file.find(self.song.file_name)]


class SongPlaylistMenu(wx.Menu):
    def __init__(self, audio_album, song):
        wx.Menu.__init__(self)
        self.audio_album = audio_album
        self.song = song
        for pl in audio_album.playlists:
            item = self.Append(-1, item=pl.title, kind=wx.ITEM_NORMAL)
            self.Bind(wx.EVT_MENU, self.on_popup_item_selected, item)
        self.AppendSeparator()
        cr_pl = self.Append(-1, item='Create new playlist', kind=wx.ITEM_NORMAL)
        self.Bind(wx.EVT_MENU, self.create_playlist, cr_pl)

    def on_popup_item_selected(self, event):
        item = self.FindItemById(event.Id)
        if not self.audio_album.add_song_to_playlist(self.song, self.audio_album.playlists_titles[item.GetText()]):
            wx.MessageBox('This playlist already contains this song')

    def create_playlist(self, event):
        title = get_playlist_title()
        if not self.audio_album.add_playlist(title, [self.song]):
            wx.MessageBox('Playlist with this name already exist')


def get_playlist_songs(audio_album):
    l = list(audio_album.songs_titles.keys())
    ch = wx.MultiChoiceDialog(None, 'Choose songs to add to your playlist', 'Choosing songs', l)
    songs = []
    if ch.ShowModal() == wx.ID_OK:
        selections = ch.GetSelections()
        songs = [audio_album.songs_titles[l[i]] for i in selections]
    ch.Destroy()
    return songs


def get_playlist_title():
    dlg = wx.TextEntryDialog(None, 'Enter playlist title', 'Playlist title')
    title = 'New playlist'
    dlg.SetValue(title)
    if dlg.ShowModal() == wx.ID_OK:
        title = dlg.GetValue()
    dlg.Destroy()
    return title


def warning():
    wx.MessageBox('Press on button update, please, or app running can be unpredictable')


class PlaylistMenu(wx.Menu):
    def __init__(self, playlist, audio_album):
        wx.Menu.__init__(self)
        self.playlist = playlist
        self.audio_album = audio_album
        items = ['Add song to playlist', 'Delete playlist', 'Change song order']
        handlers = [self.add_song, self.delete_playlist, self.change_order]
        for i in range(0, 3):
            item = self.Append(-1, item=items[i], kind=wx.ITEM_NORMAL)
            self.Bind(wx.EVT_MENU, handlers[i], item)

    def add_song(self, event):
        songs = get_playlist_songs(self.audio_album)
        if not self.audio_album.add_songs_to_playlist(songs, self.playlist):
            wx.MessageBox('This playlist already contains some of chosen songs')

    def delete_playlist(self, event):
        result = wx.MessageBox('Are you sure you want to delete this playlist?', 'Delete playlist', wx.YES_NO)
        if result == wx.YES:
            try:
                self.audio_album.delete_playlist(self.playlist)
            except ValueError as e:
                wx.MessageBox(e, 'Error', wx.ICON_ERROR)

    def change_order(self, event):
        o = SongOrderChanger(self.playlist, self.audio_album)
        o.Show()


class SongOrderChanger(wx.Dialog):
    def __init__(self, playlist, audio_album):
        wx.Dialog.__init__(self, None)
        self.playlist = playlist
        self.audio_album = audio_album
        self.selection = -1
        self.p = wx.Panel(self)
        self.s = wx.BoxSizer(wx.VERTICAL)
        update = wx.Button(self, label='UPDATE')
        self.s.Add(update)
        update.Bind(wx.EVT_BUTTON, self.update)
        self.buttons = []
        self.h_s = wx.BoxSizer(wx.HORIZONTAL)
        self.up = None
        self.down = None
        self.add_buttons()
        self.p.SetSizer(self.s)

    def add_buttons(self):
        for song in self.playlist.songs:
            button = wx.Button(self.p, song.id, label=song.title, size=(200, 25), style=wx.BU_LEFT)
            self.s.Add(button)
            self.buttons.append(button)
            button.Bind(wx.EVT_BUTTON, self.change_selection)
        self.up = wx.Button(self.p, -1, label='UP')
        self.down = wx.Button(self.p, -1, label='DOWN')
        self.h_s.Add(self.up)
        self.h_s.Add(self.down)
        self.up.Bind(wx.EVT_BUTTON, self.move_up)
        self.down.Bind(wx.EVT_BUTTON, self.move_down)
        self.s.Add(self.h_s)
        self.Layout()

    def delete_buttons(self):
        for button in self.buttons:
            button.Destroy()
        self.up.Destroy()
        self.down.Destroy()
        self.buttons = []

    def update(self, event):
        self.delete_buttons()
        self.add_buttons()

    def move_up(self, event):
        i = 0 if self.selection == -1 else self.playlist.songs.index(self.audio_album.songs_id[self.selection])
        self.playlist.swap_songs(i, i-1)

    def move_down(self, event):
        i = 0 if self.selection == -1 else self.playlist.songs.index(self.audio_album.songs_id[self.selection])
        self.playlist.swap_songs(i, i+1)

    def change_selection(self, event):
        self.selection = event.Id
