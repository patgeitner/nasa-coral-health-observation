import time
import numpy as np
import requests
import argparse


class AllenCoralGeomorphicExtractor():
    # Convert to bounding_box
    def __init__(self, latitude_min=-81.882919311523,
                 latitude_max=-81.850692749023,
                 longitude_min=24.208717346191,
                 longitude_max=24.405982971191,
                 download_path='./AllenCoralAtlas/'
                 ):
        """
        Extracts benthic data from the Allen Coral Atlas API
        """
        self.latitude_min = latitude_min
        self.latitude_max = latitude_max
        self.longitude_min = longitude_min
        self.longitude_max = longitude_max
        self.download_path = download_path

    def construct_url(self, latitude_min, latitude_max, longitude_min, longitude_max):
        return f"https://allencoralatlas.org/geoserver/ows?service=wfs&version=2.0.0&request=GetFeature&typeNames=coral-atlas:geomorphic_data_verbose&srsName=EPSG:3857&bbox={longitude_min},{latitude_min},{longitude_max},{latitude_max}&outputFormat=shape-zip"
        # https://allencoralatlas.org/geoserver/ows?service=wms&version=2.0.0&request=GetMap&layers=coral-atlas:benthic_data_verbose&crs=EPSG:4326&styles=polygon&bbox=-172.14209,-13.84543,-172.08869,-13.814&width=2048&height=2048&format=geojson

    def download_files(self, latitude_min, latitude_max, longitude_min, longitude_max):
        url = self.construct_url(latitude_min, latitude_max, longitude_min, longitude_max)
        fname = f'aca_geomorphic_{time.time_ns()}'

        headers = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.5) Gecko/20031007'}
        dl = requests.get(url, headers=headers)

        filename = self.download_path + fname + dl.headers['Content-Disposition'].split("filename=")[-1]
        with open(filename, 'wb') as f:
            f.write(dl.content)

        # subprocess.run(['wget', url,'-O',self.download_path+fname+'.zip'])
        # subprocess.run(['unzip','-d','./downloads/geomorphic_data_verbose.zip'])
        # subprocess.run(['unzip','-d',self.download_path+fname+'/',self.download_path+fname+'.zip'])
        # ogr_cmd = 'ogr2ogr -f PostgreSQL'
        # ogr_cmd= ogr_cmd + ' PG:"host=localhost port=5432 user=GOTECH dbname=coral_data"'
        # ogr_cmd = ogr_cmd + f' {self.download_path+fname}/geomorphic_data_verbose.shp'
        # ogr_cmd = ogr_cmd + ' -nlt PROMOTE_TO_MULTI -nln raw.aca_geomorphic -geomfield geom'
        # subprocess.run(ogr_cmd, shell=True)

    def extract_and_load(self):
        if self.latitude_max - self.latitude_min > 0.5 or self.longitude_max - self.longitude_min > 0.5:
            x = np.arange(self.latitude_min, self.latitude_max, 0.5)
            y = np.arange(self.longitude_min, self.longitude_max, 0.5)
            xx, yy = np.meshgrid(x, y)
            xx = xx.ravel()
            yy = yy.ravel()
            for i in range(len(xx)):
                self.download_files(xx[i], xx[i] + 0.5, yy[i], yy[i] + 0.5)
        else:
            self.download_files(self.latitude_min, self.latitude_max, self.longitude_min, self.longitude_max)

# To Implement
# if __name__ == "__main__":
# parser = argparse.ArgumentParser(description = 'Utility function to download Geomorphic data from the Allen Coral Atlas within specified boundries')
# parser.add_argument('--bounding_box', type=str, required=True, help="The area to retrieve data from. e.g. -78.82,22.96,-74.62,26.9")
# parser.add_argument('--download_path', type=str,required=False, help='where output data should be saved')
