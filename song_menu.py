import wx
import os
import shutil


def update_song(audio_album, song, song_file=None):
    pls = audio_album.song_playlists[song.title]
    audio_album.delete_song(song)
    if song_file is None:
        s = audio_album.add_song(song.file, song.file_name)
    else:
        s = audio_album.add_song(song_file['file'], song_file['name'])
    for pl in pls:
        audio_album.add_song_to_playlist(s, pl)


class SongMenu(wx.Menu):
    def __init__(self, audio_album, song):
        wx.Menu.__init__(self)
        self.audio_album = audio_album
        self.song = song
        self.submenu = SongSubMenu(audio_album, song)
        text = 'Add "{}" to playlist'.format(song.title)
        self.AppendSubMenu(self.submenu, text, 'Click here to add this song to some playlist')
        items = ['Change tags', 'Rename file', 'Change directory', 'Delete file']
        helps = ['Press here to view and change id3 tags', 'Press here to change file name of this song',
                 'Press here to change song file directory', 'Press here to delete song file from your computer']
        handlers = [self.change_id3_tags, self.rename_file, self.change_dir, self.delete_file]
        for i in range(0, 4):
            item = self.Append(-1, item=items[i], kind=wx.ITEM_NORMAL, helpString=helps[i])
            self.Bind(wx.EVT_MENU, handlers[i], item)

    def change_id3_tags(self, event):
        GetData(None, self.song, self.audio_album)

    def rename_file(self, event):
        dlg = wx.TextEntryDialog(None, 'Enter new file name', 'Rename file')
        dlg.SetValue(self.song.file_name)
        if dlg.ShowModal() == wx.ID_OK:
            file_name = dlg.GetValue()
            try:
                os.rename(self.song.file, self.get_song_dir()+file_name)
                update_song(self.audio_album, self.song, {'file': self.get_song_dir()+file_name,
                'name': file_name})
            except FileExistsError as e:
                wx.MessageBox(e.strerror, 'Error', wx.ICON_ERROR)
        dlg.Destroy()

    def delete_file(self, event):
        wx.MessageBox('Are you sure you want to delete this file?', 'Delete file', wx.YES_NO)
        try:
            os.remove(self.song.file)
            self.audio_album.delete_song(self.song)
        except OSError as e:
            wx.MessageBox(e, 'Error', wx.ICON_ERROR)

    def change_dir(self, event):
        dir_path = wx.DirSelector('Choose a new folder for file')
        if dir_path != '':
            file = dir_path+'\\'+ self.song.file_name
            shutil.move(self.song.file, file)
            update_song(self.audio_album, self.song, {'file': file, 'name': self.song.file_name})

    def get_song_dir(self):
        return self.song.file[0:self.song.file.find(self.song.file_name)]


class GetData(wx.Dialog):
    def __init__(self, parent, song, audio_album):
        wx.Dialog.__init__(self, parent, wx.ID_ANY, "Tag Input", size=(650, 240))
        self.song = song
        self.audio_album = audio_album
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
        new_title = self.title.GetValue()
        new_album = self.album.GetValue()
        new_artist = self.artist.GetValue()
        if new_album != self.song.album or new_artist != self.song.artist or new_title != self.song.title:
            self.song.change_id3_tags({'title': new_title , 'artist': new_artist,
                                   'album': new_album})
            update_song(self.audio_album, self.song)
        self.Destroy()


class SongSubMenu(wx.Menu):
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
        self.audio_album.add_song_to_playlist(self.song, self.audio_album.playlists_titles[item.GetText()])

    def create_playlist(self, event):
        dlg = wx.TextEntryDialog(None, 'Enter playlist title', 'Playlist title')
        title = 'New playlist'
        dlg.SetValue(title)
        if dlg.ShowModal() == wx.ID_OK:
            title = dlg.GetValue()
        dlg.Destroy()
        playlist = self.audio_album.add_playlist(title)
        self.audio_album.add_song_to_playlist(self.song, playlist)
