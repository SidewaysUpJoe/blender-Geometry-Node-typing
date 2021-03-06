import bpy
from bpy.app import handlers



RENDER_ON  = 0
DEBUG = 1

PERIOD_SOUND = 1
SPACE_SOUND = 0
NEWLINE_SOUND = 0


GEO_OBJ_NAME = 'GEO_OBJ_TEST'
GEO_ATT_CHR_COUNT = 'Chr_Count'
GEO_ATT_PERIOD = 'Chr_Period' # = 2
GEO_ATT_SPACE = 'Chr_Space' # = 3
GEO_ATT_NEWLINE = 'Chr_Newline' # = 4

SPEAKER_NAME = 'Speaker'

NLA_TRACK_NAME = 'SoundTrack'
NLA_STRIP_NAME = 'NLA Strip'
NLA_STRIP_LEN = 20

#
# END OF EDTING
#




oldChr = 00.0

def frame_change_def(scene):
    global oldChr
    
    GEO_OBJ = scene.objects[GEO_OBJ_NAME]
    GEO_ATT = GEO_OBJ.evaluated_get(bpy.context.evaluated_depsgraph_get()).data
    
    speaker = scene.objects[SPEAKER_NAME]
    SoundStripTyping = speaker.animation_data.nla_tracks[NLA_TRACK_NAME].strips[NLA_STRIP_NAME]
 
    newChr = oldChr
    
    # fail safes incase Attridute names are not set correctly
    chrSpace = 0
    chrPeriod = 0 
    chrNewline = 0
    
    try:
        newChr = GEO_ATT.attributes[GEO_ATT_CHR_COUNT].data[0].value
        chrSpace = GEO_ATT.attributes[GEO_ATT_SPACE].data[0].value
        chrPeriod = GEO_ATT.attributes[GEO_ATT_PERIOD].data[0].value
        chrNewline = GEO_ATT.attributes[GEO_ATT_NEWLINE].data[0].value
    except KeyError: 
        pass
    finally: 
        
         
        if newChr != oldChr:  
            
            if chrPeriod == 2:
                if PERIOD_SOUND == 1:
                    moveTypingSound(scene, SoundStripTyping)
                    if DEBUG: print(" " * 4, "PERIOD   ", "YES Sound")
                else:
                    oldChr = newChr
                    if DEBUG: print(" " * 4, "PERIOD   ", "NO Sound")
                    return
                    
            if chrSpace == 3:
                if SPACE_SOUND == 1:
                    moveTypingSound(scene, SoundStripTyping)
                    if DEBUG: print(" " * 4, "SPACE   ", "YES Sound")
                else:
                    oldChr = newChr
                    if DEBUG: print(" " * 4, "SPACE   ", " NO Sound")
                    return
            
            if chrNewline == 4:
                if NEWLINE_SOUND == 1:
                    moveTypingSound(scene, SoundStripTyping)
                    if DEBUG: print(" " * 4, "NEWLINE  ", " YES Sound")
                else:
                    oldChr = newChr
                    if DEBUG: print(" " * 4, "NEWLINE  ", "NO Sound")
                    return
            
            
            moveTypingSound(scene, SoundStripTyping)
                    
                
        oldChr = newChr
        

def moveTypingSound(scene, SoundStrip):
    global NLA_STRIP_LEN
    currentFrame = scene.frame_current
    
    if DEBUG: print(" " * 4, "BEFORE   ", SoundStrip.frame_start, SoundStrip.frame_end) 
    
    ssStart = currentFrame 
    ssEnd = ssStart + NLA_STRIP_LEN
    SoundStrip.frame_start = ssStart
    SoundStrip.frame_end = ssEnd 
    
    if DEBUG: print(" " * 4, "AFTER    ", SoundStrip.frame_start, SoundStrip.frame_end)
    if DEBUG: print("-" * 10)
    



frame_handlers = [getattr(handlers, name)
        for name in dir(handlers) if name.startswith("render_")]

def clear_handlers():
    for  handler in frame_handlers:
        handler.clear()




clear_handlers()
bpy.app.handlers.frame_change_post.clear()

print("SOUND SCRIPT ON - ", bpy.path.basename(bpy.context.blend_data.filepath))


def register():
    if RENDER_ON:
        bpy.app.handlers.render_write.append(frame_change_def)
        print("RENDER ON")
    else:
        bpy.app.handlers.frame_change_post.append(frame_change_def)
        print("RENDER OFF ")
 
if __name__ == "__main__":
    register()
