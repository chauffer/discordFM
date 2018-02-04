import asyncio
import os
import signal
import sys

import discord
import pylast
from discord import Status
from pylast import Track

token = os.environ['DISCORDFM_TOKEN']
config = {
    'lastfm_api': os.environ['DISCORDFM_LASTFM_API'],
    'lastfm_user': os.environ['DISCORDFM_LASTFM_USER'],
    'status': os.getenv('DISCORDFM_STATUS', 'online'),
    'format': os.getenv('DISCORDFM_FORMAT', '{song} by {artist}'),
}


class DiscordFM(discord.Client):
    _current_track = ''

    def __init__(self, conf, **options):
        super().__init__(**options)

        self.conf = conf
        self.status = Status.online

        if not sys.platform.startswith('win'):  # pragma: no cover
            self.loop.add_signal_handler(
                getattr(signal, 'SIGTERM'),
                self.exit,
            )

    async def on_ready(self):
        print('-' * 48)
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('-' * 48)

        self.status = Status[self.conf['status']]

        while True:
            try:
                await self.set_now_playing(self.get_np(), self.status)
                await asyncio.sleep(5)
            except pylast.WSError as e:
                print('Error: ' + e.details)
                self.exit()

    async def set_now_playing(self, track: Track, status: Status):
        if track is None:
            if self._current_track is not None:
                self._current_track = None
                await self.now_playing(None, status)
            return

        new_track = self.conf['format'].format(
            artist=track.get_artist().get_name(),
            song=track.get_name(),
        )

        if new_track != self._current_track:
            self._current_track = new_track
            print(f'Now playing: {self._current_track}')
            await self.now_playing(self._current_track, status)

    async def now_playing(self,
        song: str = None, status: Status = Status.online):

        if song is None:
            await self.change_presence(game=None)
            return

        await self.change_presence(
            game=discord.Game(name=song),
            status=status,
        )

    async def close(self):
        print('Closing...')
        await self.now_playing(None, status=self.status)
        await super().close()

    def get_np(self):

        return pylast.LastFMNetwork(
            api_key=config['lastfm_api']
        ).get_user(config['lastfm_user']).get_now_playing()

    @staticmethod
    def exit():
        # This gets handled in the run() method
        raise KeyboardInterrupt


if __name__ == '__main__':
        DiscordFM(config).run(token, bot=False)
