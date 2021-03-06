'''
 * Copyright 2019-2020, Intel Corporation
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 *
 *     * Redistributions of source code must retain the above copyright
 *       notice, this list of conditions and the following disclaimer.
 *
 *     * Redistributions in binary form must reproduce the above copyright
 *       notice, this list of conditions and the following disclaimer in
 *       the documentation and/or other materials provided with the
 *       distribution.
 *
 *     * Neither the name of the copyright holder nor the names of its
 *       contributors may be used to endorse or promote products derived
 *       from this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 * "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 * LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
 * A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
 * OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
 * SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
 * LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
 * DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
 * THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
 * OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''

import unittest
import json
import urllib.request
import os.path

import pmemkv

class TestNaughtyStrings(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.engine = r"vsmap"
        self.config = {"path":"/dev/shm","size":1073741824}
        self.strings = self._get_naughty_strings("https://raw.githubusercontent.com/minimaxir/big-list-of-naughty-strings/master/blns.json")

    def _get_naughty_strings(self, url):
        file_name = "blns.json"
        data = {}
        if not os.path.exists(file_name):
            urllib.request.urlretrieve(url, file_name)
        with open(file_name) as f:
            data = json.load(f)
        return data

    def test_puts_tricky_keys_and_values(self):
        db = pmemkv.Database(self.engine, self.config)
        data = {}
        with open("blns.json") as f:
            data = json.load(f)
        for val in data:
            db.put(val, val)
        for val in data:
            self.assertEqual(db[val], val)
        db.stop()

if __name__ == '__main__':
    unittest.main()
