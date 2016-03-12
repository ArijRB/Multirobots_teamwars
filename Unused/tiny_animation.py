sprite_name{(8,0)} = "boy"

def get_sprite_name(p):
    return sprite_name[p] if p in sprite_name else None

def update_sprite_image(lastchange,img)
"""
    lastchange is the number of frames since the last image was changed for animation purposes
    img is a pointer to the current animation image 
"""
{
  "boy": {

    "down": [(8,0),(8,1),(8,2)],
    "left": [(9,0),(9,1),(9,2)],
    "right":[(10,0),(10,1),(10,2)],
    "up":   [(11,0),(11,1),(11,2)]
  }
}
