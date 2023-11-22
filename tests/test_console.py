#!/usr/bin/python3
"""Module for TestHBNBCommand class."""

from console import HBNBCommand
from models.engine.file_storage import FileStorage as stortage
import unittest
import datetime
from unittest.mock import patch
import sys
from io import StringIO
import re
import os


class TestHBNBCommand(unittest.TestCase):

    """Tests HBNBCommand console."""

    def test_help(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help")

        s = """
Documented commands (type help <topic>):
========================================
EOF  all  count  create  destroy  help  quit  show  update

"""
        self.assertEqual(s, f.getvalue())


    def test_emptyline(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("")
        self.assertEqual(f.getvalue(), "")

    def test_create(self):

        for _class in HBNBCommand.classes.keys():
            command = "create " + _class
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(command)
            _id = f.getvalue().strip("\n")
            
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd("all")
            self.assertTrue(_id in f.getvalue())

            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd("create")
            self.assertEqual(f.getvalue().strip("\n"), "** class name missing **")
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd("create foo")
            self.assertEqual(f.getvalue().strip("\n"), "** class doesn't exist **")
    
    def test_create_with_params(self):

        valid_param = ' valid="this_is_valid"'
        nv1 = ' nvalid"this_is_not_valid'
        nv2 = ' nvalid==='
        nv3 = ' nvalid=c23.34'
        nv4 = ' nvlaid="dfkd"dfk"'

        for _class in HBNBCommand.classes.keys():
            command = "create " + _class + valid_param + nv1 + nv2 + nv3 + nv4
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(command)
            
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd("all " + _class)
                print(f.getvalue())

            self.assertTrue("valid" in f.getvalue())

            self.assertFalse("nvalid" in f.getvalue())

    def test_show(self):
        for _class in HBNBCommand.classes.keys():
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd("create " + _class)
            _id = f.getvalue().strip("\n")
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd("show " + _class + " " + _id)
            self.assertTrue(_id in f.getvalue())
            self.assertTrue(_class in f.getvalue())
