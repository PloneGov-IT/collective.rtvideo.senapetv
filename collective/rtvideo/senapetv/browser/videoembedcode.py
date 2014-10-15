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
    """ClassicSenapeTvEmbedCode
    Provides a way to have a html code to embed Senape.tv video in a web page

    >>> from zope.interface import implements
    >>> from redturtle.video.interfaces import IRTRemoteVideo
    >>> from redturtle.video.interfaces import IVideoEmbedCode
    >>> from zope.component import getMultiAdapter
    >>> from collective.rtvideo.senapetv.tests.base import TestRequest

    >>> request = TestRequest()

    >>> class RemoteVideo(object):
    ...     implements(IRTRemoteVideo)
    ...     remoteUrl = 'http://stream.senape.tv/landing/regioneal/video/UUTX7TJLBL68'
    ...     size = {'width': 640, 'height': 360}
    ...     def getRemoteUrl(self):
    ...         return self.remoteUrl
    ...     def getWidth(self):
    ...         return self.size['width']
    ...     def getHeight(self):
    ...         return self.size['height']

    >>> remotevideo = RemoteVideo()
    >>> adapter = getMultiAdapter((remotevideo, request),
    ...                                         IVideoEmbedCode,
    ...                                         name = 'stream.senape.tv')
    >>> adapter.getVideoLink()
    'http://stream.senape.tv/widget/video.action?do=iframe&v=2.0&uid=UUTX7TJLBL68&rid=regioneal'

    >>> print adapter()
    <div class="senapetvEmbedWrapper">
    <BLANKLINE>
    <iframe name="UUTX7TJLBL68"
            class="senape-widget-video-player-container"
            width="640"
            height="360"
            marginwidth="0"
            marginheight="0"
            frameborder="0"
            scrolling="no"
            src="http://stream.senape.tv/widget/video.action?do=iframe&v=2.0&uid=UUTX7TJLBL68&rid=regioneal">
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
