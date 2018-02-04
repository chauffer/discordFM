# DiscordFM

Sets your Discord Status to what you are currently playing on LastFM.


### Running
The only supported way to run this is through Docker.

#### Environment variables

**Mandatory**

- `DISCORDFM_LASTFM_API` - Your Last.fm API key
- `DISCORDFM_LASTFM_USER` - The user to get music from
- `DISCORDFM_TOKEN`  - Discord token to use

**Non-mandatory**

- `DISCORDFM_STATUS` - Discord status (online, dnd, idle, invisible)
- `DISCORDFM_FORMAT` - Text status. Defaults to `{song} by {artist}`
