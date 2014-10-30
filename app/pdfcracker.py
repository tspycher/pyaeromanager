import os, hashlib, tempfile

class PdfCracker(object):
    def crack(self, filename):
        """
        sudo port install ghostscript
        gs -q -dNOPAUSE -dBATCH -dSAFER -sDEVICE=pdfwrite -sOutputFile=LS_ADINFO_0000_LSZI_cracked.pdf -f LS_ADINFO_0000_LSZI.pdf

        :param filename:
        :return:
        """
        crackedFilename = os.path.join(tempfile.gettempdir(), "%s.pdf" % hashlib.md5(filename).hexdigest())
        #args = [
        #    "-dNOPAUSE", "-dBATCH", "-dSAFER"
        #    "-sDEVICE=pdfwrite",
        #    "-sOutputFile=" + crackedFilename,
        #    "-c", ".setpdfwrite",
        #    "-f", filename
        #    ]
        #ghostscript.Ghostscript(*args)

        os.system('gs -q -dSAFER -dNOPAUSE -dQUIET -dBATCH -sDEVICE=pdfwrite -sOUTPUTFILE=%s -c .setpdfwrite -f %s' % (crackedFilename, filename))
        return crackedFilename