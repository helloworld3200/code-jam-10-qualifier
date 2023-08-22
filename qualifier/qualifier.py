from PIL import Image

def valid_input(image_size: tuple[int, int], tile_size: tuple[int, int], ordering: list[int]) -> bool:
    """
    Return True if the given input allows the rearrangement of the image, False otherwise.

    The tile size must divide each image dimension without remainders, and `ordering` must use each input tile exactly
    once.
    """
    if image_size[0]%tile_size[0] or image_size[1]%tile_size[1]:
        print("in image size modulus")
        return False
    
    tile_count = image_size[0]/tile_size[0]*image_size[1]/tile_size[1]
    sorted_order = sorted(ordering)

    if sorted_order[-1] != tile_count-1 or len(sorted_order) > len(set(sorted_order)):
        print("in image tile sort")
        return False
    
    print("past all")
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
        tiles = []
        for x in range(0, tile_count[0]):
            for y in range(0, tile_count[1]):
                tiles.append(im.crop((x*tile_size[0], y*tile_size[1], tile_size[0], tile_size[1])))
        
        for i in ordering:
            for x in range(0, tile_count[0]):
                for y in range(0, tile_count[1]):
                    im.paste(im, tiles[i], (x*tile_size[0],y*tile_size[1]))
