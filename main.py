import pgerom as pe
pe.init()
ss = (1920, 1080) # Screen size
#ss = (600, 600)
pe.display.make(ss, "DRAW TEST", 2) # 2 for fullscreen
pe.display_work = pe.display_a
# Size Settings
maxzoom = 10
minzoom = 0.25
rect = (500, 500)

surface = pe.pygame.Surface(rect)

# Zoom and pan presets
debug = False # True to debug zoom and pan
zoompoint = (0, 0)
zoom_start_pos = (0, 0)
ss = pe.display_a.get_size()
scalex = 1
scaley = 1
posx = ss[0]/2 - rect[0]/2 # center X
posy = ss[1]/2 - rect[1]/2 # center Y
fingers = []
zooming = False
moving = False
distance = 0
#
def worldtoscreen(worldx, worldy):
    return worldx * scalex + posx, \
           worldy * scaley + posy
def screentoworld(screenx, screeny):
    return (screenx - posx) / scalex, \
           (screeny - posy) / scaley
while True:
    # Handle zoom and pan
    for pe.event.c in pe.event.get():
        pe.event.quitcheckauto()
        size = pe.display.get.size()
        if pe.event.c.type == pe.pygame.FINGERDOWN:
            fingers.append({
                'id':pe.event.c.finger_id,
                'pos':(pe.event.c.x*size[0],pe.event.c.y*size[1])
            })
        elif pe.event.c.type == pe.pygame.FINGERMOTION:
            i = 0
            while i < len(fingers):
                if fingers[i]['id'] == pe.event.c.finger_id:
                    fingers[i]['pos'] = (pe.event.c.x*size[0],pe.event.c.y*size[1])
                    break
                i += 1
        elif pe.event.c.type == pe.pygame.FINGERUP:
            i = 0
            while i < len(fingers):
                if fingers[i]['id'] == pe.event.c.finger_id:
                    del fingers[i]
                    i -= 1
                i += 1
    pe.fill.full(pe.color.black)
    if len(fingers) == 2 and not zooming:
        oldx = round(posx, 2)
        oldy = round(posy, 2)
        distance = pe.math.dist(fingers[0]['pos'], fingers[1]['pos'])
        zoom_start_pos = pe.math.lerp(
            (250, 250),
            (250, 250),
            distance / 2
        )
        start_scalex = scalex
        start_scaley = scaley
        original = tuple(zoom_start_pos)
        zoom_start_pos = screentoworld(*zoom_start_pos)
        zooming = True
        moving = False
    elif len(fingers) == 2 and zooming:
        distance_new = pe.math.dist(fingers[0]['pos'], fingers[1]['pos'])
        change = distance_new - distance
        change *= 0.02
        scalex = int(min(max(start_scalex * 1+change, minzoom), maxzoom))
        scaley = int(min(max(start_scaley * 1+change, minzoom), maxzoom))

        zoompoint = pe.math.lerp(
            (250, 250),
            (250, 250),
             distance_new / 2
        )
        afterzoomx, afterzoomy = screentoworld(*original)
        #print((zoom_start_pos[0] - afterzoomx), (zoom_start_pos[1] - afterzoomy))
        dist = pe.math.dist(zoom_start_pos, (afterzoomx, afterzoomy))
        diffx, diffy = (zoom_start_pos[0] - afterzoomx), (zoom_start_pos[1] - afterzoomy)
        posx -= diffx * scalex
        posy -= diffy * scaley
        original = tuple(zoompoint)
        zoom_start_pos = screentoworld(*zoompoint)
    elif len(fingers) == 1 and not moving and not zooming:
        distance = fingers[0]['pos']
        moving = True
    elif len(fingers) == 1 and moving and not zooming:
        posx += (fingers[0]['pos'][0] - distance[0])# * 1.5
        posy += (fingers[0]['pos'][1] - distance[1])# * 1.5
        distance = fingers[0]['pos']
    else:
        if zooming:
            print(f'offset: ({oldx}, {oldy}) world_start_pos: {zoom_start_pos} zoompoint: {zoompoint} start_scale: ({start_scalex}, {start_scaley}) -> offset: ({posx}, {posy}) scale: ({scalex}, {scaley})')
            print(f'offset_change: ({posx-oldx}, {posy-oldy}) scale_change: ({scalex-start_scalex, scaley-start_scaley})')
        zooming = False
        moving = False
        posx = int(posx / 500) * 500
        posy = int(posy / 500) * 500

    #
    temp = pe.display_a
    pe.display_a = surface
    # Inner display

    pe.fill.full(pe.color.verydarkgray)


    #
    if debug:
        pe.draw.circle(pe.color.black, screentoworld(*pe.mouse.pos()), 10, 0)
    surface = pe.display_a
    pe.display_a = temp
    # Draw the inner display

    cropped = pe.pygame.transform.scale(surface, (rect[0]*scalex, rect[1]*scaley))
    pe.draw.rect(pe.color.red, (posx, posy, rect[0]*scalex, rect[1]*scaley), 20)
    pe.display.blit.rect(cropped, (posx, posy, rect[0]*scalex, rect[1]*scaley))

    # Debug draw and update
    if debug:
        pe.draw.circle(pe.color.white, worldtoscreen(*screentoworld(*pe.mouse.pos())), 5,2)
    if debug and zooming:
        try:
            pe.draw.line(pe.color.blue, worldtoscreen(*zoom_start_pos), worldtoscreen(afterzoomx, zoom_start_pos[1]),1)
            pe.draw.line(pe.color.blue, worldtoscreen(afterzoomx, zoom_start_pos[1]), worldtoscreen(afterzoomx, afterzoomy),1)
            pe.draw.line(pe.color.red, worldtoscreen(*zoom_start_pos), worldtoscreen(afterzoomx, afterzoomy),1)
        except:
            print("waiting for values")
    pe.display.update()