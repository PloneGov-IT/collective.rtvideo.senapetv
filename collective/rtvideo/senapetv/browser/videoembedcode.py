# -*- coding: utf-8 -*-

from urlparse import urlparse
from redturtle.video.remote_thumb import RemoteThumb
from redturtle.video.browser.videoembedcode import VideoEmbedCode
try:
    from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile
except ImportError:
    # Plone < 4.1
    from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile


class SenapeTvBase(object):

    def getThumb(self):
        """
        Senape.tv API use this format to return images:
        http://stream.senape.tv/statics/video/wall/IDVIDEO.jpg

        IDVIDEO: an alphanumeric string like 'ODA33daiSS';

        So you can call somethign like:
             http://stream.senape.tv/statics/video/wall/S9UABZVATeY.jpg
        """
        parsed_remote_url = urlparse(self.context.getRemoteUrl())
        video_id = self.get_video_id(parsed_remote_url)
        img_url = 'http://stream.senape.tv/statics/video/wall/%s.jpg' % video_id
        thumb_obj = RemoteThumb(img_url,
                                'image/jpeg',
                                '%s-image.jpg' % video_id)
        return thumb_obj


class ClassicSenapeTvEmbedCode(SenapeTvBase, VideoEmbedCode):
    """ClassicYoutubeEmbedCode
    Provides a way to have a html code to embed Youtube video in a web page

    >>> from zope.interface import implements
    >>> from redturtle.video.interfaces import IRTRemoteVideo
    >>> from redturtle.video.interfaces import IVideoEmbedCode
    >>> from zope.component import getMultiAdapter
    >>> from collective.rtvideo.youtube.tests.base import TestRequest

    >>> request = TestRequest()

    >>> class RemoteVideo(object):
    ...     implements(IRTRemoteVideo)
    ...     remoteUrl = 'http://www.youtube.com/watch?v=s43WGi_QZEE&feature=related'
    ...     size = {'width': 425, 'height': 349}
    ...     def getRemoteUrl(self):
    ...         return self.remoteUrl
    ...     def getWidth(self):
    ...         return self.size['width']
    ...     def getHeight(self):
    ...         return self.size['height']

    >>> remotevideo = RemoteVideo()
    >>> adapter = getMultiAdapter((remotevideo, request),
    ...                                         IVideoEmbedCode,
    ...                                         name = 'youtube.com')
    >>> adapter.getVideoLink()
    'http://www.youtube.com/embed/s43WGi_QZEE'

    >>> print adapter()
    <div class="youtubeEmbedWrapper">
    <BLANKLINE>
    <iframe width="425"
            height="349"
            frameborder="0"
            allowfullscreen
            src="http://www.youtube.com/embed/s43WGi_QZEE">
    </iframe>
    </div>
    <BLANKLINE>

    Now check if the autoplay parameter is taken used when putted into the video source URL.

    >>> remotevideo.remoteUrl += '?AUTOPLAY=1'
    >>> print adapter()
    <div class="youtubeEmbedWrapper">
    <iframe width="425"
            height="349"
            frameborder="0"
            allowfullscreen
            src="http://www.youtube.com/embed/s43WGi_QZEE?autoplay=1&amp;enablejsapi=1">
    </iframe>
    </div>
    <BLANKLINE>

    If the request URL is provided with a "autoplay=1" parameter, autoplay and accessibility/usability
    tricks are included

    >>> request.QUERY_STRING = '?foo=5&autoplay=1&bar=7'
    >>> print adapter()
    <div class="youtubeEmbedWrapper">
    <script type="text/javascript">
    <!--
    function onYouTubePlayerReady() {
        document.getElementById('youtubeVideo').focus();
    }
    //-->
    </script>
    <iframe width="425"
            height="349"
            frameborder="0"
            allowfullscreen
            src="http://www.youtube.com/embed/s43WGi_QZEE?autoplay=1&amp;enablejsapi=1"
            tabindex="1">
    </iframe>
    </div>
    <BLANKLINE>

    """
    template = ViewPageTemplateFile('senapetvembedcode_template.pt')

    def getVideoLink(self):
        path = urlparse(self.context.getRemoteUrl())[2]
        try:
            start, landing = path.split('/landing/')
            uid, video = landing.split('/video/')
        except ValueError:
            return ''
        return 'http://stream.senape.tv/widget/video.action?do=iframe&v=2.0&uid=%s&rid=%s' % (uid,video)


    def getEmbedVideoLink(self):
        """Video link, just for embedding needs"""
        return self.getVideoLink()

    def get_video_id(self, parsed_remote_url):
        path = parsed_remote_url[2]
        try:
            return path.split('/video/')[1]
        except IndexError:
            return ''
