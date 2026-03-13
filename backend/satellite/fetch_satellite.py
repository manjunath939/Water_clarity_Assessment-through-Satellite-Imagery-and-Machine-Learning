import ee
from datetime import datetime, timedelta

def fetch_satellite_features(latitude, longitude):
    project_id=os.getenv(project_id="project_id1")
    ee.Initialize(project=project_id)

    point = ee.Geometry.Point([float(longitude), float(latitude)])

    # Use dynamic recent date range (last 90 days)
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=90)

    collection = (
        ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
        .filterBounds(point)
        .filterDate(start_date.strftime("%Y-%m-%d"),
                    end_date.strftime("%Y-%m-%d"))
        .sort("CLOUDY_PIXEL_PERCENTAGE")
    )

    image = collection.first()

    # 🔥 ADD THIS CHECK
    if image is None:
        raise Exception("No Sentinel-2 image found for this location.")

    region = point.buffer(500).bounds()

    bands = image.select(["B2", "B3", "B4", "B8"])

    stats = bands.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=region,
        scale=10,
        maxPixels=1e9
    ).getInfo()

    # 🔥 ADD SAFETY CHECK
    if stats is None:
        raise Exception("Unable to extract band statistics.")

    blue = stats.get("B2")
    green = stats.get("B3")
    red = stats.get("B4")
    nir = stats.get("B8")

    if None in [blue, green, red, nir]:
        raise Exception("Incomplete band data retrieved.")

    ndwi = (green - nir) / (green + nir)

    return {
        "blue": blue,
        "green": green,
        "red": red,
        "ndwi": ndwi
    }