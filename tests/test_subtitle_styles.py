import re
import unittest
from scripts.subtitle_styles import STYLES, bgr, build, parse_srt

SRT = '1\n00:00:00,040 --> 00:00:02,400\n你一个月只需要 200 块\n\n2\n00:00:02,400 --> 00:00:03,780\n有一个最核心的概念\n'

def text_only(line):
    return re.sub(r'\{[^}]*\}', '', line.split(',', 9)[9])

class SubtitleStylesTest(unittest.TestCase):
    def test_parse_srt(self):
        self.assertEqual(parse_srt(SRT), [(0.04, 2.4, '你一个月只需要 200 块'), (2.4, 3.78, '有一个最核心的概念')])

    def test_colour_is_bgr(self):
        self.assertEqual(bgr('#FFD400'), '&H0000D4FF')

    def test_every_style_keeps_the_words(self):
        for name in STYLES:
            words = [[['你一个月', .04, .9], ['只需要', .9, 1.5], [' 200 块', 1.5, 2.3]],
                     [['有一个', 2.4, 3.0], ['最核心的概念', 3.0, 3.7]]] if name == 'karaoke' else None
            ass, _, _ = build(parse_srt(SRT), name, highlights={'1': '200 块'}, words=words)
            main = [l for l in ass.splitlines() if l.startswith('Dialogue: 1')]
            self.assertEqual([text_only(l) for l in main], ['你一个月只需要 200 块', '有一个最核心的概念'], name)

    def test_highlight_marks_one_phrase(self):
        ass, warnings, used = build(parse_srt(SRT), 'highlight', highlights={'1': '200 块', '2': '不存在'})
        self.assertEqual(used, 1)
        self.assertIn(r'{\c&H0000D4FF\fscx115\fscy115}200 块', ass)
        self.assertTrue(any('不存在' in w for w in warnings))

    def test_karaoke_needs_real_word_times(self):
        with self.assertRaises(SystemExit):
            build(parse_srt(SRT), 'karaoke')

    def test_karaoke_keeps_pauses_between_words(self):
        srt = '1\n00:00:00,000 --> 00:00:03,000\n你好世界\n'
        ass, _, _ = build(parse_srt(srt), 'karaoke', words=[[['你好', .5, 1.0], ['世界', 2.0, 2.5]]])
        self.assertIn(r'{\k50}{\kf50}你好{\k100}{\kf50}世界', ass)

    def test_karaoke_rejects_words_that_differ_from_srt(self):
        with self.assertRaises(SystemExit):
            build(parse_srt(SRT), 'karaoke', words=[[['你一个月', .04, .9]], [['有一个', 2.4, 3.0]]])

    def test_overlong_line_is_reported_not_shrunk(self):
        long = '1\n00:00:00,000 --> 00:00:02,000\n' + '字' * 30 + '\n'
        ass, warnings, _ = build(parse_srt(long), 'standard')
        self.assertTrue(warnings)
        self.assertNotIn(r'\fscx', ass)

if __name__ == '__main__':
    unittest.main()
