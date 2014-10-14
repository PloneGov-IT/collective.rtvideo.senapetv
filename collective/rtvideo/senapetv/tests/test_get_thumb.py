# -*- coding: utf-8 -*-

import unittest

from zope.component import getMultiAdapter

from redturtle.video.tests.base import TestRequest
from redturtle.video.remote_thumb import RemoteThumb
from redturtle.video.interfaces import IVideoEmbedCode

from collective.rtvideo.senapetv.tests.base import RemoteVideo
from collective.rtvideo.senapetv.tests.base import TestCase

class TestGetThumb(TestCase):

    def test_get_thumb(self):
        remote_video = RemoteVideo()
        adapter = getMultiAdapter((remote_video, TestRequest()),
                                   IVideoEmbedCode,
                                   name = 'stream.senape.tv')

        video_id = 'UUTX7TJLBL68'
        thumb_obj = adapter.getThumb()

        self.assertEqual('image/jpeg',
                         thumb_obj.content_type)

        self.assertEqual('%s-image.jpg'%video_id,
                         thumb_obj.filename)

        self.assertEqual('http://stream.senape.tv/statics/video/wall/%s.jpg'%video_id,
                         thumb_obj.url)

        self.assertTrue(isinstance(thumb_obj, RemoteThumb))

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestGetThumb))
    return suite