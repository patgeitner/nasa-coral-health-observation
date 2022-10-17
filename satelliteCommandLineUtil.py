import argparse
import datetime
import itertools
import json
impoimport pwinput
import urllib

from bs4 import BeautifulSoup
from http.cookiejar import CookieJar
from tqdm import tqdm
from urllib.request import urlopen
from urllib.request import urlretrieve

# Satellite API URLS
ROOT_URL_MODIS = "https://oceandata.sci.gsfc.nasa.gov/api/file_search?"
ROOT_URL_CALIPSO = "https://opendap.larc.nasa.gov/opendap/CALIPSO/"
ROOT_URL_ICESAT2 = "https://cmr.earthdata.nasa.gov/search/granules.json?provider=NSIDC_ECS&sort_key[]=start_date&sort_key[]=producer_granule_id&"

# Request for MODIS
def retrieveModisFiles(satellite, start_date, end_date, level, file_pattern):
	url = ROOT_URL_MODIS + "sensor={0}&sdate={1}&edate={2}&dtype={3}&search={4}&addurl=1&results_as_file=1"\
			.format(satellite, start_date, end_date, level, file_pattern)
	
	print("Requesting: {0}\n".format(url))
	resp = urlopen(url)
	file_urls = resp.read().decode('utf8').split('\n')

	if file_urls[0] != '':
		print("Found {0} files.\n".format(len(file_urls)))
		return file_urls
	else:
		print("No files found.\n")
		return None

# Request for CALIPSO
def retrieveCalipsoFiles(dataset, year, month):
	url = ROOT_URL_CALIPSO + "{0}/{1}/{2}/"\
		.format(dataset, year, month)

	print("Requesting: {0}\n".format(url))
	resp = urlopen(url)
	soup = BeautifulSoup(resp.read(), 'lxml')

	for a in soup.find_all('a',href=True):
		link = a['href']
		if link.startswith('CAL') and link[-3:]=='hdf':
			file_urls.append(url + link)
		
	if file_urls[0] != '':
		print("Found {0} files.\n".format(len(file_urls)))
		return file_urls[:1]
	else:
		print("No files found.\n")
		return None

def retrieveIceSat2Files(short_name, time_start, time_end, bounding_box, file_pattern):
	url = ROOT_URL_ICESAT2 + "short_name={0}&temporal[]={1},{2}&bounding_box={3}"\
			.format(short_name, time_start, time_end, bounding_box)
	
	if(file_pattern):
		url += build_filename_filter(file_pattern)
	
	print("Requesting: {0}\n".format(url))
	resp = urlopen(url)
	file_page = resp.read().decode('utf8')
	file_page = json.loads(file_page)
	file_urls = filter_urls(file_page)

	if file_urls[0] != '':
		print("Found {0} files.\n".format(len(file_urls)))
		return file_urls
	else:
		print("No files found.\n")
		return None


def build_filename_filter(file_pattern):
	filters = file_pattern.split(',')
	result = '&options[producer_granule_id][pattern]=true'
	for filter in filters:
		result += '&producer_granule_id[]=' + filter
	return result

# Code taken from: https://nsidc.org/data/icesat-2/tools
def filter_urls(search_results):
    """Select only the desired data files from CMR response."""
    if 'feed' not in search_results or 'entry' not in search_results['feed']:
        return []

    entries = [e['links']
               for e in search_results['feed']['entry']
               if 'links' in e]
    # Flatten "entries" to a simple list of links
    links = list(itertools.chain(*entries))

    urls = []
    unique_filenames = set()
    for link in links:
        if 'href' not in link:
            # Exclude links with nothing to download
            continue
        if 'inherited' in link and link['inherited'] is True:
            # Why are we excluding these links?
            continue
        if 'rel' in link and 'data#' not in link['rel']:
            # Exclude links which are not classified by CMR as "data" or "metadata"
            continue

        if 'title' in link and 'opendap' in link['title'].lower():
            # Exclude OPeNDAP links--they are responsible for many duplicates
            # This is a hack; when the metadata is updated to properly identify
            # non-datapool links, we should be able to do this in a non-hack way
            continue

        filename = link['href'].split('/')[-1]
        if filename in unique_filenames:
            # Exclude links with duplicate filenames (they would overwrite)
            continue
        unique_filenames.add(filename)

        urls.append(link['href'])

    return urls	

def downloadFiles(file_urls, satellite):
	if(satellite == 'ICESAT2'):
		print("Please sign in to Earthdata to download the files.")
		usr = input("Username:")
		p = input("Password:")
	print('Downloading Files.')
	for url in tqdm(file_urls):
		filename = url.split('/')[-1]
		if(satellite == 'AQUA' or satellite == 'TERRA'):
			urlretrieve(url + "?appkey=7643fa13d56ea5f80d44d6647e98bfd4409eefb3", './files/MODIS/'+filename)
		elif(satellite == 'CALIPSO'):
			urlretrieve(url, './files/CALIPSO/'+filename)
		elif(satellite == 'ICESAT2'):
			# Code taken from: https://wiki.earthdata.nasa.gov/display/EL/How+To+Access+Data+With+Python

			# Create a password manager to deal with the 401 reponse that is returned from
			# Earthdata Login
			password_manager = urllib.request.HTTPPasswordMgrWithDefaultRealm()
			password_manager.add_password(None, "https://urs.earthdata.nasa.gov", usr, p)
			
			# Create a cookie jar for storing cookies. This is used to store and return
			# the session cookie given to use by the data server (otherwise it will just
			# keep sending us back to Earthdata Login to authenticate).  Ideally, we
			# should use a file based cookie jar to preserve cookies between runs. This
			# will make it much more efficient.
			
			cookie_jar = CookieJar()
			
			# Install all the handlers.
			opener = urllib.request.build_opener(
				urllib.request.HTTPBasicAuthHandler(password_manager),
				#urllib2.HTTPHandler(debuglevel=1),    # Uncomment these two lines to see
				#urllib2.HTTPSHandler(debuglevel=1),   # details of the requests/responses
				urllib.request.HTTPCookieProcessor(cookie_jar))
			urllib.request.install_opener(opener)
			
			
			# Create and submit the request. There are a wide range of exceptions that
			# can be thrown here, including HTTPError and URLError. These should be
			# caught and handled.
			urlretrieve(url, './files/ICESAT2/'+filename)


        
if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Utility to download data from NASA satellites. Supports the following satellites: Calipso, ICESat-2, Aqua/Terra MODIS, and Landsat.')
	subparsers = parser.add_subparsers(help='All commands.', dest="satellite")

	# Parser for MODIS
	parser_aqua = subparsers.add_parser("AQUA", help='Required arguments for AQUA/TERRA satellite.')
	parser_aqua.add_argument('start_date', type=lambda s: datetime.datetime.strptime(s, '%Y-%m-%d').date(), help="Starting date of data collection e.g. 2022-01-01.")
	parser_aqua.add_argument('end_date', type=lambda s: datetime.datetime.strptime(s, '%Y-%m-%d').date(), help="Ending date of data collection.")
	parser_aqua.add_argument('level', type=str, choices=['L0', 'L1', 'L2', 'L3b', 'L3m'], help="Product Level. See https://oceancolor.gsfc.nasa.gov/products/ for more info.")
	parser_aqua.add_argument('file_pattern', type=str, help="Files will be matched according to the wildcard pattern provided.")

	parser_terra = subparsers.add_parser("TERRA", help='Required arguments for AQUA/TERRA satellite.')
	parser_terra.add_argument('sdate', type=lambda s: datetime.datetime.strptime(s, '%Y-%m-%d').date(), help="Starting date of data collection e.g. 2022-01-01.")
	parser_terra.add_argument('edate', type=lambda s: datetime.datetime.strptime(s, '%Y-%m-%d').date(), help="Ending date of data collection.")
', type=str)
	parser_calipso.add_argument('year', type=str)
	parser_calipso.add_argument('month', type=str)

	# Parser for ICESat-2
	parser_icesat = subparsers.add_parser('ICESAT2', help='Required arguments for ICESAT-2 satellite.')
	parser_icesat.add_argument('short_name', type=str, help="The data product of interest e.g. ATL03")
	parser_icesat.add_argument('start_date', type=lambda s: datetime.datetime.strptime(s, "%Y-%m-%d").date(), help="The start date to search for data e.g. 2022-01-01")
	parser_icesat.add_argument('start_time', type=lambda s: datetime.datetime.strptime(s, "%H:%M:%S").time(), help="The start time to search for data e.g. 23:59:59")
	parser_icesat.add_argument('end_date', type=lambda s: datetime.datetime.strptime(s, "%Y-%m-%d").date(), help="The end date to search for data")
	parser_icesat.add_argument('end_time', type=lambda s: datetime.datetime.strptime(s, "%H:%M:%S").time(), help="The end time to search for data")
	parser_icesat.add_argument('--bounding_box', type=str, required=True, help="The area to retrieve data from. e.g. -78.82,22.96,-74.62,26.9")
	parser_icesat.add_argument('file_pattern', type=str, help="Files will be matched according to the wildcard pattern provided.")
	
	args = parser.parse_args()
	file_urls = []
	satellite = args.satellite
	start_date = ''
	end_date = ''
	level = ''
	file_pattern = ''
	dataset = ''
	year = ''
	month = ''
	short_name = ''
	start_time = ''
	end_time = ''
	bounding_box = ''

	# Extract command line arguments
	if(satellite == 'AQUA' or satellite == 'TERRA'):
		start_date = args.start_date
		end_date = args.end_date
		level = args.level
		file_pattern = args.file_pattern
		file_urls = retrieveModisFiles(satellite, start_date, end_date, level, file_pattern)
	elif(satellite == 'CALIPSO'):
		dataset = args.dataset
		year = args.year
		month = args.month
		file_urls = retrieveCalipsoFiles(dataset, year, month)
	elif(satellite == "ICESAT2"):
		short_name = args.short_name
		start_date_time = str(args.start_date) + "T" + str(args.start_time)
		end_date_time = str(args.end_date) + "T" + str(args.end_time)
		bounding_box = args.bounding_box
		file_pattern = args.file_pattern
		file_urls = retrieveIceSat2Files(short_name, start_date_time, end_date_time, bounding_box, file_pattern)

	if(file_urls != None):
		downloadFiles(file_urls, satellite)