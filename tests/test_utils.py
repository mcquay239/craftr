# Copyright (C) 2015 Niklas Rosenstein
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import craftr.utils
import os
import sys
import posixpath
import unittest


class PathTest(unittest.TestCase):

  def setUp(self):
    # Mock posixpath into os.path and the craftr.utils.path module.
    # This is VERY hacky, but it makes the tests work on Windows as well.
    self._old_path = os.path
    os.path = posixpath
    craftr.utils.path.join = posixpath.join
    craftr.utils.path.split = posixpath.split
    craftr.utils.path.dirname = posixpath.dirname
    craftr.utils.path.basename = posixpath.basename
    craftr.utils.path.relpath = posixpath.relpath

  def tearDown(self):
    os.path = self._old_path
    del self._old_path
    craftr.utils.path.join = os.path.join
    craftr.utils.path.split = os.path.split
    craftr.utils.path.dirname = os.path.dirname
    craftr.utils.path.basename = os.path.basename
    craftr.utils.path.relpath = os.path.relpath

  def test_addprefix(self):
    from craftr.utils.path import addprefix
    self.assertEqual(addprefix('foo/bar/baz', 'spam-'), 'foo/bar/spam-baz')
    self.assertEqual(
      addprefix([
        'foo/bar/baz',
        'foo/bar/ham/cheeck',
        '/gogodo'], 'egg_'),
      [
        'foo/bar/egg_baz',
        'foo/bar/ham/egg_cheeck',
        '/egg_gogodo'])

  def test_addsuffix(self):
    from craftr.utils.path import addsuffix
    self.assertEqual(addsuffix('foo/bar/baz', '.eggs', True), 'foo/bar/baz.eggs')
    self.assertEqual(addsuffix('foo/bar/baz.spam', '.eggs', True), 'foo/bar/baz.eggs')
    self.assertEqual(addsuffix('foo/bar/baz.spam', None, True), 'foo/bar/baz')
    self.assertEqual(addsuffix('foo/bar/baz.spam', '', True), 'foo/bar/baz')
    self.assertEqual(
      addsuffix([
        'foo/bar/baz',
        'foo/bar/baz.spam',
        'foo/bar/baz.baz'], '.eggs', True),
      [
        'foo/bar/baz.eggs',
        'foo/bar/baz.eggs',
        'foo/bar/baz.eggs'])

    self.assertEqual(addsuffix('foo/bar/baz.spam', 'eggs', False), 'foo/bar/baz.spameggs')
    self.assertEqual(addsuffix('foo/bar/baz.spam', '.eggs', False), 'foo/bar/baz.spam.eggs')
    self.assertEqual(
      addsuffix([
        'foo/bar/baz',
        'foo/bar/baz.spam',
        'foo/bar/baz.baz'], 'eggs', False),
      [
        'foo/bar/bazeggs',
        'foo/bar/baz.spameggs',
        'foo/bar/baz.bazeggs'])

  def test_commonpath(self):
    from craftr.utils.path import commonpath
    self.assertEqual(commonpath(['/foo/bar', '/foo/bar/baz']), '/foo/bar')
    self.assertEqual(commonpath(['foo/bar', 'foo/bar/baz']), 'foo/bar')
    with self.assertRaises(ValueError):
      commonpath(['/foo/bar', 'foo/bar/baz'])

  def test_move(self):
    from craftr.utils.path import move
    base = 'foo/bar'
    new_base = 'eggs/ham'
    files = [
      'foo/bar/main.c',
      'foo/bar/spam.c',
      'foo/bar/utils/eggs.c']
    expected = [
      'eggs/ham/main.c',
      'eggs/ham/spam.c',
      'eggs/ham/utils/eggs.c']
    self.assertEqual(move(files, base, new_base), expected)


class ListsTest(unittest.TestCase):

  def test_autoexpand(self):
    from craftr.utils.lists import autoexpand as a
    self.assertEqual(a('spam'), ['spam'])
    self.assertEqual(a(['spam']), ['spam'])
    self.assertEqual(a(('spam',)), ['spam'])
    self.assertEqual(a(['spam', ['eggs', ('and', set(['trails'])), 'ham']]),
                      ['spam', 'eggs', 'and', 'trails', 'ham'])



class DisTest(unittest.TestCase):

  def test_get_assigned_name(self):
    from craftr.utils.dis import get_assigned_name
    var = get_assigned_name(sys._getframe())
    self.assertEqual(var, 'var')
    obj = type('', (), {})()
    obj.bar = get_assigned_name(sys._getframe())
    self.assertEqual(obj.bar, 'obj.bar')
    with self.assertRaises(ValueError):
      (x, y) = get_assigned_name(sys._getframe())
    with self.assertRaises(ValueError):
      get_assigned_name(sys._getframe())
