# This file is part of CalibreHentoid

# CalibreHentoid is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# CalibreHentoid is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

__license__ = 'GPL v3'
__copyright__ = '2021, aBoxofTentacles <gmoney@aboxoftentacles.com>'
__docformat__ = 'restructuredtext en'

import json
import zipfile

from calibre.customize import MetadataReaderPlugin

class Hentalibre(MetadataReaderPlugin):    
    name = 'Read Hentoid Metadata'
    description = 'Read metadata from hentoid JSON stored in CBZ files'
    supported_platforms = ['linux', 'windows']
    author = 'aBoxofTentacles'
    version = (0,1,0)
    file_types = set(['cbz'])
    minimum_calibre_version = (0,7,53)

    def clean_tag(tag):
        #change some unwanted tags
        #cut out e-hentai gender specifications
        colon_index = tag.find(':')
        print(colon_index)
        if colon_index > 0 and colon_index < (len(tag) - 1):
            print('if triggered')
            return tag[(colon_index + 1):]

        return tag

    def not_blacklisted(tag):
        #detect black listed items
        blacklist = ['group:']
        
        for i in blacklist:
            if tag.find(i):
                return False
        
        return True

    def default_language(json_file):
        site_name = json_file['site']
        
        if site_name == 'TSUMINO':
            return 'English'
            
    def get_metadata(self, stream, ftype):
        from calibre.customize.builtins import ComicMetadataReader
        book_dict = {}
        #open zip
        with zipfile.ZipFile(stream) as book_archive:
            #find content json
            for item in book_archive.namelist():
                if item.endswith('contentV2.json'):
                    with book_archive.open(item) as book_file:
                        book_json = json.load(book_file)
                        #call the original cbz metadata reader
                        mi = ComicMetadataReader.get_metadata(self, stream, 'cbz')
                        #start pulling metadata
                        if 'title' in book_json:
                            mi.title = book_json['title']
                        if 'TAG' in book_json['attributes']:
                            for tag in book_json['attributes']['TAG']:
                                tag_name = str(tag['name'])
                                if self.not_blacklisted(tag_name):
                                    mi.tags.append(self.clean_tag(tag_name))
                        if 'ARTIST' in book_json['attributes']:
                            for author in book_json['attributes']['ARTIST']:
                                mi.authors.append(author['name'])
                        if 'SERIE' in book_json['attributes']:
                            for series in book_json['attributes']['SERIE']:
                                mi.series.append(series['name'])
                        if 'LANGUAGE' in book_json['attributes']:
                            for language in book_json['attributes']['LANGUAGE']:
                                mi.languages.append(language['name'])
                        else:
                            mi.languages.append(self.default_language(book_json))
                        
                        return mi