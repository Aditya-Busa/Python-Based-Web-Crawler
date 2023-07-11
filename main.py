import requests
import argparse
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import urllib3
import os

def get_file_extension(url):
    """
    Extracts the file extension from the given URL.
    """
    _, file_extension = os.path.splitext(url)
    return file_extension

urllib3.disable_warnings() #If not written,then while executing the 333rd line we are going to get lots of warnings(The warning is given in the below multiline string)

"""
/opt/homebrew/lib/python3.11/site-packages/urllib3/connectionpool.py:1045: InsecureRequestWarning: Unverified HTTPS request is being made to host 'www.iitb.ac.in'. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/1.26.x/advanced-usage.html#ssl-warnings
  warnings.warn(
  
"""

file_extensions = {
    '.3dm': 'Rhino 3D Model',
    '.3ds': '3D Studio Scene',
    '.aep': 'Adobe After Effects Project',
    '.ai': 'Adobe Illustrator Artwork',
    '.aia': 'Adobe Illustrator Actions',
    '.aip': 'Adobe Illustrator Plugin',
    '.ait': 'Adobe Illustrator Template',
    '.aitz': 'Adobe Illustrator Template Compressed',
    '.aiz': 'Adobe Illustrator Compressed',
    '.ald': 'Adobe Audition Loopology',
    '.aldz': 'Adobe Audition Loopology Compressed',
    '.ao': 'Adobe Bridge Output Module',
    '.aoz': 'Adobe Bridge Output Module Compressed',
    '.asl': 'Adobe Photoshop Style',
    '.asp': 'Active Server Page',
    '.aspx': 'Active Server Page Extended',
    '.as': 'ActionScript',
    '.atc': 'Autodesk AutoCAD Tool Palette',
    '.atcz': 'Autodesk AutoCAD Tool Palette Compressed',
    '.atn': 'Adobe Photoshop Action',
    '.aud': 'Audacity Audio',
    '.avi': 'Audio Video Interleave',
    '.bat': 'Batch File',
    '.bcol': 'Adobe Bridge Collection',
    '.bemplate': 'Adobe Bridge Template',
    '.bcache': 'Adobe Bridge Cache',
    '.bcachez': 'Adobe Bridge Cache Compressed',
    '.bpreset': 'Adobe Bridge Preset',
    '.bpresetz': 'Adobe Bridge Preset Compressed',
    '.btemplate': 'Adobe Bridge Template',
    '.btemplatez': 'Adobe Bridge Template Compressed',
    '.bz2': 'Bzip2 Compressed Archive',
    '.c': 'C Source Code',
    '.ccly': 'Adobe Creative Cloud Libraries',
    '.cdr': 'CorelDRAW Image',
    '.cdt': 'CorelDRAW Template',
    '.csv': 'Comma-Separated Values',
    '.ctb': 'AutoCAD Plot Style',
    '.ctbz': 'AutoCAD Plot Style Compressed',
    '.cpp': 'C++ Source Code',
    '.css': 'Cascading Style Sheet',
    '.cube': 'Look-Up Table 3D Cube',
    '.cub': 'Adobe Photoshop Color Lookup Table',
    '.csh': 'Adobe Photoshop Shape',
    '.cs': 'C# Source Code',
    '.ctp': 'CakePHP Template',
    '.ctx': 'CitectSCADA Exported Project',
    '.cur': 'Windows Cursor',
    '.cw': 'Circuit Wizard Circuit File',
    '.dcm': 'DICOM Image',
    '.dcm30': 'DICOM 3.0 File',
    '.db': 'Database File',
    '.dbf': 'dBASE Database',
    '.dbx': 'Outlook Express Mailbox',
    '.deb': 'Debian Package',
    '.der': 'DER Certificate',
    '.desktop': 'Linux Desktop Entry',
    '.dll': 'Dynamic Link Library',
    '.doc': 'Microsoft Word Document',
    '.docm': 'Microsoft Word Macro-Enabled Document',
    '.docx': 'Microsoft Word Open XML Document',
    '.dot': 'Microsoft Word Document Template',
    '.dotm': 'Microsoft Word Macro-Enabled Document Template',
    '.dotx': 'Microsoft Word Open XML Document Template',
    '.dpr': 'Delphi Project',
    '.dwt': 'AutoCAD Drawing Template',
    '.dwg': 'AutoCAD Drawing',
    '.dwf': 'AutoCAD Design Web Format',
    '.dwfx': 'AutoCAD Drawing Exchange Format',
    '.dxf': 'AutoCAD Drawing Exchange Format',
    '.dxfz': 'AutoCAD Drawing Exchange Format Compressed',
    '.ecw': 'Enhanced Compression Wavelet',
    '.ecwz': 'Enhanced Compression Wavelet Compressed',
    '.eml': 'Email Message',
    '.eps': 'Encapsulated PostScript',
    '.epsf': 'Encapsulated PostScript Format',
    '.epub': 'Electronic Publication',
    '.exe': 'Executable File',
    '.ffx': 'Adobe After Effects Preset',
    '.fla': 'Macromedia Flash Authoring',
    '.flac': 'Free Lossless Audio Codec',
    '.flv': 'Flash Video',
    '.fxg': 'Adobe Illustrator FXG',
    '.fxgz': 'Adobe Illustrator FXG Compressed',
    '.gif': 'Graphics Interchange Format',
    '.go': 'Go Source Code',
    '.h': 'Header File',
    '.htm': 'Hypertext Markup Language',
    '.html': 'Hypertext Markup Language',
    '.ico': 'Icon File',
    '.ics': 'iCalendar File',
    '.idb': 'IDA Database',
    '.idml': 'Adobe InDesign Markup',
    '.idms': 'Adobe InDesign Snippet',
    '.indb': 'Adobe InDesign Book',
    '.indd': 'Adobe InDesign Document',
    '.indl': 'Adobe InDesign Library',
    '.indt': 'Adobe InDesign Template',
    '.inx': 'Adobe InDesign XML Interchange',
    '.iso': 'Disc Image',
    '.itc': 'iTunes Cover Flow Data',
    '.itdb': 'iTunes Database',
    '.itl': 'iTunes Library',
    '.java': 'Java Source Code',
    '.jar': 'Java Archive',
    '.jpeg': 'JPEG Image',
    '.jpegz': 'JPEG Image Compressed',
    '.jpg': 'JPEG Image',
    '.jpgz': 'JPEG Image Compressed',
    '.js': 'JavaScript',
    '.jsp': 'Java Server Pages',
    '.json': 'JavaScript Object Notation',
    '.jsx': 'Adobe Audition Script',
    '.jsxz': 'Adobe Audition Script Compressed',
    '.kt': 'Kotlin Source Code',
    '.ktx': 'Khronos Texture File',
    '.lay': 'Autodesk AutoCAD Export Layout',
    '.layz': 'Autodesk AutoCAD Export Layout Compressed',
    '.lisp': 'Lisp Source Code',
    '.lnk': 'Windows Shortcut',
    '.log': 'Log File',
    '.lua': 'Lua Source Code',
    '.m': 'Objective-C Source Code',
    '.mat': 'MATLAB Data File',
    '.max': '3ds Max Scene',
    '.mdb': 'Microsoft Access Database',
    '.mdf': 'Microsoft SQL Server Database',
    '.mdz': 'Microsoft Access Wizard Template',
    '.mht': 'MHTML Web Archive',
    '.midi': 'MIDI Audio',
    '.mkv': 'Matroska Video',
    '.mlb': 'Autodesk AutoCAD Material Library',
    '.mlbz': 'Autodesk AutoCAD Material Library Compressed',
    '.mov': 'QuickTime Movie',
    '.mp3': 'MP3 Audio',
    '.mp4': 'MPEG-4 Video',
    '.mpeg': 'MPEG Video',
    '.mpg': 'MPEG Video',
    '.msi': 'Windows Installer Package',
    '.mswmm': 'Windows Movie Maker Project',
    '.mtl': 'Wavefront Material',
    '.obj': 'Wavefront 3D Object',
    '.odp': 'OpenDocument Presentation',
    '.ods': 'OpenDocument Spreadsheet',
    '.odt': 'OpenDocument Text',
    '.ogg': 'Ogg Vorbis Audio',
    '.ogv': 'Ogg Video',
    '.one': 'Microsoft OneNote Document',
    '.ost': 'Microsoft Outlook Offline Folder',
    '.otf': 'OpenType Font',
    '.otp': 'OpenDocument Presentation Template',
    '.ots': 'OpenDocument Spreadsheet Template',
    '.ott': 'OpenDocument Text Template',
    '.p12': 'PKCS #12 Certificate',
    '.p7b': 'PKCS #7 Certificate',
    '.p7c': 'PKCS #7 Certificate',
    '.p7s': 'PKCS #7 Signature',
    '.pages': 'Pages Document',
    '.pbf': 'Protobuf Binary Format',
    '.pbix': 'Power BI Desktop File',
    '.pc3': 'AutoCAD Plotter Configuration',
    '.pc3z': 'AutoCAD Plotter Configuration Compressed',
    '.pdf': 'Portable Document Format',
    '.pdfz': 'Portable Document Format Compressed',
    '.pef': 'Pentax RAW Image',
    '.php': 'PHP Script',
    '.php4': 'PHP 4 Script',
    '.php5': 'PHP 5 Script',
    '.phps': 'PHP Script Source',
    '.phtml': 'PHP Script',
    '.pkf': 'Adobe Audition Sound Document',
    '.pkfz': 'Adobe Audition Sound Document Compressed',
    '.pl': 'Perl Script',
    '.plugin': 'Plugin File',
    '.png': 'Portable Network Graphics',
    '.pot': 'Microsoft PowerPoint Template',
    '.potm': 'Microsoft PowerPoint Macro-Enabled Template',
    '.potx': 'Microsoft PowerPoint Open XML Template',
    '.ppa': 'Microsoft PowerPoint Add-In',
    '.ppam': 'Microsoft PowerPoint Add-In',
    '.pps': 'Microsoft PowerPoint Slide Show',
    '.ppsm': 'Microsoft PowerPoint Macro-Enabled Slide Show',
    '.ppsx': 'Microsoft PowerPoint Open XML Slide Show',
    '.ppt': 'Microsoft PowerPoint Presentation',
    '.pptm': 'Microsoft PowerPoint Macro-Enabled Presentation',
    '.pptx': 'Microsoft PowerPoint Open XML Presentation',
    '.prproj': 'Adobe Premiere Pro Project',
    '.ps': 'PostScript',
    '.psb': 'Photoshop Big Document',
    '.psd': 'Adobe Photoshop Document',
    '.psdx': 'Adobe Photoshop Touch Document',
    '.pspimage': 'PaintShop Pro Image',
    '.ptf': 'Pro Tools Session Template',
    '.ptx': 'Adobe Audition Session Template',
    '.ptxz': 'Adobe Audition Session Template Compressed',
    '.pub': 'Microsoft Publisher Document',
    '.py': 'Python Script',
    '.pyc': 'Python Compiled File',
    '.pyo': 'Python Optimized Code',
    '.pyx': 'Cython Source Code',
    '.qbw': 'QuickBooks Data File',
    '.qcp': 'PureVoice Audio File',
    '.rar': 'RAR Archive',
    '.raw': 'Raw Image Data',
    '.rm': 'RealMedia File',
    '.rpm': 'Red Hat Package Manager',
    '.rss': 'RSS Feed',
    '.rtf': 'Rich Text Format',
    '.safariextz': 'Safari Extension',
    '.sas': 'SAS Program File',
    '.sass': 'Sass Cascading Style Sheet',
    '.sav': 'SPSS Data File',
    '.sb': 'Scratch Project',
    '.sb2': 'Scratch 2.0 Project',
    '.sbs': 'Substance Designer Graph',
    '.sbsar': 'Substance Archive',
    '.sbz': 'Scratch Project Compressed',
    '.scr': 'Windows Screensaver',
    '.scrz': 'Windows Screensaver Compressed',
    '.sh': 'Bourne Shell Script',
    '.slbz': 'Autodesk AutoCAD Dictionary Compressed',
    '.sld': 'SolidWorks Drawing',
    '.slddrt': 'Autodesk AutoCAD Slide Library',
    '.slddrtz': 'Autodesk AutoCAD Slide Library Compressed',
    '.slddrw': 'SolidWorks Drawing',
    '.sldz': 'Autodesk AutoCAD Slide Compressed',
    '.sldx': 'Autodesk AutoCAD Slide Library Index',
    '.smc': 'Super Nintendo ROM',
    '.sql': 'SQL Database Script',
    '.sqlite': 'SQLite Database',
    '.sqlite3': 'SQLite 3 Database',
    '.stl': 'Stereolithography File',
    '.svg': 'Scalable Vector Graphics',
    '.svgz': 'Scalable Vector Graphics Compressed',
    '.swf': 'Small Web Format',
    '.swz': 'Adobe Flash Player Cache',
    '.tar': 'Consolidated Unix File Archive',
    '.tbz': 'Tar BZip Archive',
    '.tbz2': 'Tar BZip2 Archive',
    '.tgz': 'Tar GZ Archive',
    '.thmx': 'Microsoft Office Theme',
    '.tif': 'Tagged Image File Format',
    '.tiff': 'Tagged Image File Format',
    '.ttf': 'TrueType Font',
    '.twb': 'Tableau Workbook',
    '.txz': 'Tar XZ Archive',
    '.txt': 'Plain Text',
    '.tz': 'Gzip Tar Archive',
    '.u3d': 'Universal 3D File',
    '.udl': 'Universal Data Link',
    '.usdz': 'USDZ Universal Scene Description',
    '.vb': 'Visual Basic Source Code',
    '.vbs': 'VBScript File',
    '.vdx': 'Visio Drawing XML',
    '.vsd': 'Visio Drawing',
    '.vst': 'Visual Studio Template',
    '.vss': 'Visio Stencil',
    '.vssx': 'Visio Stencil',
    '.vstx': 'Visio Template',
    '.vsx': 'Visio Stencil XML',
    '.vtx': 'Visio Template XML',
    '.wav': 'Waveform Audio',
    '.wbmp': 'Wireless Bitmap Image',
    '.webm': 'WebM Video',
    '.webp': 'WebP Image',
    '.wmf': 'Windows Metafile',
    '.wmv': 'Windows Media Video',
    '.wpl': 'Windows Media Player Playlist',
    '.wps': 'Microsoft Works Word Processor Document',
    '.wsdl': 'Web Services Description Language',
    '.wsp': 'SharePoint Solution Package',
    '.wvx': 'Windows Media Video Redirector',
    '.xaml': 'XAML File',
    '.xap': 'Silverlight Application Package',
    '.xar': 'Xara Drawing',
    '.xbap': 'XAML Browser Application',
    '.xcf': 'GIMP Image',
    '.xhtml': 'Extensible Hypertext Markup Language',
    '.xls': 'Microsoft Excel Spreadsheet',
    '.xlsb': 'Microsoft Excel Binary Spreadsheet',
    '.xlsm': 'Microsoft Excel Macro-Enabled Spreadsheet',
    '.xlsx': 'Microsoft Excel Open XML Spreadsheet',
    '.xlt': 'Microsoft Excel Template',
    '.xltm': 'Microsoft Excel Macro-Enabled Template',
    '.xltx': 'Microsoft Excel Open XML Template',
    '.xml': 'eXtensible Markup Language',
    '.xpi': 'Mozilla Installer Package',
    '.xps': 'XML Paper Specification',
    '.xpt': 'SAS Transport File',
    '.xsd': 'XML Schema',
    '.xsl': 'XSL Transformation',
    '.xslt': 'XSL Transformation',
    '.xwd': 'X Window Dump Image',
    '.yaml': 'YAML Document',
    '.yml': 'YAML Document',
    '.zip': 'Zip Archive',
    '.zipx': 'Extended Zip Archive'
}
folders_for_exts =  {key: [] for key in file_extensions}
misc_linklist=[]
final_linkset=set()
ext_links=set()
def get_internal_links(url):
    """
    Extracts all internal links from the given URL.
    """
    internal_links = set()

    # try:
    response = requests.get(url,verify=False) #request.get also follows the redirects and we don't have to explicitly mention "allow_redirects=True"
    """
    Not having verify = False is causing trouble with
    some websites(and it is entirely safe for us to not Verify the certificate,because we are just copying the entire
    ) like https://www.iitb.ac.in
    """
    soup = BeautifulSoup(response.content, 'lxml')
        # Finding all tags with 'href' or 'src' attributes
    tags = soup.find_all(['a', 'link','area','base','img','audio','embed','iframe','input','script','source','track','video'])
    for tag in tags:
            if tag.name == 'a' or 'link' or 'area' or 'base' :
                attr='href'
            else :
                attr='src'
            link = tag.get(attr)
            if link and not link.startswith('#'): #To remove fragment identifiers/anchor links within same web page
                # while link.startswith(' '): # to remove some unnecessary spaces in the start of referenced link which will create a problem in urljoin function
                #     link=link[1:]
                parse_url=urlparse(link) #To remove fragment identifiers/anchor links within same web page
                fragment_length=len(parse_url.fragment)
                link_length=len(link)
                if fragment_length!=0:
                    unique_link=link[0:link_length-fragment_length-1]
                else:
                    unique_link=link
                internal_links.add(unique_link)

    return internal_links

def web_crawler(url, threshold,custom, output_file=None):
    """
    Performs web crawling recursively to find all unique internal and external links.
    """
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    visited_urls = set()
    count=0
    if threshold!=0:
        depth_dict={x:set() for x in range(0,threshold+1)}
    else:
        depth_dict={x:set() for x in range(1,10000)}
    if output_file:
        with open(output_file, 'a') as file:
            file.write(f'At recursion level : {threshold}\n')
    else:
        print('At recursion level :',threshold,'\n')

    def crawl(url, depth):
        while url.startswith(' '):
            url=url[1:]
        if depth > threshold and threshold!=0:
            return

        if url in visited_urls:
            return

        visited_urls.add(url)

        links = get_internal_links(url)

        for link in links:
            absolute_link= urljoin(url, link)
            parsed_link = urlparse(absolute_link)
            if absolute_link.startswith('http'):
                final_linkset.add(absolute_link)#creating a set and adding links without directly appending the links into output file allows us from repeating the links
                depth_dict[depth].add(absolute_link)
            if parsed_link.netloc == domain:  #This ensures that the link that is being further followed is of the same domain
                crawl(absolute_link, depth + 1)
    crawl(url, 1)
    for x in final_linkset:
        count=count+1
    if output_file:
        with open(output_file,'a') as file:
            file.write(f'Total files found are : {count}\n\n')
    else:
        print(f'Total files found are : {count}\n')
    if custom==0:
        for x in final_linkset:
            a=False # a is boolean variable used to determine whether a is into miscellaneous category or not 
            for y in file_extensions:
                if get_file_extension(x)== y:
                    folders_for_exts[y].append(x)
                    a=True
            if a==False:
                misc_linklist.append(x)

        for y in folders_for_exts:
            file_counter=0
            for k in folders_for_exts[y]:
                file_counter=file_counter+1
            if folders_for_exts[y]!=[]:
                if output_file:
                    with open(output_file,'a') as file:
                        file.write(f'\n\nType of File = {file_extensions[y]}({y})(No. of files = {file_counter}) :\n')
                        for x in folders_for_exts[y]:
                            file.write(f'{x}\n')
                else:
                    print(f'\nType of File = {file_extensions[y]}({y}) :')
                    for x in folders_for_exts[y]:
                        print(x)
        if misc_linklist!=[]:
            if output_file:
                with open(output_file,'a') as file:
                    file.write('\n\nMiscellaneous files/URLs : \n')
            else:
                print('\nMiscellaneous files/URLs : ')
        for z in misc_linklist:
            if output_file:
                with open(output_file,'a') as file:
                    file.write(f'{z}\n')
            else:
                print(z)          
    if custom==1:
        for x in final_linkset:
            if output_file:
                with open(output_file, 'a') as file:
                    file.write(f'{x}\n')
            else:
                print(f'{x}\n')
    if custom==2:
        for x in final_linkset:
            if urlparse(x).netloc!=domain:
                ext_links.add(x)
        if output_file:
            with open(output_file,'a') as file:
                file.write('External links : \n')
        else:
            print('External links : ')
        for x in ext_links: 
            if output_file:
                with open(output_file,'a') as file:
                    file.write(f'{x}\n')
            else:
                print(x)
        if output_file:
            with open(output_file,'a') as file:
                file.write('Internal links : \n')
        else:
            print('Internal links : ') 
        for x in final_linkset-ext_links: 
            if output_file:
                with open(output_file,'a') as file:
                    file.write(f'{x}\n')
            else:
                print(x)       
    if custom==3: 
        temp_linkset=set()   
        if threshold!=0: 
            for x in range(1,threshold+1):
                if x>1:
                    temp_linkset=temp_linkset|depth_dict[x-1]  #Gives union of all links upto depth x-1
                if output_file:
                    with open(output_file,'a') as file:
                        file.write(f'\nNew Links found at depth level {x} : \n\n')
                        for y in depth_dict[x]-temp_linkset:
                            file.write(f'{y}\n')
                else:
                    print(f'New Links found at depth level {x} : \n')
                    for y in depth_dict[x]-temp_linkset:
                        print(y)
        else:
            for x in range(1,1000):
                if x>1:
                    temp_linkset=temp_linkset|depth_dict[x-1]  #Gives union of all links upto depth x-1
                if output_file:
                    with open(output_file,'a') as file:
                        if depth_dict[x]-temp_linkset:
                            file.write(f'New Links found at depth level {x} : \n')
                            for y in depth_dict[x]-temp_linkset:
                                file.write(f'{y}\n')
                else:
                    if depth_dict[x]-temp_linkset:
                        print(f'New Links found at depth level {x} : ')
                        for y in depth_dict[x]-temp_linkset:
                            print(y)
 
 
def main():
    parser = argparse.ArgumentParser(description='Web Crawler')
    parser.add_argument('-u', '--url', type=str, help='Website URL')
    parser.add_argument('-t', '--threshold', type=int, help='Recursion threshold')
    parser.add_argument('-o', '--output', type=str, help='Output file')
    parser.add_argument('-c','--custom',type=int,help='Segregation type')
    args = parser.parse_args()

    if not args.url:
        parser.error('URL is required')

    if not args.threshold:
        args.threshold = 0
    if  args.threshold < 0:
        parser.error('Invalid recursion threshold')
    if args.custom>3 or args.custom<0:
        parser.error('Invalid custom segregation')

    web_crawler(args.url, args.threshold,args.custom, args.output)

main()
