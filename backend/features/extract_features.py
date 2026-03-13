import ee

# Initialize Earth Engine (make sure you authenticated already)
try:
    ee.Initialize()
except:
    ee.Authenticate()
    ee.Initialize()


def fetch_satellite_features(latitude, longitude):
    """
    Fetch real Sentinel-2 reflectance values and compute NDWI.
    """

    point = ee.Geometry.Point([longitude, latitude])

    # Use harmonized Sentinel-2 dataset
    collection = (
        ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
        .filterBounds(point)
        .filterDate("2026-02-01", "2026-02-28")   # fixed date for stability
        .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 20))
        .sort("CLOUDY_PIXEL_PERCENTAGE")
    )

    image = collection.median()

    if image is None:
        raise Exception("No satellite image found for this location")

    # Select required bands
    bands = image.select(["B2", "B3", "B4", "B8"])

    # Get mean reflectance around small buffer area
    stats = bands.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=point.buffer(30),   # 30m buffer
        scale=10,
        maxPixels=1e9
    ).getInfo()

    if stats is None:
        raise Exception("Unable to extract reflectance values")

    blue = stats.get("B2", 0)
    green = stats.get("B3", 0)
    red = stats.get("B4", 0)
    nir = stats.get("B8", 0)

    # NDWI formula
    if (green + nir) != 0:
        ndwi = (green - nir) / (green + nir)
    else:
        ndwi = 0

    return {
        "blue": float(blue),
        "green": float(green),
        "red": float(red),
        "ndwi": float(ndwi)
    }