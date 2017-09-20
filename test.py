#!/usr/bin/env python3
from unittest import TestCase

import protect


class KeyTest(TestCase):
    """Key class testing"""
    def setUp(self):
        self.cls = protect.Key()
        self.result = []
        self.correct = []

    def test_normalize(self):
        self.result.append(self.cls.normalize('1111111111111111'))
        self.correct.append('897A6B5C4D3E2F01')
        self.result.append(self.cls.normalize('F609EA71D58C24B3'))
        self.correct.append('F609EA71D58C24B3')
        self.result.append(self.cls.normalize('BA7437EA8F7E58AA'))
        self.correct.append('B69432C1DF7E580A')
        self.result.append(self.cls.normalize('1234567890aBdDDD'))
        self.correct.append('1234567890ABEFCD')
        for i in range(len(self.result)):
            self.assertEqual(self.result[i], self.correct[i])

    def test_to_string(self):
        self.result.append(self.cls.to_string(b'1234567890'))
        self.correct.append('31323334353637383930')
        self.result.append(self.cls.to_string(b'\x12\x34\x56\x78\x90'))
        self.correct.append('1234567890')
        for i in range(len(self.result)):
            self.assertEqual(self.result[i], self.correct[i])

class ViewTest(TestCase):
    """View class testing"""
    def setUp(self):
        self.cls = protect.View()
        self.result = []
        self.correct = []

    def check(self):
        for i in range(len(self.result)):
            self.assertEqual(self.result[i], self.correct[i])

    def test_decorate(self):
        self.result.append(self.cls.decorate(protect.Key(
            b'\x33\x44', b'fdsa', 10
        )))
        self.correct.append('1234567890')
        self.check()

