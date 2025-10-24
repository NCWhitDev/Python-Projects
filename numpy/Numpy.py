import matplotlib.pyplot as plt
import numpy as np


""" 
    Takes the latitude and longitude as signed integers and
    constructs the appropriate file name for the TIF file. 
"""
def construct_file_name(lat, lon):
    # Ensure latitude and longitude are integers
    lat = int(lat)
    lon = int(lon)

    # Construct the filename based on the quadrant
    # Latitude: North (n) if positive, South (s) if negative
    # Longitude: East (e) if positive, West (w) if negative
    if lat < 0 and lon < 0: 
        filename = "USGS_NED_1_s" + str(abs(lat)) + "w0" + str(abs(lon)) + "_IMG.tif"
    elif lat < 0 and lon > 0:
        filename = "USGS_NED_1_s" + str(abs(lat)) + "e0" + str(abs(lon)) + "_IMG.tif"
    elif lat > 0 and lon < 0:
        filename = "USGS_NED_1_n" + str(abs(lat)) + "w0" + str(abs(lon)) + "_IMG.tif"
    elif lat > 0 and lon > 0:
        filename = "USGS_NED_1_n" + str(abs(lat)) + "e0" + str(abs(lon)) + "_IMG.tif"
    print("Constructed filename: " + filename)
    return filename


""" 
    Takes the latitude and longitude as signed integers and
    loads the appropriate file. It then trims off the boundary
    of six pixels on all four sides. 
"""
def load_trim_image(lat,lon):
    image = construct_file_name(lat, lon)
    print("Loading image file: " + image)
    
    new_image = plt.imread(image, format='tif') # Load the image
    height,width = new_image.shape
    # Array slicing: Trim off 6 pixels on all sides
    trimmed_image = new_image[6:height-6, 6:width-6]
    return trimmed_image

"""
    load the four images and construct the resulting image:
    (nw_lat, nw_lon), (nw_lat, nw_lon+1)
    (nw_lat-1, nw_lon), (nw_lat-1, nw_lon+1)
"""
def stitch_four(lat, lon):
    
    top_left = load_trim_image(lat + 1, lon - 1)
    top_right = load_trim_image(lat + 1, lon)
    bottom_left = load_trim_image(lat, lon - 1)
    bottom_right = load_trim_image(lat, lon)
    nphstack1 = np.hstack((top_left, top_right))
    nphstack2 = np.hstack((bottom_left, bottom_right))
    image = np.vstack((nphstack1, nphstack2))
    return image


""" 
    Takes the latitude, minimum longitude, and number of tiles and
    returns an image that combines tiles along a row of different
    longitudes. 
"""
def get_row(lat, long_min, num_tiles):
    row_images = []
    for i in range(num_tiles):
        lon = long_min + i
        image = load_trim_image(lat, lon)
        row_images.append(image)
    full_row = np.hstack(row_images)
    return full_row


"""
    Takes the northwest coordinate (maximum latitude, minimum longitude)
    and the number of tiles in each dimension (num_lat, num_lon) and
    constructs the image containing the entire range. "
"""
def get_tile_grid(lat_max, long_min, num_lat, num_lon):
    grid_images = []
    for i in range(num_lat):
        lat = lat_max - i
        row_image = get_row(lat, long_min, num_lon)
        grid_images.append(row_image)
    image = np.vstack(grid_images)
    return image


"""
    Get the integer coordinates of the northwest corner of the tile
    that contains this decimal (lat, lon) coordinate.
"""
def get_northwest(lat, lon):
    if lat >= 0:        # If the latitude is positive round up.
        nw_lat = int(np.ceil(lat)) 
    else:               # If the latitude is negative round down.
        nw_lat = int(np.floor(lat)) 

    if lon >= 0:        # If the longitude is positive round down.
        nw_lon = int(np.ceil(lon))
    else:               # If the longitude is negative round up.
        nw_lon = int(np.floor(lon))

    return nw_lat, nw_lon


""" 
    Takes the northwest coordinate (maximum latitude, minimum longitude)
    and the number of tiles in each dimension (num_lat, num_lon) and
    constructs the image containing the entire range. 
"""
def get_tile_grid_decimal(northwest, southeast):
    nw_lat, nw_lon = northwest
    se_lat, se_lon = southeast

    # Determine the integer tile coordinates
    lat_max, lon_min = get_northwest(nw_lat, nw_lon)
    lat_min, lon_max = get_northwest(se_lat, se_lon)

    # Calculate number of tiles in each dimension
    num_lat = lat_max - lat_min + 1
    num_lon = lon_max - lon_min + 1

    # Construct the tile grid
    image = get_tile_grid(lat_max, lon_min, num_lat, num_lon)
    return image


def testerFunc():
    # Start of tests
    # ====================== Test construct_file_name function ======================

    if construct_file_name(36, -82) != "USGS_NED_1_n36w082_IMG.tif":
        print("construct_file_name function case 1 failed. Returned: " + construct_file_name(36, -82) + " Expected: USGS_NED_1_n36w082_IMG.tif")
        return False
    
    if construct_file_name(-36, 82) != "USGS_NED_1_s36e082_IMG.tif":
        print("construct_file_name function case 2 failed. Returned: " + construct_file_name(-36, 82) + " Expected: USGS_NED_1_s36e082_IMG.tif")
        return False
    
    # ====================== Test load_trim_image function ======================

    image = load_trim_image(37, -83)
    if image.shape != (3600, 3600):
        print("load_trim_image function failed. Returned: " + str(image.shape) + " Expected (3600, 3600)")
        return False

    # ====================== Test stitch_four function ======================    

    image = stitch_four(37, -83)
    if image.shape != (7200, 7200):
        print("stitch_four function failed. Returned: " + image.shape + " Expected (7200, 7200)")
        return False
    
    # ====================== Test get_row function ======================

    # image = get_row(37, -83, 2)
    # if image.shape != (3600, 7200):
    #     print("get_row function failed. Returned: " + image.shape + " Expected (3600, 7200)")
    #     return False

    # ====================== Test get_tile_grid function ======================    

    image = get_tile_grid(37, -83, 2, 2)
    if image.shape != (7200, 7200):
        print("get_tile_grid function failed. Returned: " + image.shape + " Expected (7200, 7200)")
        return False
    
    # ====================== Test get_northwest function ======================
    # Test case 1
    result1 = get_northwest(36.211389, -81.668611) 
    if result1 != (37, -82):
        print("get_northwest function failed. Returned: " + str(result1) + " Expected (37, -82)")
        return False
    
    # Test case 2
    result2 = get_northwest(36.0000, -81.668611)
    if result2 != (36, -82):
        print("get_northwest function failed. Returned: " + str(result2) + " Expected (36, -82)")
        return False
    
    # Test case 3
    result3 = get_northwest(lat=36.211389, lon=-81.00000)
    if result3 != (37, -81):
        print("get_northwest function failed. Returned: " + str(result3) + " Expected (37, -81)")
        return False
 
    # ====================== Test get_tile_grid_decimal function ======================

    # Test case 1
    nw = (37.2, -82.7)
    se = (36.6, -82.5)
    image = get_tile_grid_decimal(nw, se)
    if image.shape != (7200, 3600):
        print("get_tile_grid_decimal function failed. Returned: " + image.shape + " Expected (7200, 3600)")
        return False
    
    # Test case 2
    nw = (37.2, -83.7)
    se = (36.6, -81.5)
    image = get_tile_grid_decimal(nw, se)
    if image.shape != (7200, 10800):
        print("get_tile_grid_decimal function failed. Returned: " + image.shape + " Expected (7200, 10800)")
        return False
    
    # Test case 3
    nw = (37.5, -82.5)
    se = (36.5, -81.5)
    image = get_tile_grid_decimal(nw, se)
    if image.shape != (7200, 7200):
        print("get_tile_grid_decimal function failed. Returned: " + image.shape + " Expected (7200, 7200)")
        return False

    # If all tests pass, return True
    return True





def main(lat, lon):
    if testerFunc() == True:
        print("\nAll functions executed successfully.")
    else:
        print("\nThere was an error in executing one or more of the functions.")


if __name__ == "__main__":
    main(36, -82)  # Example coordinates for testing   

# References:
# https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.imread.html
# https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.imshow.html
# https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.show.html
# https://numpy.org/doc/1.17/reference/routines.math.html  Very useful for numpy math functions
# https://numpy.org/doc/stable/reference/generated/numpy.ndarray.T.html
# https://numpy.org/doc/stable/reference/generated/numpy.hstack.html
# https://numpy.org/doc/stable/reference/generated/numpy.vstack.html
# https://numpy.org/doc/stable/user/basics.indexing.html#slicing-and-striding
# https://numpy.org/doc/stable/reference/generated/numpy.ceil.html
# https://numpy.org/doc/stable/reference/generated/numpy.floor.html
