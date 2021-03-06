import httplib 
import mimetypes
import xml.dom.minidom

class PostFile:
    def __init__(self, host, selector, fields, files):
        
        content_type, body = self.encode_multipart_formdata(fields, files)

        h = httplib.HTTP(host)
        h.putrequest('POST', selector)
        h.putheader('content-type', content_type)
        h.putheader('content-length', str(len(body)))
        h.endheaders()
        h.send(body)

        errcode, errmsg, headers = h.getreply()
        self.response = h.file.read()
    
    def getResponse(self):
        
        dom = xml.dom.minidom.parseString(self.response)
        
        rsp = dom.getElementsByTagName("rsp")[0]
        status = rsp.getAttribute("stat")

        if ( status == "fail"):
            err = rsp.getElementsByTagName("err")[0]
            code = err.getAttribute("code")
            msg = err.getAttribute("msg")
            return code, msg
        else:
            return 0, "Upload successful"

    def encode_multipart_formdata(self,fields, files):
        """
               fields is a sequence of (name, value) elements for regular form fields.
               files is a sequence of (name, filename, value) elements for data to be uploaded as files
               Return (content_type, body) ready for httplib.HTTP instance
        """
        BOUNDARY = '----------ThIs_Is_tHe_bouNdaRY_$'
        CRLF = '\r\n'
        L = []
        for (key, value) in fields:
            L.append('--' + BOUNDARY)
            L.append('Content-Disposition: form-data; name="%s"' % key)
            L.append('')
            L.append(value)
        for (key, filename, value) in files:
            L.append('--' + BOUNDARY)
            L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, filename))
            L.append('Content-Type: %s' % mimetypes.guess_type(filename)[0] )
            L.append('')
            L.append(value)
            L.append('--' + BOUNDARY + '--')
            L.append('')
        body = CRLF.join(L)
        content_type = 'multipart/form-data; boundary=%s' % BOUNDARY

        return content_type, body
 
class TwitPic:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.msg = ""
        self.filename = ""
        self.host = "twitpic.com"
        self.selector = "/api/uploadAndPost"

    def setPicture(self, filename):
        self.filename = filename

    def setMessage(self, message):
        self.msg = message

    def upload(self):
        fields = [ ('username', self.username), ('password', self.password)]
        if ( self.msg != ""):
                fields.append( ('message', self.msg) )
        
        img = open( self.filename)
        imgdata = img.read()

        files = [ ('media', self.filename, imgdata) ]

        a = PostFile(self.host, self.selector, fields, files)
	self.resp = a.getResponse()
	print self.filename
	print self.resp

    def getResponse(self):
	return self.resp	

