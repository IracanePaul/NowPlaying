ScriptName = "Song"
Website = "https://music.netslum.dev/"
Description = "Pulls currently playing song from Spotify when called with 'commandName'" #See Line 15
Creator = "AuroTheAzure"
Version = "1.0.0"

commandName = "!song"     #String to start the command
cooldown = 20            #Cooldown of the command in seconds
userCooldown = 30        #Cooldown for individual user
spotify_username = "smallmaddog"    #Username to use to pull song from spotify

import json


def Init():
    return


def Execute(data):
    if data.GetParam(0) != commandName or Parent.IsOnCooldown(ScriptName, commandName) or Parent.IsOnUserCooldown(ScriptName, commandName, data.User): #or not Parent.IsLive():
        #If we're not called with our command name, or we're on cooldown, or the user who called it is on cooldown,
        #or streamer's not live, quit.
        #Parent.Log("!song", "We're trying our best.")
        return
    else:
        #Parent.Log("!song", "Running...?")
        Songname, Artists = GetData()
        Parent.Log("!song", "Song: {}" "Artists: {}".format(Songname, Artists))
        returnstring = FormatString(Songname, Artists)
        Parent.SendStreamMessage(returnstring)
        #Parent.AddUserCooldown(ScriptName, commandName, data.User, userCooldown)
        #Parent.AddCooldown(ScriptName, commandName, cooldown)

def Tick():
    return


def GetData():
    jsonblob = Parent.GetRequest("https://music.netslum.dev/u/{}/current-song.json".format(spotify_username), headers = {})
    Parent.Log("!song", jsonblob)
    jsonblob = json.loads(jsonblob)
    if jsonblob['status'] != 200:
        Parent.Log("!song", "???")
        Parent.SendStreamMessage("music.netslum.dev appears to be down.")
        return -1, -1
    else:
        Parent.Log("!song", "??")
        SpotifySong = json.loads(jsonblob['response'])
        return SpotifySong['name'], SpotifySong['artists']
    
def FormatString(SongName, ArtistList):
    string = SongName
    string += " by "
    for each in ArtistList:
        string += "{}, ".format(each)
    return string[:-2]