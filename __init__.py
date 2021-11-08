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
    name = 'CalibreHentoid'
    description = 'Read metadata from hentoid JSON stored in CBZ files'
    supported_platforms = ['linux']
    author = 'aBoxofTentacles'
    version = (0,1,0)
    file_types = set(['cbz'])
    minimum_calibre_version = (0,7,53)
    def clean_tag(self, tag):
        #change some unwanted tags
        #cut out e-hentai gender specifications
        colon_index = tag.find(':')
        print(colon_index)
        if colon_index > 0 and colon_index < (len(tag) - 1):
            print('if triggered')
            return tag[(colon_index + 1):]

        return tag
            
    def get_metadata(self, stream, ftype):
        from calibre.customize.builtins import ComicMetadataReader
        book_dict = {}
        #open zip
        with zipfile.ZipFile(stream) as book_archive:
            for item in book_archive.namelist():
                if item.endswith('thumb.jpg'):
                    print('thumbnail found')
                    cover_image = book_archive.open(item)
                    break

            #find content json
            for item in book_archive.namelist():
                if item.endswith('contentV2.json'):
                    content_path = item
                    print('contentV2.json found')
            #build a more useable dictionary
                    with book_archive.open(content_path) as book_file:
                        book_json = json.load(book_file)
                        book_dict = {
                            "title": book_json['title'],
                            "tags": [],
                            "authors": [],
                            "series" : []
                        }
                        if 'TAG' in book_json['attributes']:
                            for tag in book_json['attributes']['TAG']:
                                tag_name = str(tag['name'])
                                if tag_name.find('group:') == -1:
                                    book_dict["tags"].append(self.clean_tag(tag_name))
                        if 'ARTIST' in book_json['attributes']:
                            for author in book_json['attributes']['ARTIST']:
                                book_dict["authors"].append(author['name'])
                        if 'SERIE' in book_json['attributes']:
                            for series in book_json['attributes']['SERIE']:
                                book_dict["series"].append(series['name'])
                                print(book_dict)
                        #call the original cbz metadata reader
                        mi = ComicMetadataReader.get_metadata(self, stream, 'cbz')
                        if book_dict['title']:
                            mi.title = book_dict['title']
                        if book_dict['tags']:
                            mi.tags = book_dict['tags']
                        if book_dict['authors']:
                            mi.authors = book_dict['authors']
                        if book_dict['series']:
                            mi.series = book_dict['series'][0]
                        return mi