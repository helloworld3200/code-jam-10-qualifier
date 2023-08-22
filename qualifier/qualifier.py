from PIL import Image

#python -m unittest tests.py

def valid_input(image_size: tuple[int, int], tile_size: tuple[int, int], ordering: list[int]) -> bool:
    """
    Return True if the given input allows the rearrangement of the image, False otherwise.

    The tile size must divide each image dimension without remainders, and `ordering` must use each input tile exactly
    once.
    """
    modulus_x = image_size[0]%tile_size[0]
    modulus_y = image_size[1]%tile_size[1]
    #print("Modulus: ",modulus_x, modulus_y)

    if modulus_x or modulus_y:
        #print("returning from modulus")
        return False
    
    tile_count = image_size[0]/tile_size[0]*image_size[1]/tile_size[1]
    sorted_order = sorted(ordering)

    if sorted_order[-1] != tile_count-1 or len(sorted_order) > len(set(sorted_order)):
        #print("Returning from same values in sorted order")
        return False
    
    #print("Input valid")
    return True


def rearrange_tiles(image_path: str, tile_size: tuple[int, int], ordering: list[int], out_path: str) -> None:
    """
    Rearrange the image.

    The image is given in `image_path`. Split it into tiles of size `tile_size`, and rearrange them by `ordering`.
    The new image needs to be saved under `out_path`.

    The tile size must divide each image dimension without remainders, and `ordering` must use each input tile exactly
    once. If these conditions do not hold, raise a ValueError with the message:
    "The tile size or ordering are not valid for the given image".
    """
    with Image.open(image_path) as im:
        if not valid_input(im.size, tile_size, ordering):
            raise ValueError("The tile size or ordering are not valid for the given image")

        tile_count = (im.size[0]/tile_size[0], im.size[1]/tile_size[1])
        #print("Tile count before conversion: ",tile_count)
        tile_count = (int(tile_count[0]), int(tile_count[1])) # Soleley for debug purposes, replace with line below after debugging.
        #tile_count = (int(im.size[0]/tile_size[0]), int(im.size[1]/tile_size[1]))
        #print("Tile count after conversion: ",tile_count)

        tiles = []
        x_range = range(0, tile_count[0])
        y_range = range(0, tile_count[1])
        total = tile_count[0]*tile_count[1]
        print("Length of order: ",len(ordering))
        print("Length of total: ",total)
        for x in x_range:
            for y in y_range:
                pos = (x*tile_size[0], y*tile_size[1])
                tiles.append(im.crop((pos[0], pos[1], pos[0]+tile_size[0], pos[1]+tile_size[1])))
        
        output = Image.new(im.mode, im.size)

        for count, i in enumerate(ordering):
            for x in x_range:
                for y in y_range:
                    pos = (x*tile_size[0], y*tile_size[1])
                    #print("Position for current tile: ", pos)
                    im.paste(tiles[i], pos)
            print("At count: ",count," of ",total, end="\r", flush=True)

        output.save(out_path, format="png")
